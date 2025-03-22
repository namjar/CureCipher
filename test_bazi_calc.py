"""
八字计算测试脚本
计算1977年2月25日晚上8点50分在北京出生的男性的八字
"""

from models.bazi.calculator import calculate_bazi
from models.bazi.five_elements import analyze_five_elements
from models.bazi.shensha import analyze_shensha
import json

def main():
    # 将阳历时间转换为24小时制
    birth_hour = 20
    birth_minute = 50
    
    # 由于分钟可能影响小时的计算，四舍五入到整点
    if birth_minute >= 30:
        birth_hour += 1
    
    if birth_hour >= 24:
        birth_hour = 0
    
    # 计算八字
    print("计算八字中...")
    bazi_result = calculate_bazi(1977, 2, 25, birth_hour, "male", "Beijing")
    
    # 将结果保存为JSON文件以便查看
    with open("bazi_result.json", "w", encoding="utf-8") as f:
        json.dump(bazi_result, f, ensure_ascii=False, indent=2)
    
    print("八字计算完成，结果已保存到bazi_result.json")
    
    # 打印基本信息
    print("\n基本八字信息:")
    print(f"四柱: {bazi_result['bazi']['year']} {bazi_result['bazi']['month']} {bazi_result['bazi']['day']} {bazi_result['bazi']['hour']}")
    print(f"日主: {bazi_result['bazi']['day_master']} ({bazi_result['bazi']['day_master_element']})")
    
    # 分析五行
    print("\n分析五行...")
    elements_result = analyze_five_elements(bazi_result)
    with open("elements_result.json", "w", encoding="utf-8") as f:
        json.dump(elements_result, f, ensure_ascii=False, indent=2)
    
    print("五行分析完成，结果已保存到elements_result.json")
    
    # 分析神煞
    print("\n分析神煞...")
    shensha_result = analyze_shensha(bazi_result.get("shensha", []), bazi_result["bazi"]["day_master_element"])
    with open("shensha_result.json", "w", encoding="utf-8") as f:
        json.dump(shensha_result, f, ensure_ascii=False, indent=2)
    
    print("神煞分析完成，结果已保存到shensha_result.json")

if __name__ == "__main__":
    main()
