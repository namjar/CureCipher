"""
基本卦义解释模块
"""

from typing import Dict, List, Optional
from .base_interpreter import BaseInterpreter
from ...enhancements.sixtyfour_gua_info import sixtyfour_gua_info


class BasicGuaInterpreter(BaseInterpreter):
    """基本卦义解释器，解释本卦和变卦的基本含义"""
    
    def interpret(self, gua_result: Dict, day_master: Optional[str] = None, 
                 query_type: Optional[str] = None) -> str:
        """
        解释本卦和变卦的基本含义
        
        参数:
            gua_result (Dict): 卦象计算结果
            day_master (str, optional): 日主天干
            query_type (str, optional): 测算类型
            
        返回:
            str: 解释结果
        """
        ben_gua = gua_result["ben_gua"]
        bian_gua = gua_result["bian_gua"]
        
        ben_gua_name = ben_gua["name"]
        ben_gua_meaning = ben_gua.get("meaning", "")
        bian_gua_name = bian_gua["name"]
        bian_gua_meaning = bian_gua.get("meaning", "")
        
        # 获取卦辞
        ben_gua_interpretation = ben_gua.get("interpretation", {})
        ben_gua_text = ben_gua_interpretation.get("卦辞", "")
        ben_gua_explain = ben_gua_interpretation.get("卦辞解释", "")
        
        # 获取所属八宫
        ben_gua_bagong = ben_gua.get("bagong", "")
        bian_gua_bagong = bian_gua.get("bagong", "")
        
        # 组合解释
        explanation = f"本卦为「{ben_gua_name}」，{ben_gua_meaning}。"
        
        if ben_gua_text:
            explanation += f"卦辞为「{ben_gua_text}」，{ben_gua_explain}"
            
        explanation += f"\n变卦为「{bian_gua_name}」，{bian_gua_meaning}。"
        
        # 卦与卦之间的关系分析
        explanation += "\n\n本变关系："
        
        if ben_gua_name == bian_gua_name:
            explanation += "本卦与变卦相同，表示事情稳定不变。"
        elif ben_gua_bagong == bian_gua_bagong:
            explanation += f"本卦与变卦同属{ben_gua_bagong}，变化较为温和。"
        else:
            explanation += f"本卦属{ben_gua_bagong}，变卦属{bian_gua_bagong}，变化较大。"
        
        # 根据测算类型提供更具针对性的解释
        if query_type:
            explanation += f"\n\n{query_type}方面分析："
            
            if query_type == "事业":
                if "天" in ben_gua_name or "山" in ben_gua_name:
                    explanation += "本卦与事业发展关系密切，"
                    if "天" in ben_gua_name:
                        explanation += "具有开拓性和领导力。"
                    elif "山" in ben_gua_name:
                        explanation += "需要稳健和坚持。"
                        
            elif query_type == "财运":
                if "水" in ben_gua_name or "泽" in ben_gua_name:
                    explanation += "本卦与财运关系密切，"
                    if "水" in ben_gua_name:
                        explanation += "财运变化多端，需要灵活应对。"
                    elif "泽" in ben_gua_name:
                        explanation += "财运趋于聚集，有积累效应。"
                        
            elif query_type == "婚姻":
                if "离" in ben_gua_name or "坎" in ben_gua_name:
                    explanation += "本卦对婚姻有特殊意义，"
                    if "离" in ben_gua_name:
                        explanation += "婚姻关系明朗但可能有波动。"
                    elif "坎" in ben_gua_name:
                        explanation += "婚姻可能遇到困难或考验。"
                        
            elif query_type == "健康":
                if "乾" in ben_gua_name or "坤" in ben_gua_name:
                    explanation += "本卦对健康状况有指示，"
                    if "乾" in ben_gua_name:
                        explanation += "整体健康状况较好，但需注意过度消耗。"
                    elif "坤" in ben_gua_name:
                        explanation += "身体需调养生息，避免过度劳累。"
        
        return explanation
