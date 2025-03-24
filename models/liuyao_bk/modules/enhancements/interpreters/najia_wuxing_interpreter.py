"""
纳甲五行解释模块
"""

from typing import Dict, List, Optional
from .base_interpreter import BaseInterpreter

import sys
from pathlib import Path
# 添加项目根目录到路径
root_dir = Path(__file__).parent.parent.parent.parent.parent
sys.path.append(str(root_dir))
from models.bazi.calculator import get_element


class NajiaWuxingInterpreter(BaseInterpreter):
    """纳甲五行解释器，分析纳甲五行与日主的关系"""
    
    def __init__(self):
        """初始化纳甲五行解释器"""
        # 五行属性
        self.wuxing_attributes = {
            "木": {
                "特性": "生长、伸展、柔韧、直上",
                "体征": "肝、胆、筋脉、眼睛",
                "方位": "东方",
                "季节": "春季",
                "颜色": "青绿色"
            },
            "火": {
                "特性": "温热、上炎、光明、变化",
                "体征": "心、小肠、脉、舌",
                "方位": "南方",
                "季节": "夏季",
                "颜色": "红色"
            },
            "土": {
                "特性": "稳重、包容、中正、厚实",
                "体征": "脾、胃、肌肉、口",
                "方位": "中央",
                "季节": "四季末",
                "颜色": "黄色"
            },
            "金": {
                "特性": "沉降、收敛、肃杀、坚固",
                "体征": "肺、大肠、皮毛、鼻",
                "方位": "西方",
                "季节": "秋季",
                "颜色": "白色"
            },
            "水": {
                "特性": "寒冷、向下、滋润、屈曲",
                "体征": "肾、膀胱、骨髓、耳",
                "方位": "北方",
                "季节": "冬季",
                "颜色": "黑色"
            }
        }
        
        # 五行相生关系
        self.wuxing_sheng = {
            "木": "火",  # 木生火
            "火": "土",  # 火生土
            "土": "金",  # 土生金
            "金": "水",  # 金生水
            "水": "木"   # 水生木
        }
        
        # 五行相克关系
        self.wuxing_ke = {
            "木": "土",  # 木克土
            "土": "水",  # 土克水
            "水": "火",  # 水克火
            "火": "金",  # 火克金
            "金": "木"   # 金克木
        }
    
    def _get_wuxing_relation(self, element1: str, element2: str) -> Dict:
        """
        获取两个五行之间的关系
        
        参数:
            element1 (str): 第一个五行
            element2 (str): 第二个五行
            
        返回:
            Dict: 关系描述
        """
        if element1 == element2:
            return {
                "关系": "比和",
                "描述": "同类相比，力量增强",
                "方向": "同类",
                "强度": "中"
            }
        elif self.wuxing_sheng.get(element1) == element2:
            return {
                "关系": "生",
                "描述": f"{element1}生{element2}，有助力作用",
                "方向": "生",
                "强度": "强"
            }
        elif self.wuxing_sheng.get(element2) == element1:
            return {
                "关系": "被生",
                "描述": f"{element2}生{element1}，有支持作用",
                "方向": "被生",
                "强度": "中"
            }
        elif self.wuxing_ke.get(element1) == element2:
            return {
                "关系": "克",
                "描述": f"{element1}克{element2}，有制约作用",
                "方向": "克",
                "强度": "强"
            }
        elif self.wuxing_ke.get(element2) == element1:
            return {
                "关系": "被克",
                "描述": f"{element2}克{element1}，有抑制作用",
                "方向": "被克",
                "强度": "弱"
            }
        else:
            return {
                "关系": "无关",
                "描述": "五行无直接关系",
                "方向": "无",
                "强度": "弱"
            }
    
    def interpret(self, gua_result: Dict, day_master: Optional[str] = None, 
                 query_type: Optional[str] = None) -> str:
        """
        解释纳甲五行与日主的关系
        
        参数:
            gua_result (Dict): 卦象计算结果
            day_master (str, optional): 日主天干
            query_type (str, optional): 测算类型
            
        返回:
            str: 解释结果
        """
        # 检查是否提供了日主天干
        if not day_master:
            return "未提供日主天干，无法分析纳甲五行关系。纳甲五行分析需要以日主天干为参照系，建议提供日主天干以获取更准确的分析。"
        
        # 提取卦象信息
        najia = gua_result["najia"]
        dong_yao = gua_result["dong_yao"]
        shi_yao = gua_result["shi_yao"]
        
        # 获取日主五行
        day_master_element = get_element(day_master)
        
        # 组合解释
        explanation = f"纳甲五行分析（日主五行：{day_master_element}）：\n\n"
        
        # 分析各爻纳甲天干的五行与日主的关系
        explanation += "各爻纳甲与日主五行关系：\n"
        
        for i, gz in enumerate(najia):
            if i < len(najia):
                yao_num = i + 1
                yao_name = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"][i]
                gan, zhi = gz[0], gz[1:]
                
                gan_element = get_element(gan)
                zhi_element = get_element(zhi, is_dizhi=True)
                
                # 分析天干与日主的关系
                gan_relation = self._get_wuxing_relation(day_master_element, gan_element)
                
                # 分析地支与日主的关系
                zhi_relation = self._get_wuxing_relation(day_master_element, zhi_element)
                
                is_dong = yao_num == dong_yao
                is_shi = yao_num == shi_yao
                
                special_mark = ""
                if is_dong and is_shi:
                    special_mark = "（世爻、动爻）"
                elif is_dong:
                    special_mark = "（动爻）"
                elif is_shi:
                    special_mark = "（世爻）"
                
                explanation += f"第{yao_num}爻{special_mark}：纳甲「{gz}」\n"
                explanation += f"  天干「{gan}」五行属{gan_element}，与日主{day_master_element}为{gan_relation['关系']}关系，{gan_relation['描述']}。\n"
                explanation += f"  地支「{zhi}」五行属{zhi_element}，与日主{day_master_element}为{zhi_relation['关系']}关系，{zhi_relation['描述']}。\n"
        
        # 重点分析动爻和世爻的纳甲五行
        explanation += "\n关键爻位的纳甲五行深度分析：\n"
        
        # 分析动爻纳甲
        dong_yao_idx = dong_yao - 1
        if dong_yao_idx < len(najia):
            dong_gz = najia[dong_yao_idx]
            dong_gan, dong_zhi = dong_gz[0], dong_gz[1:]
            dong_gan_element = get_element(dong_gan)
            dong_zhi_element = get_element(dong_zhi, is_dizhi=True)
            
            explanation += f"动爻（第{dong_yao}爻）纳甲「{dong_gz}」分析：\n"
            explanation += f"  天干「{dong_gan}」五行属{dong_gan_element}，{self.wuxing_attributes[dong_gan_element]['特性']}。\n"
            explanation += f"  地支「{dong_zhi}」五行属{dong_zhi_element}，{self.wuxing_attributes[dong_zhi_element]['特性']}。\n"
            
            # 与日主的关系分析
            dong_gan_relation = self._get_wuxing_relation(day_master_element, dong_gan_element)
            explanation += f"  动爻天干与日主关系：{dong_gan_relation['描述']}\n"
            
            # 动爻天干五行特点详解
            explanation += f"  动爻天干五行「{dong_gan_element}」的特点：\n"
            explanation += f"    - 体征：{self.wuxing_attributes[dong_gan_element]['体征']}\n"
            explanation += f"    - 方位：{self.wuxing_attributes[dong_gan_element]['方位']}\n"
            explanation += f"    - 季节：{self.wuxing_attributes[dong_gan_element]['季节']}\n"
            
            # 动爻五行与测算类型的关联分析
            if query_type:
                explanation += f"\n  在{query_type}方面，动爻五行「{dong_gan_element}」的影响：\n"
                
                if query_type == "事业":
                    if dong_gan_element == "木":
                        explanation += "    木性主成长，事业上有扩展机会，适合创新和开拓。\n"
                    elif dong_gan_element == "火":
                        explanation += "    火性主旺盛，事业上有上升空间，适合展示和推广。\n"
                    elif dong_gan_element == "土":
                        explanation += "    土性主稳固，事业上有稳健发展，适合管理和协调。\n"
                    elif dong_gan_element == "金":
                        explanation += "    金性主坚强，事业上有收获机会，适合总结和规划。\n"
                    elif dong_gan_element == "水":
                        explanation += "    水性主柔韧，事业上有灵活调整，适合沟通和交流。\n"
                    
                elif query_type == "财运":
                    if dong_gan_element == "木":
                        explanation += "    木性主延展，财运上有增长趋势，但需要耐心等待。\n"
                    elif dong_gan_element == "火":
                        explanation += "    火性主明亮，财运上有显著变化，但需防波动过大。\n"
                    elif dong_gan_element == "土":
                        explanation += "    土性主厚重，财运上有积累效应，适合稳健投资。\n"
                    elif dong_gan_element == "金":
                        explanation += "    金性主收敛，财运上有聚财能力，适合储蓄和保值。\n"
                    elif dong_gan_element == "水":
                        explanation += "    水性主流动，财运上有灵活性，适合短期投资和周转。\n"
                    
                elif query_type == "婚姻":
                    if dong_gan_element == "木":
                        explanation += "    木性主生长，婚姻上有发展空间，需注意培养关系。\n"
                    elif dong_gan_element == "火":
                        explanation += "    火性主热情，婚姻上有激情活力，需注意情绪波动。\n"
                    elif dong_gan_element == "土":
                        explanation += "    土性主包容，婚姻上有稳固基础，适合长期经营。\n"
                    elif dong_gan_element == "金":
                        explanation += "    金性主坚固，婚姻上有责任感，需注意避免固执。\n"
                    elif dong_gan_element == "水":
                        explanation += "    水性主柔和，婚姻上有包容性，需注意定位清晰。\n"
                    
                elif query_type == "健康":
                    explanation += f"    与{self.wuxing_attributes[dong_gan_element]['体征']}相关的健康方面需要关注。\n"
        
        # 分析世爻纳甲
        shi_yao_idx = shi_yao - 1
        if shi_yao_idx < len(najia) and shi_yao != dong_yao:  # 避免重复分析
            shi_gz = najia[shi_yao_idx]
            shi_gan, shi_zhi = shi_gz[0], shi_gz[1:]
            shi_gan_element = get_element(shi_gan)
            shi_zhi_element = get_element(shi_zhi, is_dizhi=True)
            
            explanation += f"\n世爻（第{shi_yao}爻）纳甲「{shi_gz}」分析：\n"
            explanation += f"  天干「{shi_gan}」五行属{shi_gan_element}，{self.wuxing_attributes[shi_gan_element]['特性']}。\n"
            explanation += f"  地支「{shi_zhi}」五行属{shi_zhi_element}，{self.wuxing_attributes[shi_zhi_element]['特性']}。\n"
            
            # 与日主的关系分析
            shi_gan_relation = self._get_wuxing_relation(day_master_element, shi_gan_element)
            explanation += f"  世爻天干与日主关系：{shi_gan_relation['描述']}\n"
        
        # 整体五行力量分析
        explanation += "\n整体纳甲五行分布分析：\n"
        
        # 统计各五行在纳甲中的分布
        wuxing_counts = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        
        for gz in najia:
            if len(gz) >= 2:
                gan, zhi = gz[0], gz[1:]
                gan_element = get_element(gan)
                zhi_element = get_element(zhi, is_dizhi=True)
                
                wuxing_counts[gan_element] += 1
                wuxing_counts[zhi_element] += 1
        
        # 输出五行分布
        explanation += "  纳甲天干地支五行分布：\n"
        for element, count in wuxing_counts.items():
            explanation += f"    {element}：{count}个，"
            
            if count >= 4:
                explanation += "力量较强。"
            elif count >= 2:
                explanation += "力量适中。"
            else:
                explanation += "力量较弱。"
                
            explanation += "\n"
        
        # 与日主五行的整体关系
        strong_elements = [element for element, count in wuxing_counts.items() if count >= 3]
        weak_elements = [element for element, count in wuxing_counts.items() if count <= 1]
        
        explanation += "  与日主五行的整体关系：\n"
        
        # 分析对日主有利的五行
        favorable_elements = []
        
        # 相生日主的五行
        sheng_element = None
        for element, target in self.wuxing_sheng.items():
            if target == day_master_element:
                sheng_element = element
                break
        
        if sheng_element:
            favorable_elements.append(sheng_element)
            explanation += f"    {sheng_element}生{day_master_element}，对日主有助力。\n"
        
        # 被日主所克的五行
        ke_element = self.wuxing_ke.get(day_master_element)
        if ke_element:
            favorable_elements.append(ke_element)
            explanation += f"    {day_master_element}克{ke_element}，日主有制约力。\n"
        
        # 分析对日主不利的五行
        unfavorable_elements = []
        
        # 克制日主的五行
        be_ke_element = None
        for element, target in self.wuxing_ke.items():
            if target == day_master_element:
                be_ke_element = element
                break
        
        if be_ke_element:
            unfavorable_elements.append(be_ke_element)
            explanation += f"    {be_ke_element}克{day_master_element}，对日主有抑制。\n"
        
        # 被日主所生的五行（耗日主）
        be_sheng_element = self.wuxing_sheng.get(day_master_element)
        if be_sheng_element:
            unfavorable_elements.append(be_sheng_element)
            explanation += f"    {day_master_element}生{be_sheng_element}，消耗日主能量。\n"
        
        # 根据五行力量对比给出整体评价
        favorable_strength = sum(wuxing_counts.get(element, 0) for element in favorable_elements)
        unfavorable_strength = sum(wuxing_counts.get(element, 0) for element in unfavorable_elements)
        
        explanation += "\n  五行力量对比分析：\n"
        explanation += f"    有利五行总数：{favorable_strength}\n"
        explanation += f"    不利五行总数：{unfavorable_strength}\n"
        
        if favorable_strength > unfavorable_strength:
            explanation += "    整体五行配置对日主有利，吉祥之象。\n"
        elif favorable_strength < unfavorable_strength:
            explanation += "    整体五行配置对日主不利，需加强应对。\n"
        else:
            explanation += "    整体五行配置平衡，吉凶参半。\n"
        
        # 根据测算类型提供建议
        if query_type:
            explanation += f"\n根据{query_type}需求的五行调节建议：\n"
            
            if query_type == "事业":
                for element in weak_elements:
                    explanation += f"  {element}力量较弱，可通过以下方式增强：\n"
                    if element == "木":
                        explanation += "    - 增加绿色元素，放置植物\n"
                        explanation += "    - 面向东方办公或开展活动\n"
                    elif element == "火":
                        explanation += "    - 增加红色元素，使用温暖色调\n"
                        explanation += "    - 增强照明，面向南方办公\n"
                    elif element == "土":
                        explanation += "    - 增加黄色、棕色元素\n"
                        explanation += "    - 稳定工作环境，建立规律作息\n"
                    elif element == "金":
                        explanation += "    - 增加白色、金色元素\n"
                        explanation += "    - 提升组织性，面向西方办公\n"
                    elif element == "水":
                        explanation += "    - 增加黑色、蓝色元素\n"
                        explanation += "    - 提升沟通频率，面向北方办公\n"
                        
            elif query_type == "财运":
                if "金" in weak_elements:
                    explanation += "  金力量较弱，财运基础需增强：\n"
                    explanation += "    - 佩戴金属饰品，使用金色、白色元素\n"
                    explanation += "    - 加强储蓄意识，提高资产的使用效率\n"
                if "水" in weak_elements:
                    explanation += "  水力量较弱，财运流动性需提升：\n"
                    explanation += "    - 增加流水元素，使用波浪形状装饰\n"
                    explanation += "    - 提高资金灵活性，增强市场敏感度\n"
                    
            elif query_type == "婚姻":
                if "火" in weak_elements:
                    explanation += "  火力量较弱，感情热度需提升：\n"
                    explanation += "    - 增加红色元素，提升活跃度\n"
                    explanation += "    - 增加交流互动，保持激情活力\n"
                if "土" in weak_elements:
                    explanation += "  土力量较弱，关系稳定性需增强：\n"
                    explanation += "    - 增加黄色、棕色元素\n"
                    explanation += "    - 建立共同目标，增强责任感\n"
                    
            elif query_type == "健康":
                for element, organs in [
                    ("木", "肝胆系统"),
                    ("火", "心脏系统"),
                    ("土", "脾胃系统"),
                    ("金", "肺部系统"),
                    ("水", "肾脏系统")
                ]:
                    if element in unfavorable_elements and wuxing_counts[element] >= 3:
                        explanation += f"  {element}力量过强，可能对{organs}造成压力，建议：\n"
                        explanation += f"    - 减少{self.wuxing_attributes[element]['颜色']}元素\n"
                        explanation += f"    - 避免过度疲劳{self.wuxing_attributes[element]['体征']}\n"
                    elif element in weak_elements:
                        explanation += f"  {element}力量不足，可能导致{organs}功能减弱，建议：\n"
                        explanation += f"    - 适当增加{self.wuxing_attributes[element]['颜色']}元素\n"
                        explanation += f"    - 注意调养{self.wuxing_attributes[element]['体征']}\n"
        
        return explanation
