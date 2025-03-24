#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
六爻纳甲命令行工具 - 精确版
"""

import sys
import os
import datetime
import argparse
import math
from typing import Tuple, Optional, Dict, Any, Union

# 添加项目根目录到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir
sys.path.append(project_root)

# 导入六爻模块
from models.liuyao.modules.gua_calculator import gua_calculator
from models.liuyao.modules.enhanced_solar_time import enhanced_solar_time_calculator
from models.liuyao.modules.ip_service import ip_service

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='六爻纳甲命令行工具 - 精确版')
    
    # 日期参数
    parser.add_argument('--date', type=str, help='阳历日期 (YYYY-MM-DD)', default=None)
    
    # 时间参数
    parser.add_argument('--time', type=float, help='时辰 (24小时制，0-23.99)', default=None)
    
    # 位置参数
    parser.add_argument('--longitude', type=float, help='经度 (东经为正，西经为负)', default=None)
    parser.add_argument('--latitude', type=float, help='纬度 (北纬为正，南纬为负)', default=None)
    parser.add_argument('--ip', type=str, help='IP地址 (用于自动获取位置)', default=None)
    
    # 真太阳时设置
    parser.add_argument('--no-true-solar-time', action='store_false', dest='use_true_solar_time',
                      help='不使用真太阳时 (默认使用真太阳时)')
    parser.set_defaults(use_true_solar_time=True)
    
    # 八字参数
    parser.add_argument('--day-master', type=str, help='八字日主天干 (如甲、乙等)', default=None)
    parser.add_argument('--yong-shen', type=str, help='八字用神五行 (如金、木、水、火、土)', default=None)
    
    # 精确度选项
    parser.add_argument('--high-precision', action='store_true', help='使用高精度真太阳时计算', default=True)
    
    # 日照时间选项
    parser.add_argument('--show-daylight', action='store_true', help='显示日出、日落和日照时间', default=False)
    
    return parser.parse_args()

def format_time(hours: float) -> str:
    """
    将小时数格式化为时:分格式
    
    参数:
        hours (float): 小时数（24小时制）
        
    返回:
        str: 格式化后的时间字符串 (HH:MM)
    """
    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h:02d}:{m:02d}"

def format_date(date_str: str, red_text: bool = False) -> str:
    """
    格式化日期字符串
    
    参数:
        date_str (str): 日期字符串 (YYYY-MM-DD)
        red_text (bool): 是否使用红色文本
        
    返回:
        str: 格式化后的日期字符串
    """
    if red_text:
        parts = date_str.split('-')
        if len(parts) == 3:
            return f"\033[31m{parts[0]}年{parts[1]}月{parts[2]}日\033[0m"
    return date_str

def display_bagong_info():
    """显示八宫卦信息"""
    try:
        from models.liuyao.modules.gua_palace import gua_palace
        
        print("\n八宫卦表信息:\n")
        print(gua_palace.generate_all_bagong_text())
        
        print("\n请输入要查看详情的卦宫 (如'乾宫','坎宫'等),或按Enter返回:")
        palace_name = input().strip()
        
        if palace_name:
            print("\n" + "=" * 50)
            print(gua_palace.get_palace_diagram(palace_name))
            print("=" * 50)
    except Exception as e:
        print(f"显示八宫卦信息出错: {e}")

def main():
    """主函数"""
    print("六爻纳甲计算系统 - 增强版")
    print("================================")
    print("1. 开始六爻排盘")
    print("2. 查看八宫卦信息")
    print("3. 退出")
    print("\n请选择操作 (1-3):")
    
    choice = input().strip()
    
    if choice == "1":
        args = parse_arguments()
        
        # 设置日期
        if args.date:
            try:
                date_obj = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
            except ValueError:
                print(f"错误：日期格式应为 YYYY-MM-DD，例如 2023-01-01")
                sys.exit(1)
        else:
            date_obj = datetime.date.today()
        
        # 设置时间
        if args.time is not None:
            if not (0 <= args.time < 24):
                print(f"错误：时间应在 0-23.99 范围内")
                sys.exit(1)
            time_hour = args.time
        else:
            now = datetime.datetime.now()
            time_hour = now.hour + now.minute / 60.0
        
        # 设置位置
        longitude = args.longitude
        latitude = args.latitude
        
        if longitude is None or latitude is None:
            try:
                # 使用IP服务模块获取位置
                longitude, latitude = ip_service.get_location_coordinates(args.ip)
            except Exception as e:
                print(f"通过IP获取位置失败: {e}")
                # 使用默认位置（北京）
                location_info = ip_service.default_location
                longitude = location_info["longitude"]
                latitude = location_info["latitude"]
        
        # 如果启用了日照时间选项，显示日出日落信息
        if args.show_daylight:
            try:
                sunrise = enhanced_solar_time_calculator.get_sunrise_time(date_obj, longitude, latitude)
                sunset = enhanced_solar_time_calculator.get_sunset_time(date_obj, longitude, latitude)
                daylight_hours = enhanced_solar_time_calculator.get_daylight_hours(date_obj, longitude, latitude)
                
                print(f"\n日照信息 ({date_obj.strftime('%Y-%m-%d')}, 经度={longitude:.2f}, 纬度={latitude:.2f}):")
                print(f"日出: {format_time(sunrise)}")
                print(f"日落: {format_time(sunset)}")
                print(f"日照时间: {daylight_hours:.2f}小时")
                print("")
            except Exception as e:
                print(f"计算日照时间出错: {e}")
        
        # 如果启用了高精度模式和真太阳时，使用增强的真太阳时计算
        adjusted_time_hour = time_hour
        time_diff_minutes = 0.0
        
        if args.use_true_solar_time:
            try:
                if args.high_precision:
                    # 使用高精度模块计算
                    adjusted_time_hour = enhanced_solar_time_calculator.calculate_true_solar_time(
                        date_obj, time_hour, longitude, latitude
                    )
                    time_diff_minutes = enhanced_solar_time_calculator.calculate_time_diff(
                        date_obj, time_hour, longitude, latitude
                    )
                    
                    print(f"高精度真太阳时计算结果:")
                    print(f"标准时间: {format_time(time_hour)}")
                    print(f"真太阳时: {format_time(adjusted_time_hour)}")
                    print(f"时差: {time_diff_minutes:.2f}分钟")
                    print("")
                else:
                    # 使用标准模块计算（不显示中间结果）
                    adjusted_time_hour = None
            except Exception as e:
                print(f"计算真太阳时出错: {e}，将使用标准算法")
                adjusted_time_hour = None  # 使用gua_calculator中的标准算法
        
        # 计算六爻卦象
        try:
            # 根据指定的高精度设置决定是否传递已计算的真太阳时
            if args.use_true_solar_time and args.high_precision and adjusted_time_hour is not None:
                # 如果已经计算了高精度真太阳时，直接使用
                result = gua_calculator.calculate_gua(
                    solar_date=date_obj,
                    time_hour=adjusted_time_hour,  # 使用已计算的真太阳时
                    longitude=longitude,
                    latitude=latitude,
                    day_master=args.day_master,
                    yong_shen=args.yong_shen,
                    use_true_solar_time=False,  # 不再使用内部真太阳时计算
                    ip=args.ip
                )
                # 更新时间信息
                result["date_info"]["adjusted_time_hour"] = adjusted_time_hour
                result["date_info"]["use_true_solar_time"] = True
                result["date_info"]["time_diff_minutes"] = time_diff_minutes
            else:
                # 使用内部真太阳时计算
                result = gua_calculator.calculate_gua(
                    solar_date=date_obj,
                    time_hour=time_hour,
                    longitude=longitude,
                    latitude=latitude,
                    day_master=args.day_master,
                    yong_shen=args.yong_shen,
                    use_true_solar_time=args.use_true_solar_time,
                    ip=args.ip
                )
            
            # 使用增强版显示格式
            print("\n" + "="*50)
            
            # 获取位置信息
            location_info = None
            try:
                location_info = ip_service.get_location_info(args.ip)
            except Exception as e:
                location_info = ip_service.default_location
                
            location_str = f"{location_info.get('country', '')}"
            if 'city' in location_info and location_info['city']:
                location_str += f" {location_info['city']}"
                
            # 测算日期信息
            print(f"\n测算日期：{date_obj.strftime('%Y-%m-%d')}")
            
            # 地理位置信息
            print(f"位置信息：{location_str}")
            print(f"经度：{longitude:.2f}，纬度：{latitude:.2f}")
            
            # 时间信息
            print(f"当地时间：{time_hour:.2f}时")
            print(f"真太阳时：{adjusted_time_hour:.2f}时")
            
            # 提取日期时间信息
            lunar_date = result['date_info']['lunar_date']
            year_gz = result['date_info']['year_gz']
            month_gz = result['date_info']['month_gz']
            day_gz = result['date_info']['day_gz']
            hour_gz = result['date_info']['hour_gz']
            
            # 农历和四柱信息
            print(f"农历：{lunar_date}")
            print(f"四柱：{year_gz} {month_gz} {day_gz} {hour_gz}")
            
            # 日主和用神信息（如果有）
            if args.day_master:
                day_master_element = result["bazi_info"]["day_master_element"]
                print(f"日主：{args.day_master}（五行{day_master_element}）")
            if args.yong_shen:
                print(f"用神：{args.yong_shen}")
                
            # 空亡信息
            kongwang = ", ".join(result["kongwang"]) if result["kongwang"] else "无"
            print(f"空亡：{kongwang}")
            
            # 卦象信息
            ben_gua_name = result['ben_gua']['name']
            ben_gua_element = result['ben_gua']['element']
            ben_palace = result["ben_gua"].get("palace", "")
            ben_gua_type = result["ben_gua"].get("gua_type", "")
            
            bian_gua_name = result['bian_gua']['name']
            bian_gua_element = result['bian_gua']['element']
            bian_palace = result["bian_gua"].get("palace", "")
            bian_gua_type = result["bian_gua"].get("gua_type", "")
            
            print(f"本卦：{ben_gua_name}（{ben_gua_element}）")
            print(f"本卦：{ben_palace}宫 {ben_gua_name}（{ben_gua_type}）    变卦：{bian_palace}宫 {bian_gua_name}（{bian_gua_type}）")
            
            # 提取爻位信息
            shi_yao = result['shi_yao']
            ying_yao = result['ying_yao']
            dong_yao = result['dong_yao']
            
            # 输出爻位信息
            print("="*50)
            
            # 显示传统格式六爻图形
            print("\n传统排盘格式\n")
            
            # 格式化的时间字符串
            time_str = f"{int(time_hour)}时 {int((time_hour - int(time_hour)) * 60)}分"
            
            # 构建传统排盘头部
            header = f"公历：{date_obj.year}年 {date_obj.month}月 {date_obj.day}日 {time_str}\n"
            header += f"干支：{year_gz}年 {month_gz}月 {day_gz}日 {hour_gz}时 （旬空：{kongwang})\n"
            header += f"得「{ben_gua_name}」之「{bian_gua_name}」卦"
            print(header)
            
            # 构建卦宫和卦名行
            print(f"\n{ben_palace}宫:{ben_gua_name}　　　{bian_palace}宫:{bian_gua_name}")
            
            # 导入排盘相关函数和符号
            from models.liuyao.modules.gua_display import generate_najia_style_display, generate_full_gua_display, format_for_print
            
            # 使用改进后的format_for_print函数生成标准排盘效果
            print("\n传统排盘格式（标准版）：")
            traditional_display = format_for_print(result)
            print(traditional_display)
            
            # 使用改进后的排盘格式显示卦象
            print("\n传统排盘格式（改进版）：")
            print(generate_najia_style_display(result))
            
            print("\n完整排盘格式：")
            print(generate_full_gua_display(result))
            print("\n")
            
            # 显示世应爻信息
            print(f"\n世爻：第{shi_yao}爻，应爻：第{ying_yao}爻，动爻：第{dong_yao}爻")
            
            
            # 健康分析
            if 'health_analysis' in result:
                print("\n健康分析:")
                print(f"总体影响: {result['health_analysis']['overall']}")
                
                if result['health_analysis']['specific_issues']:
                    print(f"具体问题: {' '.join(result['health_analysis']['specific_issues'])}")
                    
                if result['health_analysis']['recommendations']:
                    print(f"健康建议: {', '.join(result['health_analysis']['recommendations'])}")
            
            # 保存卦象结果
            save_result = True
            if save_result:
                output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
                os.makedirs(output_dir, exist_ok=True)
                
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = os.path.join(output_dir, f"liuyao_result_{timestamp}.txt")
                
                with open(output_file, "w", encoding="utf-8") as f:
                    # 基本信息
                    f.write("="*50 + "\n")
                    f.write(f"测算日期：{date_obj.strftime('%Y-%m-%d')}\n")
                    f.write(f"经度：{longitude:.2f}，纬度：{latitude:.2f}\n")
                    f.write(f"当地时间：{time_hour:.2f}时\n")
                    f.write(f"真太阳时：{adjusted_time_hour:.2f}时\n")
                    f.write(f"农历：{lunar_date}\n")
                    f.write(f"四柱：{year_gz} {month_gz} {day_gz} {hour_gz}\n")
                    
                    # 日主和用神
                    if args.day_master:
                        f.write(f"日主：{args.day_master}（五行{day_master_element}）\n")
                    if args.yong_shen:
                        f.write(f"用神：{args.yong_shen}\n")
                    
                    # 空亡信息
                    f.write(f"空亡：{kongwang}\n")
                    
                    # 卦象信息
                    f.write(f"\n本卦：{ben_gua_name}（{ben_gua_element}）\n")
                    f.write(f"本卦：{ben_palace}宫 {ben_gua_name}（{ben_gua_type}）    变卦：{bian_palace}宫 {bian_gua_name}（{bian_gua_type}）\n")
                    
                    # 爻符号定义
                    yao_chars = {1: "━━━", 0: "━ ━"}
                    
                    # 爻位信息
                    f.write("="*50 + "\n")
                    for i in range(5, -1, -1):
                        yao_num = i + 1
                        ben_yao = result["ben_gua"]["yao"][i]
                        bian_yao = result["bian_gua"]["yao"][i]
                        
                        marks = []
                        if yao_num == dong_yao:
                            marks.append("动")
                        if yao_num == shi_yao:
                            marks.append("世")
                        if yao_num == ying_yao:
                            marks.append("应")
                        
                        mark_str = f"（{','.join(marks)}）" if marks else ""
                        
                        ben_symbol = yao_chars[ben_yao]
                        if yao_num == dong_yao:
                            ben_symbol = "○" + ben_symbol if ben_yao == 1 else "○ —"
                        
                        bian_symbol = yao_chars[bian_yao]
                        
                        liushen = result["liushen"][i] if i < len(result["liushen"]) else "未知"
                        
                        f.write(f"第{yao_num}爻：{liushen} {ben_symbol} {bian_symbol} {mark_str}\n")
                    f.write("="*50 + "\n")
                    
                    # 六亲六神信息
                    f.write("\n六神六亲信息：\n")
                    for i in range(5, -1, -1):
                        yao_num = i + 1
                        liushen = result["liushen"][i] if i < len(result["liushen"]) else "未知"
                        liuqin = result["liuqin"][i] if i < len(result["liuqin"]) else "未知"
                        najia = result["najia"][i] if i < len(result["najia"]) else "未知"
                        
                        # 判断爻的五行
                        wuxing = "未知"
                        if najia and len(najia) > 0:
                            gan = najia[0]  # 取天干
                            if gan in ["甲", "乙"]:
                                wuxing = "木"
                            elif gan in ["丙", "丁"]:
                                wuxing = "火"
                            elif gan in ["戊", "己"]:
                                wuxing = "土"
                            elif gan in ["庚", "辛"]:
                                wuxing = "金"
                            elif gan in ["壬", "癸"]:
                                wuxing = "水"
                        
                        f.write(f"第{yao_num}爻：六神【{liushen}】六亲【{liuqin}】纳甲【{najia}】五行【{wuxing}】\n")
                    
                    # 空亡信息
                    f.write(f"\n空亡：{kongwang}\n")
                    
                    # 世应爻信息
                    f.write(f"世爻：第{shi_yao}爻\n")
                    f.write(f"应爻：第{ying_yao}爻\n")
                    f.write(f"动爻：第{dong_yao}爻\n")
                    
                    # 将改进了的排盘格式保存到文件
                    f.write("\n\n符合传统排盘格式（改进版）：\n")
                    f.write(generate_najia_style_display(result))
                    
                    f.write("\n\n完整排盘格式：\n")
                    f.write(generate_full_gua_display(result))
                    
                    f.write("\n\n增强版卦象信息：\n")
                    f.write(result["enhanced_display"])
                
                print(f"\n结果已保存至: {output_file}")
            
            # 显示增强版卦象信息
            print("\n是否显示增强版卦象信息？ (y/n)")
            show_enhanced = input().strip().lower()
            if show_enhanced == 'y':
                print("\n" + "=" * 50 + "\n")
                print(result["enhanced_display"])
                print("\n" + "=" * 50)
            
        except Exception as e:
            print(f"六爻计算过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
            
    elif choice == "2":
        display_bagong_info()
    elif choice == "3":
        print("感谢使用，再见！")
        sys.exit(0)
    else:
        print("无效选择，请重试")
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n操作已取消。")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        import traceback
        traceback.print_exc()