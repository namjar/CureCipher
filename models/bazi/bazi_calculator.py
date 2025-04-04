"""
八字计算模块 - 主计算函数
使用lunar_python库计算八字、流年、流月、大运、小运和神煞
"""

def generate_text_report(report):
    """
    生成文本形式的命盘解读
    
    参数:
        report (dict): 命盘报告数据
    
    返回:
        str: 文本形式的命盘解读
    """
    lines = []
    
    # 基本信息
    lines.append("===== 八字命盘解读 =====\n")
    lines.append("[基本信息]")
    lines.append(f"四柱八字: {report['basic_info']['four_pillars']}")
    lines.append(f"天干: {report['basic_info']['gans']}")
    lines.append(f"地支: {report['basic_info']['zhis']}")
    lines.append(f"日主: {report['basic_info']['day_master']}")
    lines.append(f"阳历: {report['basic_info']['solar_date']}")
    lines.append(f"阴历: {report['basic_info']['lunar_date']}")
    lines.append("")
    
    # 命盘分析
    lines.append("[命盘分析]")
    lines.append(f"日主强度: {report['pattern_analysis']['day_master_strength']} ({report['pattern_analysis']['day_master_percentage']:.2f}%)")
    lines.append(f"五行平衡: {report['pattern_analysis']['balance_state']}")
    lines.append(f"备注: {report['pattern_analysis']['balance_description']}")
    lines.append(f"最强五行: {report['pattern_analysis']['strongest_element']}")
    lines.append(f"最弱五行: {report['pattern_analysis']['weakest_element']}")
    lines.append(f"用神: {report['pattern_analysis']['yong_shen']}")
    lines.append(f"用神说明: {report['pattern_analysis']['yong_shen_explanation']}")
    lines.append(f"用神天干: {report['pattern_analysis']['yong_gan']}")
    lines.append(f"用神地支: {report['pattern_analysis']['yong_zhi']}")
    lines.append("")
    
    # 当前大运
    lines.append("[当前大运]")
    if report['current_dayun']:
        current_dayun = report['current_dayun']
        lines.append(f"大运: {current_dayun['ganzhi']} {current_dayun['gan_shen']}{current_dayun['zhi_shen']}")
        lines.append(f"年龄范围: {current_dayun['age_range']} 岁")
        lines.append(f"纳音五行: {current_dayun['nayin']}")
        
        # 增加大运详细分析
        day_master = report['basic_info']['day_master'].split()[0]
        day_master_element = report['basic_info']['day_master'].split('(')[1].strip(')')
        dayun_element = current_dayun['element']
        yong_shen = report['pattern_analysis']['yong_shen'].split()[0]
        
        lines.append("\n[大运详细分析]")
        
        # 大运与日主的关系
        if current_dayun['gan_shen']:
            dayun_shishen = current_dayun['gan_shen']
            lines.append(f"大运天干为{current_dayun['gan']}，十神为{dayun_shishen}，{get_relationship_by_shishen(dayun_shishen)}")
            
        if dayun_element == day_master_element:
            lines.append(f"当前大运五行与日主相同，为比劫运，有增强日主力量的作用。")
        elif is_generating(dayun_element, day_master_element):
            lines.append(f"当前大运五行{dayun_element}生助日主{day_master_element}，为印枭运，对日主有滋养作用。")
        elif is_generated(dayun_element, day_master_element):
            lines.append(f"当前大运五行{dayun_element}由日主{day_master_element}所生，为食伤运，日主有泄气现象。")
        elif is_controlling(dayun_element, day_master_element):
            lines.append(f"当前大运五行{dayun_element}克制日主{day_master_element}，为官杀运，对日主有制约作用。")
        elif is_controlled(dayun_element, day_master_element):
            lines.append(f"当前大运五行{dayun_element}被日主{day_master_element}所克，为财星运，有助日主发挥克制力。")
        
        # 大运对格局的影响
        if dayun_element == yong_shen:
            lines.append(f"当前大运五行{dayun_element}与用神相同，对命局有较大助力。")
        elif is_generating(dayun_element, yong_shen):
            lines.append(f"当前大运五行{dayun_element}生助用神{yong_shen}，间接有利于命局。")
        elif is_controlling(dayun_element, yong_shen):
            lines.append(f"当前大运五行{dayun_element}克制用神{yong_shen}，可能对命局造成不利影响。")
    else:
        lines.append("尚未进入大运")
    lines.append("")
    
    # 流年流月流日
    lines.append("[当前流年流月流日]")
    lines.append(f"流年: {report['current_info']['liunian']['ganzhi']} 十神: {report['current_info']['liunian']['gan_shen']}/{report['current_info']['liunian']['zhi_shen']}")
    lines.append(f"流月: {report['current_info']['liuyue']['ganzhi']} 十神: {report['current_info']['liuyue']['gan_shen']}/{report['current_info']['liuyue']['zhi_shen']}")
    lines.append(f"流日: {report['current_info']['liuri']['ganzhi']} 十神: {report['current_info']['liuri']['gan_shen']}/{report['current_info']['liuri']['zhi_shen']}")
    
    # 增加流年流月详细分析
    day_master = report['basic_info']['day_master'].split()[0]
    day_master_element = report['basic_info']['day_master'].split('(')[1].strip(')')
    yong_shen = report['pattern_analysis']['yong_shen'].split()[0]
    
    lines.append("\n[流年流月详细分析]")
    
    # 流年分析
    liunian_gz = report['current_info']['liunian']['ganzhi']
    liunian_gan = liunian_gz[0]  # 流年天干
    liunian_gan_element = get_element(liunian_gan)
    liunian_gan_shen = report['current_info']['liunian']['gan_shen']
    
    lines.append(f"流年天干{liunian_gan}十神为{liunian_gan_shen}，{get_relationship_by_shishen(liunian_gan_shen)}")
    
    if is_generating(liunian_gan_element, day_master_element):
        lines.append(f"流年天干{liunian_gan}({liunian_gan_element})生助日主，为印枭格局，有滋养作用。")
    elif is_generated(liunian_gan_element, day_master_element):
        lines.append(f"流年天干{liunian_gan}({liunian_gan_element})被日主所生，为食伤格局，日主有泄气现象。")
    elif is_controlling(liunian_gan_element, day_master_element):
        lines.append(f"流年天干{liunian_gan}({liunian_gan_element})克制日主，为官杀格局，需注意克制力度。")
    elif is_controlled(liunian_gan_element, day_master_element):
        lines.append(f"流年天干{liunian_gan}({liunian_gan_element})被日主所克，为财星格局，日主有发挥余地。")
    elif liunian_gan_element == day_master_element:
        lines.append(f"流年天干{liunian_gan}({liunian_gan_element})与日主同五行，为比劫格局，增强日主力量。")
        
    # 流月分析
    liuyue_gz = report['current_info']['liuyue']['ganzhi']
    liuyue_gan = liuyue_gz[0]  # 流月天干
    liuyue_gan_element = get_element(liuyue_gan)
    liuyue_gan_shen = report['current_info']['liuyue']['gan_shen']
    
    lines.append(f"\n流月{liuyue_gz}十神为{liuyue_gan_shen}，{get_relationship_by_shishen(liuyue_gan_shen)}")
    
    if is_generating(liuyue_gan_element, day_master_element):
        lines.append(f"流月天干{liuyue_gan}({liuyue_gan_element})生助日主，本月较为顺利，有助力。")
    elif is_controlling(liuyue_gan_element, day_master_element):
        lines.append(f"流月天干{liuyue_gan}({liuyue_gan_element})克制日主，本月可能有阻力，需谨慎应对。")
    elif liuyue_gan_element == day_master_element:
        lines.append(f"流月天干{liuyue_gan}({liuyue_gan_element})与日主同五行，本月力量增强，但需避免冲动。")
    
    # 流年与流月组合分析
    lines.append("\n流年流月组合分析：")
    if liunian_gan_element == liuyue_gan_element:
        lines.append(f"流年与流月五行相同，都是{liunian_gan_element}，相互增强，影响更为明显。")
    elif is_generating(liunian_gan_element, liuyue_gan_element):
        lines.append(f"流年{liunian_gan_element}生助流月{liuyue_gan_element}，有利于长期计划在本月落实。")
    elif is_controlling(liunian_gan_element, liuyue_gan_element):
        lines.append(f"流年{liunian_gan_element}克制流月{liuyue_gan_element}，可能导致计划受阻，需灵活调整。")
        
    # 流年流月与用神关系分析
    lines.append(f"\n流年流月与用神({yong_shen})的关系：")
    
    if liunian_gan_element == yong_shen:
        lines.append(f"流年五行与用神相同，今年对命主较为有利。")
    elif is_generating(liunian_gan_element, yong_shen):
        lines.append(f"流年五行{liunian_gan_element}生助用神{yong_shen}，间接有利于命局发展。")
    
    if liuyue_gan_element == yong_shen:
        lines.append(f"流月五行与用神相同，本月机会较多，可积极把握。")
    elif is_controlling(liuyue_gan_element, yong_shen):
        lines.append(f"流月五行{liuyue_gan_element}克制用神{yong_shen}，本月需谨慎行事，避免损耗。")
    
    lines.append("")
    
    # 神煞信息
    lines.append("[神煞信息]")
    if report['shensha_info']:
        for shensha in report['shensha_info']:
            lines.append(f"{shensha['name']}: {shensha['description']}")
        
        # 神煞分析增强
        lines.append("\n[神煞详细分析]")
        
        # 分类收集神煞
        ji_shen = []  # 吉神
        xiong_shen = []  # 凶神
        
        for shensha in report['shensha_info']:
            if shensha['name'] in ["天德", "月德", "福神", "喜神", "红艳"]:
                ji_shen.append(shensha)
            elif shensha['name'] in ["天羊", "天刚", "灾煞", "劫煞", "岂煞", "屿煞"]:
                xiong_shen.append(shensha)
        
        # 吉神分析
        if ji_shen:
            lines.append("吉神分析：")
            for shen in ji_shen:
                lines.append(f"  - {shen['name']}在{shen['position']}柱: {shen['description']}")
            if len(ji_shen) >= 2:
                lines.append("  多个吉神同时存在，有利于提升命主运势。")
        
        # 凶神分析
        if xiong_shen:
            lines.append("凶神分析：")
            for shen in xiong_shen:
                lines.append(f"  - {shen['name']}在{shen['position']}柱: {shen['description']}")
                
            if len(xiong_shen) >= 2:
                lines.append("  多个凶神同时存在，需谨慎应对可能的挑战。")
                
        # 吉凶神比较
        if ji_shen and xiong_shen:
            if len(ji_shen) > len(xiong_shen):
                lines.append("吉神多于凶神，总体而言吉多于凶，命主运势较佳。")
            elif len(ji_shen) < len(xiong_shen):
                lines.append("凶神多于吉神，需谨慎行事，提高警惕。")
            else:
                lines.append("吉凶神数量相当，运势喜忧参半，宜谨慎中求发展。")
                
        # 神煞与日主年柱的关系
        day_pillar_shensha = [shen for shen in report['shensha_info'] if shen['position'] == "日"]
        year_pillar_shensha = [shen for shen in report['shensha_info'] if shen['position'] == "年"]
        
        if day_pillar_shensha:
            lines.append("日柱神煞分析：")
            day_ji_shen = [shen for shen in day_pillar_shensha if shen['name'] in ["天德", "月德", "福神", "喜神"]]
            day_xiong_shen = [shen for shen in day_pillar_shensha if shen['name'] in ["天羊", "天刚", "灾煞", "劫煞"]]
            
            if day_ji_shen:
                lines.append("  日柱吉神在人格上起到正面作用，表示人格积极向上。")
            if day_xiong_shen:
                lines.append("  日柱凶神影响个人性格发展，需注意自身修养。")
                
        if year_pillar_shensha:
            lines.append("年柱神煞分析：")
            year_ji_shen = [shen for shen in year_pillar_shensha if shen['name'] in ["天德", "月德", "福神", "喜神"]]
            year_xiong_shen = [shen for shen in year_pillar_shensha if shen['name'] in ["天羊", "天刚", "灾煞", "劫煞"]]
            
            if year_ji_shen:
                lines.append("  年柱吉神对祖辈运势或父母影响较为有利。")
            if year_xiong_shen:
                lines.append("  年柱凶神可能暗示和家族长辈关系有挑战。")
    else:
        lines.append("无神煞信息")
    lines.append("")
    
    # 特殊格局
    lines.append("[特殊格局分析]")
    special_patterns = report['pattern_analysis'].get('special_patterns', {})
    
    # 三合格局
    if special_patterns and 'san_he' in special_patterns and special_patterns['san_he']:
        lines.append("三合格局：")
        for pattern in special_patterns['san_he']:
            lines.append(f"  - {pattern['name']}: {pattern['description']}")
    
    # 三会格局
    if special_patterns and 'san_hui' in special_patterns and special_patterns['san_hui']:
        lines.append("三会格局：")
        for pattern in special_patterns['san_hui']:
            lines.append(f"  - {pattern['name']}: {pattern['description']}")
    
    # 冠带格局
    if special_patterns and 'guan_xin' in special_patterns and special_patterns['guan_xin']:
        lines.append("冠带格局：")
        for pattern in special_patterns['guan_xin']:
            lines.append(f"  - {pattern['name']}: {pattern['description']}")
            
    if not special_patterns or (not special_patterns.get('san_he') and 
                              not special_patterns.get('san_hui') and
                              not special_patterns.get('guan_xin')):
        lines.append("无特殊格局")
    lines.append("")
    
    # 纳音五行
    lines.append("[纳音五行]")
    for position, nayin in report['nayin'].items():
        lines.append(f"{position}: {nayin}")
    lines.append("")
    
    # 特殊信息
    lines.append("[特殊信息]")
    lines.append(f"命宫: {report['special']['ming_gong']}")
    lines.append(f"胎元: {report['special']['tai_yuan']}")
    lines.append("")
    
    # 大运流年分析指导
    lines.append("[命盘总体解读与指导]")
    if report['pattern_analysis']['day_master_strength'] in ['旺', '偏旺']:
        # 日主旺的年份
        lines.append("日主过旺，适合濒身或耗身的运势：")
        lines.append(f"1. 法子：可选择{report['pattern_analysis']['yong_shen']}的年份，帮助平衡日主。")
        lines.append(f"2. 避免过于旺盛的日主({report['basic_info']['day_master'].split()[0]})年份。")
        lines.append(f"3. 理想的大运流年应有充足的{report['pattern_analysis']['yong_shen']}手法强。")
        lines.append(f"4. 当大运为{report['pattern_analysis']['yong_shen']}五行时，可找对应行业发展。")
    elif report['pattern_analysis']['day_master_strength'] in ['弱', '偏弱']:
        # 日主弱的年份
        lines.append("日主过弱，适合滋身或扩张的运势：")
        lines.append(f"1. 法子：可选择{report['pattern_analysis']['yong_shen']}的年份，提升日主力量。")
        lines.append(f"2. 避免克法日主({report['basic_info']['day_master'].split()[0]})的年份。")
        lines.append(f"3. 理想的大运流年应有充足的{report['pattern_analysis']['yong_shen']}手法。")
        lines.append(f"4. 适合在{report['pattern_analysis']['yong_shen']}年份开始新的项目或事业。")
    else:
        # 日主中和
        lines.append("日主强度适中，可选择平衡发展的运势：")
        lines.append(f"1. 保持当前的平衡状态，不过分強调任何五行。")
        lines.append("2. 可适当发展五行中较弱的部分。")
        lines.append("3. 避免增强已经过强的五行。")
        lines.append("4. 各类大运都能找到宝贵之处，关键是保持平衡而不破坏和谐。")
        
    # 可适合行业分析
    elements_career = {
        "木": ["教育", "出版", "文化", "艺术", "园林", "农业"],
        "火": ["餐饮", "娱乐", "美容", "科技", "电子", "职业马拉松"],
        "土": ["房地产", "建筑", "金融", "养殖", "保险", "物流"],
        "金": ["机械", "计算机", "技术", "名牌集团", "法律", "额财经贸"],
        "水": ["旅游", "运输", "船只", "鱼类", "文学", "策划", "咨询"]
    }
    
    # 找出最弱的五行和用神五行，推荐行业
    weakest_element = report['pattern_analysis']['weakest_element'].split()[0]
    yong_shen_element = report['pattern_analysis']['yong_shen'].split()[0]
    
    lines.append("\n[行业建议]")
    
    # 根据日主强度推荐行业
    if report['pattern_analysis']['day_master_strength'] in ['旺', '偏旺']:
        # 日主旺，用克日主或泄日主的行业
        if yong_shen_element in elements_career:
            lines.append(f"日主过旺，适合的行业有：{', '.join(elements_career[yong_shen_element])}等。")
    elif report['pattern_analysis']['day_master_strength'] in ['弱', '偏弱']:
        # 日主弱，用生日主或按日主的行业
        if yong_shen_element in elements_career:
            lines.append(f"日主过弱，适合的行业有：{', '.join(elements_career[yong_shen_element])}等。")
    else:
        # 日主中和，推荐最弱五行的行业来平衡
        if weakest_element in elements_career:
            lines.append(f"日主较为中和，适合发展较弱的{weakest_element}行业，如：{', '.join(elements_career[weakest_element])}等。")
    
    # 增加个人发展建议
    lines.append("\n[个人发展建议]")
    day_master_element = report['basic_info']['day_master'].split('(')[1].strip(')')
    
    element_traits = {
        "木": {
            "优点": ["创意思考", "计划能力", "高瓶顶格局"],
            "注意": ["避免激进", "避免因小失大", "保持思考开阔"]
        },
        "火": {
            "优点": ["领导能力", "社交力", "高热情"],
            "注意": ["避免过度燃烧", "基础性事务不要忽略", "控制情绪波动"]
        },
        "土": {
            "优点": ["稳定可靠", "如意穷追不舍", "良好人际关系"],
            "注意": ["避免心态保守", "逻辑思维", "要勇于创新"]
        },
        "金": {
            "优点": ["细致分析力", "严格要求", "好的执行力"],
            "注意": ["避免过于刃锋", "与人交错不能太生硬", "灵活应对变化"]
        },
        "水": {
            "优点": ["智慧相通", "围魂破解", "好奇心强"],
            "注意": ["避免心理上的迷失", "没有辰信力", "不要太过理想化"]
        }
    }
    
    if day_master_element in element_traits:
        traits = element_traits[day_master_element]
        lines.append(f"日主五行属性为{day_master_element}，有以下优势：")
        for trait in traits["优点"]:
            lines.append(f"  - {trait}")
        lines.append(f"\n需要注意以下方面：")
        for trait in traits["注意"]:
            lines.append(f"  - {trait}")
    
    return "\n".join(lines)

import datetime
from collections import Counter
from lunar_python import Solar, Lunar

from .calculator import (
    get_element, get_element_english, get_default_location
)
from .lunar_extension import LunarExtension
from .lunar_extension import LunarExtension
import requests
from geopy.geocoders import Nominatim


def get_empty(day_gz, zhi):
    """
    获取空亡
    
    参数:
        day_gz (str): 日柱干支
        zhi (str): 地支
    
    返回:
        bool: 是否空亡
    """
    # 天干地支对应的六十甲子序号
    jiazi_index = {
        "甲子": 1, "乙丑": 2, "丙寅": 3, "丁卯": 4, "戊辰": 5, "己巳": 6, "庚午": 7, "辛未": 8, "壬申": 9, "癸酉": 10,
        "甲戌": 11, "乙亥": 12, "丙子": 13, "丁丑": 14, "戊寅": 15, "己卯": 16, "庚辰": 17, "辛巳": 18, "壬午": 19, "癸未": 20,
        "甲申": 21, "乙酉": 22, "丙戌": 23, "丁亥": 24, "戊子": 25, "己丑": 26, "庚寅": 27, "辛卯": 28, "壬辰": 29, "癸巳": 30,
        "甲午": 31, "乙未": 32, "丙申": 33, "丁酉": 34, "戊戌": 35, "己亥": 36, "庚子": 37, "辛丑": 38, "壬寅": 39, "癸卯": 40,
        "甲辰": 41, "乙巳": 42, "丙午": 43, "丁未": 44, "戊申": 45, "己酉": 46, "庚戌": 47, "辛亥": 48, "壬子": 49, "癸丑": 50,
        "甲寅": 51, "乙卯": 52, "丙辰": 53, "丁巳": 54, "戊午": 55, "己未": 56, "庚申": 57, "辛酉": 58, "壬戌": 59, "癸亥": 60
    }
    
    # 计算空亡地支
    if day_gz in jiazi_index:
        index = jiazi_index[day_gz] % 10  # 取余确定所在旬
        if index == 0:
            index = 10
        
        # 旬空地支列表
        xun_kong = {
            1: ["戌", "亥"],  # 甲子旬
            2: ["申", "酉"],  # 甲戌旬
            3: ["午", "未"],  # 甲申旬
            4: ["辰", "巳"],  # 甲午旬
            5: ["寅", "卯"],  # 甲辰旬
            6: ["子", "丑"],  # 甲寅旬
            7: ["戌", "亥"],  # 甲子旬
            8: ["申", "酉"],  # 甲戌旬
            9: ["午", "未"],  # 甲申旬
            10: ["辰", "巳"] # 甲午旬
        }
        
        # 检查是否空亡
        return zhi in xun_kong.get(index, [])
    
    return False


def check_gan_he(gans):
    """
    检查天干合化
    
    参数:
        gans (list): 四柱天干列表
    
    返回:
        list: 合化信息列表
    """
    he_result = []
    
    # 天干合化规则
    gan_he = {
        ("甲", "己"): {"element": "土", "description": "中正之合"},
        ("乙", "庚"): {"element": "金", "description": "仁义之合"},
        ("丙", "辛"): {"element": "水", "description": "威制之合"},
        ("丁", "壬"): {"element": "木", "description": "淫慝之合"},
        ("戊", "癸"): {"element": "火", "description": "无情之合"}
    }
    
    # 检查四柱中的天干合化
    for i in range(len(gans)):
        for j in range(i+1, len(gans)):
            pair = (gans[i], gans[j])
            if pair in gan_he:
                he_info = gan_he[pair]
                he_result.append({
                    "gan1": gans[i],
                    "gan2": gans[j],
                    "position1": ["年", "月", "日", "时"][i],
                    "position2": ["年", "月", "日", "时"][j],
                    "element": he_info["element"],
                    "description": he_info["description"]
                })
            # 检查反向合化
            pair_reverse = (gans[j], gans[i])
            if pair_reverse in gan_he:
                he_info = gan_he[pair_reverse]
                he_result.append({
                    "gan1": gans[j],
                    "gan2": gans[i],
                    "position1": ["年", "月", "日", "时"][j],
                    "position2": ["年", "月", "日", "时"][i],
                    "element": he_info["element"],
                    "description": he_info["description"]
                })
    
    return he_result


def determine_zhi_element(zhi):
    """
    确定地支的主要五行属性
    
    参数:
        zhi (str): 地支
    
    返回:
        str: 五行属性
    """
    # 定义地支五行对应关系
    zhi_elements = {
        "子": "水", "丑": "土", "寅": "木", "卯": "木",
        "辰": "土", "巳": "火", "午": "火", "未": "土",
        "申": "金", "酉": "金", "戌": "土", "亥": "水"
    }
    
    return zhi_elements.get(zhi, "")


def get_generating_element(element):
    """
    获取生我的五行
    
    参数:
        element (str): 五行属性
    
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
    获取我生的五行
    
    参数:
        element (str): 五行属性
    
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
    获取克我的五行
    
    参数:
        element (str): 五行属性
    
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
    获取我克的五行
    
    参数:
        element (str): 五行属性
    
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


def is_generating(element1, element2):
    """检查element1是否生element2（element1生element2）"""
    generating_map = {
        "木": "火",
        "火": "土",
        "土": "金",
        "金": "水",
        "水": "木"
    }
    return generating_map.get(element1) == element2

def is_generated(element1, element2):
    """检查element1是否被element2所生（element2生element1）"""
    return is_generating(element2, element1)

def is_controlling(element1, element2):
    """检查element1是否克element2（element1克element2）"""
    controlling_map = {
        "木": "土",
        "土": "水",
        "水": "火",
        "火": "金",
        "金": "木"
    }
    return controlling_map.get(element1) == element2

def is_controlled(element1, element2):
    """检查element1是否被element2所克（element2克element1）"""
    return is_controlling(element2, element1)

def get_relationship_by_shishen(shishen):
    """根据十神确定五行关系
    
    参数:
        shishen (str): 十神名称
    
    返回:
        str: 关系描述
    """
    relationship = {
        "比肩": "日主自己，增强日主力量。",
        "劫财": "与日主相同，但相互争夺资源，可能导致冲突。",
        "食神": "日主生的五行，有泄气作用。",
        "伤官": "日主生的五行，但过度泄气会损伤日主。",
        "天财": "日主所克的五行，但方式较温和。",
        "正财": "日主所克的五行，代表正当财富。",
        "七杀": "克制日主的五行，具有攻击性。",
        "正官": "克制日主的五行，但方式较为正当。",
        "偏印": "生日主的五行，但力量较弱。",
        "正印": "生日主的五行，力量较强。"
    }
    
    return relationship.get(shishen, "不确定的关系")

# 天干和地支
Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

def get_elements_balance(scores):
    """
    分析五行平衡状态
    
    参数:
        scores (dict): 五行得分
    
    返回:
        dict: 平衡分析结果
    """
    # 计算五行的标准差，越小越平衡
    avg = sum(scores.values()) / 5
    variance = sum((x - avg) ** 2 for x in scores.values()) / 5
    std_dev = variance ** 0.5
    
    # 找出最强和最弱的五行
    strongest = max(scores.items(), key=lambda x: x[1])
    weakest = min(scores.items(), key=lambda x: x[1])
    
    # 分析平衡状态
    if std_dev < 5:
        balance_state = "非常平衡"
        description = "五行分布非常均衡，有利于整体命局。"
    elif std_dev < 10:
        balance_state = "较为平衡"
        description = "五行分布较为均衡，命局较为稳定。"
    elif std_dev < 15:
        balance_state = "稍有不平衡"
        description = f"{strongest[0]}偏强，{weakest[0]}偏弱，命局稍有偏颇。"
    elif std_dev < 20:
        balance_state = "明显不平衡"
        description = f"{strongest[0]}明显过强，{weakest[0]}明显不足，命局有所缺失。"
    else:
        balance_state = "严重不平衡"
        description = f"{strongest[0]}极度过强，{weakest[0]}极度不足，命局失衡明显。"
    
    return {
        "balance_state": balance_state,
        "description": description,
        "std_deviation": round(std_dev, 2),
        "strongest": strongest[0],
        "strongest_percentage": round(strongest[1] / sum(scores.values()) * 100, 2),
        "weakest": weakest[0],
        "weakest_percentage": round(weakest[1] / sum(scores.values()) * 100, 2)
    }


def determine_pattern(day_master, gans, zhis, gan_shens, zhi_shens, scores):
    """
    根据八字格局确定用神
    
    参数:
        day_master (str): 日干
        gans (list): 四柱天干列表
        zhis (list): 四柱地支列表
        gan_shens (list): 天干十神列表
        zhi_shens (list): 地支十神列表
        scores (dict): 五行得分
    
    返回:
        dict: 格局分析和用神建议
    """
    day_master_element = gan5[day_master]
    
    # 计算五行旺衰
    elements = list(scores.keys())
    elements.sort(key=lambda x: scores[x], reverse=True)
    strongest_element = elements[0]
    weakest_element = elements[-1]
    
    # 确定日主旺衰
    day_master_score = scores[day_master_element]
    total_score = sum(scores.values())
    day_master_percentage = (day_master_score / total_score) * 100
    
    if day_master_percentage > 30:
        strength = "旺"
    elif day_master_percentage > 20:
        strength = "偏旺"
    elif day_master_percentage > 15:
        strength = "中和"
    elif day_master_percentage > 10:
        strength = "偏弱"
    else:
        strength = "弱"
    
    # 确定用神策略
    if strength in ["旺", "偏旺"]:
        # 日主过旺，用泄和耗
        # 找出克日主的五行和被日主克的五行
        ke_me = get_controlling_element(day_master_element)  # 克我者
        wo_ke = get_controlled_element(day_master_element)   # 我克者
        
        if scores[ke_me] > scores[wo_ke]:
            yong_shen = ke_me  # 用克我的五行泄身
            yong_shen_type = "泄身"
        else:
            yong_shen = wo_ke  # 用我克的五行耗身
            yong_shen_type = "耗身"
    else:  # 日主偏弱或弱
        # 日主过弱，用生和扶
        # 找出生日主的五行和日主生的五行
        sheng_me = get_generating_element(day_master_element)  # 生我者
        me_sheng = get_generated_element(day_master_element)   # 我生者
        
        if scores[sheng_me] > scores[me_sheng]:
            yong_shen = sheng_me  # 用生我的五行扶身
            yong_shen_type = "扶身"
        else:
            yong_shen = me_sheng  # 用我生的五行生身
            yong_shen_type = "生身"
    
    # 找出对应的天干和地支
    yong_gan = []
    for gan in Gan:
        if gan5[gan] == yong_shen:
            yong_gan.append(gan)
    
    yong_zhi = []
    for zhi in Zhi:
        zhi_element = determine_zhi_element(zhi)
        if zhi_element == yong_shen:
            yong_zhi.append(zhi)
    
    # 神煞分析
    shens_analysis = analyze_shens(day_master, gans, zhis)
    
    # 特殊格局分析
    special_patterns = analyze_special_patterns(zhis)
    
    return {
        "day_master": day_master,
        "day_master_element": day_master_element,
        "strength": strength,
        "strongest_element": strongest_element,
        "weakest_element": weakest_element,
        "yong_shen": yong_shen,
        "yong_shen_type": yong_shen_type,
        "yong_gan": yong_gan,
        "yong_zhi": yong_zhi,
        "shens_analysis": shens_analysis,
        "special_patterns": special_patterns,
        "explanation": f"日主{day_master}为{day_master_element}，{strength}，用神为{yong_shen}({yong_shen_type})。"
    }

def analyze_shens(day_master, gans, zhis):
    """
    分析神煞
    
    参数:
        day_master (str): 日干
        gans (list): 四柱天干列表
        zhis (list): 四柱地支列表
    
    返回:
        dict: 神煞分析
    """
    # 简单分析一些常见的神煞
    analysis = {
        "positive": [],
        "negative": [],
        "special": []
    }
    
    # 检查天干十神
    for i, gan in enumerate(gans):
        if i == 2:  # 跳过日干
            continue
        
        relation = ten_deities[day_master][gan]
        if relation in ["正印", "偏印", "食神"]:
            analysis["positive"].append({
                "name": relation,
                "position": ["年", "月", "日", "时"][i],
                "element": gan5[gan]
            })
        elif relation in ["七杀", "正官", "伤官"]:
            analysis["negative"].append({
                "name": relation,
                "position": ["年", "月", "日", "时"][i],
                "element": gan5[gan]
            })
    
    # 检查特殊格局
    special_patterns = analyze_special_patterns(zhis)
    
    # 三合格局
    for pattern in special_patterns.get("san_he", []):
        analysis["special"].append({
            "name": pattern["name"],
            "description": pattern["description"],
            "impact": f"产生{pattern['element']}气，强化命盘中{pattern['element']}五行。"
        })
    
    # 三会格局
    for pattern in special_patterns.get("san_hui", []):
        analysis["special"].append({
            "name": pattern["name"],
            "description": pattern["description"],
            "impact": f"产生{pattern['element']}气，相互成就，命局中{pattern['element']}五行特征更为明显。"
        })
    
    # 冠带格局
    for pattern in special_patterns.get("guan_xin", []):
        analysis["special"].append({
            "name": pattern["name"],
            "description": pattern["description"],
            "impact": f"有利于事业发展学业——{pattern['name']}为人生添彩。"
        })
    
    # 冠带格局
    for pattern in special_patterns.get("guan_xin", []):
        analysis["special"].append({
            "name": pattern["name"],
            "description": pattern["description"],
            "impact": f"有利于事业发展学业——{pattern['name']}为人生添彩。"
        })
    
    return analysis


def check_sanhe(zhis):
    """
    检查是否有三合局
    
    参数:
        zhis (list): 四柱地支列表
    
    返回:
        str: 三合局类型，没有则返回空字符串
    """
    # 定义三合局
    sanhe = {
        "水": set(["申", "子", "辰"]),
        "木": set(["亥", "卯", "未"]),
        "火": set(["寅", "午", "戌"]),
        "金": set(["巳", "酉", "丑"])
    }
    
    # 将地支转为集合，检查是否包含三合局中的至少两个
    zhis_set = set(zhis)
    for element, zhi_set in sanhe.items():
        common = zhis_set.intersection(zhi_set)
        if len(common) >= 2:
            return element
    
    return ""


def analyze_special_patterns(zhis):
    """
    分析特殊地支格局（三会、三合、冠带等）
    
    参数:
        zhis (list): 四柱地支
        
    返回:
        dict: 格局分析结果
    """
    result = {
        "san_he": [],   # 三合
        "san_hui": [],  # 三会
        "chong": [],    # 冲
        "hui": [],      # 会
        "he": [],       # 合
        "guan_xin": []  # 冠心格局
    }
    
    # 检查三合格局
    san_he_patters = {
        "水三合": ["子", "申", "辰"],
        "木三合": ["亥", "卯", "未"],
        "火三合": ["寅", "午", "戌"],
        "金三合": ["巳", "酉", "丑"]
    }
    
    for pattern_name, pattern_zhis in san_he_patters.items():
        matched = [zhi for zhi in zhis if zhi in pattern_zhis]
        if len(matched) >= 2:  # 至少匹配两个
            element = pattern_name[0]  # 获取五行属性（第一个字）
            result["san_he"].append({
                "name": pattern_name,
                "element": element,
                "matched": matched,
                "description": f"有{pattern_name}矩阵，产生{element}气形成灵动合力。"
            })
    
    # 检查三会格局
    san_hui_patterns = {
        "东方三会": ["寅", "卯", "辰"],  # 东方木局
        "南方三会": ["巳", "午", "未"],  # 南方火局
        "西方三会": ["申", "酉", "戌"],  # 西方金局
        "北方三会": ["亥", "子", "丑"]   # 北方水局
    }
    
    for pattern_name, pattern_zhis in san_hui_patterns.items():
        matched = [zhi for zhi in zhis if zhi in pattern_zhis]
        if len(matched) >= 2:  # 至少匹配两个
            element = "木" if pattern_name.startswith("东") else \
                     "火" if pattern_name.startswith("南") else \
                     "金" if pattern_name.startswith("西") else "水"
            result["san_hui"].append({
                "name": pattern_name,
                "element": element,
                "matched": matched,
                "description": f"有{pattern_name}矩阵，产生{element}气彼此力量聚集。"
            })
            
    # 检查月柱冠带
    if "东" in zhis and "辰" in zhis:
        result["guan_xin"].append({
            "name": "冠带格局",
            "positions": ["卯", "辰"],
            "description": "卯冠辰带，为木火形为匠版，大利学业文文。"
        })
    
    return result

# 天干五行属性
gan5 = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

# 地支藏干（每个地支包含的天干及其权重）
zhi5 = {
    "子": {"癸": 10},
    "丑": {"己": 6, "癸": 4, "辛": 0},
    "寅": {"甲": 6, "丙": 4, "戊": 0},
    "卯": {"乙": 10},
    "辰": {"戊": 6, "乙": 4, "癸": 0},
    "巳": {"丙": 6, "戊": 4, "庚": 0},
    "午": {"丁": 6, "己": 4},
    "未": {"己": 6, "丁": 4, "乙": 0},
    "申": {"庚": 6, "壬": 4, "戊": 0},
    "酉": {"辛": 10},
    "戌": {"戊": 6, "辛": 4, "丁": 0},
    "亥": {"壬": 6, "甲": 4}
}

# 十神（日元与其他天干的关系）
ten_deities = {
    "甲": {"甲": "比肩", "乙": "劫财", "丙": "食神", "丁": "伤官", "戊": "偏财", "己": "正财", "庚": "七杀", "辛": "正官", "壬": "偏印", "癸": "正印"},
    "乙": {"甲": "劫财", "乙": "比肩", "丙": "伤官", "丁": "食神", "戊": "正财", "己": "偏财", "庚": "正官", "辛": "七杀", "壬": "正印", "癸": "偏印"},
    "丙": {"甲": "偏印", "乙": "正印", "丙": "比肩", "丁": "劫财", "戊": "食神", "己": "伤官", "庚": "偏财", "辛": "正财", "壬": "七杀", "癸": "正官"},
    "丁": {"甲": "正印", "乙": "偏印", "丙": "劫财", "丁": "比肩", "戊": "伤官", "己": "食神", "庚": "正财", "辛": "偏财", "壬": "正官", "癸": "七杀"},
    "戊": {"甲": "七杀", "乙": "正官", "丙": "偏印", "丁": "正印", "戊": "比肩", "己": "劫财", "庚": "食神", "辛": "伤官", "壬": "偏财", "癸": "正财"},
    "己": {"甲": "正官", "乙": "七杀", "丙": "正印", "丁": "偏印", "戊": "劫财", "己": "比肩", "庚": "伤官", "辛": "食神", "壬": "正财", "癸": "偏财"},
    "庚": {"甲": "偏财", "乙": "正财", "丙": "七杀", "丁": "正官", "戊": "偏印", "己": "正印", "庚": "比肩", "辛": "劫财", "壬": "食神", "癸": "伤官"},
    "辛": {"甲": "正财", "乙": "偏财", "丙": "正官", "丁": "七杀", "戊": "正印", "己": "偏印", "庚": "劫财", "辛": "比肩", "壬": "伤官", "癸": "食神"},
    "壬": {"甲": "食神", "乙": "伤官", "丙": "偏财", "丁": "正财", "戊": "七杀", "己": "正官", "庚": "偏印", "辛": "正印", "壬": "比肩", "癸": "劫财"},
    "癸": {"甲": "伤官", "乙": "食神", "丙": "正财", "丁": "偏财", "戊": "正官", "己": "七杀", "庚": "正印", "辛": "偏印", "壬": "劫财", "癸": "比肩"}
}

# 纳音五行
nayin_wuxing = {
    "甲子": "海中金", "乙丑": "海中金", "丙寅": "炉中火", "丁卯": "炉中火", "戊辰": "大林木", "己巳": "大林木",
    "庚午": "路旁土", "辛未": "路旁土", "壬申": "剑锋金", "癸酉": "剑锋金", "甲戌": "山头火", "乙亥": "山头火",
    "丙子": "涧下水", "丁丑": "涧下水", "戊寅": "城头土", "己卯": "城头土", "庚辰": "白蜡金", "辛巳": "白蜡金",
    "壬午": "杨柳木", "癸未": "杨柳木", "甲申": "泉中水", "乙酉": "泉中水", "丙戌": "屋上土", "丁亥": "屋上土",
    "戊子": "霹雳火", "己丑": "霹雳火", "庚寅": "松柏木", "辛卯": "松柏木", "壬辰": "长流水", "癸巳": "长流水",
    "甲午": "砂石金", "乙未": "砂石金", "丙申": "山下火", "丁酉": "山下火", "戊戌": "平地木", "己亥": "平地木",
    "庚子": "壁上土", "辛丑": "壁上土", "壬寅": "金薄金", "癸卯": "金薄金", "甲辰": "覆灯火", "乙巳": "覆灯火",
    "丙午": "天河水", "丁未": "天河水", "戊申": "大驿土", "己酉": "大驿土", "庚戌": "钗环金", "辛亥": "钗环金",
    "壬子": "桑柘木", "癸丑": "桑柘木", "甲寅": "大溪水", "乙卯": "大溪水", "丙辰": "沙中土", "丁巳": "沙中土",
    "戊午": "天上火", "己未": "天上火", "庚申": "石榴木", "辛酉": "石榴木", "壬戌": "大海水", "癸亥": "大海水"
}

# 年支神煞
year_shens = {
    "太岁": {"子": "子", "丑": "丑", "寅": "寅", "卯": "卯", "辰": "辰", "巳": "巳", "午": "午", "未": "未", "申": "申", "酉": "酉", "戌": "戌", "亥": "亥"},
    "劫煞": {"子": "未", "丑": "申", "寅": "酉", "卯": "戌", "辰": "亥", "巳": "子", "午": "丑", "未": "寅", "申": "卯", "酉": "辰", "戌": "巳", "亥": "午"},
    "灾煞": {"子": "酉", "丑": "戌", "寅": "亥", "卯": "子", "辰": "丑", "巳": "寅", "午": "卯", "未": "辰", "申": "巳", "酉": "午", "戌": "未", "亥": "申"},
    "岁煞": {"子": "戌", "丑": "辰", "寅": "丑", "卯": "未", "辰": "寅", "巳": "申", "午": "巳", "未": "亥", "申": "午", "酉": "寅", "戌": "酉", "亥": "辰"}
}

# 月支神煞
month_shens = {}

# 日干神煞
day_shens = {
    "日德": {"甲": ["巳"], "乙": ["午"], "丙": ["申"], "丁": ["酉"], "戊": ["申"], "己": ["酉"], "庚": ["亥"], "辛": ["子"], "壬": ["寅"], "癸": ["卯"]},
    "福神": {"甲": ["寅", "卯", "辰"], "乙": ["寅", "卯", "辰"], "丙": ["巳", "午", "未"], "丁": ["巳", "午", "未"], "戊": ["巳", "午", "未"], "己": ["巳", "午", "未"], "庚": ["申", "酉", "戌"], "辛": ["申", "酉", "戌"], "壬": ["亥", "子", "丑"], "癸": ["亥", "子", "丑"]},
    "喜神": {"甲": ["寅", "卯", "辰"], "乙": ["亥", "子", "丑"], "丙": ["巳", "午", "未"], "丁": ["寅", "卯", "辰"], "戊": ["申", "酉", "戌"], "己": ["巳", "午", "未"], "庚": ["亥", "子", "丑"], "辛": ["申", "酉", "戌"], "壬": ["寅", "卯", "辰"], "癸": ["亥", "子", "丑"]}
}


def calculate_bazi(birth_year, birth_month, birth_day, birth_hour, gender, city=None):
    """
    计算八字及相关信息
    
    参数:
        birth_year (int): 出生年
        birth_month (int): 出生月
        birth_day (int): 出生日
        birth_hour (int): 出生时（24小时制）
        gender (str): 性别 ('male'/'female')
        city (str, optional): 出生城市, 默认为None, 将通过IP获取当前位置
    
    返回:
        dict: 包含八字、四柱五行、流年、流月、大运、小运、神煞的字典
    """
    try:
        # 获取位置信息
        if city is None:
            latitude, longitude = get_default_location()
        else:
            if isinstance(city, str):
                geolocator = Nominatim(user_agent="curecipher")
                location = geolocator.geocode(city)
                if location:
                    latitude, longitude = location.latitude, location.longitude
                else:
                    # 如果找不到城市，使用默认值
                    print(f"找不到城市 {city}，使用默认值")
                    latitude, longitude = get_default_location()
            else:
                # 假设city是一个包含经纬度的元组或列表
                latitude, longitude = city
        
        # 创建Solar对象（阳历）
        solar = Solar.fromYmdHms(birth_year, birth_month, birth_day, birth_hour, 0, 0)
        # 注意: 新版lunar_python可能不支持设置经纬度
        # solar.setLongitude(longitude)
        # solar.setLatitude(latitude)
        
        # 转换为Lunar对象（阴历）
        lunar = solar.getLunar()
        
        # 获取八字
        bazi = lunar.getEightChar()
        year_gz = bazi.getYear()
        month_gz = bazi.getMonth()
        day_gz = bazi.getDay()
        hour_gz = bazi.getTime()
        
        # 提取天干地支
        year_gan = year_gz[0]
        year_zhi = year_gz[1]
        month_gan = month_gz[0]
        month_zhi = month_gz[1]
        day_gan = day_gz[0]
        day_zhi = day_gz[1]
        hour_gan = hour_gz[0]
        hour_zhi = hour_gz[1]
        
        # 构建四柱
        gans = [year_gan, month_gan, day_gan, hour_gan]
        zhis = [year_zhi, month_zhi, day_zhi, hour_zhi]
        
        # 日主
        me = day_gan
        
        # 计算天干十神
        gan_shens = []
        for item in gans:
            gan_shens.append(ten_deities[me][item])
        
        # 计算地支藏干十神
        zhi_shens = []
        for item in zhis:
            hidden_gans = zhi5[item]
            if hidden_gans:
                max_energy_gan = max(hidden_gans, key=hidden_gans.get)
                zhi_shens.append(ten_deities[me][max_energy_gan])
            else:
                zhi_shens.append("")
        
        # 计算地支全部藏干的十神
        zhi_shens_all = []
        for item in zhis:
            hidden_shens = []
            for gan, value in zhi5[item].items():
                if value > 0:  # 只考虑权重大于0的天干
                    hidden_shens.append(ten_deities[me][gan])
            zhi_shens_all.append(hidden_shens)
        
        # 计算五行得分
        scores = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
        
        # 天干五行得分
        for item in gans:
            scores[gan5[item]] += 5
        
        # 地支藏干五行得分
        for item in zhis:
            for gan, weight in zhi5[item].items():
                scores[gan5[gan]] += weight / 20  # 归一化
        
        # 检查空亡
        empties = []
        day_gz_str = day_gan + day_zhi
        for zhi in zhis:
            empty = get_empty(day_gz_str, zhi)
            empties.append(empty)
        
        # 检查天干合化
        gan_hes = check_gan_he(gans)
        
        # 计算大运
        gender_code = 1 if gender.lower() == "male" else 0
        try:
            # 尝试使用新API
            dayun_data = bazi.getDaYun(gender_code)
        except AttributeError:
            # 兼容处理：如果未找到getDaYun方法，创建一个空的大运列表
            # 不输出警告，静默处理
            dayun_data = []
        
        # 使用LunarExtension计算大运
        lunar_ext = LunarExtension(lunar=lunar)
        
        # 计算起运年龄和时间
        start_age = 0
        start_year = datetime.datetime.now().year
        
        # 处理大运数据
        dayuns = []
        gender_code = 1 if gender.lower() == "male" else 0
        
        try:
            # 使用lunar_extension计算大运
            dayun_list = lunar_ext.get_day_un(gender_code=gender_code)
            
            # 如果计算成功，处理大运数据
            if dayun_list:
                # 获取起运年龄
                if dayun_list and len(dayun_list) > 0:
                    start_age = dayun_list[0]['start_age']
                    start_year = birth_year + start_age
                
                # 处理大运数据
                for i, yun in enumerate(dayun_list):
                    dayun_gz = yun['gan_zhi']
                    dayun_start_age = yun['start_age']
                    dayun_end_age = yun['end_age']  # 结束年龄
                    
                    # 大运天干地支
                    dayun_gan = dayun_gz[0]
                    dayun_zhi = dayun_gz[1]
                    
                    # 大运天干地支的十神
                    dayun_gan_shen = ten_deities[me][dayun_gan]
                    
                    # 地支藏干
                    hidden_gans = zhi5[dayun_zhi]
                    if hidden_gans:
                        max_energy_gan = max(hidden_gans, key=hidden_gans.get)
                        dayun_zhi_shen = ten_deities[me][max_energy_gan]
                    else:
                        dayun_zhi_shen = ""
                    
                    # 生克关系
                    element_relation = gan5
                    
                    dayuns.append({
                        "ganzhi": dayun_gz,
                        "gan": dayun_gan,
                        "zhi": dayun_zhi,
                        "gan_shen": dayun_gan_shen,
                        "zhi_shen": dayun_zhi_shen,
                        "start_age": dayun_start_age,
                        "end_age": dayun_end_age,
                        "element": gan5[dayun_gan],
                        "nayin": nayin_wuxing.get(dayun_gz, "")
                    })
            
        except Exception as e:
            print(f"计算大运时出错: {e}")
            # 静默处理，不输出警告
            pass
        
        # 获取当前大运
        current_age = datetime.datetime.now().year - birth_year
        current_dayun = None
        
        if dayuns:  # 只有当大运列表非空时才进行处理
            for i, yun in enumerate(dayuns):
                if i < len(dayuns) - 1:
                    if yun["start_age"] <= current_age < dayuns[i+1]["start_age"]:
                        current_dayun = yun
                        break
                else:
                    if yun["start_age"] <= current_age:
                        current_dayun = yun
        
        # 当前年月日的流年流月流日
        current_date = datetime.datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        current_day = current_date.day
        
        lunar_current = Lunar.fromYmd(current_year, current_month, current_day)
        liunian_gz = lunar_current.getYearInGanZhi()
        liuyue_gz = lunar_current.getMonthInGanZhi()
        liuri_gz = lunar_current.getDayInGanZhi()
        
        liunian_gan = liunian_gz[0]
        liunian_zhi = liunian_gz[1]
        liuyue_gan = liuyue_gz[0]
        liuyue_zhi = liuyue_gz[1]
        liuri_gan = liuri_gz[0]
        liuri_zhi = liuri_gz[1]
        
        # 计算流年十神
        liunian_gan_shen = ten_deities[me][liunian_gan]
        liunian_zhi_shen = ten_deities[me][max(zhi5[liunian_zhi], key=zhi5[liunian_zhi].get)]
        
        # 计算流月十神
        liuyue_gan_shen = ten_deities[me][liuyue_gan]
        liuyue_zhi_shen = ten_deities[me][max(zhi5[liuyue_zhi], key=zhi5[liuyue_zhi].get)]
        
        # 计算流日十神
        liuri_gan_shen = ten_deities[me][liuri_gan]
        liuri_zhi_shen = ten_deities[me][max(zhi5[liuri_zhi], key=zhi5[liuri_zhi].get)]
        
        # 使用LunarExtension计算神煞
        shenshas = []
        try:
            # 计算神煞
            shensha_list = lunar_ext.get_shen_sha()
            if shensha_list:
                shenshas = shensha_list
        except Exception as e:
            print(f"计算神煞时出错: {e}")
            # 静默处理，不输出警告
            
            # 如果LunarExtension计算失败，使用传统方法计算常见神煞
            try:
                # 年神煞
                for shen_name, shen_dict in year_shens.items():
                    if year_zhi in shen_dict:
                        target = shen_dict[year_zhi]
                        for i, zhi in enumerate(zhis):
                            if zhi == target:
                                shenshas.append({
                                    "name": shen_name,
                                    "position": ["年", "月", "日", "时"][i],
                                    "description": f"{year_zhi}年{shen_name}{target}在{['年', '月', '日', '时'][i]}"
                                })
                                
                # 月神煞
                for shen_name, shen_dict in month_shens.items():
                    if month_zhi in shen_dict:
                        target = shen_dict[month_zhi]
                        for i, gan in enumerate(gans):
                            if gan == target:
                                shenshas.append({
                                    "name": shen_name,
                                    "position": ["年", "月", "日", "时"][i],
                                    "description": f"{month_zhi}月{shen_name}{target}在{['年', '月', '日', '时'][i]}"
                                })
                
                # 日神煞
                for shen_name, shen_dict in day_shens.items():
                    if day_gan in shen_dict:
                        targets = shen_dict[day_gan]
                        for target in targets:
                            for i, zhi in enumerate(zhis):
                                if zhi == target:
                                    shenshas.append({
                                        "name": shen_name,
                                        "position": ["年", "月", "日", "时"][i],
                                        "description": f"{day_gan}日{shen_name}{target}在{['年', '月', '日', '时'][i]}"
                                    })
            except Exception:
                # 如果传统方法也失败，则静默处理
                pass
        
        # 格局与用神分析
        pattern_info = determine_pattern(me, gans, zhis, gan_shens, zhi_shens, scores)
        
        # 纳音五行
        nayin = {
            "year": nayin_wuxing.get(year_gz, "未知"),
            "month": nayin_wuxing.get(month_gz, "未知"),
            "day": nayin_wuxing.get(day_gz, "未知"),
            "hour": nayin_wuxing.get(hour_gz, "未知")
        }
        
        # 使用LunarExtension计算命宫和胎元
        try:
            # 计算命宫
            ming_gong = lunar_ext.get_ming_gong()
        except Exception as e:
            print(f"计算命宫时出错: {e}")
            ming_gong = ""
            
        try:
            # 计算胎元
            tai_yuan = lunar_ext.get_tai_yuan()
        except Exception as e:
            print(f"计算胎元时出错: {e}")
            tai_yuan = ""
        
        # 返回结果
        result = {
            "bazi": {
                "year": year_gz,
                "month": month_gz,
                "day": day_gz,
                "hour": hour_gz,
                "gans": gans,
                "zhis": zhis,
                "day_master": me,
                "day_master_element": gan5[me]
            },
            "ten_gods": {
                "gans": gan_shens,
                "zhis": zhi_shens,
                "zhis_all": zhi_shens_all
            },
            "five_elements": {
                "scores": scores,
                "year": gan5[year_gan],
                "month": gan5[month_gan],
                "day": gan5[day_gan],
                "hour": gan5[hour_gan]
            },
            "relations": {
                "empties": empties,
                "gan_hes": gan_hes
            },
            "nayin": nayin,
            "special": {
                "ming_gong": ming_gong,
                "tai_yuan": tai_yuan
            },
            "pattern": pattern_info,
            "dayuns": dayuns,
            "current_dayun": current_dayun,
            "current": {
                "liunian": liunian_gz,
                "liunian_shen": {
                    "gan": liunian_gan_shen,
                    "zhi": liunian_zhi_shen
                },
                "liuyue": liuyue_gz,
                "liuyue_shen": {
                    "gan": liuyue_gan_shen,
                    "zhi": liuyue_zhi_shen
                },
                "liuri": liuri_gz,
                "liuri_shen": {
                    "gan": liuri_gan_shen,
                    "zhi": liuri_zhi_shen
                }
            },
            "shensha": shenshas,
            "solar": {
                "year": solar.getYear(),
                "month": solar.getMonth(),
                "day": solar.getDay(),
                "hour": solar.getHour()
            },
            "lunar": {
                "year": lunar.getYear(),
                "month": lunar.getMonth(),
                "day": lunar.getDay()
            },
            "location": {
                "city": city or "默认位置",
                "latitude": latitude,
                "longitude": longitude
            }
        }
        
        # 计算命盘分析附加信息
        # 五行得分权重调整（可根据具体需求调整）
        for element, score in scores.items():
            scores[element] = round(score, 2)
            
        # 分析日主旺衰
        day_master_score = scores[gan5[day_gan]]
        total_score = sum(scores.values())
        day_master_percentage = (day_master_score / total_score) * 100
        
        if day_master_percentage > 30:
            day_master_strength = "旺"
        elif day_master_percentage > 25:
            day_master_strength = "偏旺"
        elif day_master_percentage > 20:
            day_master_strength = "中和"
        elif day_master_percentage > 15:
            day_master_strength = "偏弱"
        else:
            day_master_strength = "弱"
            
        # 计算神煞信息更详细的分析
        shenshas_analysis = {}
        for shensha in shenshas:
            shensha_name = shensha.get("name")
            if shensha_name not in shenshas_analysis:
                shenshas_analysis[shensha_name] = {
                    "positions": [],
                    "descriptions": [],
                    "influences": []
                }
            
            shenshas_analysis[shensha_name]["positions"].append(shensha.get("position"))
            shenshas_analysis[shensha_name]["descriptions"].append(shensha.get("description"))
            
        # 添加详细分析到结果
        result["analysis"] = {
            "day_master_strength": day_master_strength,
            "day_master_percentage": round(day_master_percentage, 2),
            "elements_balance": get_elements_balance(scores),
            "shenshas": shenshas_analysis
        }
            
        return result
    
    except Exception as e:
        print(f"计算八字时出错: {e}")
        import traceback
        traceback.print_exc()
        return {
            "error": str(e),
            "message": "计算八字时出错，请检查输入参数和网络连接"
        }


def generate_text_report(report):
    """
    生成文本形式的命盘解读
    
    参数:
        report (dict): 命盘报告数据
    
    返回:
        str: 文本形式的命盘解读
    """
    lines = []
    
    # 基本信息
    lines.append("===== 八字命盘解读 =====\n")
    lines.append("[基本信息]")
    lines.append(f"四柱八字: {report['basic_info']['four_pillars']}")
    lines.append(f"天干: {report['basic_info']['gans']}")
    lines.append(f"地支: {report['basic_info']['zhis']}")
    lines.append(f"日主: {report['basic_info']['day_master']}")
    lines.append(f"阳历: {report['basic_info']['solar_date']}")
    lines.append(f"阴历: {report['basic_info']['lunar_date']}")
    lines.append("")
    
    # 命盘分析
    lines.append("[命盘分析]")
    lines.append(f"日主强度: {report['pattern_analysis']['day_master_strength']} ({report['pattern_analysis']['day_master_percentage']:.2f}%)")
    lines.append(f"五行平衡: {report['pattern_analysis']['balance_state']}")
    lines.append(f"备注: {report['pattern_analysis']['balance_description']}")
    lines.append(f"最强五行: {report['pattern_analysis']['strongest_element']}")
    lines.append(f"最弱五行: {report['pattern_analysis']['weakest_element']}")
    lines.append(f"用神: {report['pattern_analysis']['yong_shen']}")
    lines.append(f"用神说明: {report['pattern_analysis']['yong_shen_explanation']}")
    lines.append(f"用神天干: {report['pattern_analysis']['yong_gan']}")
    lines.append(f"用神地支: {report['pattern_analysis']['yong_zhi']}")
    lines.append("")
    
    # 当前大运
    lines.append("[当前大运]")
    if report['current_dayun']:
        current_dayun = report['current_dayun']
        lines.append(f"大运: {current_dayun['ganzhi']} {current_dayun['gan_shen']}{current_dayun['zhi_shen']}")
        lines.append(f"年龄范围: {current_dayun['age_range']} 岁")
        lines.append(f"纳音五行: {current_dayun['nayin']}")
    else:
        lines.append("尚未进入大运")
    lines.append("")
    
    # 流年流月流日
    lines.append("[当前流年流月流日]")
    lines.append(f"流年: {report['current_info']['liunian']['ganzhi']} 十神: {report['current_info']['liunian']['gan_shen']}/{report['current_info']['liunian']['zhi_shen']}")
    lines.append(f"流月: {report['current_info']['liuyue']['ganzhi']} 十神: {report['current_info']['liuyue']['gan_shen']}/{report['current_info']['liuyue']['zhi_shen']}")
    lines.append(f"流日: {report['current_info']['liuri']['ganzhi']} 十神: {report['current_info']['liuri']['gan_shen']}/{report['current_info']['liuri']['zhi_shen']}")
    lines.append("")
    
    # 神煞信息
    lines.append("[神煞信息]")
    if report['shensha_info']:
        for shensha in report['shensha_info']:
            lines.append(f"{shensha['name']}: {shensha['description']}")
    else:
        lines.append("无神煞信息")
    lines.append("")
    
    # 纳音五行
    lines.append("[纳音五行]")
    for position, nayin in report['nayin'].items():
        lines.append(f"{position}: {nayin}")
    lines.append("")
    
    # 特殊信息
    lines.append("[特殊信息]")
    lines.append(f"命宫: {report['special']['ming_gong']}")
    lines.append(f"胎元: {report['special']['tai_yuan']}")
    lines.append("")
    
    # 大运流年分析指导
    lines.append("[大运流年分析指导]")
    if report['pattern_analysis']['day_master_strength'] in ['旺', '偏旺']:
        # 日主旺的年份
        lines.append("日主过旺，适合濒身或耗身的运势：")
        lines.append(f"1. 法子：可选择{report['pattern_analysis']['yong_shen']}的年份，帮助平衡日主。")
        lines.append(f"2. 避免过于旺盛的日主({report['basic_info']['day_master'].split()[0]})年份。")
        lines.append(f"3. 理想的大运流年应有充足的{report['pattern_analysis']['yong_shen']}手法强。")
    elif report['pattern_analysis']['day_master_strength'] in ['弱', '偏弱']:
        # 日主弱的年份
        lines.append("日主过弱，适合滋身或扩张的运势：")
        lines.append(f"1. 法子：可选择{report['pattern_analysis']['yong_shen']}的年份，提升日主力量。")
        lines.append(f"2. 避免克法日主({report['basic_info']['day_master'].split()[0]})的年份。")
        lines.append(f"3. 理想的大运流年应有充足的{report['pattern_analysis']['yong_shen']}手法。")
    else:
        # 日主中和
        lines.append("日主强度适中，可选择平衡发展的运势：")
        lines.append(f"1. 保持当前的平衡状态，不过分強调任何五行。")
        lines.append("2. 可适当发展五行中较弱的部分。")
        lines.append("3. 避免增强已经过强的五行。")
    
    return "\n".join(lines)


def generate_bazi_report(bazi_result):
    """
    生成八字命盘解读报告

    参数:
        bazi_result (dict): calculate_bazi函数的返回结果

    返回:
        dict: 格式化的命盘解读报告
    """
    # 提取基本信息
    bazi = bazi_result['bazi']
    solar = bazi_result['solar']
    lunar = bazi_result['lunar']
    ten_gods = bazi_result['ten_gods']
    five_elements = bazi_result['five_elements']
    pattern = bazi_result['pattern']
    current = bazi_result['current']
    dayuns = bazi_result['dayuns']
    current_dayun = bazi_result['current_dayun']
    analysis = bazi_result['analysis']
    
    # 基本八字信息
    basic_info = {
        "four_pillars": f"{bazi['year']} {bazi['month']} {bazi['day']} {bazi['hour']}",
        "gans": ' '.join(bazi['gans']),
        "zhis": ' '.join(bazi['zhis']),
        "day_master": f"{bazi['day_master']} ({bazi['day_master_element']})",
        "solar_date": f"{solar['year']}年{solar['month']}月{solar['day']}日 {solar['hour']}时",
        "lunar_date": f"{lunar['year']}年{lunar['month']}月{lunar['day']}日"
    }
    
    # 命盘分析
    pattern_analysis = {
        "day_master_strength": analysis['day_master_strength'],
        "day_master_percentage": analysis['day_master_percentage'],
        "strongest_element": f"{analysis['elements_balance']['strongest']} ({analysis['elements_balance']['strongest_percentage']}%)",
        "weakest_element": f"{analysis['elements_balance']['weakest']} ({analysis['elements_balance']['weakest_percentage']}%)",
        "balance_state": analysis['elements_balance']['balance_state'],
        "balance_description": analysis['elements_balance']['description'],
        "yong_shen": f"{pattern['yong_shen']} ({pattern['yong_shen_type']})",
        "yong_shen_explanation": pattern['explanation'],
        "yong_gan": ', '.join(pattern['yong_gan']),
        "yong_zhi": ', '.join(pattern['yong_zhi']),
        "special_patterns": pattern['special_patterns']
    }
    
    # 大运分析
    dayun_analysis = []
    for dayun in dayuns:
        dayun_analysis.append({
            "ganzhi": dayun['ganzhi'],
            "gan_shen": dayun['gan_shen'],
            "zhi_shen": dayun['zhi_shen'],
            "age_range": f"{dayun['start_age']}-{dayun['end_age']}",
            "element": dayun['element'],
            "nayin": dayun['nayin']
        })

    current_dayun_info = None
    if current_dayun:
        current_dayun_info = {
            "ganzhi": current_dayun['ganzhi'],
            "gan_shen": current_dayun['gan_shen'],
            "zhi_shen": current_dayun['zhi_shen'],
            "age_range": f"{current_dayun['start_age']}-{current_dayun['end_age']}",
            "element": current_dayun['element'],
            "nayin": current_dayun['nayin']
        }

    # 当前流年流月流日
    current_info = {
        "liunian": {
            "ganzhi": current['liunian'],
            "gan_shen": current['liunian_shen']['gan'],
            "zhi_shen": current['liunian_shen']['zhi']
        },
        "liuyue": {
            "ganzhi": current['liuyue'],
            "gan_shen": current['liuyue_shen']['gan'],
            "zhi_shen": current['liuyue_shen']['zhi']
        },
        "liuri": {
            "ganzhi": current['liuri'],
            "gan_shen": current['liuri_shen']['gan'],
            "zhi_shen": current['liuri_shen']['zhi']
        }
    }

    # 神煞分析
    shensha_info = []
    for shensha in bazi_result['shensha']:
        shensha_info.append({
            "name": shensha['name'],
            "position": shensha['position'],
            "description": shensha['description']
        })

    # 搭建解读报告
    report = {
        "basic_info": basic_info,
        "five_elements": {
            "scores": five_elements['scores'],
            "year": five_elements['year'],
            "month": five_elements['month'],
            "day": five_elements['day'],
            "hour": five_elements['hour']
        },
        "ten_gods": {
            "gans": ten_gods['gans'],
            "zhis": ten_gods['zhis']
        },
        "pattern_analysis": pattern_analysis,
        "dayun_analysis": dayun_analysis,
        "current_dayun": current_dayun_info,
        "current_info": current_info,
        "shensha_info": shensha_info,
        "nayin": bazi_result['nayin'],
        "special": bazi_result['special']
    }

    # 生成文本形式的命盘解读
    text_report = generate_text_report(report)
    report["text_report"] = text_report

    return report


if __name__ == "__main__":
    # 测试代码
    print("\n\n===== 计算八字与命盘分析 =====")
    bazi_result = calculate_bazi(1990, 5, 15, 12, "male", "Beijing")
    
    # 生成报告
    report = generate_bazi_report(bazi_result)
    
    # 输出文本报告
    print(report["text_report"])
    
    # 测试特殊格局分析
    print("\n===== 特殊格局分析测试 =====")
    zhis = ["子", "申", "辰", "酉"]
    patterns = analyze_special_patterns(zhis)
    print(f"\n分析地支: {', '.join(zhis)}")
    print("\n三合格局:")
    for p in patterns['san_he']:
        print(f"  - {p['name']}: {p['description']}")
    print("\n三会格局:")
    for p in patterns['san_hui']:
        print(f"  - {p['name']}: {p['description']}")
