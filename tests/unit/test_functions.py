# /Users/ericw/Documents/GitHub/CureCipher/tests/unit/test_functions.py
"""
基本函数单元测试
"""
import pytest
from models.bazi.bazi_calculator import (
    get_element, get_empty, check_gan_he, determine_zhi_element,
    get_generating_element, get_generated_element, get_controlling_element, 
    get_controlled_element, get_elements_balance
)

class TestBasicFunctions:
    def test_get_element(self):
        """测试获取天干五行属性"""
        assert get_element("甲") == "木"
        assert get_element("乙") == "木"
        assert get_element("丙") == "火"
        assert get_element("丁") == "火"
        assert get_element("戊") == "土"
        assert get_element("己") == "土"
        assert get_element("庚") == "金"
        assert get_element("辛") == "金"
        assert get_element("壬") == "水"
        assert get_element("癸") == "水"
        
    def test_determine_zhi_element(self):
        """测试获取地支五行属性"""
        assert determine_zhi_element("子") == "水"
        assert determine_zhi_element("丑") == "土"
        assert determine_zhi_element("寅") == "木"
        assert determine_zhi_element("卯") == "木"
        assert determine_zhi_element("辰") == "土"
        assert determine_zhi_element("巳") == "火"
        assert determine_zhi_element("午") == "火"
        assert determine_zhi_element("未") == "土"
        assert determine_zhi_element("申") == "金"
        assert determine_zhi_element("酉") == "金"
        assert determine_zhi_element("戌") == "土"
        assert determine_zhi_element("亥") == "水"
        
    def test_get_empty(self):
        """测试空亡计算"""
        # 甲子日空戌亥
        assert get_empty("甲子", "戌") == True
        assert get_empty("甲子", "亥") == True
        assert get_empty("甲子", "子") == False
        
        # 甲戌日空申酉
        assert get_empty("甲戌", "申") == True
        assert get_empty("甲戌", "酉") == True
        assert get_empty("甲戌", "子") == False
        
    def test_check_gan_he(self):
        """测试天干合化关系"""
        # 测试甲己合
        result = check_gan_he(["甲", "己", "丙", "丁"])
        assert len(result) == 1
        assert result[0]["gan1"] == "甲"
        assert result[0]["gan2"] == "己"
        assert result[0]["element"] == "土"
        
        # 测试多个合化
        result = check_gan_he(["甲", "己", "丙", "辛"])
        assert len(result) == 2  # 甲己合土, 丙辛合水
        
    def test_five_element_relations(self):
        """测试五行生克关系"""
        # 测试生我者
        assert get_generating_element("木") == "水"
        assert get_generating_element("火") == "木"
        assert get_generating_element("土") == "火"
        assert get_generating_element("金") == "土"
        assert get_generating_element("水") == "金"
        
        # 测试我生者
        assert get_generated_element("木") == "火"
        assert get_generated_element("火") == "土"
        assert get_generated_element("土") == "金"
        assert get_generated_element("金") == "水"
        assert get_generated_element("水") == "木"
        
        # 测试克我者
        assert get_controlling_element("木") == "金"
        assert get_controlling_element("火") == "水"
        assert get_controlling_element("土") == "木"
        assert get_controlling_element("金") == "火"
        assert get_controlling_element("水") == "土"
        
        # 测试我克者
        assert get_controlled_element("木") == "土"
        assert get_controlled_element("火") == "金"
        assert get_controlled_element("土") == "水"
        assert get_controlled_element("金") == "木"
        assert get_controlled_element("水") == "火"
        
    def test_get_elements_balance(self):
        """测试五行平衡分析"""
        # 五行均衡情况
        scores = {"木": 20, "火": 20, "土": 20, "金": 20, "水": 20}
        result = get_elements_balance(scores)
        assert result["balance_state"] == "非常平衡"
        assert result["std_deviation"] < 5
        
        # 五行极度不平衡情况
        scores = {"木": 100, "火": 10, "土": 10, "金": 10, "水": 10}
        result = get_elements_balance(scores)
        assert result["balance_state"] == "严重不平衡"
        assert result["strongest"] == "木"
        assert result["weakest"] in ["火", "土", "金", "水"]  # 所有其他元素都很弱