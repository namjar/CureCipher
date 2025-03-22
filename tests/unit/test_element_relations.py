# /Users/ericw/Documents/GitHub/CureCipher/tests/unit/test_element_relations.py
"""
五行关系单元测试
"""
import pytest
from models.bazi.bazi_calculator import (
    is_generating, is_generated, is_controlling, is_controlled,
    get_relationship_by_shishen
)

class TestElementRelations:
    def test_is_generating(self):
        """测试是否生关系"""
        # 木生火
        assert is_generating("木", "火") == True
        # 火生土
        assert is_generating("火", "土") == True
        # 土生金
        assert is_generating("土", "金") == True
        # 金生水
        assert is_generating("金", "水") == True
        # 水生木
        assert is_generating("水", "木") == True
        
        # 非生关系
        assert is_generating("木", "土") == False
        assert is_generating("火", "水") == False
    
    def test_is_generated(self):
        """测试是否被生关系"""
        # 火被木生
        assert is_generated("火", "木") == True
        # 土被火生
        assert is_generated("土", "火") == True
        # 金被土生
        assert is_generated("金", "土") == True
        # 水被金生
        assert is_generated("水", "金") == True
        # 木被水生
        assert is_generated("木", "水") == True
        
        # 非被生关系
        assert is_generated("土", "木") == False
        assert is_generated("水", "火") == False
    
    def test_is_controlling(self):
        """测试是否克关系"""
        # 木克土
        assert is_controlling("木", "土") == True
        # 土克水
        assert is_controlling("土", "水") == True
        # 水克火
        assert is_controlling("水", "火") == True
        # 火克金
        assert is_controlling("火", "金") == True
        # 金克木
        assert is_controlling("金", "木") == True
        
        # 非克关系
        assert is_controlling("木", "金") == False
        assert is_controlling("水", "土") == False
    
    def test_is_controlled(self):
        """测试是否被克关系"""
        # 土被木克
        assert is_controlled("土", "木") == True
        # 水被土克
        assert is_controlled("水", "土") == True
        # 火被水克
        assert is_controlled("火", "水") == True
        # 金被火克
        assert is_controlled("金", "火") == True
        # 木被金克
        assert is_controlled("木", "金") == True
        
        # 非被克关系
        assert is_controlled("金", "木") == False
        assert is_controlled("土", "水") == False
    
    def test_get_relationship_by_shishen(self):
        """测试通过十神获取关系描述"""
        assert "日主自己" in get_relationship_by_shishen("比肩")
        assert "相互争夺" in get_relationship_by_shishen("劫财")
        assert "泄气" in get_relationship_by_shishen("食神")
        assert "泄气" in get_relationship_by_shishen("伤官")
        assert "日主所克" in get_relationship_by_shishen("正财")
        assert "克制日主" in get_relationship_by_shishen("七杀")
        assert "生日主" in get_relationship_by_shishen("正印")
        
        # 测试未知十神
        assert "不确定" in get_relationship_by_shishen("未知十神")