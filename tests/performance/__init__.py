"""
性能测试模块初始化
确保可以正确导入项目模块
"""

import os
import sys

# 获取项目根目录路径
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# 将项目根目录添加到Python路径，确保可以导入项目模块
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
