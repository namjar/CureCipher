"""
世应爻解释模块
"""

from typing import Dict, List, Optional
from .base_interpreter import BaseInterpreter


class ShiyingInterpreter(BaseInterpreter):
    """世应爻解释器，解释世应爻的关系及其影响"""
    
    def __init__(self):
        """初始化世应爻解释器"""
        # 世应爻位置特性
        self.shi_positions = {
            1: "世爻在初爻，内卦下爻，事情刚开始，自身主导但基础较弱。",
            2: "世爻在二爻，内卦中爻，自身条件较好，能够掌握主动。",
            3: "世爻在三爻，内卦上爻，自身状态趋于变化，处于内外转折点。",
            4: "世爻在四爻，外卦下爻，外部环境开始影响，需要适应。",
            5: "世爻在五爻，外卦中爻，外部条件有利，处于有利位置。",
            6: "世爻在上爻，外卦上爻，事情接近尾声，结果可能超出掌控。"
        }
        
        self.ying_positions = {
            1: "应爻在初爻，对方或外部因素处于起始阶段。",
            2: "应爻在二爻，对方或外部因素条件较好。",
            3: "应爻在三爻，对方或外部因素处于变化中。",
            4: "应爻在四爻，外部环境对事态有影响。",
            5: "应爻在五爻，外部力量强势。",
            6: "应爻在上爻，外部因素接近终结状态。"
        }
        
        # 世应爻关系
        self.shiying_relations = {
            "世应同动": "世应爻同时变动，事情发展双方都有主动变化。",
            "世动应不动": "世爻变动应爻不变，自身主动改变而外部因素保持不变。",
            "应动世不动": "应爻变动世爻不变，外部环境变化而自身保持不变。",
            "世应皆不动": "世应爻都不变动，事情发展双方都保持稳定。"
        }
    
    def interpret(self, gua_result: Dict, day_master: Optional[str] = None, 
                 query_type: Optional[str] = None) -> str:
        """
        解释世应爻的关系及其影响
        
        参数:
            gua_result (Dict): 卦象计算结果
            day_master (str, optional): 日主天干
            query_type (str, optional): 测算类型
            
        返回:
            str: 解释结果
        """
        # 提取世应爻信息
        shi_yao = gua_result["shi_yao"]
        ying_yao = gua_result["ying_yao"]
        dong_yao = gua_result["dong_yao"]
        najia = gua_result["najia"]
        liuqin = gua_result.get("liuqin", ["未知"] * 6)
        
        shi_yao_idx = shi_yao - 1
        ying_yao_idx = ying_yao - 1
        
        shi_yao_name = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"][shi_yao_idx]
        ying_yao_name = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"][ying_yao_idx]
        
        shi_yao_najia = najia[shi_yao_idx] if shi_yao_idx < len(najia) else ""
        ying_yao_najia = najia[ying_yao_idx] if ying_yao_idx < len(najia) else ""
        
        shi_yao_liuqin = liuqin[shi_yao_idx] if shi_yao_idx < len(liuqin) else "未知"
        ying_yao_liuqin = liuqin[ying_yao_idx] if ying_yao_idx < len(liuqin) else "未知"
        
        # 世应爻动静关系
        shi_dong = shi_yao == dong_yao
        ying_dong = ying_yao == dong_yao
        shiying_relation = ""
        if shi_dong and ying_dong:
            shiying_relation = self.shiying_relations["世应同动"]
        elif shi_dong and not ying_dong:
            shiying_relation = self.shiying_relations["世动应不动"]
        elif not shi_dong and ying_dong:
            shiying_relation = self.shiying_relations["应动世不动"]
        else:
            shiying_relation = self.shiying_relations["世应皆不动"]
        
        # 组合解释
        explanation = f"世爻在第{shi_yao}爻（{shi_yao_name}），纳甲为「{shi_yao_najia}」，六亲为「{shi_yao_liuqin}」。\n"
        explanation += f"应爻在第{ying_yao}爻（{ying_yao_name}），纳甲为「{ying_yao_najia}」，六亲为「{ying_yao_liuqin}」。\n\n"
        
        # 世应爻位置特性
        if shi_yao in self.shi_positions:
            explanation += f"{self.shi_positions[shi_yao]}\n"
        if ying_yao in self.ying_positions:
            explanation += f"{self.ying_positions[ying_yao]}\n"
        
        # 世应动静关系
        explanation += f"\n世应动静：{shiying_relation}\n"
        
        # 世应六亲关系
        explanation += "\n世应六亲关系："
        if shi_yao_liuqin == ying_yao_liuqin:
            explanation += f"世应六亲相同，都是「{shi_yao_liuqin}」，代表双方处于平等地位。"
        else:
            explanation += f"世爻六亲为「{shi_yao_liuqin}」，应爻六亲为「{ying_yao_liuqin}」，"
            
            # 简单的五行生克关系判断（简化处理）
            if shi_yao_liuqin == "父母" and ying_yao_liuqin == "子孙":
                explanation += "世爻生应爻，对求测者有利。"
            elif shi_yao_liuqin == "官鬼" and ying_yao_liuqin == "父母":
                explanation += "世爻克应爻，事情发展可控。"
            elif shi_yao_liuqin == "子孙" and ying_yao_liuqin == "父母":
                explanation += "世爻被应爻所生，受外部支持。"
            elif shi_yao_liuqin == "父母" and ying_yao_liuqin == "官鬼":
                explanation += "世爻被应爻所克，受外部压制。"
            else:
                explanation += "关系需结合具体情况分析。"
        
        # 根据测算类型提供更具针对性的解释
        if query_type:
            explanation += f"\n\n在{query_type}方面："
            
            if query_type == "事业":
                if shi_yao <= 3 and shi_yao_liuqin in ["父母", "财星"]:
                    explanation += "事业发展主要依靠自身条件和资源积累。"
                elif shi_yao > 3 and shi_yao_liuqin in ["官鬼", "父母"]:
                    explanation += "事业发展受外部环境和权威影响较大。"
                    
            elif query_type == "财运":
                if shi_yao_liuqin == "财星":
                    explanation += "财运状况与自身掌控密切相关。"
                elif ying_yao_liuqin == "财星":
                    explanation += "财运受外部因素或他人影响较大。"
                    
            elif query_type == "婚姻":
                if shi_yao_liuqin in ["妻财", "官鬼"] and ying_yao_liuqin in ["子孙", "父母"]:
                    explanation += "婚姻关系可能存在权责不均，需要调整。"
                elif shi_yao_liuqin == ying_yao_liuqin:
                    explanation += "婚姻关系较为平等，有共同的价值观和目标。"
                    
            elif query_type == "健康":
                if shi_yao_liuqin == "子孙" and ying_yao_liuqin != "官鬼":
                    explanation += "健康状况较好，自我调节能力强。"
                elif shi_yao_liuqin != "子孙" and ying_yao_liuqin == "官鬼":
                    explanation += "健康可能受外部压力或环境因素影响，需要注意。"
        
        return explanation
