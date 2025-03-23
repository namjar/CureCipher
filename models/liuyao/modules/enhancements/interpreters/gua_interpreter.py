"""
六爻卦象综合解释模块 - 集成各专项解释器
"""

from typing import Dict, List, Optional, Tuple, Union
from .base_interpreter import BaseInterpreter
from .basic_gua_interpreter import BasicGuaInterpreter
from .dong_yao_interpreter import DongYaoInterpreter
from .shiying_interpreter import ShiyingInterpreter
from .liuqin_liushen_interpreter import LiuqinLiushenInterpreter
from .najia_wuxing_interpreter import NajiaWuxingInterpreter
from .specific_query_interpreter import SpecificQueryInterpreter


class GuaInterpreter(BaseInterpreter):
    """六爻卦象综合解释器，整合各子解释器的功能"""
    
    def __init__(self):
        """初始化综合解释器，加载所有子解释器"""
        self.interpreters = {
            "基本卦义": BasicGuaInterpreter(),
            "动爻解释": DongYaoInterpreter(),
            "世应关系": ShiyingInterpreter(),
            "六亲六神": LiuqinLiushenInterpreter(),
            "纳甲五行": NajiaWuxingInterpreter(),
            "专题解释": SpecificQueryInterpreter()
        }
        
        # 定义AI接口配置
        self.ai_config = {
            "enabled": False,  # 默认不启用AI增强
            "ai_service": "local",  # 默认使用本地解释库
            "prompt_template": "分析六爻卦象{ben_gua}变{bian_gua}，动爻在{dong_yao}，特别关注{aspect}方面。",
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        # 专题领域映射表
        self.domain_mapping = {
            "事业": ["career", "business", "job", "work", "profession"],
            "财运": ["wealth", "money", "finance", "financial", "investment"],
            "婚姻": ["marriage", "relationship", "love", "family", "couple"],
            "健康": ["health", "medical", "body", "physical", "wellness"],
            "学业": ["study", "education", "learning", "academic", "school"],
            "出行": ["travel", "journey", "trip", "movement", "transportation"],
            "诉讼": ["lawsuit", "legal", "court", "litigation", "dispute"],
            "寻物": ["search", "lost", "missing", "find", "seek"]
        }
    
    def interpret(self, gua_result: Dict, day_master: Optional[str] = None, 
                 query_type: Optional[str] = None) -> str:
        """
        综合解释卦象
        
        参数:
            gua_result (Dict): 卦象计算结果
            day_master (str, optional): 日主天干
            query_type (str, optional): 测算类型
            
        返回:
            str: 解释结果
        """
        # 创建综合解释结果
        all_interpretations = {}
        
        # 收集各子解释器的结果
        for name, interpreter in self.interpreters.items():
            if name == "专题解释" and not query_type:
                continue  # 如果没有指定测算类型，跳过专题解释
                
            try:
                result = interpreter.interpret(gua_result, day_master, query_type)
                all_interpretations[name] = result
            except Exception as e:
                all_interpretations[name] = f"解释过程出错: {str(e)}"
        
        # 组合解释结果
        combined_result = self._combine_interpretations(all_interpretations, query_type)
        
        return combined_result
    
    def _combine_interpretations(self, interpretations: Dict[str, str], query_type: Optional[str]) -> str:
        """
        组合各解释器的结果
        
        参数:
            interpretations (Dict[str, str]): 各解释器的结果
            query_type (str, optional): 测算类型
            
        返回:
            str: 组合后的解释
        """
        # 创建综合解释文本
        combined = "【六爻卦象综合解释】\n\n"
        
        # 添加基本卦义
        if "基本卦义" in interpretations:
            combined += "一、卦象基本信息\n"
            combined += interpretations["基本卦义"] + "\n\n"
        
        # 添加动爻解释
        if "动爻解释" in interpretations:
            combined += "二、动爻详解\n"
            combined += interpretations["动爻解释"] + "\n\n"
        
        # 添加世应关系
        if "世应关系" in interpretations:
            combined += "三、世应爻关系\n"
            combined += interpretations["世应关系"] + "\n\n"
        
        # 添加六亲六神分析
        if "六亲六神" in interpretations:
            combined += "四、六亲六神分析\n"
            combined += interpretations["六亲六神"] + "\n\n"
        
        # 如果有日主信息，添加纳甲五行分析
        if "纳甲五行" in interpretations and "未提供日主天干" not in interpretations["纳甲五行"]:
            combined += "五、纳甲五行分析\n"
            combined += interpretations["纳甲五行"] + "\n\n"
        
        # 如果指定了测算类型，添加专题解释
        if query_type and "专题解释" in interpretations:
            combined += f"六、{query_type}专题解析\n"
            combined += interpretations["专题解释"] + "\n\n"
        
        # 添加AI增强解释（如果启用）
        if self.ai_config["enabled"] and query_type:
            ai_interpretation = self._get_ai_interpretation(interpretations, query_type)
            combined += "七、AI深度解析\n"
            combined += ai_interpretation + "\n\n"
        
        # 添加综合建议
        combined += "【综合建议】\n"
        combined += self._generate_advice(interpretations, query_type) + "\n"
        
        return combined
    
    def _get_ai_interpretation(self, interpretations: Dict[str, str], query_type: str) -> str:
        """
        获取AI增强解释
        
        参数:
            interpretations (Dict[str, str]): 各解释器的结果
            query_type (str): 测算类型
            
        返回:
            str: AI增强解释
        """
        # 此方法是预留的AI接口，用于后续实现与大模型的集成
        # 在完成AI接口之前，返回适当的占位信息
        return "AI增强解释功能尚未启用。未来版本将支持通过大型语言模型提供更个性化、深入的卦象解读，敬请期待。"
    
    def _generate_advice(self, interpretations: Dict[str, str], query_type: Optional[str]) -> str:
        """
        生成综合建议
        
        参数:
            interpretations (Dict[str, str]): 各解释器的结果
            query_type (str, optional): 测算类型
            
        返回:
            str: 综合建议
        """
        advice = "根据卦象分析，提供以下综合建议：\n\n"
        
        # 从基本卦义中提取关键信息
        if "基本卦义" in interpretations:
            basic_text = interpretations["基本卦义"]
            if "有利" in basic_text:
                advice += "1. 总体形势较为有利，可积极行动，把握机遇。\n"
            elif "不利" in basic_text:
                advice += "1. 总体形势有所不利，宜谨慎行事，避免冒险。\n"
            else:
                advice += "1. 总体形势平稳，取舍进退需权衡当前具体情况。\n"
        
        # 从动爻解释中提取关键信息
        if "动爻解释" in interpretations:
            dong_text = interpretations["动爻解释"]
            
            if "青龙" in dong_text:
                advice += "2. 有贵人相助，可寻求他人支持与合作。\n"
            elif "白虎" in dong_text:
                advice += "2. 需警惕潜在风险，做好防范措施。\n"
            
            if "第5爻" in dong_text or "五爻" in dong_text:
                advice += "3. 关注权威力量或领导因素的影响，适时调整策略。\n"
            elif "第1爻" in dong_text or "初爻" in dong_text:
                advice += "3. 注重基础建设，打好根基，循序渐进。\n"
        
        # 根据测算类型提供针对性建议
        if query_type:
            advice += f"4. 在{query_type}方面："
            
            if query_type == "事业":
                advice += "保持专业能力提升，注重人际关系经营，把握机遇同时做好风险管理。\n"
            elif query_type == "财运":
                advice += "量入为出，适度投资，保持财务状况透明且具备应急准备。\n"
            elif query_type == "婚姻":
                advice += "增进沟通理解，共同面对挑战，相互尊重支持，共同构建和谐家庭。\n"
            elif query_type == "健康":
                advice += "均衡饮食，适度运动，保持良好作息，定期体检，关注身心平衡。\n"
            else:
                advice += "根据具体情况制定合理计划，保持灵活应变能力。\n"
        
        advice += "\n以上建议仅供参考，具体决策请结合实际情况综合考量。"
        
        return advice

    def enable_ai(self, enabled: bool = True, service: str = "local",
                  api_key: Optional[str] = None, max_tokens: int = 1000,
                  temperature: float = 0.7) -> None:
        """
        启用或禁用AI增强解释
        
        参数:
            enabled (bool): 是否启用AI增强
            service (str): AI服务提供商，可选值："local", "openai", "anthropic", "custom"
            api_key (str, optional): API密钥
            max_tokens (int): 最大生成令牌数
            temperature (float): 生成温度，控制创造性程度
        """
        self.ai_config["enabled"] = enabled
        self.ai_config["ai_service"] = service
        
        if api_key:
            self.ai_config["api_key"] = api_key
            
        self.ai_config["max_tokens"] = max_tokens
        self.ai_config["temperature"] = temperature
        
        # 打印设置状态
        status = "启用" if enabled else "禁用"
        print(f"AI增强解释已{status}，使用{service}服务。")

    def set_ai_prompt_template(self, template: str) -> None:
        """
        设置AI提示模板
        
        参数:
            template (str): 提示模板，可使用{ben_gua}、{bian_gua}、{dong_yao}、{aspect}等占位符
        """
        self.ai_config["prompt_template"] = template
        print(f"AI提示模板已更新：{template}")


# 导出单例实例
gua_interpreter = GuaInterpreter()
