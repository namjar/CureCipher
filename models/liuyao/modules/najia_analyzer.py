"""
纳甲分析模块 - 分析与解读天干地支关系
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from models.bazi.calculator import get_element

class NaJiaAnalyzer:
    """纳甲分析类，处理纳甲与天干地支关系"""
    
    def __init__(self):
        """初始化纳甲分析所需数据"""
        # 天干五行映射
        self.tiangan_wuxing = {
            "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
            "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"
        }
        
        # 地支五行映射
        self.dizhi_wuxing = {
            "子": "水", "丑": "土", "寅": "木", "卯": "木",
            "辰": "土", "巳": "火", "午": "火", "未": "土",
            "申": "金", "酉": "金", "戌": "土", "亥": "水"
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
        
        # 五行相生关系
        self.wuxing_sheng = {
            "木": "火", "火": "土", "土": "金", "金": "水", "水": "木"
        }
        
        # 五行相克关系
        self.wuxing_ke = {
            "木": "土", "土": "水", "水": "火", "火": "金", "金": "木"
        }
        
        # 五行健康关系
        self.wuxing_health = {
            "木": {
                "organ": "肝胆",
                "body_parts": "筋脉，四肢，神经",
                "issues": "肝胆问题、肢体不适、肌腱炎症",
                "strengths": "肝脏解毒能力、韧带弹性、身体灵活性",
                "recommendations": "保持情绪平和，按摩太冲穴，多食用绿色蔬菜",
                "enhancements": "进行伸展运动，食用护肝食材如枸杞、绿茶"
            },
            "火": {
                "organ": "心小肠",
                "body_parts": "血液，舌，面色",
                "issues": "心脏问题、高血压、焦虑抑郁",
                "strengths": "血液循环、精神活力、代谢功能",
                "recommendations": "避免过度兴奋，按摩内关穴，保持充足睡眠",
                "enhancements": "进行有氧运动，食用山楂、莲子等平心食材"
            },
            "土": {
                "organ": "脾胃",
                "body_parts": "肌肉，嘴唇，四肢",
                "issues": "脾胃不适、消化问题、肥胖",
                "strengths": "消化吸收能力、新陈代谢、体质稳定性",
                "recommendations": "规律饮食，按摩足三里，减少甜食和精制碳水摄入",
                "enhancements": "进行缓和的步行，食用健脾食材如山药、薏米"
            },
            "金": {
                "organ": "肺大肠",
                "body_parts": "皮肤，毛发，呼吸系统",
                "issues": "肺部问题、慢性疼痛、免疫系统问题",
                "strengths": "呼吸功能、皮肤修复、免疫系统",
                "recommendations": "保持呼吸顺畅，按摩合谷穴，适当增加辛辣食物",
                "enhancements": "进行呼吸练习，食用滋肺食材如梨、百合"
            },
            "水": {
                "organ": "肾膀胱",
                "body_parts": "骨骼，耳朵，泌尿系统",
                "issues": "肾功能不足、泌尿系统问题、水肿",
                "strengths": "肾脏功能、内分泌、生殖系统",
                "recommendations": "保暖腰部，按摩太溪穴，补充适量水分",
                "enhancements": "进行游泳或太极，食用补肾食材如黑豆、核桃"
            }
        }
    
    def analyze_najia(self, najia_info: List[str]) -> List[Dict]:
        """
        分析纳甲信息
        
        参数:
            najia_info (List[str]): 六爻纳甲信息
            
        返回:
            List[Dict]: 纳甲分析结果列表
        """
        results = []
        for i, gz in enumerate(najia_info):
            gan = gz[0]  # 天干
            zhi = gz[1:]  # 地支
            
            # 获取五行
            gan_element = self.tiangan_wuxing.get(gan, "")
            zhi_element = self.dizhi_wuxing.get(zhi, "")
            
            # 地支藏干
            cang_gans = self.dizhi_canggan.get(zhi, [])
            cang_elements = [self.tiangan_wuxing.get(cg, "") for cg in cang_gans]
            
            # 分析天干地支关系
            gan_zhi_relation = self._analyze_gan_zhi_relation(gan, zhi)
            
            # 爻位
            yao_position = i + 1
            yao_name = ["初爻", "二爻", "三爻", "四爻", "五爻", "六爻"][i]
            
            results.append({
                "yao_position": yao_position,
                "yao_name": yao_name,
                "gan": gan,
                "zhi": zhi,
                "gan_element": gan_element,
                "zhi_element": zhi_element,
                "cang_gans": cang_gans,
                "cang_elements": cang_elements,
                "gan_zhi_relation": gan_zhi_relation
            })
        
        return results
    
    def _analyze_gan_zhi_relation(self, gan: str, zhi: str) -> Dict:
        """
        分析天干地支之间的关系
        
        参数:
            gan (str): 天干
            zhi (str): 地支
            
        返回:
            Dict: 天干地支关系
        """
        gan_element = self.tiangan_wuxing.get(gan, "")
        zhi_element = self.dizhi_wuxing.get(zhi, "")
        
        # 默认关系
        relation = {
            "type": "无关",
            "description": "天干地支五行无明显关系"
        }
        
        # 检查天干是否通根（藏干中有天干本身）
        cang_gans = self.dizhi_canggan.get(zhi, [])
        if gan in cang_gans:
            relation["type"] = "通根"
            relation["description"] = f"天干{gan}通根于地支{zhi}藏干"
            return relation
        
        # 检查相生关系
        if self.wuxing_sheng.get(gan_element) == zhi_element:
            relation["type"] = "相生"
            relation["description"] = f"天干{gan}（{gan_element}）生地支{zhi}（{zhi_element}）"
        elif self.wuxing_sheng.get(zhi_element) == gan_element:
            relation["type"] = "被生"
            relation["description"] = f"地支{zhi}（{zhi_element}）生天干{gan}（{gan_element}）"
        
        # 检查相克关系
        elif self.wuxing_ke.get(gan_element) == zhi_element:
            relation["type"] = "相克"
            relation["description"] = f"天干{gan}（{gan_element}）克地支{zhi}（{zhi_element}）"
        elif self.wuxing_ke.get(zhi_element) == gan_element:
            relation["type"] = "被克"
            relation["description"] = f"地支{zhi}（{zhi_element}）克天干{gan}（{gan_element}）"
        
        # 检查地支是否有生天干的藏干
        for cang_gan in cang_gans:
            cang_element = self.tiangan_wuxing.get(cang_gan, "")
            if self.wuxing_sheng.get(cang_element) == gan_element:
                relation["type"] = "藏干生"
                relation["description"] = f"地支{zhi}藏干{cang_gan}（{cang_element}）生天干{gan}（{gan_element}）"
                break
            elif self.wuxing_ke.get(cang_element) == gan_element:
                relation["type"] = "藏干克"
                relation["description"] = f"地支{zhi}藏干{cang_gan}（{cang_element}）克天干{gan}（{gan_element}）"
                break
        
        return relation
    
    def analyze_health_impact(self, najia_analysis: List[Dict], day_master_element: Optional[str]=None) -> List[Dict]:
        """
        分析纳甲对健康的影响
        
        参数:
            najia_analysis (List[Dict]): 纳甲分析结果列表
            day_master_element (str, optional): 日主五行
            
        返回:
            List[Dict]: 健康影响分析列表
        """
        health_impacts = []
        
        for analysis in najia_analysis:
            health_impact = {
                "yao_position": analysis["yao_position"],
                "yao_name": analysis["yao_name"],
                "impact": [],
                "severity": "中",
                "recommendations": []
            }
            
            gan_element = analysis["gan_element"]
            zhi_element = analysis["zhi_element"]
            gan_zhi_relation = analysis["gan_zhi_relation"]
            
            # 分析天干五行对健康的影响
            if gan_element in self.wuxing_health:
                gan_health = self.wuxing_health[gan_element]
                health_impact["impact"].append(f"天干五行{gan_element}，对应{gan_health['organ']}，影响{gan_health['body_parts']}")
                
                # 如果有日主，分析与日主的关系
                if day_master_element:
                    if self._is_wuxing_sheng(gan_element, day_master_element):
                        health_impact["impact"].append(f"{gan_element}生{day_master_element}，有助于改善{self.wuxing_health.get(day_master_element, {}).get('strengths', '')}")
                        health_impact["severity"] = "轻"
                    elif self._is_wuxing_ke(gan_element, day_master_element):
                        health_impact["impact"].append(f"{gan_element}克{day_master_element}，可能加重{self.wuxing_health.get(day_master_element, {}).get('issues', '')}")
                        health_impact["severity"] = "重"
                    elif self._is_wuxing_sheng(day_master_element, gan_element):
                        health_impact["impact"].append(f"{day_master_element}生{gan_element}，体内{gan_element}气较足")
                    elif self._is_wuxing_ke(day_master_element, gan_element):
                        health_impact["impact"].append(f"{day_master_element}克{gan_element}，体内{gan_element}气较弱")
            
            # 分析地支藏干对健康的影响
            for cang_gan, cang_element in zip(analysis["cang_gans"], analysis["cang_elements"]):
                if cang_element in self.wuxing_health:
                    cang_health = self.wuxing_health[cang_element]
                    health_impact["impact"].append(f"地支藏干{cang_gan}（{cang_element}），影响{cang_health['organ']}")
                    
                    # 如果有日主，分析藏干与日主的关系
                    if day_master_element:
                        if self._is_wuxing_sheng(cang_element, day_master_element):
                            health_impact["impact"].append(f"藏干{cang_element}生{day_master_element}，有调和作用")
                        elif self._is_wuxing_ke(cang_element, day_master_element):
                            health_impact["impact"].append(f"藏干{cang_element}克{day_master_element}，有抑制作用")
            
            # 根据天干地支关系提供健康建议
            if gan_element in self.wuxing_health:
                health_impact["recommendations"].append(self.wuxing_health[gan_element]["recommendations"])
            
            if gan_zhi_relation["type"] in ["相克", "被克", "藏干克"]:
                health_impact["severity"] = "重"
                if gan_element in self.wuxing_health:
                    health_impact["recommendations"].append(self.wuxing_health[gan_element]["enhancements"])
            
            health_impacts.append(health_impact)
        
        return health_impacts
    
    def _is_wuxing_sheng(self, element1: str, element2: str) -> bool:
        """
        判断五行1是否生五行2
        
        参数:
            element1 (str): 五行1
            element2 (str): 五行2
            
        返回:
            bool: 是否相生
        """
        return self.wuxing_sheng.get(element1) == element2
    
    def _is_wuxing_ke(self, element1: str, element2: str) -> bool:
        """
        判断五行1是否克五行2
        
        参数:
            element1 (str): 五行1
            element2 (str): 五行2
            
        返回:
            bool: 是否相克
        """
        return self.wuxing_ke.get(element1) == element2

# 单例模式，导出一个实例
najia_analyzer = NaJiaAnalyzer()
