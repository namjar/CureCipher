"""
八字计算工具

命令行工具，用于计算特定出生日期的八字及相关分析
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

# 添加项目根目录到系统路径，以便导入项目模块
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from models.bazi.calculator import calculate_bazi
from models.bazi.five_elements import analyze_five_elements
from models.bazi.shensha import analyze_shensha

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='八字计算工具')
    parser.add_argument('-y', '--year', type=int, required=True, help='出生年份')
    parser.add_argument('-m', '--month', type=int, required=True, help='出生月份')
    parser.add_argument('-d', '--day', type=int, required=True, help='出生日期')
    parser.add_argument('-H', '--hour', type=int, required=True, help='出生小时（24小时制）')
    parser.add_argument('-M', '--minute', type=int, default=0, help='出生分钟')
    parser.add_argument('-g', '--gender', choices=['male', 'female'], required=True, help='性别（male/female）')
    parser.add_argument('-c', '--city', default='Beijing', help='出生城市（默认为北京）')
    parser.add_argument('-o', '--output', default=None, help='输出文件路径')
    
    return parser.parse_args()

def round_hour(hour, minute):
    """四舍五入小时"""
    if minute >= 30:
        hour += 1
    
    if hour >= 24:
        hour = 0
    
    return hour

def main():
    """主函数"""
    args = parse_arguments()
    
    # 四舍五入小时
    hour = round_hour(args.hour, args.minute)
    
    print(f"计算 {args.year}年{args.month}月{args.day}日 {hour}时 {args.gender} {args.city} 的八字...")
    
    # 计算八字
    bazi_result = calculate_bazi(args.year, args.month, args.day, hour, args.gender, args.city)
    
    # 分析五行
    elements_result = analyze_five_elements(bazi_result)
    
    # 分析神煞
    shensha_result = analyze_shensha(bazi_result.get("shensha", []), bazi_result["bazi"]["day_master_element"])
    
    # 构建完整结果
    full_result = {
        "input": {
            "birth_year": args.year,
            "birth_month": args.month,
            "birth_day": args.day,
            "birth_hour": args.hour,
            "birth_minute": args.minute,
            "rounded_hour": hour,
            "gender": args.gender,
            "city": args.city
        },
        "bazi_result": bazi_result,
        "elements_result": elements_result,
        "shensha_result": shensha_result
    }
    
    # 保存结果
    if args.output:
        output_path = Path(args.output)
    else:
        # 默认保存到项目根目录下的outputs文件夹
        output_dir = project_root / "outputs"
        if not output_dir.exists():
            os.makedirs(output_dir)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = output_dir / f"bazi_{args.year}{args.month:02d}{args.day:02d}_{timestamp}.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(full_result, f, ensure_ascii=False, indent=2)
    
    print(f"计算完成，结果已保存到 {output_path}")
    
    # 打印简要结果
    print("\n============== 八字计算结果 ==============")
    print(f"四柱: {bazi_result['bazi']['year']} {bazi_result['bazi']['month']} {bazi_result['bazi']['day']} {bazi_result['bazi']['hour']}")
    print(f"日主: {bazi_result['bazi']['day_master']} ({bazi_result['bazi']['day_master_element']})")
    
    print("\n当前运势:")
    print(f"流年: {bazi_result['current']['liunian']} ({bazi_result['current']['liunian_element']})")
    print(f"大运: {bazi_result['dayun']['ganzhi']} ({bazi_result['dayun']['element']})")
    
    print("\n五行分析:")
    print(f"五行比例: 木:{elements_result['element_percentages']['木']:.1f}% 火:{elements_result['element_percentages']['火']:.1f}% 土:{elements_result['element_percentages']['土']:.1f}% 金:{elements_result['element_percentages']['金']:.1f}% 水:{elements_result['element_percentages']['水']:.1f}%")
    print(f"平衡状态: {elements_result['balance_analysis']['balance_state']}")
    
    print("\n更多详细结果请查看保存的文件")

if __name__ == "__main__":
    main()
