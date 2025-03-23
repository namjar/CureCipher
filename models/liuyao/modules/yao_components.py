"""
爻组件模块 - 处理六亲、六神、空亡等计算
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from models.bazi.calculator import get_element

class YaoComponents:
    """爻组件类，处理六亲、六神、空亡等计算"""
    
    def __init__(self):
        """初始化爻组件计算所需的基础数据"""
        # 干支序号映射
        self.ganzhi_order = {
            "甲子": 1, "乙丑": 2, "丙寅": 3, "丁卯": 4, "戊辰": 5,
            "己巳": 6, "庚午": 7, "辛未": 8, "壬申": 9, "癸酉": 10,
            "甲戌": 11, "乙亥": 12, "丙子": 13, "丁丑": 14, "戊寅": 15,
            "己卯": 16, "庚辰": 17, "辛巳": 18, "壬午": 19, "癸未": 20,
            "甲申": 21, "乙酉": 22, "丙戌": 23, "丁亥": 24, "戊子": 25,
            "己丑": 26, "庚寅": 27, "辛卯": 28, "壬辰": 29, "癸巳": 30,
            "甲午": 31, "乙未": 32, "丙申": 33, "丁酉": 34, "戊戌": 35,
            "己亥": 36, "庚子": 37, "辛丑": 38, "壬寅": 39, "癸卯": 40,
            "甲辰": 41, "乙巳": 42, "丙午": 43, "丁未": 44, "戊申": 45,
            "己酉": 46, "庚戌": 47, "辛亥": 48, "壬子": 49, "癸丑": 50,
            "甲寅": 51, "乙卯": 52, "丙辰": 53, "丁巳": 54, "戊午": 55,
            "己未": 56, "庚申": 57, "辛酉": 58, "壬戌": 59, "癸亥": 60
        }
        
        # 地支藏干映射
        self.dizhi_canggan = {
            "子": ["癸"],
            "丑": ["己", "癸", "辛"],
            "寅": ["甲", "丙", "戊"],
            "卯": ["乙"],
            "辰": ["戊", "乙", "癸"],
            "巳": ["丙", "庚", "戊"],
            "午": ["丁", "己"],
            "未": ["己", "丁", "乙"],
            "申": ["庚", "壬", "戊"],
            "酉": ["辛"],
            "戌": ["戊", "辛", "丁"],
            "亥": ["壬", "甲"]
        }
        
        # 地支五行映射
        self.dizhi_wuxing = {
            "子": "水", "丑": "土", "寅": "木", "卯": "木",
            "辰": "土", "巳": "火", "午": "火", "未": "土",
            "申": "金", "酉": "金", "戌": "土", "亥": "水"
        }
        
        # 六神健康属性
        self.liushen_health = {
            "青龙": {
                "health_impact": "有利于气血循环，增强身体活力",
                "issues": "情绪波动，血压不稳",
                "recommendations": "静心调息，多食用绿色蔬菜"
            },
            "朱雀": {
                "health_impact": "有利于心脏功能，提高新陈代谢",
                "issues": "口舌生疮，心火过旺，失眠",
                "recommendations": "保持心情平静，饮用菊花茶"
            },
            "勾陈": {
                "health_impact": "有利于稳定情绪，增强消化功能",
                "issues": "消化不良，胃部不适，体重增加",
                "recommendations": "减少油腻食物，按摩脾胃经络"
            },
            "腾蛇": {
                "health_impact": "有利于排毒，改善血液循环",
                "issues": "皮肤问题，过敏反应，神经紧张",
                "recommendations": "保持身心平和，多饮水"
            },
            "白虎": {
                "health_impact": "有利于呼吸系统，增强免疫力",
                "issues": "慢性疼痛，肺部问题，免疫系统失调",
                "recommendations": "按合谷穴，饮山楂茶"
            },
            "玄武": {
                "health_impact": "有利于肾脏功能，改善水液代谢",
                "issues": "泌尿系统问题，水肿，腰背疼痛",
                "recommendations": "保暖腰部，多吃黑色食物如黑豆、黑芝麻"
            }
        }
    
    def calculate_liuqin(self, najia_info: List[str], day_master: Optional[str], day_zhi: str) -> List[str]:
        """
        计算六亲关系，同时考虑地支藏干
        
        参数:
            najia_info (List[str]): 六爻纳甲信息
            day_master (str, optional): 日主天干
            day_zhi (str): 日干地支中的地支
            
        返回:
            List[str]: 六亲关系列表
        """
        if not day_master:
            # 如果没有提供日主，返回空的六亲列表
            return ["未知"] * 6
        
        # 获取日主五行
        day_master_element = get_element(day_master)
        
        # 计算六爻的六亲关系
        liuqin = []
        for gz in najia_info:
            gan = gz[0]  # 取天干
            zhi = gz[1:]  # 取地支
            
            # 天干五行
            gan_element = get_element(gan)
            
            # 地支五行
            zhi_element = self.dizhi_wuxing.get(zhi, "")
            
            # 地支藏干
            cang_gans = self.dizhi_canggan.get(zhi, [])
            cang_elements = [get_element(cg) for cg in cang_gans]
            
            # 根据六亲计算规则，优先考虑天干五行
            primary_element = gan_element
            
            # 如果天干地支五行不同，且日主与藏干有特殊关系，考虑藏干影响
            if gan_element != zhi_element and cang_elements:
                # 判断藏干中是否有与日主相生或相克的特殊关系
                for ce in cang_elements:
                    # 藏干生日主，或日主克藏干，这种情况藏干影响较大
                    sheng_relation = self._is_wuxing_sheng(ce, day_master_element)
                    ke_relation = self._is_wuxing_ke(day_master_element, ce)
                    
                    if sheng_relation or ke_relation:
                        primary_element = ce
                        break
            
            relation = self._get_liuqin_relation(day_master_element, primary_element)
            liuqin.append(relation)
        
        return liuqin
    
    def calculate_liushen(self, day_gan: str) -> List[str]:
        """
        计算六神，根据日干分配六神
        
        参数:
            day_gan (str): 日干
            
        返回:
            List[str]: 六神列表，从初爻到六爻
        """
        # 六神列表：青龙、朱雀、勾陈、腾蛇、白虎、玄武
        liushen = ["青龙", "朱雀", "勾陈", "腾蛇", "白虎", "玄武"]
        
        # 根据日干旋转六神
        rotation = {
            "甲": 0, "乙": 0,  # 甲乙日，青龙在初爻
            "丙": 1, "丁": 1,  # 丙丁日，朱雀在初爻
            "戊": 2, "己": 2,  # 戊己日，勾陈在初爻
            "庚": 3, "辛": 3,  # 庚辛日，腾蛇在初爻
            "壬": 4, "癸": 4   # 壬癸日，白虎在初爻
        }
        
        # 根据日干旋转六神列表
        rot = rotation.get(day_gan, 0)
        return liushen[rot:] + liushen[:rot]
    
    def calculate_kongwang(self, day_gz: str, najia_processor) -> List[str]:
        """
        计算空亡爻，根据日干支确定空亡地支，然后找出对应的爻
        
        参数:
            day_gz (str): 日干支
            najia_processor: 纳甲处理器对象
            
        返回:
            List[str]: 空亡爻列表，例如["初爻", "二爻"]
        """
        # 根据日干支确定空亡地支
        kongwang_dizhi = self._get_kongwang_dizhi(day_gz)
        
        # 空亡爻列表
        kongwang_yaos = []
        
        # 爻序与名称对照
        yao_names = ["初爻", "二爻", "三爻", "四爻", "五爻", "六爻"]
        
        # 遍历六爻，检查每爻的地支是否空亡
        for i in range(6):
            najia = najia_processor.get_najia_by_yao_number(i + 1)  # 获取该爻的纳甲
            zhi = najia[1:]  # 取地支
            
            if zhi in kongwang_dizhi:
                kongwang_yaos.append(yao_names[i])
        
        return kongwang_yaos
    
    def _get_kongwang_dizhi(self, day_gz: str) -> List[str]:
        """
        根据日干支确定空亡地支
        
        参数:
            day_gz (str): 日干支
            
        返回:
            List[str]: 空亡地支列表，例如["戌", "亥"]
        """
        # 日干支空亡对照表
        kongwang_map = {
            "甲子": ["戌", "亥"], "甲戌": ["申", "酉"], "甲申": ["午", "未"],
            "甲午": ["辰", "巳"], "甲辰": ["寅", "卯"], "甲寅": ["子", "丑"],
            "乙丑": ["戌", "亥"], "乙亥": ["申", "酉"], "乙酉": ["午", "未"],
            "乙未": ["辰", "巳"], "乙巳": ["寅", "卯"], "乙卯": ["子", "丑"],
            "丙寅": ["戌", "亥"], "丙子": ["申", "酉"], "丙戌": ["午", "未"],
            "丙申": ["辰", "巳"], "丙午": ["寅", "卯"], "丙辰": ["子", "丑"],
            "丁卯": ["戌", "亥"], "丁丑": ["申", "酉"], "丁亥": ["午", "未"],
            "丁酉": ["辰", "巳"], "丁未": ["寅", "卯"], "丁巳": ["子", "丑"],
            "戊辰": ["戌", "亥"], "戊寅": ["申", "酉"], "戊子": ["午", "未"],
            "戊戌": ["辰", "巳"], "戊申": ["寅", "卯"], "戊午": ["子", "丑"],
            "己巳": ["戌", "亥"], "己卯": ["申", "酉"], "己丑": ["午", "未"],
            "己亥": ["辰", "巳"], "己酉": ["寅", "卯"], "己未": ["子", "丑"],
            "庚午": ["戌", "亥"], "庚辰": ["申", "酉"], "庚寅": ["午", "未"],
            "庚子": ["辰", "巳"], "庚戌": ["寅", "卯"], "庚申": ["子", "丑"],
            "辛未": ["戌", "亥"], "辛巳": ["申", "酉"], "辛卯": ["午", "未"],
            "辛丑": ["辰", "巳"], "辛亥": ["寅", "卯"], "辛酉": ["子", "丑"],
            "壬申": ["戌", "亥"], "壬午": ["申", "酉"], "壬辰": ["午", "未"],
            "壬寅": ["辰", "巳"], "壬子": ["寅", "卯"], "壬戌": ["子", "丑"],
            "癸酉": ["戌", "亥"], "癸未": ["申", "酉"], "癸巳": ["午", "未"],
            "癸卯": ["辰", "巳"], "癸丑": ["寅", "卯"], "癸亥": ["子", "丑"]
        }
        
        # 返回空亡地支
        return kongwang_map.get(day_gz, ["戌", "亥"])  # 默认返回戌亥空
    
    def _get_liuqin_relation(self, day_master_element: str, other_element: str) -> str:
        """
        获取两个五行之间的六亲关系
        
        参数:
            day_master_element (str): 日主五行
            other_element (str): 其他五行
            
        返回:
            str: 六亲关系
        """
        # 六亲关系表
        liuqin_map = {
            # 日主是木
            "木": {
                "木": "兄弟", "火": "子孙", "土": "财星",
                "金": "官鬼", "水": "父母"
            },
            # 日主是火
            "火": {
                "木": "父母", "火": "兄弟", "土": "子孙",
                "金": "财星", "水": "官鬼"
            },
            # 日主是土
            "土": {
                "木": "官鬼", "火": "父母", "土": "兄弟",
                "金": "子孙", "水": "财星"
            },
            # 日主是金
            "金": {
                "木": "财星", "火": "官鬼", "土": "父母",
                "金": "兄弟", "水": "子孙"
            },
            # 日主是水
            "水": {
                "木": "子孙", "火": "财星", "土": "官鬼",
                "金": "父母", "水": "兄弟"
            }
        }
        
        # 返回六亲关系
        return liuqin_map.get(day_master_element, {}).get(other_element, "未知")
    
    def _is_wuxing_sheng(self, element1: str, element2: str) -> bool:
        """
        判断五行1是否生五行2
        
        参数:
            element1 (str): 五行1
            element2 (str): 五行2
            
        返回:
            bool: 是否相生
        """
        # 五行相生关系：木生火，火生土，土生金，金生水，水生木
        sheng_relations = {
            "木": "火", "火": "土", "土": "金", "金": "水", "水": "木"
        }
        
        return sheng_relations.get(element1) == element2
    
    def _is_wuxing_ke(self, element1: str, element2: str) -> bool:
        """
        判断五行1是否克五行2
        
        参数:
            element1 (str): 五行1
            element2 (str): 五行2
            
        返回:
            bool: 是否相克
        """
        # 五行相克关系：木克土，土克水，水克火，火克金，金克木
        ke_relations = {
            "木": "土", "土": "水", "水": "火", "火": "金", "金": "木"
        }
        
        return ke_relations.get(element1) == element2
        
    def analyze_wuxing_relation(self, element1: str, element2: str) -> Dict:
        """
        分析两个五行之间的关系
        
        参数:
            element1 (str): 第一个五行
            element2 (str): 第二个五行
            
        返回:
            Dict: 关系分析结果
        """
        # 五行相生关系：木生火，火生土，土生金，金生水，水生木
        sheng_relations = {
            "木": "火", "火": "土", "土": "金", "金": "水", "水": "木"
        }
        
        # 五行相克关系：木克土，土克水，水克火，火克金，金克木
        ke_relations = {
            "木": "土", "土": "水", "水": "火", "火": "金", "金": "木"
        }
        
        # 默认结果
        result = {
            "relationship": "无关",
            "direction": "无",
            "strength": "中",
            "health_impact": "对健康影响中性"
        }
        
        # 分析相生关系
        if sheng_relations.get(element1) == element2:
            result["relationship"] = "相生"
            result["direction"] = "生"
            result["health_impact"] = f"{element1}生{element2}，对相关健康问题有帮助"
        elif sheng_relations.get(element2) == element1:
            result["relationship"] = "相生"
            result["direction"] = "被生"
            result["health_impact"] = f"{element2}生{element1}，身体恢复能力较强"
        
        # 分析相克关系
        elif ke_relations.get(element1) == element2:
            result["relationship"] = "相克"
            result["direction"] = "克"
            result["health_impact"] = f"{element1}克{element2}，可能加重相关健康问题"
        elif ke_relations.get(element2) == element1:
            result["relationship"] = "相克"
            result["direction"] = "被克"
            result["health_impact"] = f"{element2}克{element1}，身体抵抗力较弱"
        
        return result

# 单例模式，导出一个实例
yao_components = YaoComponents()
