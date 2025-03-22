# /Users/ericw/Documents/GitHub/CureCipher/tests/unit/test_special_patterns.py
"""
特殊格局分析单元测试
"""
import pytest
from models.bazi.bazi_calculator import analyze_special_patterns

class TestSpecialPatterns:
    def test_san_he_patterns(self, special_pattern_cases):
        """测试三合格局识别"""
        for case in special_pattern_cases:
            patterns = analyze_special_patterns(case["zhis"])
            
            # 检查三合格局
            san_he_names = [p["name"] for p in patterns["san_he"]]
            for expected in case["expected_san_he"]:
                assert expected in san_he_names, f"案例'{case['description']}'未能检测到预期的{expected}格局"
            
            # 确保没有意外的三合格局
            assert len(san_he_names) == len(case["expected_san_he"]), \
                f"案例'{case['description']}'检测到意外的三合格局: {san_he_names}"
    
    def test_san_hui_patterns(self, special_pattern_cases):
        """测试三会格局识别"""
        for case in special_pattern_cases:
            patterns = analyze_special_patterns(case["zhis"])
            
            # 检查三会格局
            san_hui_names = [p["name"] for p in patterns["san_hui"]]
            for expected in case["expected_san_hui"]:
                assert expected in san_hui_names, f"案例'{case['description']}'未能检测到预期的{expected}格局"
            
            # 确保没有意外的三会格局
            assert len(san_hui_names) == len(case["expected_san_hui"]), \
                f"案例'{case['description']}'检测到意外的三会格局: {san_hui_names}"
    
    def test_specific_patterns(self):
        """测试特定的格局组合"""
        # 测试完整的水三合
        zhis = ["子", "申", "辰"]
        patterns = analyze_special_patterns(zhis)
        assert len(patterns["san_he"]) == 1
        assert patterns["san_he"][0]["name"] == "水三合"
        assert patterns["san_he"][0]["element"] == "水"
        
        # 测试完整的东方三会
        zhis = ["寅", "卯", "辰"]
        patterns = analyze_special_patterns(zhis)
        assert len(patterns["san_hui"]) == 1
        assert patterns["san_hui"][0]["name"] == "东方三会"
        assert patterns["san_hui"][0]["element"] == "木"
        
        # 测试冠带格局
        zhis = ["寅", "卯", "辰", "酉"]
        patterns = analyze_special_patterns(zhis)
        assert len(patterns["guan_xin"]) > 0, "未检测到冠带格局"