# /Users/ericw/Documents/GitHub/CureCipher/tests/conftest.py
"""
测试配置文件，包含共用的pytest fixture
"""
import os
import sys
import json
import pytest
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def load_test_data():
    """从JSON文件加载测试数据"""
    try:
        data_file = os.path.join(os.path.dirname(__file__), 'data', 'test_cases.json')
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"无法加载测试数据: {e}")
        return {
            "verified_cases": [],
            "special_patterns": []
        }

# 加载测试数据
test_data = load_test_data()

@pytest.fixture
def sample_birth_cases():
    """返回一组测试用的出生日期案例"""
    return [
        {"year": 1990, "month": 5, "day": 15, "hour": 12, "gender": "male", "city": "Beijing"},
        {"year": 1985, "month": 1, "day": 1, "hour": 0, "gender": "female", "city": "Shanghai"},
        {"year": 2000, "month": 10, "day": 10, "hour": 10, "gender": "male", "city": "Guangzhou"},
        {"year": 1975, "month": 6, "day": 6, "hour": 6, "gender": "female", "city": "Chongqing"}
    ]
    
@pytest.fixture
def verified_cases():
    """返回一组已验证的八字案例，包含预期结果"""
    return test_data.get("verified_cases", [])

@pytest.fixture
def special_pattern_cases():
    """返回测试特殊格局的地支组合案例"""
    return test_data.get("special_patterns", [])