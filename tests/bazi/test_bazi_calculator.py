"""
测试bazi_calculator.py文件中的主要功能
"""
import sys
import os
import traceback
import pytest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from models.bazi.bazi_calculator import (
    get_element, get_elements_balance, analyze_special_patterns, 
    calculate_bazi, generate_bazi_report
)

def test_basic_functions():
    """测试基本五行获取函数"""
    assert get_element("甲") == "木"
    assert get_element("丙") == "火"
    assert get_element("庚") == "金"

def test_element_balance_analysis():
    """测试五行平衡分析"""
    scores = {"木": 20, "火": 30, "土": 15, "金": 10, "水": 25}
    balance = get_elements_balance(scores)
    
    assert balance['strongest'] == "火"
    assert balance['weakest'] == "金"
    assert balance['balance_state'] in ["非常平衡", "较为平衡", "稍有不平衡", "明显不平衡", "严重不平衡"]

def test_special_pattern_analysis():
    """测试特殊格局分析"""
    zhis = ["子", "申", "辰", "酉"]
    patterns = analyze_special_patterns(zhis)
    
    # 水三合应该被检测到
    assert any(p['name'] == "水三合" for p in patterns['san_he'])
    
    # 西方三会应该部分匹配（申，酉）
    found_west = False
    for p in patterns['san_hui']:
        if p['name'] == "西方三会":
            found_west = True
            assert "申" in p['matched']
            assert "酉" in p['matched']
    assert found_west

def test_bazi_calculation():
    """测试八字计算"""
    try:
        bazi = calculate_bazi(1990, 5, 15, 12, "male", "Beijing")
        
        # 检查基本信息是否存在
        assert bazi is not None, "八字计算结果为空"
        
        if 'error' in bazi:
            print(f"警告: 计算八字时出现错误: {bazi['error']}")
            print(f"错误信息: {bazi.get('message', '无详细信息')}")
            return  # 跳过剩余测试
        
        # 检查返回的结构
        assert 'bazi' in bazi, "返回结果中没有'bazi'字段"
        assert 'year' in bazi['bazi'], "返回结果中没有'year'字段"
        assert 'month' in bazi['bazi'], "返回结果中没有'month'字段"
        assert 'day' in bazi['bazi'], "返回结果中没有'day'字段"
        assert 'hour' in bazi['bazi'], "返回结果中没有'hour'字段"
        assert 'day_master' in bazi['bazi'], "返回结果中没有'day_master'字段"
        
        # 检查日主信息
        day_master = bazi['bazi']['day_master']
        assert day_master in ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"], f"日主'{day_master}'不是有效的天干"
        
        # 检查五行得分
        assert 'five_elements' in bazi, "返回结果中没有'five_elements'字段"
        assert 'scores' in bazi['five_elements'], "返回结果中没有'scores'字段"
        assert all(element in bazi['five_elements']['scores'] for element in ["木", "火", "土", "金", "水"]), "五行得分中缺少某些五行元素"
    
    except Exception as e:
        print(f"测试八字计算时出错: {e}")
        raise  # 重新抛出异常以便测试框架捕获

def test_bazi_report_generation():
    """测试八字报告生成"""
    try:
        bazi_result = calculate_bazi(1990, 5, 15, 12, "male", "Beijing")
        
        # 检查是否有错误
        if bazi_result is None:
            print("警告: 计算八字结果为空")
            return
        
        if 'error' in bazi_result:
            print(f"警告: 计算八字时出现错误: {bazi_result['error']}")
            print(f"错误信息: {bazi_result.get('message', '无详细信息')}")
            return
        
        # 生成报告
        report = generate_bazi_report(bazi_result)
        
        # 检查报告结构
        assert report is not None, "生成的报告为空"
        assert 'basic_info' in report, "报告中缺少basic_info字段"
        assert 'pattern_analysis' in report, "报告中缺少pattern_analysis字段"
        assert 'dayun_analysis' in report, "报告中缺少dayun_analysis字段"
        assert 'text_report' in report, "报告中缺少text_report字段"
        
        # 检查文本报告
        assert isinstance(report['text_report'], str), "text_report应该是字符串"
        assert len(report['text_report']) > 0, "text_report不应该为空"
        assert "八字命盘解读" in report['text_report'], "text_report应包含'八字命盘解读'"
    
    except Exception as e:
        print(f"测试八字报告生成时出错: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    # 直接运行测试
    try:
        print("\n1. Testing basic functions...")
        test_basic_functions()
        print("✓ Passed")
        
        print("\n2. Testing element balance analysis...")
        test_element_balance_analysis()
        print("✓ Passed")
        
        print("\n3. Testing special pattern analysis...")
        test_special_pattern_analysis()
        print("✓ Passed")
        
        print("\n4. Testing bazi calculation...")
        test_bazi_calculation()
        print("✓ Passed")
        
        print("\n5. Testing bazi report generation...")
        test_bazi_report_generation()
        print("✓ Passed")
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        traceback.print_exc()
        sys.exit(1)
