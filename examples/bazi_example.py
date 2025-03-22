"""
八字计算模块使用示例

展示如何在Python代码中使用八字计算模块
"""

import sys
import os
from pathlib import Path
import json

# 添加项目根目录到系统路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from models.bazi.calculator import calculate_bazi
from models.bazi.five_elements import analyze_five_elements
from models.bazi.shensha import analyze_shensha

def example_1():
    """基本八字计算示例"""
    print("\n=== 示例1: 基本八字计算 ===")
    
    # 计算八字
    bazi_result = calculate_bazi(
        birth_year=1977,
        birth_month=2,
        birth_day=25,
        birth_hour=21,  # 8:50pm四舍五入到9点
        gender="male",
        city="Beijing"
    )
    
    # 打印基本信息
    print(f"四柱: {bazi_result['bazi']['year']} {bazi_result['bazi']['month']} {bazi_result['bazi']['day']} {bazi_result['bazi']['hour']}")
    print(f"日主: {bazi_result['bazi']['day_master']} ({bazi_result['bazi']['day_master_element']})")
    print(f"纳音: 年-{bazi_result['nayin']['year']} 月-{bazi_result['nayin']['month']} 日-{bazi_result['nayin']['day']} 时-{bazi_result['nayin']['hour']}")

def example_2():
    """五行分析示例"""
    print("\n=== 示例2: 五行分析 ===")
    
    # 计算八字
    bazi_result = calculate_bazi(
        birth_year=1977,
        birth_month=2,
        birth_day=25,
        birth_hour=21,
        gender="male",
        city="Beijing"
    )
    
    # 分析五行
    elements_result = analyze_five_elements(bazi_result)
    
    # 打印五行分析结果
    print("五行比例:")
    for element, percentage in elements_result['element_percentages'].items():
        print(f"  {element}: {percentage:.1f}%")
    
    print(f"\n平衡状态: {elements_result['balance_analysis']['balance_state']}")
    print(f"平衡描述: {elements_result['balance_analysis']['description']}")
    print(f"日主状态: {elements_result['day_master_analysis']['strength_state']} ({elements_result['day_master_analysis']['strength']:.1f}%)")
    print(f"日主建议: {elements_result['day_master_analysis']['advice']}")

def example_3():
    """健康建议示例"""
    print("\n=== 示例3: 健康建议 ===")
    
    # 计算八字
    bazi_result = calculate_bazi(
        birth_year=1977,
        birth_month=2,
        birth_day=25,
        birth_hour=21,
        gender="male",
        city="Beijing"
    )
    
    # 分析五行
    elements_result = analyze_five_elements(bazi_result)
    
    # 分析神煞
    shensha_result = analyze_shensha(
        bazi_result.get("shensha", []),
        bazi_result["bazi"]["day_master_element"]
    )
    
    # 打印健康建议
    print("基本健康建议:")
    print(f"  {elements_result['health_advice']['general_advice']}")
    print(f"  {elements_result['health_advice']['seasonal_advice']}")
    
    print("\n饮食建议:")
    for flavor in elements_result['diet_advice']['recommended_flavors']:
        print(f"  - 推荐食用{flavor['flavor']}食物，{flavor['effect']}，补充{', '.join(flavor['nutrients'])}")
    
    print("\n运动建议:")
    for exercise in elements_result['exercise_advice']['recommended_exercises']:
        print(f"  - 推荐{', '.join(exercise['exercise_types'])}类运动，{exercise['effect']}")
    
    print("\n神煞健康建议:")
    for advice in shensha_result['health_advice']:
        print(f"  - {advice['advice']}")

def example_4():
    """批量计算示例"""
    print("\n=== 示例4: 批量计算 ===")
    
    # 准备多个出生数据
    birth_data = [
        {"year": 1977, "month": 2, "day": 25, "hour": 21, "gender": "male", "city": "Beijing"},
        {"year": 1980, "month": 5, "day": 15, "hour": 14, "gender": "female", "city": "Shanghai"},
        {"year": 1990, "month": 10, "day": 10, "hour": 10, "gender": "male", "city": "Guangzhou"}
    ]
    
    # 批量计算结果
    results = []
    for data in birth_data:
        # 计算八字
        bazi_result = calculate_bazi(
            data["year"], data["month"], data["day"], data["hour"], data["gender"], data["city"]
        )
        
        # 生成简要结果
        summary = {
            "birth_info": f"{data['year']}年{data['month']}月{data['day']}日 {data['hour']}时 {data['gender']} {data['city']}",
            "four_pillars": f"{bazi_result['bazi']['year']} {bazi_result['bazi']['month']} {bazi_result['bazi']['day']} {bazi_result['bazi']['hour']}",
            "day_master": f"{bazi_result['bazi']['day_master']} ({bazi_result['bazi']['day_master_element']})"
        }
        
        results.append(summary)
    
    # 打印结果
    for idx, result in enumerate(results, 1):
        print(f"数据{idx}:")
        print(f"  出生信息: {result['birth_info']}")
        print(f"  四柱: {result['four_pillars']}")
        print(f"  日主: {result['day_master']}")
        print()

def example_5():
    """将结果保存为JSON文件"""
    print("\n=== 示例5: 保存结果 ===")
    
    # 计算八字
    bazi_result = calculate_bazi(
        birth_year=1977,
        birth_month=2,
        birth_day=25,
        birth_hour=21,
        gender="male",
        city="Beijing"
    )
    
    # 分析五行
    elements_result = analyze_five_elements(bazi_result)
    
    # 分析神煞
    shensha_result = analyze_shensha(
        bazi_result.get("shensha", []),
        bazi_result["bazi"]["day_master_element"]
    )
    
    # 合并结果
    full_result = {
        "input": {
            "birth_year": 1977,
            "birth_month": 2,
            "birth_day": 25,
            "birth_hour": 21,
            "gender": "male",
            "city": "Beijing"
        },
        "bazi_result": bazi_result,
        "elements_result": elements_result,
        "shensha_result": shensha_result
    }
    
    # 保存为JSON文件
    output_dir = project_root / "examples" / "output"
    if not output_dir.exists():
        os.makedirs(output_dir)
    
    output_path = output_dir / "bazi_example_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(full_result, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到 {output_path}")

if __name__ == "__main__":
    print("八字计算模块使用示例")
    print("=" * 40)
    
    # 运行示例
    example_1()
    example_2()
    example_3()
    example_4()
    example_5()
    
    print("\n示例运行完成！")
