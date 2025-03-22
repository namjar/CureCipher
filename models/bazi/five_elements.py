"""
五行分析模块
计算八字中五行的比例并分析其生克关系
提供健康建议
"""

import json
import os
import datetime
from pathlib import Path

def analyze_five_elements(bazi_result):
    """
    分析八字中的五行比例和健康影响
    
    参数:
        bazi_result (dict): calculate_bazi 函数的返回结果
    
    返回:
        dict: 五行分析结果，包括五行比例和健康建议
    """
    # 提取八字中的五行
    elements = {
        "木": 0,
        "火": 0,
        "土": 0,
        "金": 0,
        "水": 0
    }
    
    # 年月日时的五行
    elements[bazi_result["elements"]["year"]] += 1
    elements[bazi_result["elements"]["month"]] += 1
    elements[bazi_result["elements"]["day"]] += 1
    elements[bazi_result["elements"]["hour"]] += 1
    
    # 纳音五行（权重较低）
    nayin_weight = 0.5
    nayin_elements = extract_elements_from_nayin(bazi_result["nayin"])
    for element, count in nayin_elements.items():
        elements[element] += count * nayin_weight
    
    # 当前流年流月的五行（权重较高）
    current_weight = 1.5
    elements[bazi_result["current"]["liunian_element"]] += current_weight
    elements[bazi_result["current"]["liuyue_element"]] += current_weight
    
    # 大运小运的五行（权重较高）
    dayun_weight = 2.0
    xiaoyun_weight = 1.0
    if bazi_result["dayun"]["element"]:
        elements[bazi_result["dayun"]["element"]] += dayun_weight
    elements[bazi_result["xiaoyun"]["element"]] += xiaoyun_weight
    
    # 计算总权重
    total_weight = sum(elements.values())
    
    # 计算百分比
    element_percentages = {element: (count / total_weight) * 100 for element, count in elements.items()}
    
    # 分析五行平衡状态
    balance_analysis = analyze_balance(element_percentages)
    
    # 根据日主分析旺衰
    day_master = bazi_result["bazi"]["day_master_element"]
    day_master_analysis = analyze_day_master(day_master, element_percentages)
    
    # 生克关系分析
    relations_analysis = analyze_relations(day_master, element_percentages)
    
    # 健康建议
    health_advice = generate_health_advice(day_master, element_percentages, balance_analysis)
    
    # 整合饮食和运动建议
    diet_advice = generate_diet_advice(element_percentages)
    exercise_advice = generate_exercise_advice(element_percentages)
    
    return {
        "element_counts": elements,
        "element_percentages": element_percentages,
        "balance_analysis": balance_analysis,
        "day_master_analysis": day_master_analysis,
        "relations_analysis": relations_analysis,
        "health_advice": health_advice,
        "diet_advice": diet_advice,
        "exercise_advice": exercise_advice
    }

def extract_elements_from_nayin(nayin_dict):
    """
    从纳音五行中提取五行元素
    
    参数:
        nayin_dict (dict): 纳音五行字典
    
    返回:
        dict: 五行元素计数
    """
    elements = {
        "木": 0,
        "火": 0,
        "土": 0,
        "金": 0,
        "水": 0
    }
    
    # 纳音五行通常包含两个字，如"山下火"，取最后一个字作为五行
    for key, value in nayin_dict.items():
        if value.endswith("木"):
            elements["木"] += 1
        elif value.endswith("火"):
            elements["火"] += 1
        elif value.endswith("土"):
            elements["土"] += 1
        elif value.endswith("金"):
            elements["金"] += 1
        elif value.endswith("水"):
            elements["水"] += 1
    
    return elements

def analyze_balance(element_percentages):
    """
    分析五行平衡状态
    
    参数:
        element_percentages (dict): 五行百分比
    
    返回:
        dict: 平衡分析结果
    """
    # 计算五行的标准差，越小越平衡
    avg = sum(element_percentages.values()) / 5
    variance = sum((x - avg) ** 2 for x in element_percentages.values()) / 5
    std_dev = variance ** 0.5
    
    # 找出最强和最弱的五行
    strongest = max(element_percentages.items(), key=lambda x: x[1])
    weakest = min(element_percentages.items(), key=lambda x: x[1])
    
    # 分析平衡状态
    if std_dev < 5:
        balance_state = "非常平衡"
        description = "五行分布非常均衡，有利于整体健康。"
    elif std_dev < 10:
        balance_state = "较为平衡"
        description = "五行分布较为均衡，整体健康状况良好。"
    elif std_dev < 15:
        balance_state = "稍有不平衡"
        description = f"{strongest[0]}偏强，{weakest[0]}偏弱，可能需要适当调整。"
    elif std_dev < 20:
        balance_state = "明显不平衡"
        description = f"{strongest[0]}明显过强，{weakest[0]}明显不足，需要重点调整。"
    else:
        balance_state = "严重不平衡"
        description = f"{strongest[0]}极度过强，{weakest[0]}极度不足，健康可能受到影响，需要及时调整。"
    
    return {
        "balance_state": balance_state,
        "description": description,
        "std_deviation": std_dev,
        "strongest": strongest[0],
        "strongest_percentage": strongest[1],
        "weakest": weakest[0],
        "weakest_percentage": weakest[1]
    }

def analyze_day_master(day_master, element_percentages):
    """
    根据日主分析旺衰
    
    参数:
        day_master (str): 日主五行
        element_percentages (dict): 五行百分比
    
    返回:
        dict: 日主分析结果
    """
    # 获取生我和克我的五行
    sheng_wo = get_generating_element(day_master)
    ke_wo = get_controlling_element(day_master)
    
    # 获取我生和我克的五行
    wo_sheng = get_generated_element(day_master)
    wo_ke = get_controlled_element(day_master)
    
    # 日主强度
    day_master_strength = element_percentages[day_master]
    
    # 分析日主旺衰
    if day_master_strength > 30:
        strength_state = "过旺"
        advice = f"需要抑制{day_master}，可以增强{wo_ke}以泄过旺之气。"
    elif day_master_strength > 25:
        strength_state = "偏旺"
        advice = f"稍微抑制{day_master}，适当增强{wo_ke}。"
    elif day_master_strength > 15:
        strength_state = "适中"
        advice = "日主强度适中，保持当前状态即可。"
    elif day_master_strength > 10:
        strength_state = "偏弱"
        advice = f"需要补充{day_master}，或增强{sheng_wo}来帮助生发。"
    else:
        strength_state = "过弱"
        advice = f"日主严重不足，急需补充{day_master}，并大量增强{sheng_wo}，同时避免{ke_wo}的消耗。"
    
    return {
        "day_master": day_master,
        "strength": day_master_strength,
        "strength_state": strength_state,
        "advice": advice,
        "relationships": {
            "sheng_wo": sheng_wo,
            "ke_wo": ke_wo,
            "wo_sheng": wo_sheng,
            "wo_ke": wo_ke
        }
    }

def analyze_relations(day_master, element_percentages):
    """
    分析五行之间的生克关系
    
    参数:
        day_master (str): 日主五行
        element_percentages (dict): 五行百分比
    
    返回:
        dict: 生克关系分析
    """
    # 生克关系
    relations = {}
    
    # 五行相生关系
    for element in ["木", "火", "土", "金", "水"]:
        sheng = get_generating_element(element)
        sheng_by = get_generated_element(element)
        ke = get_controlling_element(element)
        ke_by = get_controlled_element(element)
        
        relations[element] = {
            "percentage": element_percentages[element],
            "sheng_by": {
                "element": sheng,
                "strength": element_percentages[sheng]
            },
            "sheng": {
                "element": sheng_by,
                "strength": element_percentages[sheng_by]
            },
            "ke_by": {
                "element": ke_by,
                "strength": element_percentages[ke_by]
            },
            "ke": {
                "element": ke,
                "strength": element_percentages[ke]
            }
        }
    
    # 分析关键关系
    key_relations = []
    
    # 日主被克过重
    if relations[day_master]["ke_by"]["strength"] > relations[day_master]["percentage"]:
        key_relations.append({
            "type": "日主被克过重",
            "description": f"{relations[day_master]['ke_by']['element']}过强，过度克制{day_master}，可能导致健康问题。",
            "health_impact": f"可能导致与{day_master}相关的身体系统功能减弱。"
        })
    
    # 日主生过重
    if relations[day_master]["sheng"]["strength"] < relations[day_master]["percentage"] * 0.5:
        key_relations.append({
            "type": "日主生力不足",
            "description": f"{day_master}无法有效滋养{relations[day_master]['sheng']['element']}，可能导致能量不足。",
            "health_impact": f"可能导致与{relations[day_master]['sheng']['element']}相关的身体系统能量不足。"
        })
    
    # 五行相克过重的情况
    for element, relation in relations.items():
        if relation["ke_by"]["strength"] > relation["percentage"] * 1.5 and relation["ke_by"]["strength"] > 25:
            key_relations.append({
                "type": f"{element}被克过重",
                "description": f"{relation['ke_by']['element']}过强，过度克制{element}，破坏五行平衡。",
                "health_impact": f"可能导致与{element}相关的身体系统功能紊乱。"
            })
    
    return {
        "detailed_relations": relations,
        "key_relations": key_relations
    }

def generate_health_advice(day_master, element_percentages, balance_analysis):
    """
    根据五行分析生成健康建议
    
    参数:
        day_master (str): 日主五行
        element_percentages (dict): 五行百分比
        balance_analysis (dict): 平衡分析结果
    
    返回:
        dict: 健康建议
    """
    # 五行对应的身体系统
    element_body_systems = {
        "木": ["肝", "胆", "筋络", "眼睛"],
        "火": ["心", "小肠", "血脉", "舌"],
        "土": ["脾", "胃", "肌肉", "口"],
        "金": ["肺", "大肠", "皮毛", "鼻"],
        "水": ["肾", "膀胱", "骨髓", "耳"]
    }
    
    # 过强和过弱的五行
    excess_elements = [e for e, p in element_percentages.items() if p > 25]
    deficient_elements = [e for e, p in element_percentages.items() if p < 10]
    
    # 健康风险
    health_risks = []
    for element in excess_elements:
        health_risks.append({
            "element": element,
            "affected_systems": element_body_systems[element],
            "risk_type": "过盛",
            "description": f"{element}过盛，可能导致{', '.join(element_body_systems[element])}功能亢进或炎症"
        })
    
    for element in deficient_elements:
        health_risks.append({
            "element": element,
            "affected_systems": element_body_systems[element],
            "risk_type": "不足",
            "description": f"{element}不足，可能导致{', '.join(element_body_systems[element])}功能减弱"
        })
    
    # 日主相关的健康建议
    day_master_advice = {
        "木": "注意保护肝脏，避免情绪激动，保持规律作息，适当进行舒展性运动。",
        "火": "注意心脏健康，避免过度兴奋，保持情绪平和，适当进行有氧运动但避免过度。",
        "土": "注意脾胃健康，定时规律饮食，避免过食生冷，加强肌肉锻炼。",
        "金": "注意呼吸系统健康，避免接触烟尘环境，保持环境通风，注意皮肤保湿。",
        "水": "注意肾脏和泌尿系统健康，保持充足的睡眠，避免过度劳累，补充足够水分。"
    }
    
    # 季节性建议
    seasonal_advice = {
        "春季": {
            "木": "春季肝气旺盛，不宜过度滋补，以平和调理为主。",
            "火": "春季注意心火上炎，保持心情平和，避免过度刺激。",
            "土": "春季脾胃功能相对减弱，饮食宜温和，避免生冷。",
            "金": "春季肺气相对偏弱，注意保暖，防止风邪入侵。",
            "水": "春季肾水应养护，避免过度消耗，保持充足休息。"
        },
        "夏季": {
            "木": "夏季肝火易旺，注意清热解毒，避免过度疲劳。",
            "火": "夏季心火最旺，注意清心降火，避免暴晒和情绪激动。",
            "土": "夏季湿热影响脾胃，饮食宜清淡，避免重油腻食物。",
            "金": "夏季肺气最弱，注意防暑降温，保持呼吸道湿润。",
            "水": "夏季肾水易亏，注意补水养阴，避免过度出汗。"
        },
        "秋季": {
            "木": "秋季肝气收敛，注意情志调养，避免抑郁。",
            "火": "秋季心火渐弱，注意保持情绪稳定，防止虚火上浮。",
            "土": "秋季脾胃功能逐渐恢复，饮食宜平和，补充纤维质。",
            "金": "秋季肺气最旺，注意防燥润肺，避免辛辣刺激。",
            "水": "秋季肾水需养护，注意保暖，防止寒邪入侵。"
        },
        "冬季": {
            "木": "冬季肝气闭藏，注意舒肝解郁，避免情绪压抑。",
            "火": "冬季心火内敛，注意保持心阳，避免过度寒冷。",
            "土": "冬季脾胃需温养，饮食宜温热，适当增加热量。",
            "金": "冬季肺气偏弱，注意保暖防寒，避免呼吸道感染。",
            "水": "冬季肾水当令，注意培补肾精，避免过度劳累。"
        }
    }
    
    # 确定当前季节
    month = datetime.datetime.now().month
    season = ""
    if 3 <= month <= 5:
        season = "春季"
    elif 6 <= month <= 8:
        season = "夏季"
    elif 9 <= month <= 11:
        season = "秋季"
    else:
        season = "冬季"
    
    return {
        "general_advice": day_master_advice[day_master],
        "seasonal_advice": seasonal_advice[season][day_master],
        "health_risks": health_risks,
        "balance_recommendation": balance_analysis["description"],
        "specific_recommendations": [
            f"增强{balance_analysis['weakest']}的相关功能",
            f"适当控制{balance_analysis['strongest']}的过度表现"
        ]
    }

def generate_diet_advice(element_percentages):
    """
    根据五行分析生成饮食建议
    
    参数:
        element_percentages (dict): 五行百分比
    
    返回:
        dict: 饮食建议
    """
    # 加载五行口味数据
    flavors_data = load_json_data("five_elements_flavors.json")
    
    # 确定需要增强和减弱的五行
    sorted_elements = sorted(element_percentages.items(), key=lambda x: x[1])
    weakest_elements = sorted_elements[:2]  # 最弱的两个五行
    strongest_elements = sorted_elements[-2:]  # 最强的两个五行
    
    # 根据五行转换为英文
    weakest_elements_en = [(get_element_english(e), p) for e, p in weakest_elements]
    strongest_elements_en = [(get_element_english(e), p) for e, p in strongest_elements]
    
    # 根据五行生成饮食建议
    recommended_flavors = []
    for element, _ in weakest_elements:
        element_en = get_element_english(element)
        if element_en in flavors_data:
            flavor = flavors_data[element_en]["flavor"]
            effect = flavors_data[element_en]["effect"]
            nutrients = flavors_data[element_en]["nutrients"]
            
            recommended_flavors.append({
                "element": element,
                "flavor": flavor,
                "effect": effect,
                "nutrients": nutrients,
                "reason": f"增强{element}五行"
            })
    
    avoid_flavors = []
    for element, _ in strongest_elements:
        element_en = get_element_english(element)
        if element_en in flavors_data:
            flavor = flavors_data[element_en]["flavor"]
            
            avoid_flavors.append({
                "element": element,
                "flavor": flavor,
                "reason": f"降低过盛的{element}五行"
            })
    
    # 从diet_recipes.json加载季节食谱
    recipes_data = load_json_data("diet_recipes.json")
    
    # 确定当前季节
    month = datetime.datetime.now().month
    if 3 <= month <= 5:
        season = "spring"
    elif 6 <= month <= 8:
        season = "summer"
    elif 9 <= month <= 11:
        season = "autumn"
    else:
        season = "winter"
    
    # 获取当前季节的食谱
    seasonal_recipes = recipes_data.get(season, [])
    
    # 根据弱势五行选择合适的食谱
    recommended_recipes = []
    weakest_elements_set = {e for e, _ in weakest_elements_en}
    
    for recipe in seasonal_recipes:
        suitable_elements_set = set(recipe.get("suitable_elements", []))
        if weakest_elements_set.intersection(suitable_elements_set):
            recommended_recipes.append({
                "name": recipe["name"],
                "ingredients": recipe["ingredients"],
                "effect": recipe["effect"]
            })
    
    return {
        "recommended_flavors": recommended_flavors,
        "avoid_flavors": avoid_flavors,
        "seasonal_recipes": recommended_recipes,
        "general_advice": "根据五行平衡状态，调整饮食口味和成分，以达到调和阴阳、平衡五行的目的。"
    }

def generate_exercise_advice(element_percentages):
    """
    根据五行分析生成运动建议
    
    参数:
        element_percentages (dict): 五行百分比
    
    返回:
        dict: 运动建议
    """
    # 加载五行运动数据
    exercises_data = load_json_data("five_elements_exercises.json")
    
    # 确定需要增强和减弱的五行
    sorted_elements = sorted(element_percentages.items(), key=lambda x: x[1])
    weakest_elements = sorted_elements[:2]  # 最弱的两个五行
    balanced_elements = sorted_elements[2:3]  # 居中的一个五行
    
    # 根据五行转换为英文
    weakest_elements_en = [(get_element_english(e), p) for e, p in weakest_elements]
    balanced_elements_en = [(get_element_english(e), p) for e, p in balanced_elements]
    
    # 根据五行生成运动建议
    recommended_exercises = []
    for element, _ in weakest_elements:
        element_en = get_element_english(element)
        if element_en in exercises_data:
            exercise_types = exercises_data[element_en]["exercise_types"]
            effect = exercises_data[element_en]["effect"]
            
            recommended_exercises.append({
                "element": element,
                "exercise_types": exercise_types,
                "effect": effect,
                "reason": f"增强{element}五行"
            })
    
    for element, _ in balanced_elements:
        element_en = get_element_english(element)
        if element_en in exercises_data:
            exercise_types = exercises_data[element_en]["exercise_types"]
            effect = exercises_data[element_en]["effect"]
            
            recommended_exercises.append({
                "element": element,
                "exercise_types": exercise_types,
                "effect": effect,
                "reason": f"保持{element}五行平衡"
            })
    
    return {
        "recommended_exercises": recommended_exercises,
        "general_advice": "根据五行平衡状态，选择适合的运动方式，以调节气血、平衡五行、增强体质。",
        "frequency_advice": "每周至少进行3-5次适度运动，每次30-60分钟，以达到最佳效果。"
    }

def load_json_data(filename):
    """
    加载JSON数据文件
    
    参数:
        filename (str): JSON文件名
    
    返回:
        dict: JSON数据
    """
    try:
        # 定位到项目根目录的data文件夹
        base_dir = Path(__file__).parent.parent.parent
        data_file = base_dir / "data" / filename
        
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载JSON文件出错: {e}")
        return {}

def get_generating_element(element):
    """
    获取生我的五行（生我者）
    
    参数:
        element (str): 五行名称
    
    返回:
        str: 生我的五行
    """
    generating_map = {
        "木": "水",
        "火": "木",
        "土": "火",
        "金": "土",
        "水": "金"
    }
    return generating_map.get(element, "")

def get_generated_element(element):
    """
    获取我生的五行（我生者）
    
    参数:
        element (str): 五行名称
    
    返回:
        str: 我生的五行
    """
    generated_map = {
        "木": "火",
        "火": "土",
        "土": "金",
        "金": "水",
        "水": "木"
    }
    return generated_map.get(element, "")

def get_controlling_element(element):
    """
    获取克我的五行（克我者）
    
    参数:
        element (str): 五行名称
    
    返回:
        str: 克我的五行
    """
    controlling_map = {
        "木": "金",
        "火": "水",
        "土": "木",
        "金": "火",
        "水": "土"
    }
    return controlling_map.get(element, "")

def get_controlled_element(element):
    """
    获取我克的五行（我克者）
    
    参数:
        element (str): 五行名称
    
    返回:
        str: 我克的五行
    """
    controlled_map = {
        "木": "土",
        "火": "金",
        "土": "水",
        "金": "木",
        "水": "火"
    }
    return controlled_map.get(element, "")

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

if __name__ == "__main__":
    # 测试代码
    test_bazi_result = {
        "bazi": {
            "year": "庚午",
            "month": "丙申",
            "day": "甲子",
            "hour": "壬寅",
            "day_master": "甲",
            "day_master_element": "木"
        },
        "elements": {
            "year": "金",
            "month": "火",
            "day": "木",
            "hour": "水"
        },
        "nayin": {
            "year": "路旁土",
            "month": "山下火",
            "day": "海中金",
            "hour": "涧下水"
        },
        "current": {
            "liunian": "乙巳",
            "liunian_element": "木",
            "liuyue": "壬寅",
            "liuyue_element": "水"
        },
        "dayun": {
            "ganzhi": "丙戌",
            "element": "火",
            "start_age": 28,
            "end_age": 38
        },
        "xiaoyun": {
            "ganzhi": "丁亥",
            "element": "火"
        }
    }
    result = analyze_five_elements(test_bazi_result)
    print(result)
