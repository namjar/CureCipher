
"""
测试八字计算器完整功能

在项目根目录运行：
$ python -m unittest tests.test_bazi_calculator_full
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
from models.bazi.bazi_calculator import calculate_bazi, generate_bazi_report

class TestBaziCalculator(unittest.TestCase):
    """测试八字计算器完整功能"""
    
    def test_calculate_bazi(self):
        """测试八字计算功能"""
        # 测试男命
        bazi_result_male = calculate_bazi(1990, 5, 15, 12, "male")
        
        self.assertIsNotNone(bazi_result_male)
        self.assertIsInstance(bazi_result_male, dict)
        
        # 检查基本信息
        self.assertIn('bazi', bazi_result_male)
        self.assertIn('ten_gods', bazi_result_male)
        self.assertIn('five_elements', bazi_result_male)
        self.assertIn('nayin', bazi_result_male)
        self.assertIn('special', bazi_result_male)
        self.assertIn('dayuns', bazi_result_male)
        self.assertIn('current_dayun', bazi_result_male)
        self.assertIn('shensha', bazi_result_male)
        
        # 检查命宫和胎元计算结果
        self.assertIn('ming_gong', bazi_result_male['special'])
        self.assertIn('tai_yuan', bazi_result_male['special'])
        
        # 检查神煞计算结果
        self.assertIsInstance(bazi_result_male['shensha'], list)
        
        # 测试女命
        bazi_result_female = calculate_bazi(1990, 5, 15, 12, "female")
        self.assertIsNotNone(bazi_result_female)
        
        # 检查大运是否不同（男女向不同）
        if len(bazi_result_male['dayuns']) > 0 and len(bazi_result_female['dayuns']) > 0:
            male_first_dayun = bazi_result_male['dayuns'][0]['ganzhi'] if bazi_result_male['dayuns'] else None
            female_first_dayun = bazi_result_female['dayuns'][0]['ganzhi'] if bazi_result_female['dayuns'] else None
            
            # 男女大运可能不同
            if male_first_dayun and female_first_dayun:
                print(f"男命首个大运：{male_first_dayun}")
                print(f"女命首个大运：{female_first_dayun}")
    
    def test_generate_bazi_report(self):
        """测试八字报告生成功能"""
        # 计算八字
        bazi_result = calculate_bazi(1990, 5, 15, 12, "male")
        
        # 生成报告
        report = generate_bazi_report(bazi_result)
        
        self.assertIsNotNone(report)
        self.assertIsInstance(report, dict)
        
        # 检查报告内容
        self.assertIn('basic_info', report)
        self.assertIn('five_elements', report)
        self.assertIn('pattern_analysis', report)
        self.assertIn('current_dayun', report)
        self.assertIn('current_info', report)
        self.assertIn('shensha_info', report)
        self.assertIn('nayin', report)
        self.assertIn('special', report)
        self.assertIn('text_report', report)
        
        # 检查文本报告是否生成
        self.assertIsInstance(report['text_report'], str)
        self.assertGreater(len(report['text_report']), 100)  # 确保报告有足够的内容
        
        # 打印报告的部分内容
        print("八字报告生成成功，部分内容：")
        print("-" * 50)
        print(report['text_report'][:500] + "...")  # 只打印前500个字符

if __name__ == '__main__':
    unittest.main()
