
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字计算命令行工具

在项目根目录下运行：
$ python bazi_cli.py <参数>
"""

import argparse
import json
import os
import sys

# 确保可以正确导入项目模块
def ensure_path():
    # 获取当前脚本的绝对路径
    script_path = os.path.abspath(__file__)
    # 获取脚本所在的目录（项目根目录）
    root_dir = os.path.dirname(script_path)
    
    # 切换到项目根目录
    if os.getcwd() != root_dir:
        os.chdir(root_dir)
        print(f"已切换到项目根目录: {root_dir}")
    
    # 将项目根目录添加到系统路径
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

# 先确保路径正确
ensure_path()

# 然后导入模块
from models.bazi.bazi_calculator import calculate_bazi, generate_bazi_report

def main():
    """主函数"""
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='八字计算命令行工具')
    parser.add_argument('year', type=int, help='出生年份')
    parser.add_argument('month', type=int, help='出生月份')
    parser.add_argument('day', type=int, help='出生日期')
    parser.add_argument('hour', type=int, help='出生时辰（24小时制）')
    parser.add_argument('-g', '--gender', choices=['male', 'female'], default='male', 
                        help='性别（male男性/female女性，默认为male）')
    parser.add_argument('-c', '--city', type=str, default=None, 
                        help='出生城市（可选，默认根据IP定位）')
    parser.add_argument('-f', '--format', choices=['text', 'json'], default='text', 
                        help='输出格式（text文本/json JSON，默认为text）')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 计算八字
    bazi_result = calculate_bazi(
        args.year, args.month, args.day, args.hour, 
        args.gender, args.city
    )
    
    # 生成报告
    report = generate_bazi_report(bazi_result)
    
    # 输出结果
    if args.format == 'json':
        # JSON格式输出
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        # 文本格式输出
        print("="*50)
        print("八字命盘分析")
        print("="*50)
        print(report['text_report'])
        print("\n")
        print("="*50)
        print("详细信息")
        print("="*50)
        print(f"出生时间: {report['basic_info']['solar_date']} ({report['basic_info']['lunar_date']})")
        print(f"八字: {report['basic_info']['four_pillars']}")
        print(f"五行得分: {report['five_elements']['scores']}")
        print(f"日主强度: {report['pattern_analysis']['day_master_strength']} ({report['pattern_analysis']['day_master_percentage']}%)")
        print(f"用神: {report['pattern_analysis']['yong_shen']}")
        print(f"命宫: {report['special']['ming_gong']}")
        print(f"胎元: {report['special']['tai_yuan']}")
        
        # 打印大运信息
        print("\n大运:")
        if report['current_dayun']:
            print(f"当前大运: {report['current_dayun']['ganzhi']} ({report['current_dayun']['age_range']}岁)")
        for dayun in report['dayun_analysis']:
            print(f"  {dayun['ganzhi']} ({dayun['age_range']}岁)")
        
        # 打印神煞信息
        print("\n神煞:")
        for shensha in report['shensha_info']:
            print(f"  {shensha['name']} ({shensha['position']}柱): {shensha['description']}")

if __name__ == "__main__":
    main()
