#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
流年分析模块 - 提供详细的流年运势分析，包括健康影响
"""

from datetime import datetime
from .calculator import get_element  # 假设calculator.py有get_element函数

def analyze_liunian(report, year=None, details_level=1):
    """
    分析指定年份或当前年份的流年运势
    
    参数:
        report (dict): 八字命盘报告
        year (int, optional): 要分析的年份，默认为当前年份
        details_level (int): 详细程度，1-简要，2-中等，3-详细
        
    返回:
        dict: 流年分析结果
    """
    if not report:
        return {"error": "报告数据不完整，无法分析流年"}
    
    # 使用指定年份或当前年份
    if year is None:
        year = datetime.now().year
    
    # 基本信息
    day_master = report['basic_info']['day_master'].split()[0]  # 日主天干
    day_master_element = report['basic_info']['day_master'].split('(')[1].strip(')')  # 日主五行
    day_master_strength = report['pattern_analysis']['day_master_strength']  # 日主强度
    yong_shen = report['pattern_analysis'].get('yong_shen', '').split()[0]  # 用神
    
    # 获取当前大运信息
    current_dayun = report.get('current_dayun', None)
    
    # 获取流年干支信息
    liunian_ganzhi = calculate_liunian_ganzhi(year)
    liunian_gan = liunian_ganzhi[0]  # 流年天干
    liunian_zhi = liunian_ganzhi[1]  # 流年地支
    
    # 计算十神信息
    gan_shen = calculate_shishen(day_master, liunian_gan)  # 流年天干十神
    zhi_shen = calculate_shishen(day_master, liunian_zhi)  # 流年地支十神（简化）
    
    # 分析流年五行
    liunian_element = get_element(liunian_gan)  # 流年天干五行
    
    # 分析流年与日主的关系
    relation_with_day_master = analyze_relation(liunian_element, day_master_element)
    
    # 分析流年与用神的关系
    relation_with_yong_shen = analyze_relation(liunian_element, yong_shen)
    
    # 分析大运与流年的关系
    dayun_liunian_relation = ""
    if current_dayun:
        dayun_gan = current_dayun['ganzhi'][0]
        dayun_element = get_element(dayun_gan)
        dayun_liunian_relation = analyze_relation(dayun_element, liunian_element)
    
    # 计算流年运势评分
    score = calculate_liunian_score(
        relation_with_day_master, 
        relation_with_yong_shen, 
        dayun_liunian_relation,
        day_master_strength, 
        gan_shen
    )
    
    # 分析流年的生活领域影响（含健康）
    impacts = analyze_liunian_impacts(liunian_gan, liunian_zhi, gan_shen, score)
    
    # 生成流年运势描述
    description = generate_liunian_description(
        year, liunian_ganzhi, gan_shen, zhi_shen, liunian_element, score, impacts, details_level
    )
    
    # 生成流年建议
    advice = generate_liunian_advice(
        score, impacts, relation_with_day_master, relation_with_yong_shen, day_master_strength, details_level
    )
    
    # 分析流月运势
    months_analysis = []
    if details_level >= 2:
        months_analysis = analyze_liuyue(
            year, liunian_ganzhi, day_master, day_master_element, yong_shen, score
        )
    
    # 分析重要时期
    key_periods = identify_key_periods(
        year, liunian_ganzhi, day_master, impacts, score, months_analysis
    )
    
    return {
        "year": year,
        "ganzhi": liunian_ganzhi,
        "gan_shen": gan_shen,
        "zhi_shen": zhi_shen,
        "element": liunian_element,
        "score": score,
        "luck_level": translate_score_to_luck(score),
        "relation_with_day_master": relation_with_day_master,
        "relation_with_yong_shen": relation_with_yong_shen,
        "dayun_liunian_relation": dayun_liunian_relation,
        "impacts": impacts,
        "description": description,
        "advice": advice,
        "key_periods": key_periods,
        "months": months_analysis if details_level >= 2 else []
    }

def calculate_liunian_ganzhi(year):
    """计算指定年份的干支"""
    Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    gan_index = (year - 1984) % 10
    zhi_index = (year - 1984) % 12
    if gan_index < 0:
        gan_index += 10
    if zhi_index < 0:
        zhi_index += 12
    return Gan[gan_index] + Zhi[zhi_index]

def calculate_shishen(day_master, char):
    """计算十神关系"""
    shi_shen_table = {
        '甲': {'甲': '比肩', '乙': '劫财', '丙': '食神', '丁': '伤官', '戊': '偏财', 
               '己': '正财', '庚': '七杀', '辛': '正官', '壬': '偏印', '癸': '正印',
               '寅': '比肩', '卯': '劫财', '巳': '食神', '午': '伤官', '辰': '偏财', 
               '戌': '正财', '申': '七杀', '酉': '正官', '亥': '偏印', '子': '正印'},
        '乙': {'甲': '劫财', '乙': '比肩', '丙': '伤官', '丁': '食神', '戊': '正财', 
               '己': '偏财', '庚': '正官', '辛': '七杀', '壬': '正印', '癸': '偏印',
               '寅': '劫财', '卯': '比肩', '巳': '伤官', '午': '食神', '辰': '正财', 
               '戌': '偏财', '申': '正官', '酉': '七杀', '亥': '正印', '子': '偏印'},
        '丙': {'甲': '偏印', '乙': '正印', '丙': '比肩', '丁': '劫财', '戊': '食神', 
               '己': '伤官', '庚': '偏财', '辛': '正财', '壬': '七杀', '癸': '正官',
               '寅': '偏印', '卯': '正印', '巳': '比肩', '午': '劫财', '辰': '食神', 
               '戌': '伤官', '申': '偏财', '酉': '正财', '亥': '七杀', '子': '正官'},
        '丁': {'甲': '正印', '乙': '偏印', '丙': '劫财', '丁': '比肩', '戊': '伤官', 
               '己': '食神', '庚': '正财', '辛': '偏财', '壬': '正官', '癸': '七杀',
               '寅': '正印', '卯': '偏印', '巳': '劫财', '午': '比肩', '辰': '伤官', 
               '戌': '食神', '申': '正财', '酉': '偏财', '亥': '正官', '子': '七杀'},
        '戊': {'甲': '七杀', '乙': '正官', '丙': '偏印', '丁': '正印', '戊': '比肩', 
               '己': '劫财', '庚': '食神', '辛': '伤官', '壬': '偏财', '癸': '正财',
               '寅': '七杀', '卯': '正官', '巳': '偏印', '午': '正印', '辰': '比肩', 
               '戌': '劫财', '申': '食神', '酉': '伤官', '亥': '偏财', '子': '正财'},
        '己': {'甲': '正官', '乙': '七杀', '丙': '正印', '丁': '偏印', '戊': '劫财', 
               '己': '比肩', '庚': '伤官', '辛': '食神', '壬': '正财', '癸': '偏财',
               '寅': '正官', '卯': '七杀', '巳': '正印', '午': '偏印', '辰': '劫财', 
               '戌': '比肩', '申': '伤官', '酉': '食神', '亥': '正财', '子': '偏财'},
        '庚': {'甲': '偏财', '乙': '正财', '丙': '七杀', '丁': '正官', '戊': '偏印', 
               '己': '正印', '庚': '比肩', '辛': '劫财', '壬': '食神', '癸': '伤官',
               '寅': '偏财', '卯': '正财', '巳': '七杀', '午': '正官', '辰': '偏印', 
               '戌': '正印', '申': '比肩', '酉': '劫财', '亥': '食神', '子': '伤官'},
        '辛': {'甲': '正财', '乙': '偏财', '丙': '正官', '丁': '七杀', '戊': '正印', 
               '己': '偏印', '庚': '劫财', '辛': '比肩', '壬': '伤官', '癸': '食神',
               '寅': '正财', '卯': '偏财', '巳': '正官', '午': '七杀', '辰': '正印', 
               '戌': '偏印', '申': '劫财', '酉': '比肩', '亥': '伤官', '子': '食神'},
        '壬': {'甲': '食神', '乙': '伤官', '丙': '偏财', '丁': '正财', '戊': '七杀', 
               '己': '正官', '庚': '偏印', '辛': '正印', '壬': '比肩', '癸': '劫财',
               '寅': '食神', '卯': '伤官', '巳': '偏财', '午': '正财', '辰': '七杀', 
               '戌': '正官', '申': '偏印', '酉': '正印', '亥': '比肩', '子': '劫财'},
        '癸': {'甲': '伤官', '乙': '食神', '丙': '正财', '丁': '偏财', '戊': '正官', 
               '己': '七杀', '庚': '正印', '辛': '偏印', '壬': '劫财', '癸': '比肩',
               '寅': '伤官', '卯': '食神', '巳': '正财', '午': '偏财', '辰': '正官', 
               '戌': '七杀', '申': '正印', '酉': '偏印', '亥': '劫财', '子': '比肩'}
    }
    return shi_shen_table.get(day_master, {}).get(char, "未知")

def analyze_relation(element1, element2):
    """分析两个五行之间的生克关系"""
    relations = {
        "wood": {"wood": "比助", "fire": "生", "earth": "克", "metal": "被克", "water": "被生"},
        "fire": {"wood": "被生", "fire": "比助", "earth": "生", "metal": "克", "water": "被克"},
        "earth": {"wood": "被克", "fire": "被生", "earth": "比助", "metal": "生", "water": "克"},
        "metal": {"wood": "克", "fire": "被克", "earth": "被生", "metal": "比助", "water": "生"},
        "water": {"wood": "生", "fire": "克", "earth": "被克", "metal": "被生", "water": "比助"}
    }
    return relations.get(element1, {}).get(element2, "未知")

def calculate_liunian_score(relation_dm, relation_ys, relation_dy, strength, gan_shen):
    """计算流年运势评分"""
    score = 50  # 基准分
    if relation_dm in ["生", "比助"]:
        score += 20
    elif relation_dm == "克":
        score -= 20
    if relation_ys in ["生", "比助"]:
        score += 15
    elif relation_ys == "克":
        score -= 15
    if relation_dy in ["生", "比助"]:
        score += 10
    if strength == "旺":
        score += 10
    elif strength == "弱":
        score -= 10
    if gan_shen in ["正官", "七杀"]:
        score -= 10  # 官杀压制
    return max(0, min(100, score))

def analyze_liunian_impacts(liunian_gan, liunian_zhi, gan_shen, score):
    """分析流年对生活领域的影响，包括健康"""
    impacts = {"health": [], "wealth": [], "career": [], "relationship": []}
    if gan_shen in ["七杀", "伤官"]:
        impacts["health"].append("压力大，易慢性疼痛")
        impacts["career"].append("竞争激烈")
    elif gan_shen in ["正财", "偏财"]:
        impacts["wealth"].append("财运佳")
    if score < 40:
        impacts["health"].append("健康下滑，注意脾胃或肾虚")
    return impacts

def generate_liunian_description(year, ganzhi, gan_shen, zhi_shen, element, score, impacts, details_level):
    """生成流年运势描述"""
    base = f"{year}年{ganzhi}，天干十神为{gan_shen}，地支十神为{zhi_shen}，五行{element}。"
    if details_level >= 2:
        base += f" 运势评分{score}，影响领域：{impacts}。"
    return base

def generate_liunian_advice(score, impacts, relation_dm, relation_ys, strength, details_level):
    """生成流年建议"""
    advice = []
    if score < 50:
        advice.append("流年不利，注意健康调理")
        if "health" in impacts and impacts["health"]:
            advice.append("多按足三里，喝山楂茶改善代谢")
    else:
        advice.append("流年顺利，保持现状即可")
    return advice

def analyze_liuyue(year, liunian_ganzhi, day_master, day_master_element, yong_shen, score):
    """简易流月分析"""
    return [{"month": i, "description": f"{year}年{i}月运势平稳"} for i in range(1, 13)]

def identify_key_periods(year, liunian_ganzhi, day_master, impacts, score, months_analysis):
    """识别流年关键时期"""
    return {"peak": f"{year}年中期", "low": f"{year}年下半年"}

def translate_score_to_luck(score):
    """将评分转换为运势等级"""
    if score > 80:
        return "大吉"
    elif score > 60:
        return "吉"
    elif score > 40:
        return "平"
    else:
        return "凶"

if __name__ == "__main__":
    # 测试代码
    test_report = {
        "basic_info": {"day_master": "甲 (wood)"},
        "pattern_analysis": {"day_master_strength": "旺", "yong_shen": "水"},
        "current_dayun": {"ganzhi": "癸亥"}
    }
    result = analyze_liunian(test_report, year=2025, details_level=2)
    print("流年分析结果：")
    for key, value in result.items():
        print(f"{key}: {value}")