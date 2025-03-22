"""
八字计算模块测试
测试特定出生日期的八字计算结果
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# 添加项目根目录到系统路径，以便导入项目模块
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from models.bazi.calculator import calculate_bazi
from models.bazi.five_elements import analyze_five_elements
from models.bazi.shensha import analyze_shensha

def test_specific_bazi():
    """
    测试特定八字 - 1977年2月25日晚上8点50分，男性，北京
    """
    # 将阳历时间转换为24小时制
    birth_year = 1977
    birth_month = 2
    birth_day = 25
    birth_hour = 20
    birth_minute = 50
    
    # 由于分钟可能影响小时的计算，四舍五入到整点
    if birth_minute >= 30:
        birth_hour += 1
    
    if birth_hour >= 24:
        birth_hour = 0
    
    print(f"测试数据: {birth_year}年{birth_month}月{birth_day}日 {birth_hour}点，男性，北京")
    
    # 计算八字
    print("计算八字中...")
    bazi_result = calculate_bazi(birth_year, birth_month, birth_day, birth_hour, "male", "Beijing")
    
    # 分析五行
    print("分析五行中...")
    elements_result = analyze_five_elements(bazi_result)
    
    # 分析神煞
    print("分析神煞中...")
    shensha_result = analyze_shensha(bazi_result.get("shensha", []), bazi_result["bazi"]["day_master_element"])
    
    # 确保输出目录存在
    output_dir = project_root / "tests" / "output"
    if not output_dir.exists():
        os.makedirs(output_dir)
    
    # 保存计算结果到JSON文件
    with open(output_dir / "bazi_result.json", "w", encoding="utf-8") as f:
        json.dump(bazi_result, f, ensure_ascii=False, indent=2)
    
    with open(output_dir / "elements_result.json", "w", encoding="utf-8") as f:
        json.dump(elements_result, f, ensure_ascii=False, indent=2)
    
    with open(output_dir / "shensha_result.json", "w", encoding="utf-8") as f:
        json.dump(shensha_result, f, ensure_ascii=False, indent=2)
    
    # 输出结果
    print("\n============== 八字计算结果 ==============")
    print(f"四柱: {bazi_result['bazi']['year']} {bazi_result['bazi']['month']} {bazi_result['bazi']['day']} {bazi_result['bazi']['hour']}")
    print(f"日主: {bazi_result['bazi']['day_master']} ({bazi_result['bazi']['day_master_element']})")
    print(f"纳音: 年-{bazi_result['nayin']['year']} 月-{bazi_result['nayin']['month']} 日-{bazi_result['nayin']['day']} 时-{bazi_result['nayin']['hour']}")
    
    print("\n当前运势:")
    print(f"流年: {bazi_result['current']['liunian']} ({bazi_result['current']['liunian_element']})")
    print(f"流月: {bazi_result['current']['liuyue']} ({bazi_result['current']['liuyue_element']})")
    print(f"大运: {bazi_result['dayun']['ganzhi']} ({bazi_result['dayun']['element']}), 年龄: {bazi_result['dayun']['start_age']}-{bazi_result['dayun']['end_age']}")
    print(f"小运: {bazi_result['xiaoyun']['ganzhi']} ({bazi_result['xiaoyun']['element']})")
    
    print("\n五行分析:")
    print(f"五行比例: 木:{elements_result['element_percentages']['木']:.1f}% 火:{elements_result['element_percentages']['火']:.1f}% 土:{elements_result['element_percentages']['土']:.1f}% 金:{elements_result['element_percentages']['金']:.1f}% 水:{elements_result['element_percentages']['水']:.1f}%")
    print(f"平衡状态: {elements_result['balance_analysis']['balance_state']}")
    print(f"平衡描述: {elements_result['balance_analysis']['description']}")
    print(f"日主状态: {elements_result['day_master_analysis']['strength_state']} ({elements_result['day_master_analysis']['strength']:.1f}%)")
    print(f"日主建议: {elements_result['day_master_analysis']['advice']}")
    
    print("\n神煞分析:")
    if shensha_result['positive_impacts']:
        print(f"吉神: {', '.join([impact['name'] for impact in shensha_result['positive_impacts']])}")
    else:
        print("吉神: 无")
    
    if shensha_result['negative_impacts']:
        print(f"凶神: {', '.join([impact['name'] for impact in shensha_result['negative_impacts']])}")
    else:
        print("凶神: 无")
    
    print(f"总体趋势: {shensha_result['overall_analysis']['tendency']}")
    print(f"日主相性: {shensha_result['overall_analysis']['day_master_impact']}")
    
    print("\n健康建议:")
    print(f"整体健康状况: {shensha_result['overall_analysis']['health_analysis']['overall_status']}")
    
    if shensha_result['overall_analysis']['health_analysis']['health_strengths']:
        print(f"健康优势: {', '.join(shensha_result['overall_analysis']['health_analysis']['health_strengths'])}")
    else:
        print("健康优势: 无特定优势")
    
    if shensha_result['overall_analysis']['health_analysis']['health_weaknesses']:
        print(f"健康劣势: {', '.join(shensha_result['overall_analysis']['health_analysis']['health_weaknesses'])}")
    else:
        print("健康劣势: 无特定劣势")
    
    for advice in shensha_result['health_advice']:
        print(f"- {advice['advice']}")
    
    print("\n饮食建议:")
    for flavor in elements_result['diet_advice']['recommended_flavors']:
        print(f"- 推荐食用{flavor['flavor']}食物，{flavor['effect']}，补充{', '.join(flavor['nutrients'])}")
    
    print("\n运动建议:")
    for exercise in elements_result['exercise_advice']['recommended_exercises']:
        print(f"- 推荐{', '.join(exercise['exercise_types'])}类运动，{exercise['effect']}")
    
    print("\n计算结果已保存到tests/output目录")
    return bazi_result, elements_result, shensha_result

if __name__ == "__main__":
    test_specific_bazi()
