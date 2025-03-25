def analyze_shensha(shensha_list, gua_element, day_master_strength="neutral", flow_year_element="金", mode="liuyao", najia_data=None):
    positive_impacts = []
    negative_impacts = []
    health_advice = []
    god6_impacts = []

    # 五行映射
    element_map = {"metal": "金", "wood": "木", "water": "水", "fire": "火", "earth": "土"}
    gua_element_mapped = element_map.get(gua_element.lower(), gua_element)
    flow_year_element_mapped = element_map.get(flow_year_element.lower(), flow_year_element)

    # 六神影响映射
    god6_effects = {
        "青龙": {"effect": "吉，利于行动和决策", "health": "精神焕发"},
        "朱雀": {"effect": "中性，注意口舌是非", "health": "可能口干舌燥"},
        "勾陈": {"effect": "中性，宜稳重", "health": "可能消化不佳"},
        "螣蛇": {"effect": "中性，注意精神压力", "health": "可能焦虑"},
        "白虎": {"effect": "凶，注意冲突和伤害", "health": "可能外伤"},
        "玄武": {"effect": "中性，注意隐疾", "health": "可能肾虚"}
    }

    # 动爻位置与身体部位的映射
    yao_position_effects = {
        0: {"position": "初爻", "body_part": "下焦（肾、膀胱、足部）", "health_impact": "可能影响肾功能或下肢"},
        1: {"position": "二爻", "body_part": "下腹（生殖系统、大肠）", "health_impact": "可能影响生殖或排泄"},
        2: {"position": "三爻", "body_part": "中焦（脾胃、腰部）", "health_impact": "可能影响消化或腰部"},
        3: {"position": "四爻", "body_part": "胸部（心肺）", "health_impact": "可能影响心肺功能"},
        4: {"position": "五爻", "body_part": "上焦（头颈、肩部）", "health_impact": "可能影响头部或肩颈"},
        5: {"position": "上爻", "body_part": "头部（脑部、面部）", "health_impact": "可能影响头部或精神状态"}
    }

    # 变卦五行
    bian_gua_element = gua_element_mapped
    if najia_data and "bian" in najia_data and najia_data["bian"]["name"]:
        bian_gua_name = najia_data["bian"]["name"]
        gua_element_map = {
            '乾为天': '金', '天风姤': '金', '天山遁': '金', '天地否': '金',
            '风地观': '金', '山地剥': '金', '火地晋': '金', '火天大有': '金',
            '坎为水': '水', '水泽节': '水', '水雷屯': '水', '水火既济': '水',
            '泽火革': '水', '雷火丰': '水', '地火明夷': '水', '地水师': '水',
            '艮为山': '土', '山火贲': '土', '山天大畜': '土', '山泽损': '土',
            '火泽睽': '土', '天泽履': '土', '风泽中孚': '土', '风山渐': '土',
            '震为雷': '木', '雷地豫': '木', '雷水解': '木', '雷风恒': '木',
            '地风升': '木', '水风井': '木', '泽风大过': '木', '泽雷随': '木',
            '巽为风': '木', '风天小畜': '木', '风火家人': '木', '风雷益': '木',
            '天雷无妄': '木', '火雷噬嗑': '木', '山雷颐': '木', '山风蛊': '木',
            '离为火': '火', '火山旅': '火', '火风鼎': '火', '火水未济': '火',
            '山水蒙': '火', '风水涣': '火', '天水讼': '火', '天火同人': '火',
            '坤为地': '土', '地雷复': '土', '地泽临': '土', '地天泰': '土',
            '雷天大壮': '土', '泽天夬': '土', '水天需': '土', '水地比': '土',
            '兑为泽': '金', '泽水困': '金', '泽地萃': '金', '泽山咸': '金',
            '水山蹇': '金', '地山谦': '金', '雷山小过': '金', '雷泽归妹': '金'
        }
        bian_gua_element = gua_element_map.get(bian_gua_name, gua_element_mapped)

    # 分析神煞
    for shensha in shensha_list:
        shensha_data = None
        shensha_type = None
        if shensha in najia_data["shensha_data"]["positive"]:
            shensha_data = najia_data["shensha_data"]["positive"][shensha]
            shensha_type = "positive"
        elif shensha in najia_data["shensha_data"]["negative"]:
            shensha_data = najia_data["shensha_data"]["negative"][shensha]
            shensha_type = "negative"

        if not shensha_data:
            continue

        # 确定健康影响
        day_master_key = f"day_master_{day_master_strength.lower()}"
        health_impact = shensha_data["health_aspects"].get(day_master_key, ["无特定影响"])

        # 确定流年影响（考虑五行相生相克）
        shensha_element = shensha_data["element"]
        flow_year_effect = "中性"
        if flow_year_element_mapped in [element_map.get(e, e) for e in shensha_data["flow_year_boost"]]:
            flow_year_effect = "增强"
        elif flow_year_element_mapped in [element_map.get(e, e) for e in shensha_data["flow_year_suppress"]]:
            flow_year_effect = "减弱"
        else:
            # 考虑五行相生相克
            five_elements_interaction = {
                ("金", "木"): "减弱",  # 木克金
                ("木", "土"): "减弱",  # 木克土
                ("土", "水"): "减弱",  # 土克水
                ("水", "火"): "减弱",  # 水克火
                ("火", "金"): "减弱",  # 火克金
                ("木", "金"): "增强",  # 金克木
                ("土", "木"): "增强",  # 土克木
                ("水", "土"): "增强",  # 水克土
                ("火", "水"): "增强",  # 火克水
                ("金", "火"): "增强",  # 金克火
                ("金", "水"): "增强",  # 金生水
                ("水", "木"): "增强",  # 水生木
                ("木", "火"): "增强",  # 木生火
                ("火", "土"): "增强",  # 火生土
                ("土", "金"): "增强",  # 土生金
            }
            interaction_key = (shensha_element, flow_year_element_mapped)
            interaction_key_reverse = (flow_year_element_mapped, shensha_element)
            if interaction_key in five_elements_interaction:
                flow_year_effect = five_elements_interaction[interaction_key]
            elif interaction_key_reverse in five_elements_interaction:
                flow_year_effect = five_elements_interaction[interaction_key_reverse]

        # 考虑变卦五行的影响
        if bian_gua_element != gua_element_mapped:
            five_elements_interaction = {
                ("金", "木"): "木克金，可能加重呼吸系统问题",
                ("金", "水"): "水生金，可能缓解呼吸系统问题",
                ("金", "火"): "火克金，可能加重心肺问题",
                ("金", "土"): "金生土，可能缓解消化问题",
                ("木", "金"): "木克金，可能加重呼吸系统问题",
                ("木", "水"): "水生木，可能缓解肝胆问题",
                ("木", "火"): "木生火，可能加重心血管问题",
                ("木", "土"): "木克土，可能加重脾胃问题",
                ("土", "金"): "土生金，可能缓解呼吸系统问题",
                ("土", "木"): "木克土，可能加重脾胃问题",
                ("土", "水"): "土克水，可能加重肾脏问题",
                ("土", "火"): "火生土，可能缓解心血管问题",
                ("水", "土"): "土克水，可能加重肾脏问题",
                ("水", "木"): "水生木，可能缓解肝胆问题",
                ("水", "火"): "水克火，可能加重心血管问题",
                ("水", "金"): "金生水，可能缓解肾脏问题",
                ("火", "土"): "火生土，可能缓解脾胃问题",
                ("火", "水"): "水克火，可能加重心血管问题",
                ("火", "金"): "火克金，可能加重呼吸系统问题",
                ("火", "木"): "木生火，可能加重心血管问题",
            }
            interaction_key = (gua_element_mapped, bian_gua_element)
            interaction_effect = five_elements_interaction.get(interaction_key, "五行影响中性")
            health_impact.append(interaction_effect)

        # 考虑动爻位置的影响
        if najia_data and "dong" in najia_data and najia_data["dong"]:
            for dong_yao in najia_data["dong"]:
                if dong_yao in yao_position_effects:
                    health_impact.append(f"{yao_position_effects[dong_yao]['health_impact']}（{yao_position_effects[dong_yao]['body_part']}）")

        # 确定日主亲和性
        day_master_affinity = "高" if gua_element_mapped in [element_map.get(e, e) for e in shensha_data["element_affinity"]] else "一般"

        # 构建神煞影响
        impact = {
            "name": shensha,
            "description": shensha_data["description"],
            "impact": shensha_data["impact"],
            "health": health_impact,
            "element": shensha_element,
            "day_master_affinity": day_master_affinity,
            "flow_year_effect": flow_year_effect,
            "remedy": shensha_data.get("remedy", [])
        }

        if shensha_type == "positive":
            positive_impacts.append(impact)
        else:
            negative_impacts.append(impact)

    # 分析健康建议
    health_advice = []
    for impact in positive_impacts + negative_impacts:
        if impact["health"] != ["无特定影响"] and impact["remedy"]:
            remedies = ", ".join(impact["remedy"]) if impact["remedy"] else "暂无具体建议"
            health_advice.append(
                f"{impact['name']}({impact['flow_year_effect']})可能导致{', '.join(impact['health'])}，"
                f"流年{impact['flow_year_effect']}其影响，建议：{remedies}。"
            )

    # 分析六神影响
    if najia_data and "god6" in najia_data:
        for god in najia_data["god6"]:
            if god in god6_effects:
                god6_impacts.append({
                    "name": god,
                    "effect": god6_effects[god]["effect"],
                    "health": god6_effects[god]["health"]
                })

    # 确定受影响的身体系统
    body_systems = []
    element_to_systems = {
        "金": ["肺", "大肠", "呼吸系统", "皮肤"],
        "木": ["肝", "胆", "神经系统"],
        "水": ["肾", "膀胱", "生殖系统"],
        "火": ["心", "小肠", "循环系统"],
        "土": ["脾", "胃", "消化系统"]
    }
    for impact in negative_impacts:
        shensha_element_mapped = element_map.get(impact["element"].lower(), impact["element"])
        if shensha_element_mapped in element_to_systems:
            body_systems.extend(element_to_systems[shensha_element_mapped])
    if bian_gua_element in element_to_systems:
        body_systems.extend(element_to_systems[bian_gua_element])
    body_systems = list(set(body_systems))  # 去重

    # 计算流年影响
    positive_enhanced = sum(1 for impact in positive_impacts if impact["flow_year_effect"] == "增强")
    positive_weakened = sum(1 for impact in positive_impacts if impact["flow_year_effect"] == "减弱")
    negative_enhanced = sum(1 for impact in negative_impacts if impact["flow_year_effect"] == "增强")
    negative_weakened = sum(1 for impact in negative_impacts if impact["flow_year_effect"] == "减弱")

    # 整体分析
    overall_analysis = {
        "positive_count": len(positive_impacts),
        "negative_count": len(negative_impacts),
        "tendency": "非常凶险" if len(negative_impacts) > len(positive_impacts) else "中性",
        "day_master_impact": "凶神相性较强，不利于日主健康" if len(negative_impacts) > 0 else "中性",
        "flow_year_impact": "流年增强" if (positive_enhanced + negative_enhanced) > (positive_weakened + negative_weakened) else "流年减弱" if (positive_weakened + negative_weakened) > (positive_enhanced + negative_enhanced) else "流年中性",
        "positive_enhanced": positive_enhanced,
        "positive_weakened": positive_weakened,
        "negative_enhanced": negative_enhanced,
        "negative_weakened": negative_weakened,
        "health_analysis": {
            "overall_status": "总体健康状况有待改善" if len(negative_impacts) > 0 else "总体健康状况良好",
            "focus_advice": "需要特别关注以下健康方面:",
            "health_strengths": [h for impact in positive_impacts for h in impact["health"] if impact["health"] != ["无特定影响"]],
            "health_weaknesses": [h for impact in negative_impacts for h in impact["health"] if impact["health"] != ["无特定影响"]],
            "body_systems_to_focus": body_systems
        }
    }

    return {
        "positive_impacts": positive_impacts,
        "negative_impacts": negative_impacts,
        "health_advice": health_advice,
        "overall_analysis": overall_analysis,
        "god6_impacts": god6_impacts
    }