# /Users/ericw/Documents/GitHub/CureCipher/tests/run_tests.py
"""
运行所有测试
"""
import sys
import os
import pytest
import subprocess

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print(" "*20 + "八字排盘测试工具")
    print("="*60 + "\n")
    
    print("1. 运行单元测试")
    unit_result = subprocess.run(["pytest", "unit/", "-v"], cwd=os.path.dirname(__file__))
    
    print("\n2. 运行集成测试")
    integration_result = subprocess.run(["pytest", "integration/", "-v"], cwd=os.path.dirname(__file__))
    
    print("\n3. 运行验证测试")
    validation_result = subprocess.run(["pytest", "validation/", "-v"], cwd=os.path.dirname(__file__))
    
    print("\n4. 运行性能测试")
    performance_result = subprocess.run(["pytest", "performance/", "-v"], cwd=os.path.dirname(__file__))
    
    print("\n5. 运行边界情况测试")
    edge_result = subprocess.run(["pytest", "edge_cases/", "-v"], cwd=os.path.dirname(__file__))
    
    print("\n" + "="*60)
    print(" "*20 + "测试结果摘要")
    print("="*60 + "\n")
    
    results = {
        "单元测试": unit_result.returncode == 0,
        "集成测试": integration_result.returncode == 0,
        "验证测试": validation_result.returncode == 0,
        "性能测试": performance_result.returncode == 0,
        "边界情况测试": edge_result.returncode == 0,
    }
    
    for test_name, passed in results.items():
        result_str = "通过" if passed else "失败"
        print(f"{test_name}: {result_str}")
    
    all_passed = all(results.values())
    print("\n总体结果:", "全部通过" if all_passed else "部分失败")
    
    return all_passed

def run_interactive_test():
    """运行交互式测试"""
    print("\n运行交互式测试...")
    subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "cli/interactive_test.py")])

if __name__ == "__main__":
    # 处理命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive_test()
    else:
        success = run_all_tests()
        
        print("\n要运行交互式测试工具，请使用: python run_tests.py --interactive")
        
        # 返回适当的退出代码
        sys.exit(0 if success else 1)