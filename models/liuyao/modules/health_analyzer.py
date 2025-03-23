"""
健康分析模块 - 结合六爻信息分析健康问题
"""

import json
import os
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from models.bazi.calculator import get_element

from .yao_components import yao_components

class HealthAnalyzer:
    """健康分析类，分析六爻卦象对健康的影响"""
    
    def __init__(self, shensha_data_path=None):
        """
        初始化健康分析器
        
        参数:
            shensha_data_path (str, optional): 神煞数据文件路径
        """
        # 如果未提供路径，使用默认路径
        if shensha_data_path is None:
            root_dir = Path(__file__).parent.parent.parent.parent
            self.shensha_data_path = os.path.join(root_dir, "data", "shensha_impacts.json")
        else:
            self.shensha_data_path = shensha_data_path
            
        # 加载神煞数据
        self.shensha_data = self._load_shensha_data()
        
        # 流年信息（2025年为乙巳年）
        self.flow_year = {"year": 2025, "gz": "乙巳", "element": "木火"}
        
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
    
    def _load_shensha_data(self) -> Dict:
        """
        加载神煞数据
        
        返回:
            Dict: 包含神煞影响的字典
        """
        try:
            with open(self.shensha_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载神煞数据失败: {e}")
            return {"positive": {}, "negative": {}}
    
    def analyze_health(self, gua_result: Dict, day_master: Optional[str], 
                       yong_shen: Optional[str]) -> Dict:
        """
        分析健康问题，结合变卦、用神强弱、日建、月建
        
        参数:
            gua_result (Dict): 卦象结果
            day_master (str, optional): 日主天干
            yong_shen (str, optional): 用神五行
            
        返回:
            Dict: 健康分析结果
        """
        # 获取卦象和神煞信息
        ben_gua = gua_result["ben_gua"]
        bian_gua = gua_result["bian_gua"]
        najia = gua_result["najia"]
        liuqin = gua_result["liuqin"]
        liushen = gua_result["liushen"]
        kongwang = gua_result["kongwang"]
        dong_yao = gua_result["dong_yao"]
        shi_yao = gua_result["shi_yao"]
        day_gz = gua_result["date_info"]["day_gz"]
        month_gz = gua_result["date_info"]["month_gz"]
        
        # 获取本卦、变卦五行
        ben_gua_element = ben_gua["element"]
        bian_gua_element = bian_gua["element"]
        
        # 获取日主五行（如果有）
        day_master_element = get_element(day_master) if day_master else None
        
        # 健康分析结果
        health_result = {
            "overall": "",
            "specific_issues": [],
            "recommendations": []
        }
        
        # 获取动爻的五行、六亲、六神
        dong_yao_idx = dong_yao - 1
        dong_yao_najia = najia[dong_yao_idx]
        dong_yao_gan = dong_yao_najia[0]  # 天干
        dong_yao_zhi = dong_yao_najia[1:]  # 地支
        dong_yao_element = get_element(dong_yao_gan)
        dong_yao_zhi_element = self.dizhi_wuxing.get(dong_yao_zhi, "")
        dong_yao_liuqin = liuqin[dong_yao_idx]
        dong_yao_liushen = liushen[dong_yao_idx]
        
        # 获取世爻的信息
        shi_yao_idx = shi_yao - 1
        shi_yao_najia = najia[shi_yao_idx]
        shi_yao_gan = shi_yao_najia[0]
        shi_yao_zhi = shi_yao_najia[1:]
        shi_yao_element = get_element(shi_yao_gan)
        shi_yao_zhi_element = self.dizhi_wuxing.get(shi_yao_zhi, "")
        
        # 分析五行相克关系对健康的影响
        if day_master_element:
            # 本卦五行与日主
            ben_relation = yao_components.analyze_wuxing_relation(day_master_element, ben_gua_element)
            health_result["overall"] = ben_relation["health_impact"]
            
            # 变卦五行与日主
            bian_relation = yao_components.analyze_wuxing_relation(day_master_element, bian_gua_element)
            if bian_relation["relationship"] == "相克" and bian_relation["direction"] == "被克":
                health_result["specific_issues"].append(
                    f"变卦{bian_gua['name']}五行{bian_gua_element}克{day_master_element}，可能加重{self._get_health_issue(day_master_element)}"
                )
                health_result["recommendations"].append(
                    f"建议{self._get_health_recommendation(day_master_element)}"
                )
            elif bian_relation["relationship"] == "相生" and bian_relation["direction"] == "被生":
                health_result["specific_issues"].append(
                    f"变卦{bian_gua['name']}五行{bian_gua_element}生{day_master_element}，有助于改善{self._get_health_strength(day_master_element)}"
                )
                health_result["recommendations"].append(
                    f"可进一步{self._get_health_enhancement(day_master_element)}"
                )
        
        # 分析用神强弱（用神对应的六亲）
        if yong_shen and day_master_element:
            yong_shen_liuqin = yao_components._get_liuqin_relation(day_master_element, yong_shen)
            yong_shen_yao = None
            for i, lq in enumerate(liuqin):
                if lq == yong_shen_liuqin:
                    yong_shen_yao = i + 1
                    break
        
            if yong_shen_yao:
                yong_yao_idx = yong_shen_yao - 1
                yong_yao_najia = najia[yong_yao_idx]
                yong_yao_gan = yong_yao_najia[0]
                yong_yao_zhi = yong_yao_najia[1:]
                yong_yao_element = get_element(yong_yao_gan)
                yong_yao_zhi_element = self.dizhi_wuxing.get(yong_yao_zhi, "")
                yong_yao_liushen = liushen[yong_yao_idx]
                
                # 用神与动爻的关系
                dong_relation = yao_components.analyze_wuxing_relation(yong_yao_element, dong_yao_element)
                if dong_relation["relationship"] == "相克" and dong_relation["direction"] == "被克":
                    health_result["specific_issues"].append(
                        f"用神{yong_shen_liuqin}（五行{yong_shen}）在第{yong_shen_yao}爻，受到动爻五行{dong_yao_element}克制，可能加重{self._get_health_issue(yong_shen)}"
                    )
                    health_result["recommendations"].append(
                        f"建议{self._get_health_recommendation(yong_shen)}"
                    )
                elif dong_relation["relationship"] == "相生" and dong_relation["direction"] == "被生":
                    health_result["specific_issues"].append(
                        f"用神{yong_shen_liuqin}（五行{yong_shen}）在第{yong_shen_yao}爻，受到动爻五行{dong_yao_element}生助，有助于改善{self._get_health_strength(yong_shen)}"
                    )
                    health_result["recommendations"].append(
                        f"可进一步{self._get_health_enhancement(yong_shen)}"
                    )
                
                # 用神与世爻的关系（世爻代表求测者自身）
                shi_relation = yao_components.analyze_wuxing_relation(yong_yao_element, shi_yao_element)
                if shi_relation["relationship"] == "相克" and shi_relation["direction"] == "被克":
                    health_result["specific_issues"].append(
                        f"用神{yong_shen_liuqin}（五行{yong_shen}）在第{yong_shen_yao}爻，受到世爻五行{shi_yao_element}克制，健康问题可能更明显"
                    )
                elif shi_relation["relationship"] == "相生" and shi_relation["direction"] == "被生":
                    health_result["specific_issues"].append(
                        f"用神{yong_shen_liuqin}（五行{yong_shen}）在第{yong_shen_yao}爻，受到世爻五行{shi_yao_element}生助，健康状况可能改善"
                    )
                
                # 用神所在爻是否空亡
                yong_yao_name = ["初爻", "二爻", "三爻", "四爻", "五爻", "六爻"][yong_yao_idx]
                if yong_yao_name in kongwang:
                    health_result["specific_issues"].append(
                        f"用神{yong_shen_liuqin}所在{yong_yao_name}空亡，其对健康的影响减弱"
                    )
                
                # 用神所在爻的六神影响
                yong_yao_liushen_data = self.liushen_health.get(yong_yao_liushen, {})
                if yong_yao_liushen_data:
                    health_result["specific_issues"].append(
                        f"用神{yong_shen_liuqin}所在爻的六神为{yong_yao_liushen}，{yong_yao_liushen_data['issues']}"
                    )
                    health_result["recommendations"].append(
                        f"建议{yong_yao_liushen_data['recommendations']}"
                    )
        
        # 分析世爻和动爻的健康含义
        if shi_yao == dong_yao:
            health_result["specific_issues"].append("世爻动，对健康问题更敏感")
        
        # 分析六亲关系对健康的影响
        if dong_yao_liuqin in ["官鬼", "子孙"]:
            health_result["specific_issues"].append(
                f"动爻为{dong_yao_liuqin}，可能与{self._get_liuqin_health_issue(dong_yao_liuqin)}有关"
            )
            health_result["recommendations"].append(
                f"建议{self._get_liuqin_health_recommendation(dong_yao_liuqin)}"
            )
        
        # 分析六神对健康的影响
        liushen_data = self.liushen_health.get(dong_yao_liushen, {})
        if liushen_data:
            health_result["specific_issues"].append(
                f"动爻六神为{dong_yao_liushen}，{liushen_data['issues']}"
            )
            health_result["recommendations"].append(
                f"建议{liushen_data['recommendations']}"
            )
        
        # 分析空亡影响
        dong_yao_name = f"第{dong_yao}爻"
        if dong_yao_name in kongwang:
            health_result["specific_issues"].append(
                f"动爻{dong_yao_name}空亡，健康影响减弱"
            )
        
        # 分析日建、月建五行影响
        day_gan, day_zhi = day_gz[0], day_gz[1:]
        month_gan, month_zhi = month_gz[0], month_gz[1:]
        day_gan_element = get_element(day_gan)
        day_zhi_element = self.dizhi_wuxing.get(day_zhi, "")
        month_gan_element = get_element(month_gan)
        month_zhi_element = self.dizhi_wuxing.get(month_zhi, "")
        
        if day_master_element:
            # 日建五行
            day_zhi_relation = yao_components.analyze_wuxing_relation(day_master_element, day_zhi_element)
            if day_zhi_relation["relationship"] == "相克" and day_zhi_relation["direction"] == "被克":
                health_result["specific_issues"].append(
                    f"日建地支{day_zhi}（五行{day_zhi_element}）克{day_master_element}，可能加重{self._get_health_issue(day_master_element)}"
                )
            
            # 月建五行
            month_zhi_relation = yao_components.analyze_wuxing_relation(day_master_element, month_zhi_element)
            if month_zhi_relation["relationship"] == "相克" and month_zhi_relation["direction"] == "被克":
                health_result["specific_issues"].append(
                    f"月建地支{month_zhi}（五行{month_zhi_element}）克{day_master_element}，可能加重{self._get_health_issue(day_master_element)}"
                )
        
        # 分析神煞信息
        shensha = self.select_shensha(gua_result, day_master_element)
        if shensha:
            health_result["specific_issues"].append(
                f"有{shensha['name']}神煞影响，{shensha['impact']}"
            )
            if "remedy" in shensha:
                health_result["recommendations"].append(f"建议{shensha['remedy']}")
        
        # 最终健康总结
        health_result["overall"] = (
            f"{ben_gua['name']}卦{ben_gua_element}，"
            f"动爻在第{dong_yao}爻（{dong_yao_liuqin}），"
            f"{health_result['overall']}"
        )
        
        return health_result
    
    def select_shensha(self, gua_result: Dict, day_master_element: Optional[str]) -> Dict:
        """
        选择神煞，结合流年、日建、月建、世爻位置
        
        参数:
            gua_result (Dict): 卦象结果
            day_master_element (str, optional): 日主五行
            
        返回:
            Dict: 神煞信息
        """
        ben_gua_element = gua_result["ben_gua"]["element"]
        shi_yao = gua_result["shi_yao"]
        shi_yao_idx = shi_yao - 1
        shi_yao_najia = gua_result["najia"][shi_yao_idx]
        shi_yao_zhi = shi_yao_najia[1:]
        day_gz = gua_result["date_info"]["day_gz"]
        month_gz = gua_result["date_info"]["month_gz"]
        
        # 流年五行
        flow_year_elements = self.flow_year["element"].split()
        
        # 导入神煞数据
        positive_shensha = self.shensha_data.get("positive", {})
        negative_shensha = self.shensha_data.get("negative", {})
        
        # 合并所有神煞
        all_shensha = {}
        all_shensha.update(positive_shensha)
        all_shensha.update(negative_shensha)
        
        # 优先选择与世爻地支、流年、日建、月建相关的神煞
        related_shensha = []
        for name, info in all_shensha.items():
            # 检查神煞五行是否与卦象五行、世爻地支五行匹配
            shensha_element = info.get("element", "")
            element_affinity = info.get("element_affinity", [])
            flow_year_boost = info.get("flow_year_boost", [])
            
            # 优先级1：世爻地支五行匹配
            shi_zhi_element = self.dizhi_wuxing.get(shi_yao_zhi, "")
            if shensha_element == shi_zhi_element or shi_zhi_element in element_affinity:
                related_shensha.append({"name": name, **info, "priority": 3})
                continue
            
            # 优先级2：流年增强
            if any(elem in flow_year_boost for elem in flow_year_elements):
                related_shensha.append({"name": name, **info, "priority": 2})
                continue
            
            # 优先级3：日建、月建五行匹配
            day_zhi = day_gz[1:]
            month_zhi = month_gz[1:]
            day_zhi_element = self.dizhi_wuxing.get(day_zhi, "")
            month_zhi_element = self.dizhi_wuxing.get(month_zhi, "")
            if shensha_element in [day_zhi_element, month_zhi_element] or \
               day_zhi_element in element_affinity or month_zhi_element in element_affinity:
                related_shensha.append({"name": name, **info, "priority": 1})
                continue
            
            # 优先级4：卦象五行匹配
            if shensha_element == ben_gua_element or ben_gua_element in element_affinity:
                related_shensha.append({"name": name, **info, "priority": 0})
        
        # 按优先级排序
        related_shensha.sort(key=lambda x: x["priority"], reverse=True)
        
        # 如果有相关神煞，选择优先级最高的
        if related_shensha:
            selected = related_shensha[0]
            selected.pop("priority", None)
            
            # 如果有日主，获取相应强度的健康影响
            if day_master_element and "health_aspects" in selected:
                day_master_strength = "day_master_neutral"
                if "day_master_strong" in selected["health_aspects"]:
                    day_master_strength = "day_master_strong"
                elif "day_master_weak" in selected["health_aspects"]:
                    day_master_strength = "day_master_weak"
                
                # 获取健康影响
                health_impact = selected["health_aspects"].get(day_master_strength, [])
                if health_impact:
                    # 检查流年增强
                    if any(elem in selected.get("flow_year_boost", []) for elem in flow_year_elements):
                        health_impact = [f"{impact}（流年增强）" for impact in health_impact]
                    selected["impact"] = f"影响：{', '.join(health_impact)}"
            
            return selected
        
        return {}
    
    def _get_health_issue(self, element: str) -> str:
        """
        根据五行属性获取可能的健康问题
        
        参数:
            element (str): 五行属性
            
        返回:
            str: 健康问题描述
        """
        health_issues = {
            "木": "肝胆问题、肢体不适、肌腱炎症",
            "火": "心脏问题、高血压、焦虑抑郁",
            "土": "脾胃不适、消化问题、肥胖",
            "金": "肺部问题、慢性疼痛、免疫系统问题",
            "水": "肾功能不足、泌尿系统问题、水肿"
        }
        return health_issues.get(element, "未知健康问题")
    
    def _get_health_strength(self, element: str) -> str:
        """
        根据五行属性获取健康优势
        
        参数:
            element (str): 五行属性
            
        返回:
            str: 健康优势描述
        """
        health_strengths = {
            "木": "肝脏解毒能力、韧带弹性、身体灵活性",
            "火": "血液循环、精神活力、代谢功能",
            "土": "消化吸收能力、新陈代谢、体质稳定性",
            "金": "呼吸功能、皮肤修复、免疫系统",
            "水": "肾脏功能、内分泌、生殖系统"
        }
        return health_strengths.get(element, "整体健康状况")
    
    def _get_health_recommendation(self, element: str) -> str:
        """
        根据五行属性获取健康建议
        
        参数:
            element (str): 五行属性
            
        返回:
            str: 健康建议
        """
        recommendations = {
            "木": "保持情绪平和，按摩太冲穴，多食用绿色蔬菜",
            "火": "避免过度兴奋，按摩内关穴，保持充足睡眠",
            "土": "规律饮食，按摩足三里，减少甜食和精制碳水摄入",
            "金": "保持呼吸顺畅，按摩合谷穴，适当增加辛辣食物",
            "水": "保暖腰部，按摩太溪穴，补充适量水分"
        }
        return recommendations.get(element, "调整作息，均衡饮食，适度锻炼")
    
    def _get_health_enhancement(self, element: str) -> str:
        """
        根据五行属性获取健康增强方法
        
        参数:
            element (str): 五行属性
            
        返回:
            str: 健康增强方法
        """
        enhancements = {
            "木": "进行伸展运动，食用护肝食材如枸杞、绿茶",
            "火": "进行有氧运动，食用山楂、莲子等平心食材",
            "土": "进行缓和的步行，食用健脾食材如山药、薏米",
            "金": "进行呼吸练习，食用滋肺食材如梨、百合",
            "水": "进行游泳或太极，食用补肾食材如黑豆、核桃"
        }
        return enhancements.get(element, "进行适合体质的运动和饮食调理")
    
    def _get_liuqin_health_issue(self, liuqin: str) -> str:
        """
        根据六亲关系获取健康问题
        
        参数:
            liuqin (str): 六亲关系
            
        返回:
            str: 健康问题描述
        """
        issues = {
            "父母": "内分泌系统、精力不足",
            "兄弟": "免疫系统、抵抗力",
            "官鬼": "压力、自律系统",
            "财星": "营养吸收、代谢功能",
            "子孙": "生殖系统、精神状态"
        }
        return issues.get(liuqin, "整体健康")
    
    def _get_liuqin_health_recommendation(self, liuqin: str) -> str:
        """
        根据六亲关系获取健康建议
        
        参数:
            liuqin (str): 六亲关系
            
        返回:
            str: 健康建议
        """
        recommendations = {
            "父母": "调整作息，提高睡眠质量",
            "兄弟": "增强锻炼，提高身体素质",
            "官鬼": "减轻压力，进行放松练习",
            "财星": "改善饮食，增加营养均衡性",
            "子孙": "保持心情愉悦，避免过度焦虑"
        }
        return recommendations.get(liuqin, "综合调理身心健康")

# 单例模式，导出一个实例
health_analyzer = HealthAnalyzer()
