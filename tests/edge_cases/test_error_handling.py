# /Users/ericw/Documents/GitHub/CureCipher/tests/edge_cases/test_error_handling.py
"""
边界情况和错误处理测试
"""
import pytest
from models.bazi.bazi_calculator import calculate_bazi

class TestErrorHandling:
    def test_invalid_dates(self):
        """测试无效日期处理"""
        invalid_cases = [
            # 2月30日不存在
            {"year": 2021, "month": 2, "day": 30, "hour": 12, "gender": "male"},
            # 4月31日不存在
            {"year": 2021, "month": 4, "day": 31, "hour": 12, "gender": "female"},
            # 无效小时
            {"year": 2021, "month": 1, "day": 1, "hour": 25, "gender": "male"}
        ]
        
        for case in invalid_cases:
            print(f"\n测试无效日期: {case}")
            result = calculate_bazi(**case)
            assert "error" in result or "message" in result, f"未正确处理无效日期: {case}"
            print(f"错误处理结果: {result.get('message', '')}")
            
    def test_error_messages(self):
        """测试错误信息明确性"""
        try:
            result = calculate_bazi(2021, 2, 30, 12, "male")
            if "error" in result:
                error_msg = result["message"]
                assert "日期" in error_msg, "错误信息不明确"
        except Exception as e:
            assert "日期" in str(e), "异常信息不明确"
            
    def test_boundary_dates(self):
        """测试边界日期处理"""
        boundary_cases = [
            # 早期日期
            {"year": 1900, "month": 1, "day": 1, "hour": 0, "gender": "male"},
            # 闰年2月29日
            {"year": 2000, "month": 2, "day": 29, "hour": 12, "gender": "female"},
            # 远期日期
            {"year": 2050, "month": 12, "day": 31, "hour": 23, "gender": "male"}
        ]
        
        for case in boundary_cases:
            print(f"\n测试边界日期: {case}")
            result = calculate_bazi(**case)
            assert "bazi" in result, f"未正确处理边界日期: {case}"
            print(f"边界日期处理结果: {result['bazi']}")
            
    def test_city_handling(self):
        """测试城市处理"""
        # 无效城市
        result = calculate_bazi(1990, 1, 1, 12, "male", "NonExistingCity")
        assert "bazi" in result, "未正确处理无效城市情况"
        print(f"\n无效城市处理: {result['location']}")
        
        # 不提供城市
        result = calculate_bazi(1990, 1, 1, 12, "male")
        assert "bazi" in result, "未正确处理无城市情况"
        print(f"无城市处理: {result['location']}")