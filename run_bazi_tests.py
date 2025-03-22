#!/usr/bin/env python3
"""
运行八字模块所有测试的入口点
"""
import sys
import os
import subprocess

# 运行测试函数
def run_test(test_script):
    """运行指定的测试脚本"""
    test_path = os.path.join(os.path.dirname(__file__), "tests", "bazi", test_script)
    print(f"运行测试脚本: {test_path}")
    
    try:
        subprocess.run([sys.executable, test_path], check=False)
        print(f"✅ {test_script} 测试运行完成")
        return True
    except Exception as e:
        print(f"❌ {test_script} 测试运行失败: {e}")
        return False

def main():
    """运行所有测试"""
    print("\n===== 运行八字模块测试 =====\n")
    
    # 测试列表
    tests = [
        "time_test.py",           # 时轴计算测试
        "test_bazi_calculator.py",  # 基本功能测试
        "test_specific.py"          # 特定八字测试
    ]
    
    # 运行所有测试
    success = True
    for test in tests:
        if not run_test(test):
            success = False
        print("")  # 添加空行
    
    # 显示测试结果
    if success:
        print("\n🎉 所有测试运行完成!")
        return 0
    else:
        print("\n⚠️ 部分测试运行失败，请检查错误信息。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
