"""
八字命盘报告生成模块
生成八字命盘分析报告和文本解读
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
        "yong_zhi": ', '.join(pattern['yong_zhi'])
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
    # 测试代码 - 需要导入bazi_calculator模块才能运行
    try:
        from bazi_calculator import calculate_bazi
        
        print("\n\n===== 测试八字命盘报告生成 =====")
        bazi_result = calculate_bazi(1990, 5, 15, 12, "male", "Beijing")
        
        # 生成报告
        report = generate_bazi_report(bazi_result)
        
        # 输出文本报告
        print(report["text_report"])
    except ImportError:
        print("请先导入bazi_calculator模块")
