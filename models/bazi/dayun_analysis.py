#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大运流年分析模块 - 提供更详细的大运流年分析
"""

from collections import defaultdict

def analyze_dayun(report, gender_code=1, details_level=1):
    """
    分析大运信息，提供更详细的大运走势分析
    
    参数:
        report (dict): 八字命盘报告
        gender_code (int): 性别代码，1为男，0为女
        details_level (int): 详细程度，1-简要，2-中等，3-详细
    
    返回:
        dict: 大运分析结果
    """
    if not report or 'dayun_analysis' not in report:
        return {"error": "报告数据不完整，无法分析大运"}
    
    dayuns = report.get('dayun_analysis', [])
    if not dayuns:
        return {"error": "未找到大运数据"}
    
    # 基本信息
    day_master = report['basic_info']['day_master'].split()[0]  # 提取日主天干
    day_master_element = report['basic_info']['day_master'].split('(')[1].strip(')')  # 提取日主五行属性
    day_master_strength = report['pattern_analysis']['day_master_strength']  # 日主强度
    yong_shen = report['pattern_analysis'].get('yong_shen', '').split()[0]  # 用神
    
    # 分析结果
    result = {
        "summary": "大运总体走势分析",
        "dayuns": [],
        "key_periods": [],
        "life_stages": []
    }
    
    # 分析每个大运
    for i, dayun in enumerate(dayuns):
        dayun_analysis = analyze_single_dayun(dayun, day_master, day_master_element, 
                                           day_master_strength, yong_shen, gender_code, details_level)
        result["dayuns"].append(dayun_analysis)
    
    # 总体分析和关键时期
    result["summary"] = generate_dayun_summary(result["dayuns"], day_master_strength, yong_shen)
    result["key_periods"] = identify_key_periods(result["dayuns"], day_master_element)
    result["life_stages"] = analyze_life_stages(result["dayuns"])
    
    return result

def analyze_single_dayun(dayun, day_master, day_master_element, day_master_strength, yong_shen, gender_code, details_level):
    """
    分析单个大运的吉凶和影响
    """
    gan_zhi = dayun['ganzhi']
    gan = gan_zhi[0]  # 大运天干
    zhi = gan_zhi[1]  # 大运地支
    age_range = dayun['age_range']
    gan_shen = dayun.get('gan_shen', '')  # 天干十神
    zhi_shen = dayun.get('zhi_shen', '')  # 地支十神
    element = dayun.get('element', '')  # 大运五行
    nayin = dayun.get('nayin', '')  # 大运纳音
    
    # 分析大运与日主的关系
    relation_with_day_master = analyze_relation(element, day_master_element)
    
    # 分析大运与用神的关系
    relation_with_yong_shen = analyze_relation(element, yong_shen)
    
    # 吉凶评分（简化版）-5到5分制
    score = calculate_dayun_score(relation_with_day_master, relation_with_yong_shen, 
                                day_master_strength, gan_shen, zhi_shen)
    
    # 生活领域影响
    impacts = analyze_impacts(gan, zhi, gan_shen, score, gender_code)
    
    # 处理建议（根据详细程度）
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
    """分析两个五行元素之间的关系"""
    if not element1 or not element2:
        return "未知"
    
    # 五行相生关系
    generating_relations = {
        "木": "水", "火": "木", "土": "火", "金": "土", "水": "金"
    }
    
    # 五行相克关系
    controlling_relations = {
        "木": "土", "火": "金", "土": "水", "金": "木", "水": "火"
    }
    
    if element1 == element2:
        return "比劫"
    elif generating_relations.get(element1) == element2:
        return "生"
    elif generating_relations.get(element2) == element1:
        return "被生"
    elif controlling_relations.get(element1) == element2:
        return "克"
    elif controlling_relations.get(element2) == element1:
        return "被克"
    else:
        return "中和"

def calculate_dayun_score(relation_with_day_master, relation_with_yong_shen, day_master_strength, gan_shen, zhi_shen):
    """计算大运吉凶评分"""
    score = 0
    
    # 根据与日主的关系
    if relation_with_day_master == "比劫":
        score += 1 if day_master_strength in ["旺", "偏旺"] else 3
    elif relation_with_day_master == "生":
        score += 3 if day_master_strength in ["弱", "偏弱"] else 1
    elif relation_with_day_master == "被生":
        score += -1 if day_master_strength in ["旺", "偏旺"] else 1
    elif relation_with_day_master == "克":
        score += -3 if day_master_strength in ["弱", "偏弱"] else -1
    elif relation_with_day_master == "被克":
        score += -1 if day_master_strength in ["旺", "偏旺"] else -3
    
    # 根据与用神的关系
    if relation_with_yong_shen == "比劫":
        score += 2
    elif relation_with_yong_shen == "生":
        score += 3
    elif relation_with_yong_shen == "被生":
        score += 1
    elif relation_with_yong_shen == "克":
        score += -3
    elif relation_with_yong_shen == "被克":
        score += -2
    
    # 根据十神关系调整
    if gan_shen in ["正印", "偏印"]:
        score += 2 if day_master_strength in ["弱", "偏弱"] else 1
    elif gan_shen in ["正官", "七杀"]:
        score += 2 if day_master_strength in ["旺", "偏旺"] else -2
    elif gan_shen in ["正财", "偏财"]:
        score += 1 if day_master_strength in ["旺", "偏旺"] else 2
    elif gan_shen in ["食神", "伤官"]:
        score += 1
    elif gan_shen in ["比肩", "劫财"]:
        score += 1 if day_master_strength in ["弱", "偏弱"] else -1
    
    # 确保分数在-5到5之间
    return max(-5, min(5, score))

def translate_score_to_luck(score):
    """将分数转换为吉凶级别"""
    if score >= 4:
        return "上吉"
    elif score >= 2:
        return "吉"
    elif score >= 0:
        return "平"
    elif score >= -2:
        return "凶"
    else:
        return "大凶"

def analyze_impacts(gan, zhi, gan_shen, score, gender_code):
    """分析大运对各个生活领域的影响"""
    impacts = {}
    
    # 基于天干地支的五行属性分析各领域
    gan_element = get_element(gan)
    zhi_element = get_element(zhi)
    
    # 事业影响
    if gan_element in ["木", "火"]:
        impacts["career"] = "积极进取" if score > 0 else "变动较大"
    elif gan_element in ["金", "水"]:
        impacts["career"] = "稳步发展" if score > 0 else "挑战较多"
    else:  # 土
        impacts["career"] = "稳定成长" if score > 0 else "需要调整"
    
    # 财运影响
    if gan_shen in ["正财", "偏财"]:
        impacts["wealth"] = "财运良好" if score > 0 else "财务压力"
    elif gan_shen in ["食神", "伤官"]:
        impacts["wealth"] = "创业有利" if score > 0 else "投资谨慎"
    else:
        impacts["wealth"] = "正常收入" if score > 0 else "需开源节流"
    
    # 健康影响
    health_element = {"木": "肝胆", "火": "心脏", "土": "消化系统", "金": "肺部", "水": "肾脏"}
    impacts["health"] = f"注意{health_element.get(gan_element, '')}健康" if score < 0 else "健康状况良好"
    
    # 感情影响（根据性别不同）
    if gender_code == 1:  # 男性
        if gan_shen in ["正财", "偏财"]:
            impacts["relationship"] = "桃花运旺" if score > 0 else "感情波折"
        else:
            impacts["relationship"] = "感情稳定" if score > 0 else "易有变化"
    else:  # 女性
        if gan_shen in ["正官", "七杀"]:
            impacts["relationship"] = "感情幸福" if score > 0 else "婚姻压力"
        else:
            impacts["relationship"] = "家庭和谐" if score > 0 else "关系紧张"
    
    return impacts

def generate_advice(score, impacts, day_master_strength, relation_with_yong_shen, details_level):
    """根据分析生成建议"""
    advice = []
    
    # 基础建议
    if score >= 3:
        advice.append("此大运整体较为有利，可积极进取，把握机会。")
    elif score >= 0:
        advice.append("此大运平稳，维持现状为宜，可稳健发展。")
    else:
        advice.append("此大运有一定阻力，宜低调行事，避免冒险。")
    
    # 领域建议
    if "career" in impacts:
        if "变动" in impacts["career"] or "挑战" in impacts["career"]:
            advice.append("事业方面：避免频繁跳槽，稳定为主。")
        elif "积极" in impacts["career"] or "发展" in impacts["career"]:
            advice.append("事业方面：可适当主动求变，争取晋升机会。")
    
    if "wealth" in impacts:
        if "压力" in impacts["wealth"] or "谨慎" in impacts["wealth"]:
            advice.append("财务方面：控制支出，避免大额投资和不必要消费。")
        elif "良好" in impacts["wealth"] or "有利" in impacts["wealth"]:
            advice.append("财务方面：可适度投资，但保持合理资产配置。")
    
    if "health" in impacts and "注意" in impacts["health"]:
        advice.append(f"健康方面：{impacts['health']}，保持规律作息。")
    
    if "relationship" in impacts and ("波折" in impacts["relationship"] or "压力" in impacts["relationship"]):
        advice.append("感情方面：耐心沟通，避免冲动决策。")
    
    # 根据与用神关系的建议
    if relation_with_yong_shen in ["克", "被克"]:
        advice.append("此运与用神相冲，宜谨慎行事，避免大起大落。")
    elif relation_with_yong_shen in ["生", "比劫"]:
        advice.append("此运有利于用神发展，可把握机会积极进取。")
    
    # 根据详细程度返回建议
    if details_level == 1:
        return advice[0]
    elif details_level == 2:
        return " ".join(advice[:2])
    else:
        return " ".join(advice)

def generate_description(gan_zhi, gan_shen, zhi_shen, element, score, impacts, details_level):
    """生成大运描述"""
    descriptions = []
    
    # 基础描述
    base_desc = f"{gan_zhi}大运，五行属{element}，天干十神为{gan_shen}，地支十神为{zhi_shen}。"
    descriptions.append(base_desc)
    
    # 根据吉凶评分添加描述
    if score >= 4:
        descriptions.append("此运为大运中的高峰期，诸事顺利，易有重大突破。")
    elif score >= 2:
        descriptions.append("此运较为顺遂，能稳步发展，适合稳扎稳打。")
    elif score >= 0:
        descriptions.append("此运平平，无明显波动，宜守成不宜大动。")
    elif score >= -2:
        descriptions.append("此运有一定阻力，需谨慎行事，防止损失。")
    else:
        descriptions.append("此运较为艰难，多有波折，需低调度过。")
    
    # 领域描述
    area_desc = []
    for area, impact in impacts.items():
        if area == "career":
            area_desc.append(f"事业: {impact}")
        elif area == "wealth":
            area_desc.append(f"财运: {impact}")
        elif area == "health":
            area_desc.append(f"健康: {impact}")
        elif area == "relationship":
            area_desc.append(f"感情: {impact}")
    
    # 根据详细程度返回描述
    if details_level == 1:
        return descriptions[0]
    elif details_level == 2:
        return descriptions[0] + " " + descriptions[1]
    else:
        return descriptions[0] + " " + descriptions[1] + " " + "；".join(area_desc)

def generate_dayun_summary(dayuns, day_master_strength, yong_shen):
    """生成大运总体走势分析"""
    if not dayuns:
        return "无法生成大运总体分析"
    
    # 找出最好和最差的大运
    best_dayun = max(dayuns, key=lambda x: x['score'])
    worst_dayun = min(dayuns, key=lambda x: x['score'])
    
    # 计算平均分数
    avg_score = sum(d['score'] for d in dayuns) / len(dayuns)
    
    # 生成总体描述
    if avg_score >= 2:
        summary = "命主大运整体向好，人生发展较为顺利。"
    elif avg_score >= 0:
        summary = "命主大运平稳，起伏不大，可稳步发展。"
    else:
        summary = "命主大运有一定挑战，需谨慎应对，避免大起大落。"
    
    # 添加最好/最差大运信息
    summary += f" 其中{best_dayun['ganzhi']}大运({best_dayun['age_range']})为相对高峰期，"
    summary += f"而{worst_dayun['ganzhi']}大运({worst_dayun['age_range']})则需特别留意。"
    
    # 根据日主强弱和用神给出建议
    if day_master_strength in ["旺", "偏旺"]:
        summary += f" 日主偏强，大运中应注重用神{yong_shen}的调节作用，避免刚强过盛。"
    elif day_master_strength in ["弱", "偏弱"]:
        summary += f" 日主偏弱，大运中应寻求用神{yong_shen}的支持，以增强自身力量。"
    else:
        summary += f" 日主中和，大运中保持平衡发展为宜，用神{yong_shen}可助力成长。"
    
    return summary

def identify_key_periods(dayuns, day_master_element):
    """识别人生关键时期"""
    if not dayuns:
        return []
    
    key_periods = []
    
    # 找出转折点（评分变化明显的大运交接处）
    for i in range(1, len(dayuns)):
        score_change = dayuns[i]['score'] - dayuns[i-1]['score']
        if abs(score_change) >= 3:
            direction = "上升" if score_change > 0 else "下降"
            key_periods.append({
                "age": dayuns[i]['age_range'].split('-')[0],
                "type": f"运势{direction}",
                "description": f"{dayuns[i-1]['ganzhi']}大运进入{dayuns[i]['ganzhi']}大运，人生轨迹有明显{direction}。"
            })
    
    # 找出特别吉利或凶险的大运
    for dayun in dayuns:
        if dayun['score'] >= 4:
            key_periods.append({
                "age_range": dayun['age_range'],
                "type": "高峰期",
                "description": f"{dayun['ganzhi']}大运为人生高峰期，各方面发展顺利，可积极进取。"
            })
        elif dayun['score'] <= -4:
            key_periods.append({
                "age_range": dayun['age_range'],
                "type": "低谷期",
                "description": f"{dayun['ganzhi']}大运为人生挑战期，需谨慎应对，避免重大决策。"
            })
    
    # 分析与日主五行相生相克的大运对应的人生阶段
    for dayun in dayuns:
        if dayun['relation_with_day_master'] == "生" and dayun['score'] > 0:
            key_periods.append({
                "age_range": dayun['age_range'],
                "type": "成长期",
                "description": f"{dayun['ganzhi']}大运五行生助日主，为个人成长和能力发展的重要阶段。"
            })
        elif dayun['relation_with_day_master'] == "克" and dayun['score'] < 0:
            key_periods.append({
                "age_range": dayun['age_range'],
                "type": "调整期",
                "description": f"{dayun['ganzhi']}大运五行克制日主，为人生调整和转型的关键时期。"
            })
    
    return key_periods

def analyze_life_stages(dayuns):
    """分析人生阶段发展趋势"""
    if len(dayuns) < 3:
        return []
    
    # 将大运分为几个阶段
    early_stage = dayuns[:2]  # 早年
    middle_stage = dayuns[2:5]  # 中年
    late_stage = dayuns[5:]  # 晚年
    
    stages = []
    
    # 分析早年
    early_avg = sum(d['score'] for d in early_stage) / len(early_stage)
    if early_avg >= 2:
        early_desc = "早年运势较好，起步顺利，基础牢固。"
    elif early_avg >= 0:
        early_desc = "早年运势平稳，发展稳健，打下基础。"
    else:
        early_desc = "早年运势较弱，起步艰难，需努力奋斗。"
    
    stages.append({
        "stage": "早年",
        "score": early_avg,
        "description": early_desc
    })
    
    # 分析中年
    if middle_stage:
        middle_avg = sum(d['score'] for d in middle_stage) / len(middle_stage)
        if middle_avg >= 2:
            middle_desc = "中年事业有成，发展迅速，是人生巅峰期。"
        elif middle_avg >= 0:
            middle_desc = "中年发展平稳，事业逐步成型，家庭趋于稳定。"
        else:
            middle_desc = "中年面临挑战，需调整方向，重新规划未来。"
        
        stages.append({
            "stage": "中年",
            "score": middle_avg,
            "description": middle_desc
        })
    
    # 分析晚年
    if late_stage:
        late_avg = sum(d['score'] for d in late_stage) / len(late_stage)
        if late_avg >= 2:
            late_desc = "晚年福寿双全，享受成果，生活安康。"
        elif late_avg >= 0:
            late_desc = "晚年生活平稳，家庭和睦，安享晚年。"
        else:
            late_desc = "晚年需注意健康，避免奔波，保持心态平和。"
        
        stages.append({
            "stage": "晚年",
            "score": late_avg,
            "description": late_desc
        })
    
    return stages

def get_element(char):
    """获取天干或地支的五行属性"""
    # 天干五行
    gan_5_elements = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }
    
    # 地支五行（主气）
    zhi_5_elements = {
        "寅": "木", "卯": "木",
        "巳": "火", "午": "火",
        "辰": "土", "戌": "土", "丑": "土", "未": "土",
        "申": "金", "酉": "金",
        "亥": "水", "子": "水"
    }
    
    # 优先检查天干
    if char in gan_5_elements:
        return gan_5_elements[char]
    # 然后检查地支
    elif char in zhi_5_elements:
        return zhi_5_elements[char]
    else:
        return ""

# 测试代码
if __name__ == "__main__":
    # 创建一个测试样例
    test_report = {
        'basic_info': {
            'day_master': '甲(木)',
            'gans': '甲 乙 丙 丁',
            'zhis': '子 丑 寅 卯',
        },
        'pattern_analysis': {
            'day_master_strength': '中和',
            'day_master_percentage': 25.0,
            'yong_shen': '火 (生身)'
        },
        'dayun_analysis': [
            {
                'ganzhi': '丙寅',
                'age_range': '6-15',
                'gan_shen': '食神',
                'zhi_shen': '比肩',
                'element': '火',
                'nayin': '炉中火'
            },
            {
                'ganzhi': '丁卯',
                'age_range': '16-25',
                'gan_shen': '伤官',
                'zhi_shen': '劫财',
                'element': '火',
                'nayin': '炉中火'
            },
            {
                'ganzhi': '戊辰',
                'age_range': '26-35',
                'gan_shen': '偏财',
                'zhi_shen': '财',
                'element': '土',
                'nayin': '大林木'
            }
        ]
    }
    
    # 分析大运
    result = analyze_dayun(test_report)
    
    # 打印结果
    print("大运总体分析:", result["summary"])
    print("\n关键时期:")
    for period in result["key_periods"]:
        print(f"- {period['type']} ({period['age_range']}): {period['description']}")
    
    print("\n人生阶段:")
    for stage in result["life_stages"]:
        print(f"- {stage['stage']} (评分: {stage['score']:.1f}): {stage['description']}")
    
    print("\n各大运详细分析:")
    for i, dayun in enumerate(result["dayuns"]):
        print(f"\n大运 {i+1}: {dayun['ganzhi']} ({dayun['age_range']})")
        print(f"五行: {dayun['element']}, 纳音: {dayun['nayin']}")
        print(f"天干十神: {dayun['gan_shen']}, 地支十神: {dayun['zhi_shen']}")
        print(f"吉凶评分: {dayun['score']} ({dayun['luck_level']})")
        print(f"描述: {dayun['description']}")
        print(f"建议: {dayun['advice']}")
