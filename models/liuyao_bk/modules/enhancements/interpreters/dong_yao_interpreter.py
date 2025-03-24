"""
动爻解释模块
"""

from typing import Dict, List, Optional
from .base_interpreter import BaseInterpreter


class DongYaoInterpreter(BaseInterpreter):
    """动爻解释器，解释动爻的含义和影响"""
    
    def __init__(self):
        """初始化动爻解释器"""
        # 爻位特性说明
        self.yao_positions = {
            1: "初爻为基础，代表事情的开始阶段。",
            2: "二爻为内卦中爻，代表内部条件或自身准备。",
            3: "三爻为内外过渡，代表变化的转折点。",
            4: "四爻为外卦初爻，代表外部环境的影响。",
            5: "五爻为外卦中爻，九五之尊，代表最有力的外部条件。",
            6: "上爻为终结之爻，代表事情的结果或未来趋势。"
        }
        
        # 六亲关系与解释
        self.liuqin_meanings = {
            "兄弟": "同辈、竞争、平行关系、合作与竞争",
            "子孙": "后辈、收获、成果、子女、学生",
            "父母": "长辈、权威、支持、资源、帮助",
            "官鬼": "权力、压力、管束、规则、法律",
            "财星": "财富、收益、资源、物质",
            "妻财": "妻子、感情、财富、资源"
        }
        
        # 六神与解释
        self.liushen_meanings = {
            "青龙": "吉神，主贵人、喜事、福气",
            "朱雀": "凶神，主口舌、是非、争端",
            "勾陈": "半吉半凶，主阻滞、耽误、迟缓",
            "腾蛇": "凶神，主变动、波折、反复",
            "白虎": "凶神，主损伤、损失、疾病",
            "玄武": "凶神，主暗昧、隐藏、盗贼"
        }
    
    def interpret(self, gua_result: Dict, day_master: Optional[str] = None, 
                 query_type: Optional[str] = None) -> str:
        """
        解释动爻的含义和影响
        
        参数:
            gua_result (Dict): 卦象计算结果
            day_master (str, optional): 日主天干
            query_type (str, optional): 测算类型
            
        返回:
            str: 解释结果
        """
        # 提取卦象基本信息
        ben_gua = gua_result["ben_gua"]
        najia = gua_result["najia"]
        dong_yao = gua_result["dong_yao"]
        liuqin = gua_result.get("liuqin", ["未知"] * 6)
        liushen = gua_result.get("liushen", ["未知"] * 6)
        
        # 获取动爻信息
        dong_yao_idx = dong_yao - 1
        dong_yao_najia = najia[dong_yao_idx] if dong_yao_idx < len(najia) else ""
        dong_yao_liuqin = liuqin[dong_yao_idx] if dong_yao_idx < len(liuqin) else "未知"
        dong_yao_liushen = liushen[dong_yao_idx] if dong_yao_idx < len(liushen) else "未知"
        
        # 动爻爻辞
        dong_yao_name = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"][dong_yao_idx]
        ben_gua_interpretation = ben_gua.get("interpretation", {})
        yaoci = ben_gua_interpretation.get("爻辞", {})
        yaoci_explain = ben_gua_interpretation.get("爻辞解释", {})
        
        # 阳爻动与阴爻动的区别
        ben_yao = ben_gua["yao"]
        yao_type = "阳爻" if dong_yao_idx < len(ben_yao) and ben_yao[dong_yao_idx] == 1 else "阴爻"
        
        # 组合解释
        explanation = f"动爻在第{dong_yao}爻（{dong_yao_name}），属{yao_type}，六亲为「{dong_yao_liuqin}」，六神为「{dong_yao_liushen}」，纳甲为「{dong_yao_najia}」。\n"
        
        # 动爻爻辞解释
        yao_key = f"{'九' if yao_type == '阳爻' else '六'}{['初', '二', '三', '四', '五', '上'][dong_yao_idx]}"
        if yao_key in yaoci and yao_key in yaoci_explain:
            explanation += f"\n爻辞：「{yaoci[yao_key]}」，{yaoci_explain[yao_key]}\n"
        
        # 动爻位置的特性
        if dong_yao in self.yao_positions:
            explanation += f"\n{self.yao_positions[dong_yao]}\n"
        
        # 六亲特性
        if dong_yao_liuqin in self.liuqin_meanings:
            explanation += f"\n动爻六亲为「{dong_yao_liuqin}」，{self.liuqin_meanings[dong_yao_liuqin]}。"
        
        # 六神特性
        if dong_yao_liushen in self.liushen_meanings:
            explanation += f"\n动爻六神为「{dong_yao_liushen}」，{self.liushen_meanings[dong_yao_liushen]}。"
        
        # 根据测算类型提供更具针对性的解释
        if query_type:
            explanation += f"\n\n在{query_type}方面："
            
            if query_type == "事业":
                if dong_yao_liuqin == "官鬼":
                    explanation += "动爻为官鬼，事业上可能面临权威或规则的影响，宜谨慎行事。"
                elif dong_yao_liuqin == "父母":
                    explanation += "动爻为父母，事业上可能有贵人相助或资源支持，宜把握机会。"
                    
                if dong_yao_liushen == "青龙":
                    explanation += "动爻六神为青龙，事业发展有吉兆，可能有好机遇。"
                elif dong_yao_liushen == "白虎":
                    explanation += "动爻六神为白虎，事业上需谨防损失或阻力。"
                    
            elif query_type == "财运":
                if dong_yao_liuqin == "财星":
                    explanation += "动爻为财星，财运上有变动，需把握时机。"
                elif dong_yao_liuqin == "官鬼":
                    explanation += "动爻为官鬼，财运可能受到规则或限制的影响。"
                    
                if dong_yao_liushen == "青龙":
                    explanation += "动爻六神为青龙，财运有好转迹象。"
                elif dong_yao_liushen == "玄武":
                    explanation += "动爻六神为玄武，财运上需防隐藏风险或欺诈。"
                    
            elif query_type == "婚姻":
                if dong_yao_liuqin == "子孙":
                    explanation += "动爻为子孙，婚姻上可能与子女或家庭相关事项有变化。"
                elif dong_yao_liuqin == "妻财":
                    explanation += "动爻为妻财，婚姻关系本身有变动。"
                    
                if dong_yao_liushen == "朱雀":
                    explanation += "动爻六神为朱雀，婚姻中可能有口舌是非，需加强沟通。"
                elif dong_yao_liushen == "腾蛇":
                    explanation += "动爻六神为腾蛇，婚姻关系有不稳定因素，需更多包容。"
                    
            elif query_type == "健康":
                if dong_yao_liuqin == "官鬼":
                    explanation += "动爻为官鬼，健康上可能有压力相关的问题。"
                elif dong_yao_liuqin == "子孙":
                    explanation += "动爻为子孙，健康状况可能与生活习惯或长期积累有关。"
                    
                if dong_yao_liushen == "白虎":
                    explanation += "动爻六神为白虎，健康上需警惕外伤或急性疾病。"
                elif dong_yao_liushen == "玄武":
                    explanation += "动爻六神为玄武，健康上需关注隐藏性或慢性疾病。"
        
        return explanation
