def analyze_liuyue(year, liunian_ganzhi, day_master, day_master_element, yong_shen, liunian_score):
    """分析流月运势"""
    months_analysis = []
    
    # 简化月份干支计算规则（实际应更复杂）
    month_ganzhi_base = {
        "甲子": ["丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戎", "乙亥", "丙子", "丁丑"],
        "乙丑": ["戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未", "甲申", "乙酉", "丙戎", "丁亥", "戊子", "己丑"],
        # ... 其他流年干支对应的流月干支
    }
    
    # 使用简化版的流月计算（实际应更准确）
    months_ganzhi = []
    if liunian_ganzhi in month_ganzhi_base:
        months_ganzhi = month_ganzhi_base[liunian_ganzhi]
    else:
        # 简单示例规则，实际应更复杂
        base = ["丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戎", "乙亥", "丙子", "丁丑"]
        months_ganzhi = base
    
    # 分析每个月的运势
    for i, month_ganzhi in enumerate(months_ganzhi):
        month_index = i + 1  # 月份索引（1-12）
        
        # 分析月干支
        month_gan = month_ganzhi[0]
        month_element = get_element(month_gan)
        
        # 计算十神
        month_gan_shen = calculate_shishen(day_master, month_gan)
        
        # 分析与日主关系
        relation = analyze_relation(month_element, day_master_element)
        
        # 计算月份评分（简化）
        month_score = 0
        if relation == "生" and day_master_element != "旺":
            month_score += 1
        elif relation == "克" and day_master_element == "旺":
            month_score += 1
        elif relation == "被克" and day_master_element != "旺":
            month_score -= 1
        
        # 考虑流年影响
        month_score += liunian_score * 0.5  # 流年对流月有一定影响
        
        # 分析重要事件（示例）
        events = []
        if month_score >= 1.5:
            events.append("重要机遇期")
        elif month_score <= -1.5:
            events.append("谨慎应对期")
        
        months_analysis.append({
            "month": month_index,
            "ganzhi": month_ganzhi,
            "gan_shen": month_gan_shen,
            "relation": relation,
            "score": month_score,
            "luck_level": translate_score_to_luck(month_score),
            "events": events,
            "description": generate_liuyue_description(month_index, month_ganzhi, month_gan_shen, month_score)
        })
    
    return months_analysis

def generate_liuyue_description(month, ganzhi, gan_shen, score):
    """生成流月运势描述"""
    month_names = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二"]
    
    if score >= 1.5:
        return f"{month_names[month-1]}月运势较佳，干支为{ganzhi}，十神为{gan_shen}，宜积极进取，主动把握机会。"
    elif score >= 0:
        return f"{month_names[month-1]}月运势平稳，干支为{ganzhi}，十神为{gan_shen}，可稳健发展，保持正常节奏。"
    elif score >= -1.5:
        return f"{month_names[month-1]}月运势略有波动，干支为{ganzhi}，十神为{gan_shen}，宜谨慎行事，不适合重大决策。"
    else:
        return f"{month_names[month-1]}月运势不佳，干支为{ganzhi}，十神为{gan_shen}，需低调处事，避免风险和冲突。"

def identify_key_periods(year, liunian_ganzhi, day_master, impacts, score, months_analysis):
    """识别重要时期"""
    key_periods = []
    
    # 根据整年评分添加关键时期
    if score >= 2:
        key_periods.append({
            "type": "高峰期",
            "period": f"{year}年全年",
            "description": f"{year}年整体运势较好，是发展和把握机遇的重要时期。"
        })
    elif score <= -2:
        key_periods.append({
            "type": "低谷期",
            "period": f"{year}年全年",
            "description": f"{year}年整体运势不佳，需谨慎应对，维持低调。"
        })
    
    # 根据不同领域的影响添加关键时期
    for area, impact in impacts.items():
        if area == "career" and "发展活跃" in impact:
            key_periods.append({
                "type": "事业发展期",
                "period": f"{year}年",
                "description": f"{year}年事业发展机会较多，适合拓展业务和接受新挑战。"
            })
        elif area == "wealth" and "财运良好" in impact:
            key_periods.append({
                "type": "财运丰收期",
                "period": f"{year}年",
                "description": f"{year}年财运较好，适合投资理财和拓展财源。"
            })
        elif (area == "health" and "注意" in impact) or score < -1:
            key_periods.append({
                "type": "健康谨慎期",
                "period": f"{year}年",
                "description": f"{year}年需注意身体健康，加强锻炼，保持良好生活习惯。"
            })
    
    # 根据流月分析添加关键时期
    if months_analysis:
        # 找出最吉利的月份
        best_months = [m for m in months_analysis if m["score"] >= 1.5]
        if best_months:
            months_str = ", ".join([f"{m['month']}月" for m in best_months])
            key_periods.append({
                "type": "月度高峰期",
                "period": months_str,
                "description": f"{months_str}为全年运势最好的时期，适合重要决策和关键行动。"
            })
        
        # 找出最不利的月份
        worst_months = [m for m in months_analysis if m["score"] <= -1.5]
        if worst_months:
            months_str = ", ".join([f"{m['month']}月" for m in worst_months])
            key_periods.append({
                "type": "月度低谷期",
                "period": months_str,
                "description": f"{months_str}运势较差，宜低调处事，避免重大决策和决策。"
            })
    
    # 根据干支关系分析足够重要的月份（如天克地冲）
    # 这里可以根据干支的知识进行更详细的分析
    
    return key_periods

# 测试代码
if __name__ == "__main__":
    # 测试流年分析功能
    from datetime import datetime
    
    # 创建一个测试用的假拟命盘报告
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
        'current_dayun': {
            'ganzhi': '丙寅',
            'age_range': '26-35',
        }
    }
    
    # 分析当前年份的流年运势
    result = analyze_liunian(test_report, datetime.now().year)
    
    # 打印分析结果
    print(f"流年: {result['year']}年 {result['ganzhi']}")
    print(f"十神: {result['gan_shen']}({result['zhi_shen']})")
    print(f"吉凶: {result['score']} ({result['luck_level']})")
    print(f"运势描述: {result['description']}")
    print(f"建议: {result['advice']}")
    
    print("\n\u91cd要时期:")
    for period in result["key_periods"]:
        print(f"- {period['type']}({period['period']}): {period['description']}")
    
    if result.get("months"):
        print("\n\u6d41月分析:")
        for month in result["months"]:
            print(f"- {month['month']}月: {month['description']}")#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
流年分析模块 - 提供详细的流年运势分析
"""

from datetime import datetime
from .calculator import get_element

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
    day_master = report['basic_info']['day_master'].split()[0]  # 提取日主天干
    day_master_element = report['basic_info']['day_master'].split('(')[1].strip(')')  # 提取日主五行属性
    day_master_strength = report['pattern_analysis']['day_master_strength']  # 日主强度
    yong_shen = report['pattern_analysis'].get('yong_shen', '').split()[0]  # 用神
    
    # 获取当前大运信息
    current_dayun = report.get('current_dayun', None)
    
    # 获取流年干支信息（这里需要根据年份计算流年干支）
    liunian_ganzhi = calculate_liunian_ganzhi(year)
    liunian_gan = liunian_ganzhi[0]  # 流年天干
    liunian_zhi = liunian_ganzhi[1]  # 流年地支
    
    # 计算十神信息
    gan_shen = calculate_shishen(day_master, liunian_gan)  # 流年天干十神
    zhi_shen = calculate_shishen(day_master, liunian_zhi)  # 流年地支十神（简化处理）
    
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
    
    # 分析流年的生活领域影响
    impacts = analyze_liunian_impacts(liunian_gan, liunian_zhi, gan_shen, score)
    
    # 生成流年运势描述
    description = generate_liunian_description(
        year, 
        liunian_ganzhi, 
        gan_shen, 
        zhi_shen, 
        liunian_element, 
        score, 
        impacts, 
        details_level
    )
    
    # 生成流年建议
    advice = generate_liunian_advice(
        score, 
        impacts, 
        relation_with_day_master, 
        relation_with_yong_shen, 
        day_master_strength, 
        details_level
    )
    
    # 分析流月运势
    months_analysis = []
    if details_level >= 2:  # 中等或详细级别才分析流月
        months_analysis = analyze_liuyue(
            year, 
            liunian_ganzhi, 
            day_master, 
            day_master_element, 
            yong_shen, 
            score
        )
    
    # 分析重要时期
    key_periods = identify_key_periods(
        year, 
        liunian_ganzhi, 
        day_master, 
        impacts, 
        score, 
        months_analysis
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
    """
    计算指定年份的干支
    
    参数:
        year (int): 公历年份
        
    返回:
        str: 干支表示，如"甲子"
    """
    # 天干和地支列表
    Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 计算干支序号（1984年为甲子年）
    gan_index = (year - 1984) % 10
    zhi_index = (year - 1984) % 12
    
    # 校正负数索引
    if gan_index < 0:
        gan_index += 10
    if zhi_index < 0:
        zhi_index += 12
    
    # 返回干支
    return Gan[gan_index] + Zhi[zhi_index]

def calculate_shishen(day_master, char):
    """
    计算天干或地支相对于日主的十神关系
    
    参数:
        day_master (str): 日主天干
        char (str): 要计算的天干或地支
        
    返回:
        str: 十神关系
    """
    # 十神对照表（简化版）
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
    
    # 查找十神关系
    if day_master in shi_shen_table and char in shi_shen_table[day_master]:
        return shi_shen_table[day_master][char]
    return "未知"

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

def calculate_liunian_score(relation_with_day_master, relation_with_yong_shen, 
                           dayun_liunian_relation, day_master_strength, gan_shen):
    """计算流年运势评分"""
    score = 0
    
    # 根据与日主的关系
    if relation_with_day_master == "比劫":
        score += 1 if day_master_strength in ["旺", "偏旺"] else 2
    elif relation_with_day_master == "生":
        score += 2 if day_master_strength in ["弱", "偏弱"] else 1
    elif relation_with_day_master == "被生":
        score += -1 if day_master_strength in ["旺", "偏旺"] else 0
    elif relation_with_day_master == "克":
        score += -2 if day_master_strength in ["弱", "偏弱"] else 0
    elif relation_with_day_master == "被克":
        score += -1 if day_master_strength in ["旺", "偏旺"] else -2
    
    # 根据与用神的关系
    if relation_with_yong_shen == "比劫":
        score += 1
    elif relation_with_yong_shen == "生":
        score += 2
    elif relation_with_yong_shen == "被生":
        score += 1
    elif relation_with_yong_shen == "克":
        score += -2
    elif relation_with_yong_shen == "被克":
        score += -1
    
    # 根据大运流年关系
    if dayun_liunian_relation == "比劫":
        score += 1
    elif dayun_liunian_relation == "生":
        score += 1
    elif dayun_liunian_relation == "被生":
        score += 0
    elif dayun_liunian_relation == "克":
        score += -1
    elif dayun_liunian_relation == "被克":
        score += -1
    
    # 根据十神关系调整
    if gan_shen in ["正印", "偏印"]:
        score += 1 if day_master_strength in ["弱", "偏弱"] else 0
    elif gan_shen in ["正官", "七杀"]:
        score += 1 if day_master_strength in ["旺", "偏旺"] else -1
    elif gan_shen in ["正财", "偏财"]:
        score += 1 if day_master_strength in ["旺", "偏旺"] else 1
    elif gan_shen in ["食神", "伤官"]:
        score += 1
    elif gan_shen in ["比肩", "劫财"]:
        score += 0 if day_master_strength in ["弱", "偏弱"] else -1
    
    # 确保分数在-3到3之间
    return max(-3, min(3, score))

def translate_score_to_luck(score):
    """将分数转换为吉凶级别"""
    if score >= 2:
        return "吉"
    elif score >= 0:
        return "平"
    elif score >= -2:
        return "小凶"
    else:
        return "凶"

def analyze_liunian_impacts(gan, zhi, gan_shen, score):
    """分析流年对各个生活领域的影响"""
    impacts = {}
    
    # 基于天干地支的五行属性分析各领域
    gan_element = get_element(gan)
    
    # 事业影响
    if gan_element in ["木", "火"]:
        impacts["career"] = "发展活跃" if score > 0 else "变动较大"
    elif gan_element in ["金", "水"]:
        impacts["career"] = "稳步前进" if score > 0 else "稳中有阻"
    else:  # 土
        impacts["career"] = "中规中矩" if score > 0 else "进展缓慢"
    
    # 财运影响
    if gan_shen in ["正财", "偏财"]:
        impacts["wealth"] = "财运良好" if score > 0 else "开支增加"
    elif gan_shen in ["食神", "伤官"]:
        impacts["wealth"] = "财源广进" if score > 0 else "投资谨慎"
    elif gan_shen in ["正印", "偏印"]:
        impacts["wealth"] = "稳健增长" if score > 0 else "理财保守"
    else:
        impacts["wealth"] = "收支平衡" if score > 0 else "财务压力"
    
    # 健康影响
    health_element = {"木": "肝胆", "火": "心脏", "土": "脾胃", "金": "肺部", "水": "肾脏"}
    if score < 0:
        impacts["health"] = f"注意{health_element.get(gan_element, '')}健康"
    else:
        impacts["health"] = "整体健康良好"
    
    # 人际关系影响
    if gan_shen in ["比肩", "劫财"]:
        impacts["relationship"] = "人际关系活跃" if score > 0 else "竞争增加"
    elif gan_shen in ["正官", "七杀"]:
        impacts["relationship"] = "社交圈扩大" if score > 0 else "人际关系紧张"
    else:
        impacts["relationship"] = "社交和谐" if score > 0 else "需多关注人际关系"
    
    return impacts

def generate_liunian_description(year, ganzhi, gan_shen, zhi_shen, element, score, impacts, details_level):
    """生成流年运势描述"""
    descriptions = []
    
    # 基础描述
    base_desc = f"{year}年，{ganzhi}年，五行属{element}，天干十神为{gan_shen}，地支十神为{zhi_shen}。"
    descriptions.append(base_desc)
    
    # 根据吉凶评分添加描述
    if score >= 2:
        descriptions.append("今年整体运势较好，是发展的顺利时期。")
    elif score >= 0:
        descriptions.append("今年运势平稳，各方面发展中规中矩。")
    elif score >= -2:
        descriptions.append("今年运势略有波折，需谨慎应对。")
    else:
        descriptions.append("今年运势较为不利，需低调行事，避免风险。")
    
    # 领域描述
    area_desc = []
    for area, impact in impacts.items():
        if area == "career":
            area_desc.append(f"事业方面：{impact}")
        elif area == "wealth":
            area_desc.append(f"财运方面：{impact}")
        elif area == "health":
            area_desc.append(f"健康方面：{impact}")
        elif area == "relationship":
            area_desc.append(f"人际关系：{impact}")
    
    # 根据详细程度返回描述
    if details_level == 1:
        return descriptions[0] + " " + descriptions[1]
    elif details_level == 2:
        return descriptions[0] + " " + descriptions[1] + " " + area_desc[0] + " " + area_desc[1]
    else:
        return descriptions[0] + " " + descriptions[1] + " " + "; ".join(area_desc)

def generate_liunian_advice(score, impacts, relation_with_day_master, relation_with_yong_shen, day_master_strength, details_level):
    """生成流年建议"""
    advice = []
    
    # 基础建议
    if score >= 2:
        advice.append("今年运势良好，可积极推进计划，抓住机遇。")
    elif score >= 0:
        advice.append("今年运势平稳，可稳步发展，适度进取。")
    elif score >= -2:
        advice.append("今年运势有一定阻力，宜稳健为主，避免大的风险。")
    else:
        advice.append("今年运势不佳，宜低调行事，保守发展，减少重大决策。")
    
    # 领域建议
    if "career" in impacts:
        if "变动" in impacts["career"] or "阻" in impacts["career"]:
            advice.append("事业方面：避免频繁换工作，稳定为主，积累经验和人脉。")
        elif "发展" in impacts["career"] or "进" in impacts["career"]:
            advice.append("事业方面：可适当寻求晋升和拓展，接受新的挑战。")
    
    if "wealth" in impacts:
        if "开支" in impacts["wealth"] or "压力" in impacts["wealth"] or "谨慎" in impacts["wealth"]:
            advice.append("财务方面：控制不必要开支，减少大额投资，量入为出。")
        elif "良好" in impacts["wealth"] or "进" in impacts["wealth"]:
            advice.append("财务方面：可适当增加投资，但仍要保持合理资产配置。")
    
    if "health" in impacts and "注意" in impacts["health"]:
        advice.append(f"健康方面：{impacts['health']}，增加锻炼，保持良好作息习惯。")
    
    if "relationship" in impacts and ("竞争" in impacts["relationship"] or "紧张" in impacts["relationship"]):
        advice.append("人际关系：避免正面冲突，多沟通，维护重要人脉。")
    
    # 根据与用神的关系给出建议
    if relation_with_yong_shen in ["克", "被克"]:
        advice.append("用神受损，宜守不宜攻，避免大的变动和冒险。")
    elif relation_with_yong_shen in ["生", "比劫"]:
        advice.append("用神得力，可适度进取，把握机会。")
    
    # 根据日主状态给出建议
    if day_master_strength in ["旺", "偏旺"]:
        if relation_with_day_master == "比劫":
            advice.append("日主旺而逢比劫之年，易冲动，宜控制情绪，谨慎决策。")
        elif relation_with_day_master == "克":
            advice.append("日主旺逢克泄之年，有助平衡，可适度发展。")
    elif day_master_strength in ["弱", "偏弱"]:
        if relation_with_day_master == "生":
            advice.append("日主弱逢生助之年，有利发展，可积极进取。")
        elif relation_with_day_master == "被克":
            advice.append("日主弱逢克扰之年，宜低调保守，避免重大决策。")
    
    # 根据详细程度返回建议
    if details_level == 1:
        return advice[0]
    elif details_level == 2:
        return advice[0] + " " + (advice[1] if len(advice) > 1 else "")
    else:
        return " ".join(advice)

def analyze_liuyue(year, liunian_ganzhi, day_master, day_master_element, yong_shen, liunian_score):
    """分析流月运势"""
    months_analysis = []
    
    # 简化月份干支计算规则（实际应更复杂）
    month_ganzhi_base = {
        "甲子": ["丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥", "丙子", "丁丑"],
        "乙丑": ["戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未", "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑"],
        "丙寅": ["庚寅", "辛卯", "壬辰", "癸巳", "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑"],
        "丁卯": ["壬寅", "癸卯", "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑"],
        "戊辰": ["甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥", "甲子", "乙丑"],
        "己巳": ["丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥", "丙子", "丁丑"],
    }
    
    # 使用简化版的流月计算（实际应更准确）
    months_ganzhi = []
    if liunian_ganzhi in month_ganzhi_base:
        months_ganzhi = month_ganzhi_base[liunian_ganzhi]
    else:
        # 简单示例规则，实际应更复杂
        base = ["丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥", "丙子", "丁丑"]
        months_ganzhi = base
    
    # 分析每个月的运势
    for i, month_ganzhi in enumerate(months_ganzhi):
        month_index = i + 1  # 月份索引（1-12）
        
        # 分析月干支
        month_gan = month_ganzhi[0]  # 流月天干
        month_zhi = month_ganzhi[1]  # 流月地支
        month_element = get_element(month_gan)  # 流月五行
        
        # 计算十神关系
        month_gan_shen = calculate_shishen(day_master, month_gan)  # 流月天干十神
        month_zhi_shen = calculate_shishen(day_master, month_zhi)  # 流月地支十神
        
        # 分析与日主关系
        relation = analyze_relation(month_element, day_master_element)
        
        # 计算月份评分（简化）
        month_score = 0
        if relation == "生" and day_master_element != "旺":
            month_score += 1
        elif relation == "克" and day_master_element == "旺":
            month_score += 1
        elif relation == "被克" and day_master_element != "旺":
            month_score -= 1
        
        # 根据十神关系调整
        if month_gan_shen in ["正印", "偏印"]:
            month_score += 0.5 if day_master_element in ["弱", "偏弱"] else 0
        elif month_gan_shen in ["正官", "七杀"]:
            month_score += 0.5 if day_master_element in ["旺", "偏旺"] else -0.5
        elif month_gan_shen in ["正财", "偏财"]:
            month_score += 0.5
        
        # 考虑流年影响
        month_score += liunian_score * 0.3  # 流年对流月有一定影响
        
        # 分析重要事件（示例）
        events = []
        if month_score >= 1.5:
            events.append("机遇期")
        elif month_score <= -1.5:
            events.append("谨慎期")
        
        # 月份的生活领域影响
        month_impacts = {}
        if month_gan_shen in ["正财", "偏财"]:
            month_impacts["wealth"] = "财运良好" if month_score > 0 else "财务压力"
        elif month_gan_shen in ["正官", "七杀"]:
            month_impacts["career"] = "事业有利" if month_score > 0 else "工作压力"
        elif month_gan_shen in ["正印", "偏印"]:
            month_impacts["study"] = "学习进步" if month_score > 0 else "专注不足"
        
        # 按中国农历月份计算，简化起见使用索引+1
        solar_month = i + 1
        
        months_analysis.append({
            "month": solar_month,
            "lunar_month": f"农历{['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '冬', '腊'][i]}月",
            "ganzhi": month_ganzhi,
            "gan_shen": month_gan_shen,
            "zhi_shen": month_zhi_shen,
            "element": month_element,
            "relation": relation,
            "score": round(month_score, 1),
            "luck_level": translate_score_to_luck(month_score),
            "events": events,
            "impacts": month_impacts
        })
    
    return months_analysis

def identify_key_periods(year, liunian_ganzhi, day_master, impacts, score, months_analysis):
    """识别流年中的重要时期"""
    key_periods = []
    
    # 如果没有流月分析，返回空列表
    if not months_analysis:
        return key_periods
    
    # 找出运势最好和最差的月份
    best_month = max(months_analysis, key=lambda x: x['score'])
    worst_month = min(months_analysis, key=lambda x: x['score'])
    
    # 添加最佳月份
    if best_month['score'] > 1.0:
        key_periods.append({
            "type": "最佳月份",
            "period": f"{year}年{best_month['month']}月",
            "lunar_month": best_month['lunar_month'],
            "ganzhi": best_month['ganzhi'],
            "description": f"此月运势较佳，适合积极进取，把握机会。",
            "advice": f"可在{best_month['month']}月推进重要计划或做出关键决策。"
        })
    
    # 添加最差月份
    if worst_month['score'] < -1.0:
        key_periods.append({
            "type": "谨慎月份",
            "period": f"{year}年{worst_month['month']}月",
            "lunar_month": worst_month['lunar_month'],
            "ganzhi": worst_month['ganzhi'],
            "description": f"此月运势偏弱，宜谨慎行事，避免冒险。",
            "advice": f"建议在{worst_month['month']}月保持低调，推迟重要决策。"
        })
    
    # 分析事业发展期
    career_months = [m for m in months_analysis if m['score'] > 0.5 and ('career' in m['impacts'] or 'career' in impacts and '发展' in impacts['career'])]
    if career_months:
        career_periods = [f"{m['month']}月" for m in career_months]
        key_periods.append({
            "type": "事业发展期",
            "period": f"{year}年{','.join(career_periods)}",
            "description": "这些月份事业运势较好，适合积极拓展和提升。",
            "advice": "可以在这些时段寻求晋升、转换工作或开展新项目。"
        })
    
    # 分析财运高峰期
    wealth_months = [m for m in months_analysis if m['score'] > 0.5 and ('wealth' in m['impacts'] or 'wealth' in impacts and '良好' in impacts['wealth'])]
    if wealth_months:
        wealth_periods = [f"{m['month']}月" for m in wealth_months]
        key_periods.append({
            "type": "财运高峰期",
            "period": f"{year}年{','.join(wealth_periods)}",
            "description": "这些月份财运较好，收入可能增加。",
            "advice": "适合在这些时段进行合理投资或规划重要财务决策。"
        })
    
    # 分析需要注意健康的时期
    if score < 0 and 'health' in impacts and '注意' in impacts['health']:
        health_concern_months = [m for m in months_analysis if m['score'] < -0.5]
        if health_concern_months:
            health_periods = [f"{m['month']}月" for m in health_concern_months]
            key_periods.append({
                "type": "健康关注期",
                "period": f"{year}年{','.join(health_periods)}",
                "description": f"这些月份需特别关注{impacts['health']}。",
                "advice": "建议增加锻炼，保持规律作息，注意饮食健康。"
            })
    
    return key_periods

# 测试代码
if __name__ == "__main__":
    # 测试样例
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
        }
    }
    
    # 测试流年分析
    year = 2023
    result = analyze_liunian(test_report, year)
    
    # 打印结果
    print(f"{year}年流年运势分析：")
    print(f"干支：{result['ganzhi']}")
    print(f"运势评分：{result['score']} ({result['luck_level']})")
    print(f"描述：{result['description']}")
    print(f"建议：{result['advice']}")
    
    # 打印关键时期
    print("\n重要时期：")
    for period in result['key_periods']:
        print(f"- {period['type']} ({period['period']}): {period['description']}")
        
    # 打印流月分析
    if result['months']:
        print("\n流月分析：")
        for month in result['months']:
            print(f"{month['month']}月 ({month['ganzhi']}): {month['luck_level']} {month['score']}分")

def analyze_liuyue(year, liunian_ganzhi, day_master, day_master_element, yong_shen, liunian_score):
    """分析流月运势"""
    months_analysis = []
    
    # 简化月份干支计算规则（实际应更复杂）
    month_ganzhi_base = {
        "甲子": ["丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥", "丙子", "丁丑"],
        "乙丑": ["戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未", "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑"],
        "丙寅": ["庚寅", "辛卯", "壬辰", "癸巳", "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑"],
        "丁卯": ["壬寅", "癸卯", "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑"],
        "戊辰": ["甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥", "甲子", "乙丑"],
        "己巳": ["丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥", "丙子", "丁丑"],
        "庚午": ["戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未", "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑"],
        "辛未": ["庚寅", "辛卯", "壬辰", "癸巳", "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑"],
        "壬申": ["壬寅", "癸卯", "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑"],
        "癸酉": ["甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥", "甲子", "乙丑"],
    }
    
    # 使用简化版的流月计算（实际应更准确）
    months_ganzhi = []
    if liunian_ganzhi in month_ganzhi_base:
        months_ganzhi = month_ganzhi_base[liunian_ganzhi]
    else:
        # 简单示例规则，实际应更复杂
        base = ["丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥", "丙子", "丁丑"]
        months_ganzhi = base
    
    # 分析每个月的运势
    for i, month_ganzhi in enumerate(months_ganzhi):
        month_index = i + 1  # 月份索引（1-12）
        
        # 分析月干支
        month_gan = month_ganzhi[0]
        month_zhi = month_ganzhi[1]
        month_element = get_element(month_gan)
        
        # 计算十神
        month_gan_shen = calculate_shishen(day_master, month_gan)
        month_zhi_shen = calculate_shishen(day_master, month_zhi)
        
        # 分析与日主关系
        relation = analyze_relation(month_element, day_master_element)
        
        # 计算月份评分（简化）
        month_score = 0
        if relation == "生" and day_master_element != "旺":
            month_score += 1
        elif relation == "克" and day_master_element == "旺":
            month_score += 1
        elif relation == "被克" and day_master_element != "旺":
            month_score -= 1
        
        # 考虑流年影响
        month_score += liunian_score * 0.5  # 流年对流月有一定影响
        
        # 分析重要事件（示例）
        events = []
        if month_score >= 1.5:
            events.append("重要机遇期")
        elif month_score <= -1.5:
            events.append("谨慎应对期")
        
        # 月份运势描述
        description = f"{month_index}月干支为{month_ganzhi}，天干十神为{month_gan_shen}，与日主关系为{relation}。"
        if month_score >= 1.5:
            description += "本月运势较好，可积极把握机会。"
        elif month_score >= 0:
            description += "本月运势平稳，维持正常发展即可。"
        elif month_score >= -1.5:
            description += "本月运势略有波折，宜谨慎行事。"
        else:
            description += "本月运势不佳，应低调保守，避免冒险。"
        
        # 添加月份分析结果
        months_analysis.append({
            "month": month_index,
            "ganzhi": month_ganzhi,
            "gan_shen": month_gan_shen,
            "zhi_shen": month_zhi_shen,
            "relation": relation,
            "score": month_score,
            "luck_level": translate_score_to_luck(month_score),
            "events": events,
            "description": description
        })
    
    return months_analysis

def identify_key_periods(year, liunian_ganzhi, day_master, impacts, score, months_analysis):
    """分析关键时期"""
    key_periods = []
    
    # 根据月份分析找出关键月份
    if months_analysis:
        # 找出评分最高的月份
        best_month = max(months_analysis, key=lambda x: x['score'])
        if best_month['score'] >= 1.5:
            key_periods.append({
                "period": f"{year}年{best_month['month']}月",
                "type": "最佳月份",
                "description": f"本年度最佳月份，运势较好，适合重要事项推进。干支：{best_month['ganzhi']}"
            })
        
        # 找出评分最低的月份
        worst_month = min(months_analysis, key=lambda x: x['score'])
        if worst_month['score'] <= -1.5:
            key_periods.append({
                "period": f"{year}年{worst_month['month']}月",
                "type": "谨慎月份",
                "description": f"本年度需特别注意的月份，宜低调谨慎，避免重要决策。干支：{worst_month['ganzhi']}"
            })
        
        # 找出连续评分变化较大的月份
        for i in range(1, len(months_analysis)):
            score_change = months_analysis[i]['score'] - months_analysis[i-1]['score']
            if abs(score_change) >= 2:
                if score_change > 0:
                    key_periods.append({
                        "period": f"{year}年{months_analysis[i]['month']}月",
                        "type": "运势转好",
                        "description": f"运势由低转高的关键时期，可适度积极进取。"
                    })
                else:
                    key_periods.append({
                        "period": f"{year}年{months_analysis[i]['month']}月",
                        "type": "运势转弱",
                        "description": f"运势由高转低的转折期，宜谨慎保守，避免冒险。"
                    })
    
    # 根据流年评分分析关键时期
    if score >= 2:
        key_periods.append({
            "period": f"{year}年全年",
            "type": "发展年",
            "description": f"本年整体运势较好，适合积极发展，把握机遇。"
        })
    elif score <= -2:
        key_periods.append({
            "period": f"{year}年全年",
            "type": "守成年",
            "description": f"本年整体运势略显不利，宜稳健守成，避免冒险。"
        })
    
    # 根据生活领域影响分析关键事项
    if "career" in impacts and "发展" in impacts["career"]:
        key_periods.append({
            "period": f"{year}年",
            "type": "事业发展期",
            "description": f"事业方面有较好机遇，可适度进取。"
        })
    
    if "wealth" in impacts and "良好" in impacts["wealth"]:
        key_periods.append({
            "period": f"{year}年",
            "type": "财运期",
            "description": f"财运相对良好，可适当规划投资理财。"
        })
    
    if "health" in impacts and "注意" in impacts["health"]:
        key_periods.append({
            "period": f"{year}年",
            "type": "健康关注期",
            "description": f"需注意健康，增加锻炼，保持良好作息。"
        })
    
    return key_periods

# 测试代码
if __name__ == "__main__":
    # 创建一个示例报告用于测试
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
        'current_dayun': {
            'ganzhi': '丙午',
            'age_range': '26-35',
            'element': '火'
        }
    }
    
    # 分析2025年运势
    result = analyze_liunian(test_report, 2025, 3)
    
    # 打印结果
    print(f"2025年{result['ganzhi']}年运势分析")
    print(f"五行属性: {result['element']}")
    print(f"天干十神: {result['gan_shen']}")
    print(f"地支十神: {result['zhi_shen']}")
    print(f"运势评分: {result['score']} ({result['luck_level']})")
    print(f"运势描述: {result['description']}")
    print(f"\n运势建议: {result['advice']}")
    
    print("\n关键时期:")
    for period in result['key_periods']:
        print(f"  {period['period']} - {period['type']}: {period['description']}")
    
    print("\n月份分析:")
    for month in result['months']:
        print(f"  {month['month']}月: {month['ganzhi']} - {month['luck_level']} - {month['description']}")

def analyze_liuyue(year, liunian_ganzhi, day_master, day_master_element, yong_shen, liunian_score):
    """分析流月运势"""
    months_analysis = []
    
    # 月份干支计算规则
    month_gan_base = ["丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁"]
    month_zhi_base = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]
    
    # 根据流年天干确定月干偏移
    liunian_gan = liunian_ganzhi[0]
    gan_offset = {"甲": 0, "乙": 2, "丙": 4, "丁": 6, "戊": 8, 
                 "己": 0, "庚": 2, "辛": 4, "壬": 6, "癸": 8}
    
    # 计算流月干支
    months_ganzhi = []
    for i in range(12):
        month_gan_index = (i + gan_offset.get(liunian_gan, 0)) % 10
        month_gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"][month_gan_index]
        month_zhi = month_zhi_base[i]
        months_ganzhi.append(month_gan + month_zhi)
    
    # 分析每个月的运势
    for i, month_ganzhi in enumerate(months_ganzhi):
        month_index = i + 1  # 月份索引（1-12）
        
        # 分析月干支
        month_gan = month_ganzhi[0]
        month_zhi = month_ganzhi[1]
        month_element = get_element(month_gan)
        
        # 计算十神
        month_gan_shen = calculate_shishen(day_master, month_gan)
        month_zhi_shen = calculate_shishen(day_master, month_zhi)
        
        # 分析与日主关系
        relation = analyze_relation(month_element, day_master_element)
        
        # 计算月份评分（简化）
        month_score = 0
        if relation == "生" and day_master_element != "旺":
            month_score += 1
        elif relation == "克" and day_master_element == "旺":
            month_score += 1
        elif relation == "被克" and day_master_element != "旺":
            month_score -= 1
        
        # 考虑流年影响
        month_score += liunian_score * 0.5  # 流年对流月有一定影响
        
        # 分析重要事件（示例）
        events = []
        if month_score >= 1.5:
            events.append("重要机遇期")
        elif month_score <= -1.5:
            events.append("谨慎应对期")
        
        # 根据十神分析适合的活动
        activities = []
        if month_gan_shen in ["食神", "伤官"]:
            activities.append("适合学习进修、创意工作")
        elif month_gan_shen in ["正财", "偏财"]:
            activities.append("适合投资理财、拓展业务")
        elif month_gan_shen in ["正官", "七杀"]:
            activities.append("适合参与竞争、争取晋升")
        elif month_gan_shen in ["正印", "偏印"]:
            activities.append("适合沉淀积累、稳固基础")
        elif month_gan_shen in ["比肩", "劫财"]:
            activities.append("适合合作共事、扩展人脉")
        
        months_analysis.append({
            "month": month_index,
            "ganzhi": month_ganzhi,
            "gan_shen": month_gan_shen,
            "zhi_shen": month_zhi_shen,
            "relation": relation,
            "score": month_score,
            "luck_level": translate_score_to_luck(month_score),
            "events": events,
            "activities": activities,
            "description": f"{month_index}月，{month_ganzhi}月，与日主{relation}关系，运势{translate_score_to_luck(month_score)}"
        })
    
    return months_analysis

def identify_key_periods(year, liunian_ganzhi, day_master, impacts, score, months_analysis):
    """确定重要时期"""
    key_periods = []
    
    # 基于流年评分判断整体趋势
    if score >= 2:
        key_periods.append({
            "period": "全年",
            "type": "发展期",
            "score": score,
            "description": f"{year}年整体运势良好，是积极发展的重要年份。"
        })
    elif score <= -2:
        key_periods.append({
            "period": "全年",
            "type": "调整期",
            "score": score,
            "description": f"{year}年整体运势偏弱，宜低调行事，避免大的风险与变动。"
        })
    
    # 分析流月中的重要时期
    if months_analysis:
        # 找出最好和最差的月份
        best_month = max(months_analysis, key=lambda x: x["score"])
        worst_month = min(months_analysis, key=lambda x: x["score"])
        
        # 添加重要月份信息
        if best_month["score"] > 1:
            key_periods.append({
                "period": f"{best_month['month']}月",
                "type": "高峰期",
                "score": best_month["score"],
                "description": f"{best_month['month']}月为{year}年运势高峰期，可积极把握机会。{'; '.join(best_month['activities'])}"
            })
        
        if worst_month["score"] < -1:
            key_periods.append({
                "period": f"{worst_month['month']}月",
                "type": "低谷期",
                "score": worst_month["score"],
                "description": f"{worst_month['month']}月为{year}年运势低谷期，宜谨慎行事，避免重大决策。"
            })
        
        # 分析转折点
        trend_changes = []
        for i in range(1, len(months_analysis)):
            score_change = months_analysis[i]["score"] - months_analysis[i-1]["score"]
            if abs(score_change) >= 1.5:
                direction = "上升" if score_change > 0 else "下降"
                trend_changes.append({
                    "month": months_analysis[i]["month"],
                    "direction": direction,
                    "change": abs(score_change)
                })
        
        # 添加最显著的转折点
        if trend_changes:
            most_significant = max(trend_changes, key=lambda x: x["change"])
            key_periods.append({
                "period": f"{most_significant['month']}月",
                "type": f"运势{most_significant['direction']}",
                "score": most_significant["change"],
                "description": f"{most_significant['month']}月为{year}年运势明显{most_significant['direction']}期，趋势变化显著。"
            })
    
    # 分析事业和财运高峰期
    if "career" in impacts and "发展" in impacts["career"]:
        career_months = [m for m in months_analysis if m["score"] > 0 and m["gan_shen"] in ["正官", "七杀", "食神", "伤官"]]
        if career_months:
            best_career_month = max(career_months, key=lambda x: x["score"])
            key_periods.append({
                "period": f"{best_career_month['month']}月",
                "type": "事业机遇期",
                "score": best_career_month["score"],
                "description": f"{best_career_month['month']}月为事业发展良机，适合把握机会，推进重要项目。"
            })
    
    if "wealth" in impacts and ("良好" in impacts["wealth"] or "广进" in impacts["wealth"]):
        wealth_months = [m for m in months_analysis if m["score"] > 0 and m["gan_shen"] in ["正财", "偏财"]]
        if wealth_months:
            best_wealth_month = max(wealth_months, key=lambda x: x["score"])
            key_periods.append({
                "period": f"{best_wealth_month['month']}月",
                "type": "财运高峰期",
                "score": best_wealth_month["score"],
                "description": f"{best_wealth_month['month']}月为财运高峰期，适合投资、理财或财务规划。"
            })
    
    return key_periods

# 测试代码
if __name__ == "__main__":
    # 简单测试
    year = 2023
    ganzhi = "癸卯"
    day_master = "甲"
    day_master_element = "木"
    yong_shen = "火"
    liunian_score = 1.5
    
    months = analyze_liuyue(year, ganzhi, day_master, day_master_element, yong_shen, liunian_score)
    
    impacts = {
        "career": "发展活跃",
        "wealth": "财运良好",
        "health": "整体健康良好",
        "relationship": "人际关系活跃"
    }
    
    key_periods = identify_key_periods(year, ganzhi, day_master, impacts, liunian_score, months)
    
    print("\n==== 流月分析 ====")
    for month in months:
        print(f"{month['month']}月: {month['ganzhi']} - {month['luck_level']} - {', '.join(month['events'])}")
    
    print("\n==== 重要时期 ====")
    for period in key_periods:
        print(f"{period['period']}: {period['type']} - {period['description']}")
