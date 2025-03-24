"""
六亲六神解释模块
"""

from typing import Dict, List, Optional
from .base_interpreter import BaseInterpreter


class LiuqinLiushenInterpreter(BaseInterpreter):
    """六亲六神解释器，分析六亲六神组合对卦象的影响"""
    
    def __init__(self):
        """初始化六亲六神解释器"""
        # 六亲含义和属性
        self.liuqin_meanings = {
            "兄弟": {
                "含义": "同辈、竞争、平行关系、合作与竞争",
                "属性": "中性", 
                "吉凶": "中性",
                "解释": "代表平等关系，可能有合作也可能有竞争，需平衡发展。"
            },
            "子孙": {
                "含义": "后辈、收获、成果、子女、学生",
                "属性": "吉", 
                "吉凶": "吉",
                "解释": "代表收获和成果，通常为吉利之象，能得到满足。"
            },
            "父母": {
                "含义": "长辈、权威、支持、资源、帮助",
                "属性": "中吉", 
                "吉凶": "偏吉",
                "解释": "代表支持和帮助，通常有利于发展，但也可能有依赖性。"
            },
            "官鬼": {
                "含义": "权力、压力、管束、规则、法律",
                "属性": "凶", 
                "吉凶": "偏凶",
                "解释": "代表压力和限制，通常表示需要谨慎行事，有约束或考验。"
            },
            "财星": {
                "含义": "财富、收益、资源、物质",
                "属性": "吉", 
                "吉凶": "吉",
                "解释": "代表物质收获，通常为吉利之象，但也需要适度。"
            },
            "妻财": {
                "含义": "妻子、感情、财富、资源",
                "属性": "吉", 
                "吉凶": "吉",
                "解释": "代表关系和感情，通常利于情感和合作关系发展。"
            }
        }
        
        # 六神含义和属性
        self.liushen_meanings = {
            "青龙": {
                "含义": "贵人、喜事、福气、发展",
                "属性": "吉", 
                "吉凶": "大吉",
                "解释": "主吉祥喜庆，有贵人相助，事业顺利发展。"
            },
            "朱雀": {
                "含义": "口舌、是非、争端、消息",
                "属性": "凶", 
                "吉凶": "小凶",
                "解释": "主口舌是非，有争议和纠纷，但也代表信息和消息。"
            },
            "勾陈": {
                "含义": "阻滞、耽误、迟缓、稳固",
                "属性": "中性", 
                "吉凶": "中性",
                "解释": "主事物进展缓慢，有停滞现象，但也有稳定之意。"
            },
            "腾蛇": {
                "含义": "变动、波折、反复、不稳定",
                "属性": "凶", 
                "吉凶": "小凶",
                "解释": "主变化多端，有反复和波折，情况不稳定。"
            },
            "白虎": {
                "含义": "伤害、损失、疾病、灾难",
                "属性": "凶", 
                "吉凶": "大凶",
                "解释": "主凶险和损伤，有意外或伤害，需要谨慎防范。"
            },
            "玄武": {
                "含义": "暗昧、隐藏、盗贼、隐患",
                "属性": "凶", 
                "吉凶": "中凶",
                "解释": "主隐藏和暗昧，有暗中损害或隐患，需要警惕。"
            }
        }
        
        # 六亲六神组合吉凶
        self.liuqin_liushen_combinations = {
            "子孙_青龙": "非常吉利，代表收获和贵人相助，事情顺利发展。",
            "子孙_白虎": "吉中带凶，虽有收获但可能伴随损失或伤害。",
            "财星_青龙": "非常吉利，财运亨通，有贵人助力。",
            "财星_玄武": "吉中带凶，财运有隐藏风险，需警惕欺诈。",
            "官鬼_白虎": "非常凶险，代表强大压力和损害，需谨慎应对。",
            "官鬼_青龙": "凶中带吉，压力虽大但有贵人化解，可转危为安。",
            "父母_青龙": "非常吉利，有强力支持和贵人帮助。",
            "父母_腾蛇": "吉中带凶，支持不稳定，可能反复变化。"
        }
    
    def interpret(self, gua_result: Dict, day_master: Optional[str] = None, 
                 query_type: Optional[str] = None) -> str:
        """
        解释六亲六神组合对卦象的影响
        
        参数:
            gua_result (Dict): 卦象计算结果
            day_master (str, optional): 日主天干
            query_type (str, optional): 测算类型
            
        返回:
            str: 解释结果
        """
        # 提取六亲六神信息
        liuqin = gua_result.get("liuqin", ["未知"] * 6)
        liushen = gua_result.get("liushen", ["未知"] * 6)
        dong_yao = gua_result["dong_yao"]
        shi_yao = gua_result["shi_yao"]
        
        dong_yao_idx = dong_yao - 1
        shi_yao_idx = shi_yao - 1
        
        # 动爻六亲六神
        dong_liuqin = liuqin[dong_yao_idx] if dong_yao_idx < len(liuqin) else "未知"
        dong_liushen = liushen[dong_yao_idx] if dong_yao_idx < len(liushen) else "未知"
        
        # 世爻六亲六神
        shi_liuqin = liuqin[shi_yao_idx] if shi_yao_idx < len(liuqin) else "未知"
        shi_liushen = liushen[shi_yao_idx] if shi_yao_idx < len(liushen) else "未知"
        
        # 生成六神概况
        liushen_summary = "六神分布：\n"
        for i, shen in enumerate(liushen):
            if i < len(liushen):
                yao_name = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"][i]
                liushen_summary += f"{yao_name}：{shen}，"
                if (i + 1) % 3 == 0:
                    liushen_summary = liushen_summary.rstrip("，") + "\n"
        
        # 生成六亲概况
        liuqin_summary = "六亲分布：\n"
        for i, qin in enumerate(liuqin):
            if i < len(liuqin):
                yao_name = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"][i]
                liuqin_summary += f"{yao_name}：{qin}，"
                if (i + 1) % 3 == 0:
                    liuqin_summary = liuqin_summary.rstrip("，") + "\n"
        
        # 组合解释
        explanation = f"{liuqin_summary}\n{liushen_summary}\n"
        
        explanation += "重要爻位分析：\n"
        
        # 动爻六亲六神分析
        explanation += f"动爻（第{dong_yao}爻）：六亲为「{dong_liuqin}」，六神为「{dong_liushen}」\n"
        
        if dong_liuqin in self.liuqin_meanings:
            explanation += f"六亲含义：{self.liuqin_meanings[dong_liuqin]['含义']}，{self.liuqin_meanings[dong_liuqin]['解释']}\n"
            
        if dong_liushen in self.liushen_meanings:
            explanation += f"六神含义：{self.liushen_meanings[dong_liushen]['含义']}，{self.liushen_meanings[dong_liushen]['解释']}\n"
            
        # 动爻六亲六神组合分析
        combo_key = f"{dong_liuqin}_{dong_liushen}"
        if combo_key in self.liuqin_liushen_combinations:
            explanation += f"组合效应：{self.liuqin_liushen_combinations[combo_key]}\n"
        
        # 世爻六亲六神分析
        explanation += f"\n世爻（第{shi_yao}爻）：六亲为「{shi_liuqin}」，六神为「{shi_liushen}」\n"
        
        if shi_liuqin in self.liuqin_meanings:
            explanation += f"六亲含义：{self.liuqin_meanings[shi_liuqin]['含义']}，{self.liuqin_meanings[shi_liuqin]['解释']}\n"
            
        if shi_liushen in self.liushen_meanings:
            explanation += f"六神含义：{self.liushen_meanings[shi_liushen]['含义']}，{self.liushen_meanings[shi_liushen]['解释']}\n"
            
        # 世爻六亲六神组合分析
        combo_key = f"{shi_liuqin}_{shi_liushen}"
        if combo_key in self.liuqin_liushen_combinations:
            explanation += f"组合效应：{self.liuqin_liushen_combinations[combo_key]}\n"
        
        # 六亲六神整体吉凶判断
        explanation += "\n整体六亲六神趋势判断：\n"
        
        # 统计吉神凶神比例
        good_gods = sum(1 for s in liushen if s in ["青龙"])
        bad_gods = sum(1 for s in liushen if s in ["白虎", "玄武"])
        neutral_gods = sum(1 for s in liushen if s in ["勾陈", "腾蛇", "朱雀"])
        
        # 统计吉神凶神在关键爻的分布
        key_yao_goods = 0
        key_yao_bads = 0
        
        if dong_liushen in ["青龙"]:
            key_yao_goods += 1
        if dong_liushen in ["白虎", "玄武"]:
            key_yao_bads += 1
            
        if shi_liushen in ["青龙"]:
            key_yao_goods += 1
        if shi_liushen in ["白虎", "玄武"]:
            key_yao_bads += 1
        
        # 根据统计做出判断
        if good_gods > bad_gods:
            explanation += "六神总体偏吉，"
            if key_yao_goods > key_yao_bads:
                explanation += "且吉神位于关键爻位，整体发展趋势良好。"
            else:
                explanation += "但关键爻位缺乏吉神支持，发展可能不够稳定。"
        elif good_gods < bad_gods:
            explanation += "六神总体偏凶，"
            if key_yao_goods < key_yao_bads:
                explanation += "且凶神位于关键爻位，整体发展趋势不佳，需谨慎应对。"
            else:
                explanation += "但关键爻位有吉神支持，仍有转机可能。"
        else:
            explanation += "六神吉凶平衡，"
            if key_yao_goods > key_yao_bads:
                explanation += "且关键爻位有吉神支持，总体较为有利。"
            elif key_yao_goods < key_yao_bads:
                explanation += "但关键爻位多凶神，还需警惕不利因素。"
            else:
                explanation += "整体发展中性，进退需把握时机。"
        
        # 根据测算类型提供更具针对性的解释
        if query_type:
            explanation += f"\n\n在{query_type}方面的六亲六神分析：\n"
            
            if query_type == "事业":
                # 分析与事业相关的六亲
                career_qins = ["官鬼", "父母"]
                career_qin_count = sum(1 for q in liuqin if q in career_qins)
                
                if career_qin_count >= 3:
                    explanation += "卦中官鬼、父母爻较多，事业运势较强，有管理或领导机会。"
                else:
                    explanation += "卦中官鬼、父母爻较少，事业发展需更多自主努力。"
                
                # 分析动爻和世爻的六亲六神组合对事业的影响
                if dong_liuqin in career_qins:
                    explanation += f"\n动爻为{dong_liuqin}，事业方面有明显变动，"
                    if dong_liushen == "青龙":
                        explanation += "且有贵人相助，变动趋于有利。"
                    elif dong_liushen in ["白虎", "玄武"]:
                        explanation += "但有不利因素干扰，变动需谨慎应对。"
                    else:
                        explanation += "变动方向需结合其他因素判断。"
                
            elif query_type == "财运":
                # 分析与财运相关的六亲
                wealth_qins = ["财星", "妻财"]
                wealth_qin_count = sum(1 for q in liuqin if q in wealth_qins)
                
                if wealth_qin_count >= 3:
                    explanation += "卦中财星爻较多，财运基础较好，有收益机会。"
                else:
                    explanation += "卦中财星爻较少，财运需要更多努力积累。"
                
                # 分析动爻和世爻的六亲六神组合对财运的影响
                if dong_liuqin in wealth_qins:
                    explanation += f"\n动爻为{dong_liuqin}，财运方面有明显变动，"
                    if dong_liushen == "青龙":
                        explanation += "且有意外之喜，变动趋于获利。"
                    elif dong_liushen == "玄武":
                        explanation += "但有隐藏风险，收益需谨慎保障。"
                    else:
                        explanation += "变动方向需结合其他因素判断。"
                
            elif query_type == "婚姻":
                # 分析与婚姻相关的六亲
                marriage_qins = ["妻财", "官鬼"]
                marriage_qin_count = sum(1 for q in liuqin if q in marriage_qins)
                
                if marriage_qin_count >= 3:
                    explanation += "卦中与婚姻相关的爻较多，感情运势较强。"
                else:
                    explanation += "卦中与婚姻相关的爻较少，感情方面需更多主动经营。"
                
                # 分析动爻和世爻的六亲六神组合对婚姻的影响
                if dong_liuqin in marriage_qins:
                    explanation += f"\n动爻为{dong_liuqin}，婚姻关系有明显变动，"
                    if dong_liushen == "青龙":
                        explanation += "整体趋于和谐发展。"
                    elif dong_liushen == "朱雀":
                        explanation += "可能有口舌争端，需加强沟通。"
                    elif dong_liushen == "腾蛇":
                        explanation += "关系较不稳定，需增进互信和理解。"
                    else:
                        explanation += "变动方向需结合其他因素判断。"
                
            elif query_type == "健康":
                # 分析与健康相关的六亲
                health_qins = ["子孙", "父母"]
                health_shen = ["青龙", "白虎"]
                
                # 分析动爻和世爻的六亲六神组合对健康的影响
                if dong_liuqin in health_qins:
                    explanation += f"动爻为{dong_liuqin}，健康状况有变化，"
                    if dong_liushen == "青龙":
                        explanation += "整体趋于改善。"
                    elif dong_liushen == "白虎":
                        explanation += "需警惕外伤或急性疾病。"
                    elif dong_liushen == "玄武":
                        explanation += "需关注隐藏性或慢性健康问题。"
                    else:
                        explanation += "变化方向需结合其他因素判断。"
                
                # 白虎爻的健康警示
                white_tiger_positions = [i+1 for i, s in enumerate(liushen) if s == "白虎"]
                if white_tiger_positions:
                    explanation += f"\n白虎神在第{', '.join(map(str, white_tiger_positions))}爻，"
                    if dong_yao in white_tiger_positions:
                        explanation += "且为动爻，需特别注意健康问题。"
                    else:
                        explanation += "需警惕相关部位或系统的健康问题。"
        
        return explanation
