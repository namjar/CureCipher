#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字计算示例

在项目根目录下运行：
$ python examples/bazi_example.py
"""

import os
import sys

# 确保可以正确导入项目模块
def ensure_path():
    # 获取当前脚本的绝对路径
    script_path = os.path.abspath(__file__)
    # 获取脚本所在的目录
    script_dir = os.path.dirname(script_path)
    # 获取项目根目录
    root_dir = os.path.dirname(script_dir)
    
    # 切换到项目根目录
    if os.getcwd() != root_dir:
        os.chdir(root_dir)
        print(f"已切换到项目根目录: {root_dir}")
    
    # 将项目根目录添加到系统路径
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
        print(f"已将项目根目录添加到系统路径")

# 先确保路径正确
ensure_path()

# 然后导入模块
from models.bazi.bazi_calculator import calculate_bazi, generate_bazi_report

def main():
    """主函数"""
    # 示例数据
    birth_year = 1990
    birth_month = 5
    birth_day = 15
    birth_hour = 12
    gender = "male"
    city = "北京"
    
    print(f"计算八字：{birth_year}年{birth_month}月{birth_day}日{birth_hour}时 {gender} {city}")
    print("=" * 60)
    
    # 计算八字
    bazi_result = calculate_bazi(birth_year, birth_month, birth_day, birth_hour, gender, city)
    
    # 基本信息
    print("基本信息：")
    print(f"四柱八字：{bazi_result['bazi']['year']} {bazi_result['bazi']['month']} {bazi_result['bazi']['day']} {bazi_result['bazi']['hour']}")
    print(f"天干：{' '.join(bazi_result['bazi']['gans'])}")
    print(f"地支：{' '.join(bazi_result['bazi']['zhis'])}")
    print(f"日主：{bazi_result['bazi']['day_master']} ({bazi_result['bazi']['day_master_element']})")
    print("=" * 60)
    
    # 五行得分
    print("五行得分：")
    for element, score in bazi_result['five_elements']['scores'].items():
        print(f"{element}: {score}")
    print("=" * 60)
    
    # 命宫和胎元
    print("命宫和胎元：")
    print(f"命宫：{bazi_result['special']['ming_gong']}")
    print(f"胎元：{bazi_result['special']['tai_yuan']}")
    print("=" * 60)
    
    # 神煞信息
    print("神煞信息：")
    for shensha in bazi_result['shensha']:
        print(f"{shensha['name']} ({shensha['position']}柱)：{shensha['description']}")
    print("=" * 60)
    
    # 大运信息
    print("大运信息：")
    for i, dayun in enumerate(bazi_result['dayuns']):
        print(f"{i+1}. {dayun['ganzhi']} ({dayun['start_age']}-{dayun['end_age']}岁) 天干十神: {dayun['gan_shen']} 地支十神: {dayun['zhi_shen']}")
    print("=" * 60)
    
    # 生成完整报告
    print("生成完整报告...")
    report = generate_bazi_report(bazi_result)
    
    # 打印报告摘要
    print("报告摘要：")
    print(f"日主强度: {report['pattern_analysis']['day_master_strength']} ({report['pattern_analysis']['day_master_percentage']}%)")
    print(f"五行平衡: {report['pattern_analysis']['balance_state']}")
    print(f"用神: {report['pattern_analysis']['yong_shen']}")
    
    # 保存报告到文件
    report_file = f"bazi_report_{birth_year}_{birth_month}_{birth_day}.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report['text_report'])
    
    print(f"\n完整报告已保存到 {report_file}")

if __name__ == "__main__":
    main()
