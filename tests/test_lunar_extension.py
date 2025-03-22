
"""
测试lunar_extension扩展功能

在项目根目录运行：
$ python -m unittest tests.test_lunar_extension
"""

import unittest
from datetime import datetime
import os
import sys

# 确保可以正确导入项目模块
def ensure_path():
    # 获取当前脚本的绝对路径
    script_path = os.path.abspath(__file__)
    # 获取脚本所在的目录
    script_dir = os.path.dirname(script_path)
    # 获取项目根目录
    root_dir = os.path.dirname(script_dir)
    
    # 将项目根目录添加到系统路径
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

# 先确保路径正确
ensure_path()

# 然后导入项目模块
from lunar_python import Solar, Lunar
from models.bazi.lunar_extension import LunarExtension

class TestLunarExtension(unittest.TestCase):
    """测试LunarExtension类"""
    
    def setUp(self):
        # 创建测试数据
        self.solar = Solar.fromYmdHms(1990, 5, 15, 12, 0, 0)
        self.lunar = self.solar.getLunar()
        self.lunar_ext = LunarExtension(solar=self.solar)
        
    def test_get_day_un(self):
        """测试大运计算"""
        # 测试男命大运
        day_uns_male = self.lunar_ext.get_day_un(gender_code=1)
        
        self.assertIsNotNone(day_uns_male)
        self.assertIsInstance(day_uns_male, list)
        self.assertGreater(len(day_uns_male), 0)
        
        # 确保每个大运条目包含必要的字段
        for day_un in day_uns_male:
            self.assertIn('gan_zhi', day_un)
            self.assertIn('start_age', day_un)
            self.assertIn('end_age', day_un)
            self.assertIn('is_current', day_un)
            
        # 测试女命大运
        day_uns_female = self.lunar_ext.get_day_un(gender_code=0)
        self.assertIsNotNone(day_uns_female)
        self.assertIsInstance(day_uns_female, list)
        self.assertGreater(len(day_uns_female), 0)
    
    def test_get_ming_gong(self):
        """测试命宫计算"""
        ming_gong = self.lunar_ext.get_ming_gong()
        
        self.assertIsNotNone(ming_gong)
        self.assertIsInstance(ming_gong, str)
        self.assertTrue(ming_gong in "子丑寅卯辰巳午未申酉戌亥")
    
    def test_get_tai_yuan(self):
        """测试胎元计算"""
        tai_yuan = self.lunar_ext.get_tai_yuan()
        
        self.assertIsNotNone(tai_yuan)
        self.assertIsInstance(tai_yuan, str)
        self.assertEqual(len(tai_yuan), 2)  # 干支两个字符
        self.assertTrue(tai_yuan[0] in "甲乙丙丁戊己庚辛壬癸")
        self.assertTrue(tai_yuan[1] in "子丑寅卯辰巳午未申酉戌亥")
    
    def test_get_shen_sha(self):
        """测试神煞计算"""
        shen_sha = self.lunar_ext.get_shen_sha()
        
        self.assertIsNotNone(shen_sha)
        self.assertIsInstance(shen_sha, list)
        
        # 确保神煞列表中的每个条目包含必要的字段
        for item in shen_sha:
            self.assertIn('name', item)
            self.assertIn('position', item)
            self.assertIn('description', item)

if __name__ == '__main__':
    unittest.main()
