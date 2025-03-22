# /Users/ericw/Documents/GitHub/CureCipher/tests/integration/test_full_calculation.py
"""
完整八字计算流程集成测试
"""
import pytest
from models.bazi.bazi_calculator import calculate_bazi, generate_bazi_report

class TestFullCalculation:
    def test_calculate_bazi(self, sample_birth_cases):
        """测试完整的八字计算流程"""
        for case in sample_birth_cases:
            result = calculate_bazi(
                case["year"], case["month"], case["day"], 
                case["hour"], case["gender"], case["city"]
            )
            
            # 验证结果结构
            assert "bazi" in result
            assert "five_elements" in result
            assert "ten_gods" in result
            assert "pattern" in result
            assert "dayuns" in result
            assert "current" in result
            assert "special" in result
            assert "nayin" in result
            assert "analysis" in result
            
            # 验证基本信息
            assert len(result["bazi"]["gans"]) == 4
            assert len(result["bazi"]["zhis"]) == 4
            assert result["bazi"]["day_master"] in "甲乙丙丁戊己庚辛壬癸"
            
    def test_report_generation(self, sample_birth_cases):
        """测试报告生成流程"""
        for case in sample_birth_cases:
            bazi_result = calculate_bazi(
                case["year"], case["month"], case["day"], 
                case["hour"], case["gender"], case["city"]
            )
            
            report = generate_bazi_report(bazi_result)
            
            # 验证报告结构
            assert "basic_info" in report
            assert "pattern_analysis" in report
            assert "dayun_analysis" in report
            assert "current_info" in report
            assert "text_report" in report
            
            # 验证文本报告内容
            text_report = report["text_report"]
            assert "八字命盘解读" in text_report
            assert "基本信息" in text_report
            assert "命盘分析" in text_report
            assert "当前大运" in text_report
            assert "流年流月流日" in text_report
            assert "特殊格局分析" in text_report