# /Users/ericw/Documents/GitHub/CureCipher/tests/performance/test_performance.py
"""
性能测试
"""
import time
import pytest
from models.bazi.bazi_calculator import calculate_bazi, generate_bazi_report

class TestPerformance:
    def test_calculation_performance(self):
        """测试计算性能"""
        iterations = 50  # 迭代次数
        start_time = time.time()
        
        for i in range(iterations):
            year = 1900 + (i % 100)
            month = 1 + (i % 12)
            day = 1 + (i % 28)
            hour = (i % 24)
            gender = "male" if i % 2 == 0 else "female"
            
            _ = calculate_bazi(year, month, day, hour, gender)
        
        end_time = time.time()
        elapsed = end_time - start_time
        avg_time = elapsed / iterations
        
        print(f"\n性能测试结果:")
        print(f"总耗时: {elapsed:.2f}秒")
        print(f"平均每次: {avg_time*1000:.2f}毫秒")
        
        # 验证性能是否在可接受范围内
        assert avg_time < 1.0, f"计算性能不足，平均耗时 {avg_time*1000:.2f} 毫秒"
        
    def test_report_generation_performance(self):
        """测试报告生成性能"""
        iterations = 20  # 迭代次数
        
        # 预先计算八字结果
        results = []
        for i in range(iterations):
            year = 1900 + (i % 100)
            month = 1 + (i % 12)
            day = 1 + (i % 28)
            hour = (i % 24)
            gender = "male" if i % 2 == 0 else "female"
            
            result = calculate_bazi(year, month, day, hour, gender)
            results.append(result)
        
        # 测试报告生成性能
        start_time = time.time()
        for result in results:
            _ = generate_bazi_report(result)
        
        end_time = time.time()
        elapsed = end_time - start_time
        avg_time = elapsed / iterations
        
        print(f"\n报告生成性能测试结果:")
        print(f"总耗时: {elapsed:.2f}秒")
        print(f"平均每次: {avg_time*1000:.2f}毫秒")
        
        # 验证性能是否在可接受范围内
        assert avg_time < 0.5, f"报告生成性能不足，平均耗时 {avg_time*1000:.2f} 毫秒"