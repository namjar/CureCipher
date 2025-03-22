"""
运行所有八字模块相关测试
"""
import sys
import os
import importlib

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# 导入测试模块
from tests.bazi.test_bazi_calculator import (
    test_basic_functions,
    test_element_balance_analysis,
    test_special_pattern_analysis,
    test_bazi_calculation,
    test_bazi_report_generation
)

if __name__ == "__main__":
    try:
        print("\n===== 运行八字模块测试 =====")
        
        print("\n1. 测试基本函数...")
        test_basic_functions()
        print("✓ 通过")
        
        print("\n2. 测试五行平衡分析...")
        test_element_balance_analysis()
        print("✓ 通过")
        
        print("\n3. 测试特殊格局分析...")
        test_special_pattern_analysis()
        print("✓ 通过")
        
        print("\n4. 测试八字计算...")
        test_bazi_calculation()
        print("✓ 通过")
        
        print("\n5. 测试八字报告生成...")
        test_bazi_report_generation()
        print("✓ 通过")
        
        print("\n所有测试全部通过！")
        sys.exit(0)
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
