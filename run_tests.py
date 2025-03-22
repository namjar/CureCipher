#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行脚本

在项目根目录下运行：
$ python run_tests.py
"""

import unittest
import sys
import os

# 确保我们在正确的目录下运行
def ensure_root_directory():
    # 获取当前脚本的绝对路径
    script_path = os.path.abspath(__file__)
    # 获取脚本所在的目录（项目根目录）
    root_dir = os.path.dirname(script_path)
    
    # 切换到项目根目录
    if os.getcwd() != root_dir:
        os.chdir(root_dir)
        print(f"已切换到项目根目录: {root_dir}")
    
    # 将项目根目录添加到Python路径
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
        print(f"已将项目根目录添加到Python路径: {root_dir}")

if __name__ == "__main__":
    # 确保在项目根目录运行
    ensure_root_directory()
    
    # 发现并运行所有测试
    print("正在发现测试用例...")
    test_suite = unittest.defaultTestLoader.discover('tests')
    
    # 运行测试
    print("开始运行测试...\n")
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    
    # 输出测试结果
    print("\n==============================")
    print(f"运行测试: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.errors) - len(result.failures)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print("==============================")
    
    # 设置退出码
    if result.wasSuccessful():
        print("所有测试通过！")
        sys.exit(0)
    else:
        print("测试失败或错误，请查看详细输出。")
        sys.exit(1)
