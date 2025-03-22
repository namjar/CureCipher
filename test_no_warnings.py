"""
测试没有警告信息的八字计算
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from models.bazi.bazi_calculator import calculate_bazi, generate_bazi_report

def main():
    """测试没有警告信息的八字计算"""
    print("===== 测试八字计算（无警告信息）=====")
    
    # 测试案例：1977年2月25日20:50（晚上8点50分）在北京出生的男性
    print("计算八字中...")
    bazi_result = calculate_bazi(1977, 2, 25, 20, "male", "Beijing")
    
    # 生成报告
    print("生成报告中...")
    report = generate_bazi_report(bazi_result)
    
    # 输出关键信息
    print("\n八字基本信息:")
    print(f"四柱: {bazi_result['bazi']['year']} {bazi_result['bazi']['month']} {bazi_result['bazi']['day']} {bazi_result['bazi']['hour']}")
    print(f"日主: {bazi_result['bazi']['day_master']} ({bazi_result['bazi']['day_master_element']})")
    
    print("\n五行得分:")
    for element, score in bazi_result['five_elements']['scores'].items():
        print(f"{element}: {score}")
    
    print("\n测试完成！")

if __name__ == "__main__":
    main()
