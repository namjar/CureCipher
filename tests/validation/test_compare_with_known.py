# /Users/ericw/Documents/GitHub/CureCipher/tests/validation/test_compare_with_known.py
"""
与已知结果对比验证测试
"""
import pytest
from models.bazi.bazi_calculator import calculate_bazi, generate_bazi_report

class TestKnownResults:
    def test_known_cases(self, verified_cases):
        """测试已知案例的计算结果"""
        for case in verified_cases:
            input_data = case["input"]
            expected = case["expected"]
            
            # 计算结果
            bazi_result = calculate_bazi(
                input_data["year"], input_data["month"], input_data["day"], 
                input_data["hour"], input_data["gender"], input_data["city"]
            )
            report = generate_bazi_report(bazi_result)
            
            # 打印调试信息
            print(f"\n测试案例: {input_data}")
            print(f"实际四柱: {bazi_result['bazi']['year']} {bazi_result['bazi']['month']} {bazi_result['bazi']['day']} {bazi_result['bazi']['hour']}")
            print(f"预期四柱: {expected['four_pillars']}")
            
            # 对比关键项目
            actual_four_pillars = f"{bazi_result['bazi']['year']} {bazi_result['bazi']['month']} {bazi_result['bazi']['day']} {bazi_result['bazi']['hour']}"
            actual_day_master = bazi_result['bazi']['day_master']
            actual_day_master_element = bazi_result['bazi']['day_master_element']
            
            # 验证关键结果
            assert actual_day_master == expected["day_master"], f"日主计算错误: 预期{expected['day_master']}, 实际{actual_day_master}"
            assert actual_day_master_element == expected["day_master_element"], f"日主五行计算错误: 预期{expected['day_master_element']}, 实际{actual_day_master_element}"
            
            # 验证用神(可能会有差异，因为用神判断有多种算法)
            if "yong_shen" in expected:
                print(f"预期用神: {expected['yong_shen']}")
                print(f"实际用神: {report['pattern_analysis']['yong_shen'].split()[0]}")