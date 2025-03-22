"""
神煞分析模块
分析八字中的神煞对健康的影响
"""

import json
from pathlib import Path

def analyze_shensha(shensha_list, day_master_element):
    """
    分析神煞及其健康影响
    
    参数:
        shensha_list (list): 神煞名称列表
        day_master_element (str): 日主五行
    
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
    
    # 将日主五行转换为英文
    day_master_element_en = get_element_english(day_master_element)
    
    # 遍历神煞列表
    for shensha in shensha_list:
        # 先查看是否在吉神列表中
        if shensha in shensha_data.get("positive", {}):
            info = shensha_data["positive"][shensha]
            health_aspects = info.get("health_aspects", [])
            element_affinity = info.get("element_affinity", [])
            
            # 评估与日主的相性
            element_match = day_master_element_en in element_affinity
            affinity_level = "高" if element_match else "一般"
            
            positive_impacts.append({
                "name": shensha,
                "description": info.get("description", ""),
                "impact": info.get("impact", ""),
                "health_aspects": health_aspects,
                "element_affinity": element_affinity,
                "day_master_affinity": affinity_level
            })
            
            # 添加健康建议
            if health_aspects:
                health_advice.append({
                    "from_shensha": shensha,
                    "type": "positive",
                    "advice": f"{shensha}有助于{', '.join(health_aspects)}，可以适当发挥其优势。"
                })
        
        # 再查看是否在凶神列表中
        elif shensha in shensha_data.get("negative", {}):
            info = shensha_data["negative"][shensha]
            health_aspects = info.get("health_aspects", [])
            element_affinity = info.get("element_affinity", [])
            remedy = info.get("remedy", [])
            
            # 评估与日主的相性
            element_match = day_master_element_en in element_affinity
            affinity_level = "高" if element_match else "一般"
            
            negative_impacts.append({
                "name": shensha,
                "description": info.get("description", ""),
                "impact": info.get("impact", ""),
                "health_aspects": health_aspects,
                "element_affinity": element_affinity,
                "day_master_affinity": affinity_level,
                "remedy": remedy
            })
            
            # 添加健康建议
            if health_aspects and remedy:
                health_advice.append({
                    "from_shensha": shensha,
                    "type": "negative",
                    "affected_aspects": health_aspects,
                    "remedy": remedy,
                    "advice": f"{shensha}可能导致{', '.join(health_aspects)}，建议{', '.join(remedy)}以减轻影响。"
                })
    
    # 分析总体影响
    overall_analysis = analyze_overall_impact(positive_impacts, negative_impacts, day_master_element)
    
    return {
        "positive_impacts": positive_impacts,
        "negative_impacts": negative_impacts,
        "health_advice": health_advice,
        "overall_analysis": overall_analysis
    }

def analyze_overall_impact(positive_impacts, negative_impacts, day_master_element):
    """
    分析神煞的总体影响
    
    参数:
        positive_impacts (list): 吉神影响列表
        negative_impacts (list): 凶神影响列表
        day_master_element (str): 日主五行
    
    返回:
        dict: 总体影响分析
    """
    positive_count = len(positive_impacts)
    negative_count = len(negative_impacts)
    
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
        all_health_aspects.extend([(aspect, "positive") for aspect in impact.get("health_aspects", [])])
    
    for impact in negative_impacts:
        all_health_aspects.extend([(aspect, "negative") for aspect in impact.get("health_aspects", [])])
    
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

if __name__ == "__main__":
    # 测试代码
    test_shensha_list = ["天乙", "文昌", "劫煞"]
    test_day_master = "木"
    result = analyze_shensha(test_shensha_list, test_day_master)
    print(result)
