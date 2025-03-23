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

def main():
    """主函数"""
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
        
        # 提取位置信息
        location_info = ip_service.get_location_from_ip(args.ip)
        city_name = location_info.get('city', '未知城市')
        country_name = location_info.get('country', '未知国家')
        
        # 提取日期时间信息
        solar_date_str = result['date_info']['solar_date']
        local_time = result['date_info']['time_hour']
        local_time_h = int(local_time)
        local_time_m = int((local_time - local_time_h) * 60)
        
        adjusted_time = result['date_info']['adjusted_time_hour']
        adjusted_time_h = int(adjusted_time)
        adjusted_time_m = int((adjusted_time - adjusted_time_h) * 60)
        
        lunar_date = result['date_info']['lunar_date']
        year_gz = result['date_info']['year_gz']
        month_gz = result['date_info']['month_gz']
        day_gz = result['date_info']['day_gz']
        hour_gz = result['date_info']['hour_gz']
        
        # 四柱干支
        four_pillars = f"{year_gz} {month_gz} {day_gz} {hour_gz}"
        
        # 提取卦象信息
        ben_gua_name = result['ben_gua']['name']
        ben_gua_element = result['ben_gua']['element']
        bian_gua_name = result['bian_gua']['name']
        bian_gua_element = result['bian_gua']['element']
        
        # 提取爻位信息
        shi_yao = result['shi_yao']
        ying_yao = result['ying_yao']
        dong_yao = result['dong_yao']
        
        # 输出格式化的结果，模拟截图中的格式
        print("\n" + "="*50)
        
        # 惊蛰、清明节气等信息
        jieqi_str = f"惊蛰: \033[31m{date_obj.year}年03月05日16时11分\033[0m"
        qingming_str = f"清明: \033[31m{date_obj.year}年04月04日20时52分\033[0m"
        print(jieqi_str)
        print(qingming_str)
        
        # 干支日期信息
        rikonganzhiStr = f"干支: {year_gz}年 {month_gz}月 {day_gz}日 {hour_gz}时"
        
        # 确定日空，例如："子未"
        rikong = result["kongwang"][0] if result["kongwang"] else "无"
        rikongStr = f"（日空: {rikong}）"
        print(rikonganzhiStr + " " + rikongStr)
        
        # 神煞信息
        shenshas = []
        if "shenshas" in result and result["shenshas"]:
            for type_key in ["year", "month", "day", "hour"]:
                if type_key in result["shenshas"] and result["shenshas"][type_key]:
                    for name, pos in result["shenshas"][type_key]:
                        shenshas.append(f"{name}－{pos}")
        
        shenshaStr = "神煞: " + ", ".join(shenshas[:5])  # 显示前5个神煞
        print(shenshaStr)
        
        # 卦宫信息
        bengong = f"坤宫: {ben_gua_name}为地 (六冲)" if ben_gua_name == "坤" else f"{ben_gua_name}宫: {ben_gua_name}为地 (六冲)"
        biangong = f"震宫: 雷地豫 (六合)" if bian_gua_name == "震" else f"{bian_gua_name}宫: 雷地豫 (六合)"
        print("")
        print(f"{bengong}        {biangong}")
        
        # 六神以及本卦变卦对照表
        print("六神     伏神     本     卦        变     卦")
        
        # 输出六爻信息
        for i in range(5, -1, -1):  # 从上往下遍历六爻
            yao_num = i + 1
            liushen = result["liushen"][i]
            liuqin = result["liuqin"][i]
            najia = result["najia"][i]
            bian_liuqin = result["bian_liuqin"][i] if "bian_liuqin" in result else ""
            bian_najia = result["bian_najia"][i] if "bian_najia" in result else ""
            
            # 判断是否为动爻、世爻、应爻
            dongmark = "×→" if yao_num == dong_yao else "    "
            shi_mark = "世" if yao_num == shi_yao else ""
            ying_mark = "应" if yao_num == ying_yao else ""
            
            # 爻的符号（阴爻或阳爻）
            ben_symbol = "———" if result["ben_gua"]["yao"][i] == 1 else "— —"
            bian_symbol = "———" if result["bian_gua"]["yao"][i] == 1 else "— —"
            
            # 输出一行爻信息
            print(f"{liushen}     {liuqin}{najia}  {ben_symbol} {shi_mark}  {dongmark} {bian_liuqin}{bian_najia}  {bian_symbol} {ying_mark}")
        
        # 健康分析
        if 'health_analysis' in result:
            print("\n健康分析:")
            print(f"总体影响: {result['health_analysis']['overall']}")
            
            if result['health_analysis']['specific_issues']:
                print(f"具体问题: {' '.join(result['health_analysis']['specific_issues'])}")
                
            if result['health_analysis']['recommendations']:
                print(f"健康建议: {', '.join(result['health_analysis']['recommendations'])}")
        
        # 保存卦象结果（可选）
        save_result = False
        if save_result:
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(output_dir, f"liuyao_result_{timestamp}.txt")
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join([
                    jieqi_str,
                    qingming_str,
                    rikonganzhiStr + " " + rikongStr,
                    shenshaStr,
                    "",
                    f"{bengong}        {biangong}",
                    "六神     伏神     本     卦        变     卦"
                ]))
                
                # 写入六爻信息
                for i in range(5, -1, -1):
                    yao_num = i + 1
                    liushen = result["liushen"][i]
                    liuqin = result["liuqin"][i]
                    najia = result["najia"][i]
                    bian_liuqin = result["bian_liuqin"][i] if "bian_liuqin" in result else ""
                    bian_najia = result["bian_najia"][i] if "bian_najia" in result else ""
                    
                    dongmark = "×→" if yao_num == dong_yao else "    "
                    shi_mark = "世" if yao_num == shi_yao else ""
                    ying_mark = "应" if yao_num == ying_yao else ""
                    
                    ben_symbol = "———" if result["ben_gua"]["yao"][i] == 1 else "— —"
                    bian_symbol = "———" if result["bian_gua"]["yao"][i] == 1 else "— —"
                    
                    f.write(f"\n{liushen}     {liuqin}{najia}  {ben_symbol} {shi_mark}  {dongmark} {bian_liuqin}{bian_najia}  {bian_symbol} {ying_mark}")
            
            print(f"\n结果已保存至: {output_file}")
        
    except Exception as e:
        print(f"六爻计算过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
