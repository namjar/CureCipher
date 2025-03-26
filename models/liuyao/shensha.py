import json
from pathlib import Path

# 五行生克关系
WUXING_RELATIONS = {
    "金": {"generates": "水", "restricts": "木"},
    "木": {"generates": "火", "restricts": "土"},
    "水": {"generates": "木", "restricts": "火"},
    "火": {"generates": "土", "restricts": "金"},
    "土": {"generates": "金", "restricts": "水"}
}

# 动爻位置与身体部位
YAO_BODY_PARTS = {
    0: {"position": "初爻", "body": "足部/肾脏", "system": "水"},
    1: {"position": "二爻", "body": "腿部/生殖", "system": "水"},
    2: {"position": "三爻", "body": "腰部/脾胃", "system": "土"},
    3: {"position": "四爻", "body": "胸部/心肺", "system": "火"},
    4: {"position": "五爻", "body": "肩颈/喉咙", "system": "金"},
    5: {"position": "上爻", "body": "头部/脑部", "system": "火"}
}

# 六亲健康影响
QIN6_EFFECTS = {
    "父母": {"health": "肺部/呼吸", "system": "金"},
    "兄弟": {"health": "肝胆/神经", "system": "木"},
    "官鬼": {"health": "心血管", "system": "火"},
    "妻财": {"health": "脾胃/消化", "system": "土"},
    "子孙": {"health": "肾脏/生殖", "system": "水"}
}

# 六神健康影响
GOD6_EFFECTS = {
    "青龙": {"effect": "精神焕发", "system": "木"},
    "朱雀": {"effect": "口舌不适", "system": "火"},
    "勾陈": {"effect": "消化不良", "system": "土"},
    "螣蛇": {"effect": "焦虑紧张", "system": "火"},
    "白虎": {"effect": "外伤风险", "system": "金"},
    "玄武": {"effect": "肾虚隐疾", "system": "水"}
}

# 调理建议模板
REMEDIES = {
    "金": ["深呼吸练习", "辛味食物（如葱姜）", "按摩肺经（太渊穴）"],
    "木": ["舒展运动（如瑜伽）", "酸味食物（如山楂）", "按摩肝经（太冲穴）"],
    "水": ["游泳或静坐", "咸味食物（如海带）", "按摩肾经（太溪穴）"],
    "火": ["有氧运动（如慢跑）", "苦味食物（如苦瓜）", "按摩心经（神门穴）"],
    "土": ["散步或八段锦", "甘味食物（如红枣）", "按摩脾经（足三里）"]
}

# 地支五行映射
ZHI_ELEMENTS = {
    "寅": "木", "卯": "木",
    "巳": "火", "午": "火",
    "申": "金", "酉": "金",
    "亥": "水", "子": "水",
    "辰": "土", "戌": "土",
    "丑": "土", "未": "土"
}

def load_shensha_data():
    data_file = Path(__file__).parent.parent.parent / "data" / "shensha_impacts.json"
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"找不到shensha_impacts.json文件，请确保文件存在于{data_file}: {e}")
    except Exception as e:
        raise Exception(f"加载shensha_impacts.json时出错: {e}")

def calculate_shensha_zhi(shensha_name, day_gan, day_zhi):
    """计算神煞对应的地支"""
    # 天乙贵人（以日干查）
    tianyi_gui = {
        "甲": ["丑", "未"], "乙": ["申", "子"], "丙": ["寅", "亥"], "丁": ["酉", "亥"],
        "戊": ["丑", "未"], "己": ["申", "子"], "庚": ["卯", "巳"], "辛": ["午", "寅"],
        "壬": ["卯", "巳"], "癸": ["亥", "酉"]
    }
    # 福星贵人（以日干查）
    fuxing_gui = {
        "甲": ["寅"], "乙": ["卯"], "丙": ["巳"], "丁": ["午"],
        "戊": ["巳"], "己": ["午"], "庚": ["申"], "辛": ["酉"],
        "壬": ["亥"], "癸": ["子"]
    }
    # 国印贵人（以日干查）
    guoyin_gui = {
        "甲": ["戌"], "乙": ["亥"], "丙": ["丑"], "丁": ["寅"],
        "戊": ["丑"], "己": ["寅"], "庚": ["辰"], "辛": ["巳"],
        "壬": ["未"], "癸": ["申"]
    }
    # 金舆（以日干查）
    jin_yu = {
        "甲": ["辰"], "乙": ["巳"], "丙": ["未"], "丁": ["申"],
        "戊": ["未"], "己": ["申"], "庚": ["戌"], "辛": ["亥"],
        "壬": ["丑"], "癸": ["寅"]
    }
    # 华盖（以日支查）
    huagai = {
        "寅": ["戌"], "午": ["戌"], "戌": ["戌"],
        "申": ["辰"], "子": ["辰"], "辰": ["辰"],
        "亥": ["未"], "卯": ["未"], "未": ["未"],
        "巳": ["丑"], "酉": ["丑"], "丑": ["丑"]
    }
    # 天医（以日支近似）
    tianyi = {
        "寅": ["丑"], "卯": ["寅"], "辰": ["卯"], "巳": ["辰"],
        "午": ["巳"], "未": ["午"], "申": ["未"], "酉": ["申"],
        "戌": ["酉"], "亥": ["戌"], "子": ["亥"], "丑": ["子"]
    }
    # 白虎（以日支查）
    baihu = {
        "寅": ["寅"], "午": ["寅"], "戌": ["寅"],
        "申": ["申"], "子": ["申"], "辰": ["申"],
        "亥": ["亥"], "卯": ["亥"], "未": ["亥"],
        "巳": ["巳"], "酉": ["巳"], "丑": ["巳"]
    }
    # 亡神（以日支查）
    wangshen = {
        "寅": ["亥"], "午": ["亥"], "戌": ["亥"],
        "申": ["巳"], "子": ["巳"], "辰": ["巳"],
        "亥": ["申"], "卯": ["申"], "未": ["申"],
        "巳": ["寅"], "酉": ["寅"], "丑": ["寅"]
    }
    # 飞刃（以日干查）
    feiren = {
        "甲": ["酉"], "乙": ["戌"], "丙": ["子"], "丁": ["丑"],
        "戊": ["卯"], "己": ["辰"], "庚": ["午"], "辛": ["未"],
        "壬": ["酉"], "癸": ["戌"]
    }
    # 吊客（以日支查）
    diaoke = {
        "寅": ["酉"], "午": ["酉"], "戌": ["酉"],
        "申": ["卯"], "子": ["卯"], "辰": ["卯"],
        "亥": ["午"], "卯": ["午"], "未": ["午"],
        "巳": ["子"], "酉": ["子"], "丑": ["子"]
    }

    # 根据神煞名称选择计算规则
    if shensha_name in ["天乙贵人", "太极贵人"]:  # 兼容太极贵人
        return tianyi_gui.get(day_gan, [])
    elif shensha_name == "福星贵人":
        return fuxing_gui.get(day_gan, [])
    elif shensha_name == "国印贵人":
        return guoyin_gui.get(day_gan, [])
    elif shensha_name == "金舆":
        return jin_yu.get(day_gan, [])
    elif shensha_name == "华盖":
        return huagai.get(day_zhi, [])
    elif shensha_name == "天医":
        return tianyi.get(day_zhi, [])
    elif shensha_name == "白虎":
        return baihu.get(day_zhi, [])
    elif shensha_name == "亡神":
        return wangshen.get(day_zhi, [])
    elif shensha_name == "飞刃":
        return feiren.get(day_gan, [])
    elif shensha_name == "吊客":
        return diaoke.get(day_zhi, [])
    return []

def analyze_shensha(shensha_list, gua_element, day_master_strength="neutral", flow_year_element="金", mode="liuyao", najia_data=None):
    shensha_data = load_shensha_data()
    positive_impacts = []
    negative_impacts = []
    health_advice = []
    god6_impacts = []
    dong_yao_health = []
    dong_yao_remedies = []

    # 提取日干和日支
    day_gan = najia_data["lunar"]["gz"]["day"][0] if najia_data and "lunar" in najia_data else "癸"
    day_zhi = najia_data["lunar"]["gz"]["day"][1] if najia_data and "lunar" in najia_data else "巳"

    # 动爻分析
    dong_yao_effects = []
    if najia_data and "dong" in najia_data and najia_data["dong"]:
        for dong_idx in najia_data["dong"]:
            yao = YAO_BODY_PARTS[dong_idx]
            qin6 = najia_data["qin6"][dong_idx]
            god6 = najia_data["god6"][dong_idx]
            qin_effect = QIN6_EFFECTS.get(qin6, {"health": "未知", "system": gua_element})
            god_effect = GOD6_EFFECTS.get(god6, {"effect": "未知", "system": gua_element})
            health_impact = f"{qin_effect['health']}可能受影响，{god_effect['effect']}"
            dong_yao_effects.append({
                "position": yao["position"],
                "body": yao["body"],
                "health": health_impact,
                "system": qin_effect["system"],
                "god6": god_effect["effect"]
            })
            dong_yao_health.append(f"{qin_effect['health']}可能受影响（{yao['body']}），{god_effect['effect']}")
            dong_yao_remedies.extend(REMEDIES.get(yao["system"], []))
            dong_yao_remedies.extend(REMEDIES.get(god_effect["system"], []))

    # 变卦五行分析
    bian_gua_element = gua_element
    if najia_data and "bian" in najia_data and "name" in najia_data["bian"]:
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
        bian_gua_element = gua_element_map.get(najia_data["bian"]["name"], gua_element)

    # 变卦五行影响
    bian_effect = ""
    if bian_gua_element != gua_element:
        if WUXING_RELATIONS[gua_element]["generates"] == bian_gua_element:
            bian_effect = f"{gua_element}生{bian_gua_element}，相关系统功能增强，但可能亢奋。"
        elif WUXING_RELATIONS[gua_element]["restricts"] == bian_gua_element:
            bian_effect = f"{gua_element}克{bian_gua_element}，相关系统受抑，需调理。"
        elif WUXING_RELATIONS[bian_gua_element]["restricts"] == gua_element:
            bian_effect = f"{bian_gua_element}克{gua_element}，本卦系统受损，需关注。"
    else:
        if najia_data and "params" in najia_data:
            dong_idx = najia_data["dong"][0] if najia_data["dong"] else -1
            if dong_idx >= 0:
                param = najia_data["params"][dong_idx]
                if param == 3:  # 老阳（阳变阴）
                    bian_effect = f"动爻阳变阴，金气减弱，肺部功能可能下降。"
                elif param == 4:  # 老阴（阴变阳）
                    bian_effect = f"动爻阴变阳，金气增强，肺部功能可能亢奋。"
                else:
                    bian_effect = f"动爻五行与本卦相同，金系统影响加剧。"

    if dong_yao_effects:
        dong_system = dong_yao_effects[0]["system"]
        if dong_system == gua_element:
            bian_effect += f" 动爻五行与本卦相同，{dong_system}系统影响加剧。"
        elif dong_system == bian_gua_element:
            bian_effect += f" 动爻五行与变卦相同，{dong_system}系统变化更显著。"

    # 提取爻位地支
    yao_zhi = najia_data["zhi"] if najia_data and "zhi" in najia_data else ["丑", "亥", "酉", "未", "巳", "卯"]

    # 神煞分析
    for shensha in shensha_list:
        data = shensha_data["positive"].get(shensha) or shensha_data["negative"].get(shensha)
        if not data:
            continue
        shensha_type = "positive" if shensha in shensha_data["positive"] else "negative"

        # 计算神煞地支
        shensha_zhi = calculate_shensha_zhi(shensha, day_gan, day_zhi)

        # 流年影响
        flow_effect = "中性"
        if flow_year_element in data["flow_year_boost"]:
            flow_effect = "增强"
        elif flow_year_element in data["flow_year_suppress"]:
            flow_effect = "减弱"

        # 匹配爻位地支
        matched_yao = []
        for zhi in shensha_zhi:
            for idx, yz in enumerate(yao_zhi):
                if zhi == yz:
                    yao_info = YAO_BODY_PARTS[idx]
                    qin6 = najia_data["qin6"][idx] if najia_data and "qin6" in najia_data else "未知"
                    qin_effect = QIN6_EFFECTS.get(qin6, {"health": "未知", "system": "未知"})
                    matched_yao.append({
                        "position": yao_info["position"],
                        "body": yao_info["body"],
                        "qin_health": qin_effect["health"],
                        "system": qin_effect["system"],
                        "zhi": zhi
                    })

        # 健康影响
        health = data["health_aspects"].get(f"day_master_{day_master_strength}", ["无特定影响"])
        specific_health = []
        for match in matched_yao:
            base_health = health[0] if health else "无特定影响"
            specific_desc = f"{base_health}（{match['body']}，{match['qin_health']}相关）"
            specific_health.append(specific_desc)
        if not specific_health:
            specific_health = health

        # 默认建议
        remedy = data.get("remedy", REMEDIES.get(data["element"], []))

        impact = {
            "name": shensha,
            "description": data["description"],
            "zhi": shensha_zhi,
            "matched_yao": matched_yao,
            "health": specific_health,
            "flow_year_effect": flow_effect,
            "remedy": remedy
        }
        if shensha_type == "positive":
            positive_impacts.append(impact)
        else:
            negative_impacts.append(impact)

    # 六神影响
    if najia_data and "god6" in najia_data:
        for idx, god in enumerate(najia_data["god6"]):
            if god in GOD6_EFFECTS and idx in najia_data["dong"]:
                effect = GOD6_EFFECTS[god]
                god6_impacts.append({
                    "name": god,
                    "effect": effect["effect"],
                    "health": f"{effect['effect']}（{YAO_BODY_PARTS[idx]['body']}）"
                })

    # 健康建议
    for impact in positive_impacts + negative_impacts:
        if impact["health"] != ["无特定影响"]:
            remedies = ", ".join(impact["remedy"]) if impact["remedy"] else "暂无具体建议"
            zhi_str = "、".join(impact["zhi"]) if impact["zhi"] else "无地支"
            health_advice.append(f"{impact['name']}（{zhi_str}，{impact['flow_year_effect']}）：{', '.join(impact['health'])}，建议：{remedies}")

    # 整体分析
    overall = {
        "dong_yao": dong_yao_effects,
        "bian_gua_effect": bian_effect,
        "positive_count": len(positive_impacts),
        "negative_count": len(negative_impacts),
        "health_status": "需关注" if len(negative_impacts) > len(positive_impacts) else "平稳"
    }

    return {
        "positive_impacts": positive_impacts,
        "negative_impacts": negative_impacts,
        "health_advice": health_advice,
        "god6_impacts": god6_impacts,
        "overall_analysis": overall,
        "dong_yao_health": dong_yao_health,
        "dong_yao_remedies": dong_yao_remedies
    }