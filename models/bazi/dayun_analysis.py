#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大运分析模块 - 提供详细的大运走势分析，含健康影响
"""

from collections import defaultdict
from datetime import datetime
from pathlib import Path
import json

def load_shensha_data():
    """加载神煞影响数据"""
    try:
        base_dir = Path(__file__).parent.parent.parent
        data_file = base_dir / "data" / "shensha_impacts.json"
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载神煞数据出错: {e}")
        return {}

def analyze_dayun(report, gender_code=1, details_level=1, flow_year=None):
    """
    分析大运信息，提供详细走势和健康分析
    
    参数:
        report (dict): 八字命盘报告
        gender_code (int): 性别代码，1为男，0为女
        details_level (int): 详细程度，1-简要，2-中等，3-详细
        flow_year (int, optional): 当前流年，影响大运评分
    
    返回:
        dict: 大运分析结果
    """
    if not report or 'dayun_analysis' not in report:
        return {"error": "报告数据不完整，无法分析大运"}
    
    dayuns = report.get('dayun_analysis', [])
    if not dayuns:
        return {"error": "未找到大运数据"}
    
    # 基本信息
    day_master = report['basic_info']['day_master'].split()[0]  # 日主天干
    day_master_element = report['basic_info']['day_master'].split('(')[1].strip(')')  # 日主五行
    day_master_strength = report['pattern_analysis']['day_master_strength']  # 日主强度
    yong_shen = report['pattern_analysis'].get('yong_shen', '').split()[0]  # 用神
    
    # 加载神煞数据
    shensha_data = load_shensha_data()
    
    # 流年五行（可选）
    flow_year_element = get_element(calculate_ganzhi(flow_year)[0]) if flow_year else None
    
    # 分析结果
    result = {
        "summary": "大运总体走势分析",
        "dayuns": [],
        "key_periods": [],
        "life_stages": []
    }
    
    # 分析每个大运
    for dayun in dayuns:
        dayun_analysis = analyze_single_dayun(dayun, day_master, day_master_element, 
                                            day_master_strength, yong_shen, gender_code, 
                                            details_level, shensha_data, flow_year_element)
        result["dayuns"].append(dayun_analysis)
    
    # 总体分析和关键时期
    result["summary"] = generate_dayun_summary(result["dayuns"], day_master_strength, yong_shen)
    result["key_periods"] = identify_key_periods(result["dayuns"], day_master_element)
    result["life_stages"] = analyze_life_stages(result["dayuns"])
    
    return result

def analyze_single_dayun(dayun, day_master, day_master_element, day_master_strength, yong_shen, 
                        gender_code, details_level, shensha_data, flow_year_element):
    """分析单个大运的吉凶、健康和影响"""
    gan_zhi = dayun['ganzhi']
    gan = gan_zhi[0]  # 大运天干
    zhi = gan_zhi[1]  # 大运地支
    age_range = dayun['age_range']
    gan_shen = dayun.get('gan_shen', calculate_shishen(day_master, gan))  # 天干十神
    zhi_shen = dayun.get('zhi_shen', calculate_shishen(day_master, zhi))  # 地支十神
    element = get_element(gan)  # 大运五行
    nayin = dayun.get('nayin', '')  # 大运纳音
    
    # 分析大运与日主的关系
    relation_with_day_master = analyze_relation(element, day_master_element)
    
    # 分析大运与用神的关系
    relation_with_yong_shen = analyze_relation(element, yong_shen)
    
    # 吉凶评分（考虑流年和神煞）
    score = calculate_dayun_score(relation_with_day_master, relation_with_yong_shen, 
                                 day_master_strength, gan_shen, zhi_shen, flow_year_element)
    
    # 生活领域影响（含健康）
    impacts = analyze_impacts(gan, zhi, gan_shen, score, gender_code, shensha_data, 
                            day_master_element, day_master_strength, flow_year_element)
    
    # 处理建议
    advice = generate_advice(score, impacts, day_master_strength, relation_with_yong_shen, details_level)
    
    # 区间描述
    description = generate_description(gan_zhi, gan_shen, zhi_shen, element, score, impacts, details_level)
    
    return {
        "ganzhi": gan_zhi,
        "age_range": age_range,
        "gan_shen": gan_shen,
        "zhi_shen": zhi_shen,
        "element": element,
        "nayin": nayin,
        "score": score,
        "luck_level": translate_score_to_luck(score),
        "relation_with_day_master": relation_with_day_master,
        "relation_with_yong_shen": relation_with_yong_shen,
        "impacts": impacts,
        "description": description,
        "advice": advice
    }

def analyze_relation(element1, element2):
    """分析五行生克关系"""
    relations = {
        "wood": {"wood": "比助", "fire": "生", "earth": "克", "metal": "被克", "water": "被生"},
        "fire": {"wood": "被生", "fire": "比助", "earth": "生", "metal": "克", "water": "被克"},
        "earth": {"wood": "被克", "fire": "被生", "earth": "比助", "metal": "生", "water": "克"},
        "metal": {"wood": "克", "fire": "被克", "earth": "被生", "metal": "比助", "water": "生"},
        "water": {"wood": "生", "fire": "克", "earth": "被克", "metal": "被生", "water": "比助"}
    }
    return relations.get(element1, {}).get(element2, "未知")

def calculate_dayun_score(relation_dm, relation_ys, strength, gan_shen, zhi_shen, flow_year_element):
    """计算大运评分，考虑流年"""
    score = 0
    if relation_dm in ["生", "比助"]:
        score += 3 if strength in ["弱", "偏弱"] else 1
    elif relation_dm == "克":
        score -= 3 if strength in ["弱", "偏弱"] else -1
    if relation_ys in ["生", "比助"]:
        score += 2
    elif relation_ys == "克":
        score -= 2
    if gan_shen in ["正官", "七杀"]:
        score -= 2 if strength in ["弱", "偏弱"] else 1
    elif gan_shen in ["正印", "偏印"]:
        score += 2 if strength in ["弱", "偏弱"] else 1
    if flow_year_element and flow_year_element == get_element(gan_shen):
        score += 1  # 流年增强大运
    return max(-5, min(5, score))

def translate_score_to_luck(score):
    """评分转吉凶"""
    if score >= 4: return "上吉"
    elif score >= 2: return "吉"
    elif score >= 0: return "平"
    elif score >= -2: return "凶"
    else: return "大凶"

def analyze_impacts(gan, zhi, gan_shen, score, gender_code, shensha_data, day_master_element, 
                   day_master_strength, flow_year_element):
    """分析大运影响，含健康和神煞"""
    impacts = {"health": [], "wealth": [], "career": [], "relationship": []}
    gan_element = get_element(gan)
    
    # 健康影响（结合神煞和五行）
    health_map = {
        "wood": ["肝火旺", "慢性疼痛"] if score < 0 else ["肝胆健康"],
        "fire": ["高血压", "糖尿病并发心血管"] if score < 0 else ["心脏健康"],
        "earth": ["肥胖", "脾虚"] if score < 0 else ["消化良好"],
        "metal": ["慢性疼痛", "肺病"] if score < 0 else ["呼吸顺畅"],
        "water": ["肾虚", "疫苗后遗症疲劳"] if score < 0 else ["肾气足"]
    }
    impacts["health"] = health_map.get(gan_element, [])
    
    # 神煞影响
    shensha_list = [s for s in shensha_data["positive"] if shensha_data["positive"][s]["element"] == gan_element] + \
                   [s for s in shensha_data["negative"] if shensha_data["negative"][s]["element"] == gan_element]
    for shensha in shensha_list:
        data = shensha_data["positive"].get(shensha, shensha_data["negative"].get(shensha))
        aspects = data["health_aspects"]["day_master_" + ("strong" if "旺" in strength else "weak" if "弱" in strength else "neutral")]
        if flow_year_element in data.get("flow_year_boost", []):
            aspects = [f"{a} (流年增强)" for a in aspects]
        impacts["health"].extend(aspects)
    
    # 其他领域
    if gan_shen in ["正财", "偏财"]:
        impacts["wealth"] = ["财运佳"] if score > 0 else ["财务压力"]
    if gan_shen in ["正官", "七杀"]:
        impacts["career"] = ["竞争加剧"] if score < 0 else ["事业稳步"]
    impacts["relationship"] = ["感情稳定"] if score > 0 else ["波折较多"]
    
    return impacts

def generate_advice(score, impacts, day_master_strength, relation_with_yong_shen, details_level):
    """生成大运建议"""
    advice = []
    if score < 0:
        advice.append("大运不利，注意健康和财务风险")
        if "health" in impacts:
            advice.extend([f"调理{h}：按足三里，喝山楂茶" for h in impacts["health"] if "慢性疼痛" in h or "肥胖" in h])
            advice.extend([f"调理{h}：按太溪穴，吃黑豆" for h in impacts["health"] if "肾虚" in h])
    else:
        advice.append("大运平稳，可稳步发展")
    return advice if details_level > 1 else [advice[0]]

def generate_description(gan_zhi, gan_shen, zhi_shen, element, score, impacts, details_level):
    """生成大运描述"""
    desc = f"{gan_zhi}大运，五行{element}，天干十神{gan_shen}，地支十神{zhi_shen}，评分{score}。"
    if details_level > 1:
        desc += " 影响：" + "; ".join([f"{k}: {', '.join(v)}" for k, v in impacts.items()])
    return desc

def generate_dayun_summary(dayuns, day_master_strength, yong_shen):
    """大运总结"""
    avg_score = sum(d['score'] for d in dayuns) / len(dayuns)
    best = max(dayuns, key=lambda x: x['score'])
    worst = min(dayuns, key=lambda x: x['score'])
    return f"整体运势{'吉' if avg_score > 0 else '凶'}，最佳{best['ganzhi']}({best['age_range']})，最差{worst['ganzhi']}({worst['age_range']})。"

def identify_key_periods(dayuns, day_master_element):
    """关键时期"""
    return [{"age_range": d['age_range'], "type": "高峰" if d['score'] > 2 else "低谷", 
             "description": f"{d['ganzhi']}运势{d['luck_level']}"} for d in dayuns if abs(d['score']) > 2]

def analyze_life_stages(dayuns):
    """人生阶段"""
    stages = []
    for i, stage in enumerate([dayuns[:2], dayuns[2:5], dayuns[5:]], 1):
        if stage:
            avg = sum(d['score'] for d in stage) / len(stage)
            stages.append({"stage": ["早年", "中年", "晚年"][i-1], "score": avg, 
                          "description": f"{'顺利' if avg > 0 else '挑战'}"})
    return stages

def get_element(char):
    """获取五行"""
    gan_elements = {"甲": "wood", "乙": "wood", "丙": "fire", "丁": "fire", "戊": "earth", 
                    "己": "earth", "庚": "metal", "辛": "metal", "壬": "water", "癸": "water"}
    zhi_elements = {"寅": "wood", "卯": "wood", "巳": "fire", "午": "fire", "辰": "earth", 
                    "戌": "earth", "丑": "earth", "未": "earth", "申": "metal", "酉": "metal", 
                    "亥": "water", "子": "water"}
    return gan_elements.get(char, zhi_elements.get(char, ""))

def calculate_shishen(day_master, char):
    """计算十神（简化版）"""
    shi_shen = {
        "甲": {"甲": "比肩", "丙": "食神", "戊": "偏财", "庚": "七杀", "壬": "偏印"},
        "丙": {"丙": "比肩", "戊": "食神", "庚": "偏财", "壬": "七杀", "甲": "偏印"}
    }  # 完整表太长，简化示例
    return shi_shen.get(day_master, {}).get(char, "未知")

def calculate_ganzhi(year):
    """计算流年干支"""
    Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    gan_index = (year - 1984) % 10
    zhi_index = (year - 1984) % 12
    return Gan[gan_index] + Zhi[zhi_index]

if __name__ == "__main__":
    test_report = {
        'basic_info': {'day_master': '甲 (wood)'},
        'pattern_analysis': {'day_master_strength': '旺', 'yong_shen': '水'},
        'dayun_analysis': [
            {'ganzhi': '丙寅', 'age_range': '6-15', 'element': 'fire', 'nayin': '炉中火'},
            {'ganzhi': '丁卯', 'age_range': '16-25', 'element': 'fire', 'nayin': '炉中火'},
            {'ganzhi': '戊辰', 'age_range': '26-35', 'element': 'earth', 'nayin': '大林木'},
            {'ganzhi': '己巳', 'age_range': '36-45', 'element': 'earth', 'nayin': '大林木'},
            {'ganzhi': '庚午', 'age_range': '46-55', 'element': 'metal', 'nayin': '路旁土'}
        ]
    }
    result = analyze_dayun(test_report, flow_year=2025, details_level=2)
    print("大运分析结果：")
    print(f"总结: {result['summary']}")
    print("关键时期:", result['key_periods'])
    print("人生阶段:", result['life_stages'])
    for d in result['dayuns']:
        print(f"{d['ganzhi']} ({d['age_range']}): {d['description']}, 建议: {d['advice']}")