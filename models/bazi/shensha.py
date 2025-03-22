"""
神煞分析模块
分析八字中的神煞对健康的影响
"""

import json
from pathlib import Path

def analyze_shensha(shensha_list, day_master_element, day_master_strength="neutral", flow_year_element=None):
    """
    分析神煞及其健康影响
    
    参数:
        shensha_list (list): 神煞名称列表
        day_master_element (str): 日主五行
        day_master_strength (str): 日主强度，可选值为 "strong", "weak", "neutral"，默认为 "neutral"
        flow_year_element (str): 流年五行，用于分析流年对神煞的影响
    
    返回:
        dict: 神煞分析结果和健康建议
    """
    # 加载神煞影响数据
    shensha_data = load_shensha_data()
    
    if not shensha_data:
        return {
            "error": "无法加载神煞数据",
            "message": "请检查数据文件是否存在"
        }
    
    # 分析结果
    positive_impacts = []
    negative_impacts = []
    health_advice = []
    
    # 将日主五行和流年五行转换为英文
    day_master_element_en = get_element_english(day_master_element)
    flow_year_element_en = get_element_english(flow_year_element) if flow_year_element else None
    
    # 根据日主强度确定健康影响键
    day_master_key = f"day_master_{day_master_strength}"
    
    # 遍历神煞列表
    for shensha in shensha_list:
        # 先查看是否在吉神列表中
        if shensha in shensha_data.get("positive", {}):
            info = shensha_data["positive"][shensha]
            
            # 获取健康影响，根据日主强度
            health_impacts = []
            if "health_aspects" in info:
                if day_master_key in info["health_aspects"]:
                    health_impacts = info["health_aspects"][day_master_key]
                elif "day_master_neutral" in info["health_aspects"]:
                    health_impacts = info["health_aspects"]["day_master_neutral"]
            
            # 评估与日主的相性
            element_affinity = info.get("element_affinity", [])
            element_match = day_master_element_en in element_affinity
            affinity_level = "高" if element_match else "一般"
            
            # 分析流年影响
            flow_year_effect = "中性"
            if flow_year_element_en:
                boost_elements = info.get("flow_year_boost", [])
                suppress_elements = info.get("flow_year_suppress", [])
                
                if flow_year_element_en in boost_elements:
                    flow_year_effect = "增强"
                elif flow_year_element_en in suppress_elements:
                    flow_year_effect = "减弱"
            
            impact_info = {
                "name": shensha,
                "description": info.get("description", ""),
                "impact": info.get("impact", ""),
                "health": ", ".join(health_impacts) if health_impacts else "无特定影响",
                "element": info.get("element", ""),
                "day_master_affinity": affinity_level,
                "flow_year_effect": flow_year_effect
            }
            
            positive_impacts.append(impact_info)
            
            # 添加健康建议
            if health_impacts:
                advice = f"{shensha}({flow_year_effect})有助于{', '.join(health_impacts)}，"
                if flow_year_effect == "增强":
                    advice += "流年增强其效果，可以充分发挥其优势。"
                elif flow_year_effect == "减弱":
                    advice += "流年减弱其效果，注意保健以维持其优势。"
                else:
                    advice += "可以适当发挥其优势。"
                    
                health_advice.append(advice)
        
        # 再查看是否在凶神列表中
        elif shensha in shensha_data.get("negative", {}):
            info = shensha_data["negative"][shensha]
            
            # 获取健康影响，根据日主强度
            health_impacts = []
            if "health_aspects" in info:
                if day_master_key in info["health_aspects"]:
                    health_impacts = info["health_aspects"][day_master_key]
                elif "day_master_neutral" in info["health_aspects"]:
                    health_impacts = info["health_aspects"]["day_master_neutral"]
            
            # 评估与日主的相性
            element_affinity = info.get("element_affinity", [])
            element_match = day_master_element_en in element_affinity
            affinity_level = "高" if element_match else "一般"
            
            # 分析流年影响
            flow_year_effect = "中性"
            if flow_year_element_en:
                boost_elements = info.get("flow_year_boost", [])
                suppress_elements = info.get("flow_year_suppress", [])
                
                if flow_year_element_en in boost_elements:
                    flow_year_effect = "增强"
                elif flow_year_element_en in suppress_elements:
                    flow_year_effect = "减弱"
            
            remedy = info.get("remedy", [])
            
            impact_info = {
                "name": shensha,
                "description": info.get("description", ""),
                "impact": info.get("impact", ""),
                "health": ", ".join(health_impacts) if health_impacts else "无特定影响",
                "element": info.get("element", ""),
                "day_master_affinity": affinity_level,
                "flow_year_effect": flow_year_effect,
                "remedy": remedy
            }
            
            negative_impacts.append(impact_info)
            
            # 添加健康建议
            if health_impacts and remedy:
                advice = f"{shensha}({flow_year_effect})可能导致{', '.join(health_impacts)}，"
                if flow_year_effect == "增强":
                    advice += f"流年增强其影响，建议积极采取以下措施：{', '.join(remedy)}。"
                elif flow_year_effect == "减弱":
                    advice += f"流年减弱其影响，可以采取以下措施进一步缓解：{', '.join(remedy)}。"
                else:
                    advice += f"建议{', '.join(remedy)}以减轻影响。"
                    
                health_advice.append(advice)
    
    # 分析总体影响
    overall_analysis = analyze_overall_impact(positive_impacts, negative_impacts, day_master_element, flow_year_element)
    
    return {
        "positive_impacts": positive_impacts,
        "negative_impacts": negative_impacts,
        "health_advice": health_advice,
        "overall_analysis": overall_analysis
    }

def analyze_overall_impact(positive_impacts, negative_impacts, day_master_element, flow_year_element=None):
    """
    分析神煞的总体影响
    
    参数:
        positive_impacts (list): 吉神影响列表
        negative_impacts (list): 凶神影响列表
        day_master_element (str): 日主五行
        flow_year_element (str): 流年五行
    
    返回:
        dict: 总体影响分析
    """
    positive_count = len(positive_impacts)
    negative_count = len(negative_impacts)
    
    # 统计增强和减弱的神煞数量
    positive_enhanced = sum(1 for impact in positive_impacts if impact["flow_year_effect"] == "增强")
    positive_weakened = sum(1 for impact in positive_impacts if impact["flow_year_effect"] == "减弱")
    negative_enhanced = sum(1 for impact in negative_impacts if impact["flow_year_effect"] == "增强")
    negative_weakened = sum(1 for impact in negative_impacts if impact["flow_year_effect"] == "减弱")
    
    # 计算流年影响
    flow_year_impact = ""
    if flow_year_element:
        if positive_enhanced > positive_weakened and negative_weakened > negative_enhanced:
            flow_year_impact = "流年有利，增强吉神效果，减弱凶神影响"
        elif positive_weakened > positive_enhanced and negative_enhanced > negative_weakened:
            flow_year_impact = "流年不利，减弱吉神效果，增强凶神影响"
        elif positive_enhanced > positive_weakened and negative_enhanced > negative_weakened:
            flow_year_impact = "流年作用混合，同时增强吉凶神煞效果"
        elif positive_weakened > positive_enhanced and negative_weakened > negative_enhanced:
            flow_year_impact = "流年作用减弱，同时减弱吉凶神煞效果"
        else:
            flow_year_impact = "流年影响中性"
    
    # 统计与日主相性高的神煞数量
    positive_high_affinity = sum(1 for impact in positive_impacts if impact["day_master_affinity"] == "高")
    negative_high_affinity = sum(1 for impact in negative_impacts if impact["day_master_affinity"] == "高")
    
    # 计算总体倾向
    if positive_count > negative_count * 2:
        tendency = "非常吉利"
    elif positive_count > negative_count:
        tendency = "较为吉利"
    elif positive_count == negative_count:
        tendency = "吉凶参半"
    elif negative_count > positive_count * 2:
        tendency = "非常凶险"
    else:
        tendency = "较为凶险"
    
    # 计算日主相性
    if positive_high_affinity > negative_high_affinity:
        day_master_impact = "吉神相性较强，有助于日主健康"
    elif positive_high_affinity < negative_high_affinity:
        day_master_impact = "凶神相性较强，不利于日主健康"
    else:
        day_master_impact = "吉凶神相性相当，对日主健康影响中性"
    
    # 生成总体健康分析
    health_analysis = generate_health_analysis(positive_impacts, negative_impacts, day_master_element)
    
    return {
        "positive_count": positive_count,
        "negative_count": negative_count,
        "tendency": tendency,
        "day_master_impact": day_master_impact,
        "flow_year_impact": flow_year_impact,
        "positive_enhanced": positive_enhanced,
        "positive_weakened": positive_weakened,
        "negative_enhanced": negative_enhanced,
        "negative_weakened": negative_weakened,
        "health_analysis": health_analysis
    }

def generate_health_analysis(positive_impacts, negative_impacts, day_master_element):
    """
    生成总体健康分析
    
    参数:
        positive_impacts (list): 吉神影响列表
        negative_impacts (list): 凶神影响列表
        day_master_element (str): 日主五行
    
    返回:
        dict: 健康分析结果
    """
    # 收集所有健康方面的影响
    all_health_aspects = []
    
    for impact in positive_impacts:
        health = impact.get("health", "")
        if health and health != "无特定影响":
            aspects = [aspect.strip() for aspect in health.split(",")]
            all_health_aspects.extend([(aspect, "positive") for aspect in aspects])
    
    for impact in negative_impacts:
        health = impact.get("health", "")
        if health and health != "无特定影响":
            aspects = [aspect.strip() for aspect in health.split(",")]
            all_health_aspects.extend([(aspect, "negative") for aspect in aspects])
    
    # 统计各方面的影响
    aspect_counter = {}
    for aspect, impact_type in all_health_aspects:
        if aspect not in aspect_counter:
            aspect_counter[aspect] = {"positive": 0, "negative": 0}
        
        aspect_counter[aspect][impact_type] += 1
    
    # 确定需要关注的健康方面
    health_strengths = []
    health_weaknesses = []
    
    for aspect, counts in aspect_counter.items():
        if counts["positive"] > counts["negative"]:
            health_strengths.append(aspect)
        elif counts["positive"] < counts["negative"]:
            health_weaknesses.append(aspect)
    
    # 根据日主五行确定重点关注的身体系统
    body_systems = get_body_systems_by_element(day_master_element)
    
    # 生成总体健康建议
    if len(health_strengths) > len(health_weaknesses):
        overall_status = "总体健康状况良好"
        focus_advice = "可以重点关注以下方面来进一步提升健康水平:"
    elif len(health_strengths) < len(health_weaknesses):
        overall_status = "总体健康状况有待改善"
        focus_advice = "需要特别关注以下健康方面:"
    else:
        overall_status = "总体健康状况平衡"
        focus_advice = "建议均衡关注各方面健康:"
    
    return {
        "overall_status": overall_status,
        "focus_advice": focus_advice,
        "health_strengths": health_strengths,
        "health_weaknesses": health_weaknesses,
        "body_systems_to_focus": body_systems
    }

def load_shensha_data():
    """
    加载神煞影响数据
    
    返回:
        dict: 神煞影响数据
    """
    try:
        # 定位到项目根目录的data文件夹
        base_dir = Path(__file__).parent.parent.parent
        data_file = base_dir / "data" / "shensha_impacts.json"
        
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载神煞数据出错: {e}")
        return {}

def get_element_english(chinese_element):
    """
    将中文五行属性转换为英文
    
    参数:
        chinese_element (str): 中文五行属性
    
    返回:
        str: 英文五行属性 ('wood', 'fire', 'earth', 'metal', 'water')
    """
    element_map = {
        "木": "wood",
        "火": "fire",
        "土": "earth",
        "金": "metal",
        "水": "water"
    }
    
    return element_map.get(chinese_element, "unknown")

def get_body_systems_by_element(element):
    """
    根据五行获取对应的身体系统
    
    参数:
        element (str): 五行属性
    
    返回:
        list: 身体系统列表
    """
    body_systems = {
        "木": ["肝胆系统", "眼睛", "筋络"],
        "火": ["心脏", "血液循环", "小肠"],
        "土": ["脾胃", "消化系统", "肌肉"],
        "金": ["肺", "大肠", "呼吸系统", "皮肤"],
        "水": ["肾脏", "泌尿系统", "生殖系统", "骨骼"]
    }
    
    return body_systems.get(element, [])

def format_simplified_result(result):
    """
    将分析结果格式化为简化版本
    
    参数:
        result (dict): 分析结果
        
    返回:
        dict: 简化版分析结果
    """
    positive_impacts = []
    negative_impacts = []
    health_advice = []
    
    for impact in result.get("positive_impacts", []):
        positive_impacts.append({
            "name": impact["name"],
            "health": impact["health"],
            "flow_year_effect": impact["flow_year_effect"]
        })
    
    for impact in result.get("negative_impacts", []):
        negative_impacts.append({
            "name": impact["name"],
            "health": impact["health"],
            "flow_year_effect": impact["flow_year_effect"]
        })
    
    health_advice = result.get("health_advice", [])
    
    return {
        "positive_impacts": positive_impacts,
        "negative_impacts": negative_impacts,
        "health_advice": health_advice
    }

if __name__ == "__main__":
    # 测试代码
    test_shensha_list = ["天乙贵人", "白虎"]
    test_day_master = "木"
    test_day_master_strength = "strong"  # 日主强度：strong, weak, neutral
    test_flow_year = "金"  # 2025年乙巳转申年，流年属金
    
    # 进行神煞分析
    result = analyze_shensha(
        test_shensha_list, 
        test_day_master, 
        day_master_strength=test_day_master_strength,
        flow_year_element=test_flow_year
    )
    
    # 输出简化版结果
    simplified_result = format_simplified_result(result)
    print("神煞分析结果 (简化版):")
    print(json.dumps(simplified_result, ensure_ascii=False, indent=2))
    
    # 输出完整结果
    print("\n神煞分析结果 (完整版):")
    print(json.dumps(result, ensure_ascii=False, indent=2))
