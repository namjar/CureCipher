"""
八宫卦数据模块 - 提供六爻八宫卦数据及相关信息
"""

from typing import Dict, List, Tuple, Any

# 八宫卦表数据
BAGONG_GUA_DATA = {
    "乾宫": [
        {
            "name": "乾为天",
            "alias": "乾卦",
            "gua_type": "本宫卦",
            "xiang": "天",
            "yao_array": [1, 1, 1, 1, 1, 1],
            "description": "刚健中正"
        },
        {
            "name": "天风姤",
            "alias": "姤卦",
            "gua_type": "一世卦",
            "xiang": "天下有风",
            "yao_array": [1, 1, 1, 0, 1, 1],
            "description": "天下有风，姤；后以施命诰四方"
        },
        {
            "name": "天山遁",
            "alias": "遁卦",
            "gua_type": "二世卦",
            "xiang": "天下有山",
            "yao_array": [1, 1, 1, 0, 0, 1],
            "description": "天下有山，遁；君子以远小人，不恶而严"
        },
        {
            "name": "天地否",
            "alias": "否卦",
            "gua_type": "三世卦",
            "xiang": "天地不交",
            "yao_array": [1, 1, 1, 0, 0, 0],
            "description": "天地不交，否；君子以俭德辟难，不可荣以禄"
        },
        {
            "name": "风地观",
            "alias": "观卦",
            "gua_type": "四世卦",
            "xiang": "风行地上",
            "yao_array": [0, 1, 1, 0, 0, 0],
            "description": "风行地上，观；先王以省方，观民设教"
        },
        {
            "name": "山地剥",
            "alias": "剥卦",
            "gua_type": "五世卦",
            "xiang": "山附于地",
            "yao_array": [0, 0, 1, 0, 0, 0],
            "description": "山附于地，剥；上以厚下，安宅"
        },
        {
            "name": "火地晋",
            "alias": "晋卦",
            "gua_type": "游魂卦",
            "xiang": "日出地上",
            "yao_array": [1, 0, 1, 0, 0, 0],
            "description": "日出地上，晋；君子以自昭明德"
        },
        {
            "name": "火天大有",
            "alias": "大有卦",
            "gua_type": "归魂卦",
            "xiang": "火在天上",
            "yao_array": [1, 0, 1, 1, 1, 1],
            "description": "火在天上，大有；君子以遏恶扬善，顺天休命"
        }
    ],
    "坎宫": [
        {
            "name": "坎为水",
            "alias": "坎卦",
            "gua_type": "本宫卦",
            "xiang": "水",
            "yao_array": [0, 1, 0, 0, 1, 0],
            "description": "险陷重重"
        },
        {
            "name": "水泽节",
            "alias": "节卦",
            "gua_type": "一世卦",
            "xiang": "水上有泽",
            "yao_array": [0, 1, 0, 1, 1, 0],
            "description": "水在泽中，节；君子以制数度，议德行"
        },
        {
            "name": "水雷屯",
            "alias": "屯卦",
            "gua_type": "二世卦",
            "xiang": "水上有雷",
            "yao_array": [0, 1, 0, 1, 0, 0],
            "description": "云雷，屯；君子以经纶"
        },
        {
            "name": "水火既济",
            "alias": "既济卦",
            "gua_type": "三世卦",
            "xiang": "水在火上",
            "yao_array": [0, 1, 0, 1, 0, 1],
            "description": "水在火上，既济；君子以思患而豫防之"
        },
        {
            "name": "泽火革",
            "alias": "革卦",
            "gua_type": "四世卦",
            "xiang": "泽中有火",
            "yao_array": [1, 1, 0, 1, 0, 1],
            "description": "泽中有火，革；君子以治历明时"
        },
        {
            "name": "雷火丰",
            "alias": "丰卦",
            "gua_type": "五世卦",
            "xiang": "雷电交加",
            "yao_array": [1, 0, 0, 1, 0, 1],
            "description": "雷电皆至，丰；君子以折狱致刑"
        },
        {
            "name": "地火明夷",
            "alias": "明夷卦",
            "gua_type": "游魂卦",
            "xiang": "日入于地",
            "yao_array": [0, 0, 0, 1, 0, 1],
            "description": "明入地中，明夷；君子以莅众，用晦而明"
        },
        {
            "name": "地水师",
            "alias": "师卦",
            "gua_type": "归魂卦",
            "xiang": "地中有水",
            "yao_array": [0, 0, 0, 0, 1, 0],
            "description": "地中有水，师；君子以容民畜众"
        }
    ],
    "艮宫": [
        {
            "name": "艮为山",
            "alias": "艮卦",
            "gua_type": "本宫卦",
            "xiang": "山",
            "yao_array": [0, 0, 1, 0, 0, 1],
            "description": "止于所当止"
        },
        {
            "name": "山火贲",
            "alias": "贲卦",
            "gua_type": "一世卦",
            "xiang": "山下有火",
            "yao_array": [0, 0, 1, 1, 0, 1],
            "description": "山下有火，贲；君子以明庶政，无敢折狱"
        },
        {
            "name": "山天大畜",
            "alias": "大畜卦",
            "gua_type": "二世卦",
            "xiang": "山上有天",
            "yao_array": [0, 0, 1, 1, 1, 1],
            "description": "云在天上，大畜；君子以多识前言往行，以畜其德"
        },
        {
            "name": "山泽损",
            "alias": "损卦",
            "gua_type": "三世卦",
            "xiang": "山附于泽",
            "yao_array": [0, 0, 1, 1, 1, 0],
            "description": "山下有泽，损；君子以惩忿窒欲"
        },
        {
            "name": "火泽睽",
            "alias": "睽卦",
            "gua_type": "四世卦",
            "xiang": "火在泽上",
            "yao_array": [1, 0, 1, 1, 1, 0],
            "description": "上火下泽，睽；君子以同而异"
        },
        {
            "name": "天泽履",
            "alias": "履卦",
            "gua_type": "五世卦",
            "xiang": "天上有泽",
            "yao_array": [1, 1, 1, 1, 1, 0],
            "description": "上天下泽，履；君子以辩上下，定民志"
        },
        {
            "name": "风泽中孚",
            "alias": "中孚卦",
            "gua_type": "游魂卦",
            "xiang": "泽上有风",
            "yao_array": [0, 1, 1, 1, 1, 0],
            "description": "泽上有风，中孚；君子以议狱缓死"
        },
        {
            "name": "风山渐",
            "alias": "渐卦",
            "gua_type": "归魂卦",
            "xiang": "山上有风",
            "yao_array": [0, 1, 1, 0, 0, 1],
            "description": "山上有木，渐；君子以居贤德，善俗"
        }
    ],
    "震宫": [
        {
            "name": "震为雷",
            "alias": "震卦",
            "gua_type": "本宫卦",
            "xiang": "雷",
            "yao_array": [1, 0, 0, 1, 0, 0],
            "description": "洞察坤元"
        },
        {
            "name": "雷地豫",
            "alias": "豫卦",
            "gua_type": "一世卦",
            "xiang": "雷出地上",
            "yao_array": [1, 0, 0, 0, 0, 0],
            "description": "雷出地上，豫；先王以作乐崇德，殷荐之上帝，以配祖考"
        },
        {
            "name": "雷水解",
            "alias": "解卦",
            "gua_type": "二世卦",
            "xiang": "雷在水上",
            "yao_array": [1, 0, 0, 0, 1, 0],
            "description": "雷雨作，解；君子以赦过宥罪"
        },
        {
            "name": "雷风恒",
            "alias": "恒卦",
            "gua_type": "三世卦",
            "xiang": "雷随风出",
            "yao_array": [1, 0, 0, 0, 1, 1],
            "description": "雷风，恒；君子以立不易方"
        },
        {
            "name": "地风升",
            "alias": "升卦",
            "gua_type": "四世卦",
            "xiang": "风行地上",
            "yao_array": [0, 0, 0, 0, 1, 1],
            "description": "木生土中，升；君子以顺德，积小以高大"
        },
        {
            "name": "水风井",
            "alias": "井卦",
            "gua_type": "五世卦",
            "xiang": "水在风上",
            "yao_array": [0, 1, 0, 0, 1, 1],
            "description": "木上有水，井；君子以劳民劝相"
        },
        {
            "name": "泽风大过",
            "alias": "大过卦",
            "gua_type": "游魂卦",
            "xiang": "泽灭木",
            "yao_array": [1, 1, 0, 0, 1, 1],
            "description": "泽灭木，大过；君子以独立不惧，遁世无闷"
        },
        {
            "name": "泽雷随",
            "alias": "随卦",
            "gua_type": "归魂卦",
            "xiang": "泽中有雷",
            "yao_array": [1, 1, 0, 1, 0, 0],
            "description": "泽中有雷，随；君子以向晦入宴息"
        }
    ],
    "巽宫": [
        {
            "name": "巽为风",
            "alias": "巽卦",
            "gua_type": "本宫卦",
            "xiang": "风",
            "yao_array": [0, 1, 1, 0, 1, 1],
            "description": "入而不争"
        },
        {
            "name": "风天小畜",
            "alias": "小畜卦",
            "gua_type": "一世卦",
            "xiang": "风行天上",
            "yao_array": [0, 1, 1, 1, 1, 1],
            "description": "风行天上，小畜；君子以懿文德"
        },
        {
            "name": "风火家人",
            "alias": "家人卦",
            "gua_type": "二世卦",
            "xiang": "风自火出",
            "yao_array": [0, 1, 1, 1, 0, 1],
            "description": "风自火出，家人；君子以言有物，而行有恒"
        },
        {
            "name": "风雷益",
            "alias": "益卦",
            "gua_type": "三世卦",
            "xiang": "风雷互动",
            "yao_array": [0, 1, 1, 1, 0, 0],
            "description": "风雷，益；君子以见善则迁，有过则改"
        },
        {
            "name": "天雷无妄",
            "alias": "无妄卦",
            "gua_type": "四世卦",
            "xiang": "天下雷行",
            "yao_array": [1, 1, 1, 1, 0, 0],
            "description": "天下雷行，物与无妄；先王以茂对时，育万物"
        },
        {
            "name": "火雷噬嗑",
            "alias": "噬嗑卦",
            "gua_type": "五世卦",
            "xiang": "雷电交作",
            "yao_array": [1, 0, 1, 1, 0, 0],
            "description": "雷电噬嗑；君子以慎言语，节饮食"
        },
        {
            "name": "山雷颐",
            "alias": "颐卦",
            "gua_type": "游魂卦",
            "xiang": "山下出雷",
            "yao_array": [0, 0, 1, 1, 0, 0],
            "description": "山下有雷，颐；君子以慎言语，节饮食"
        },
        {
            "name": "山风蛊",
            "alias": "蛊卦",
            "gua_type": "归魂卦",
            "xiang": "山下有风",
            "yao_array": [0, 0, 1, 0, 1, 1],
            "description": "山下有风，蛊；君子以振民育德"
        }
    ],
    "离宫": [
        {
            "name": "离为火",
            "alias": "离卦",
            "gua_type": "本宫卦",
            "xiang": "火",
            "yao_array": [1, 0, 1, 1, 0, 1],
            "description": "丽泽中正"
        },
        {
            "name": "火山旅",
            "alias": "旅卦",
            "gua_type": "一世卦",
            "xiang": "火焚山林",
            "yao_array": [1, 0, 1, 0, 0, 1],
            "description": "山上有火，旅；君子以明慎用刑，而不留狱"
        },
        {
            "name": "火风鼎",
            "alias": "鼎卦",
            "gua_type": "二世卦",
            "xiang": "火上有风",
            "yao_array": [1, 0, 1, 0, 1, 1],
            "description": "木上有火，鼎；君子以正位凝命"
        },
        {
            "name": "火水未济",
            "alias": "未济卦",
            "gua_type": "三世卦",
            "xiang": "火在水上",
            "yao_array": [1, 0, 1, 0, 1, 0],
            "description": "火在水上，未济；君子以慎辨物居方"
        },
        {
            "name": "山水蒙",
            "alias": "蒙卦",
            "gua_type": "四世卦",
            "xiang": "山下出水",
            "yao_array": [0, 0, 1, 0, 1, 0],
            "description": "山下出泉，蒙；君子以果行育德"
        },
        {
            "name": "风水涣",
            "alias": "涣卦",
            "gua_type": "五世卦",
            "xiang": "风在水上",
            "yao_array": [0, 1, 1, 0, 1, 0],
            "description": "风行水上，涣；先王以享于帝，立庙"
        },
        {
            "name": "天水讼",
            "alias": "讼卦",
            "gua_type": "游魂卦",
            "xiang": "天与水违行",
            "yao_array": [1, 1, 1, 0, 1, 0],
            "description": "天与水违行，讼；君子以作事谋始"
        },
        {
            "name": "天火同人",
            "alias": "同人卦",
            "gua_type": "归魂卦",
            "xiang": "天与火同德",
            "yao_array": [1, 1, 1, 1, 0, 1],
            "description": "天与火，同人；君子以类族辨物"
        }
    ],
    "坤宫": [
        {
            "name": "坤为地",
            "alias": "坤卦",
            "gua_type": "本宫卦",
            "xiang": "地",
            "yao_array": [0, 0, 0, 0, 0, 0],
            "description": "柔顺中正"
        },
        {
            "name": "地雷复",
            "alias": "复卦",
            "gua_type": "一世卦",
            "xiang": "春雷动地",
            "yao_array": [0, 0, 0, 1, 0, 0],
            "description": "雷在地中，复；先王以至日闭关，商旅不行，后不省方"
        },
        {
            "name": "地泽临",
            "alias": "临卦",
            "gua_type": "二世卦",
            "xiang": "地上有泽",
            "yao_array": [0, 0, 0, 1, 1, 0],
            "description": "泽上有地，临；君子以教思无穷，容保民无疆"
        },
        {
            "name": "地天泰",
            "alias": "泰卦",
            "gua_type": "三世卦",
            "xiang": "地天交泰",
            "yao_array": [0, 0, 0, 1, 1, 1],
            "description": "天地交，泰；后以财成天地之道，辅相天地之宜，以左右民"
        },
        {
            "name": "雷天大壮",
            "alias": "大壮卦",
            "gua_type": "四世卦",
            "xiang": "雷在天上",
            "yao_array": [1, 0, 0, 1, 1, 1],
            "description": "雷在天上，大壮；君子以非礼弗履"
        },
        {
            "name": "泽天夬",
            "alias": "夬卦",
            "gua_type": "五世卦",
            "xiang": "泽在天上",
            "yao_array": [1, 1, 0, 1, 1, 1],
            "description": "泽在天上，夬；君子以施禄及下，居德则忌"
        },
        {
            "name": "水天需",
            "alias": "需卦",
            "gua_type": "游魂卦",
            "xiang": "云上有水",
            "yao_array": [0, 1, 0, 1, 1, 1],
            "description": "云上于天，需；君子以饮食宴乐"
        },
        {
            "name": "水地比",
            "alias": "比卦",
            "gua_type": "归魂卦",
            "xiang": "地上有水",
            "yao_array": [0, 1, 0, 0, 0, 0],
            "description": "地上有水，比；先王以建万国，亲诸侯"
        }
    ],
    "兑宫": [
        {
            "name": "兑为泽",
            "alias": "兑卦",
            "gua_type": "本宫卦",
            "xiang": "泽",
            "yao_array": [1, 1, 0, 1, 1, 0],
            "description": "和悦中正"
        },
        {
            "name": "泽水困",
            "alias": "困卦",
            "gua_type": "一世卦",
            "xiang": "泽无水",
            "yao_array": [1, 1, 0, 0, 1, 0],
            "description": "泽无水，困；君子以致命遂志"
        },
        {
            "name": "泽地萃",
            "alias": "萃卦",
            "gua_type": "二世卦",
            "xiang": "泽泛滥于地",
            "yao_array": [1, 1, 0, 0, 0, 0],
            "description": "泽上于地，萃；君子以除戎器，戒不虞"
        },
        {
            "name": "泽山咸",
            "alias": "咸卦",
            "gua_type": "三世卦",
            "xiang": "上泽下山",
            "yao_array": [1, 1, 0, 0, 0, 1],
            "description": "山上有泽，咸；君子以虚受人"
        },
        {
            "name": "水山蹇",
            "alias": "蹇卦",
            "gua_type": "四世卦",
            "xiang": "水在山上",
            "yao_array": [0, 1, 0, 0, 0, 1],
            "description": "山上有水，蹇；君子以反身修德"
        },
        {
            "name": "地山谦",
            "alias": "谦卦",
            "gua_type": "五世卦",
            "xiang": "地中有山",
            "yao_array": [0, 0, 0, 0, 0, 1],
            "description": "地中有山，谦；君子以裒多益寡，称物平施"
        },
        {
            "name": "雷山小过",
            "alias": "小过卦",
            "gua_type": "游魂卦",
            "xiang": "山上有雷",
            "yao_array": [1, 0, 0, 0, 0, 1],
            "description": "山上有雷，小过；君子以行过乎恭，丧过乎哀，用过乎俭"
        },
        {
            "name": "雷泽归妹",
            "alias": "归妹卦",
            "gua_type": "归魂卦",
            "xiang": "泽中有雷",
            "yao_array": [1, 0, 0, 1, 1, 0],
            "description": "泽上有雷，归妹；君子以永终知敝"
        }
    ]
}

# 六亲关系数据
LIUQIN_DATA = {
    "兄弟": {
        "description": "同气类，同辈关系",
        "wuxing_relation": "比和",
        "liuqin_type": "中性"
    },
    "子孙": {
        "description": "所生类，后代",
        "wuxing_relation": "我生",
        "liuqin_type": "有利"
    },
    "妻财": {
        "description": "所聚类，情感与物质",
        "wuxing_relation": "生我",
        "liuqin_type": "有利"
    },
    "官鬼": {
        "description": "所制类，权威与压力",
        "wuxing_relation": "克我",
        "liuqin_type": "不利"
    },
    "父母": {
        "description": "所仰类，长辈与资助",
        "wuxing_relation": "我克",
        "liuqin_type": "有力"
    }
}

# 六神数据
LIUSHEN_DATA = {
    "青龙": {
        "nature": "吉",
        "description": "吉神，主贵人、喜庆",
        "health_impact": "气血流通，益精气"
    },
    "朱雀": {
        "nature": "凶",
        "description": "凶神，主口舌、是非",
        "health_impact": "心火上炎，口腔不适"
    },
    "勾陈": {
        "nature": "平",
        "description": "中性，主迟滞、稳固",
        "health_impact": "消化系统，脾胃不适"
    },
    "腾蛇": {
        "nature": "凶",
        "description": "凶神，主变动、多变",
        "health_impact": "皮肤问题，神经紧张"
    },
    "白虎": {
        "nature": "凶",
        "description": "凶神，主伤害、灾祸",
        "health_impact": "外伤，急性疾病，肺部问题"
    },
    "玄武": {
        "nature": "凶",
        "description": "凶神，主暗昧、隐患",
        "health_impact": "泌尿系统问题，水肿"
    }
}

# 五行属性数据
WUXING_DATA = {
    "金": {
        "color": "白",
        "direction": "西",
        "season": "秋",
        "shape": "圆",
        "organs": ["肺", "大肠"],
        "nature": "收敛坚强"
    },
    "木": {
        "color": "青",
        "direction": "东",
        "season": "春",
        "shape": "长",
        "organs": ["肝", "胆"],
        "nature": "生发条达"
    },
    "水": {
        "color": "黑",
        "direction": "北",
        "season": "冬",
        "shape": "曲",
        "organs": ["肾", "膀胱"],
        "nature": "寒冷潜藏"
    },
    "火": {
        "color": "赤",
        "direction": "南",
        "season": "夏",
        "shape": "尖",
        "organs": ["心", "小肠"],
        "nature": "炎热上升"
    },
    "土": {
        "color": "黄",
        "direction": "中",
        "season": "四季末",
        "shape": "方",
        "organs": ["脾", "胃"],
        "nature": "厚重中正"
    }
}

# 卦宫与五行对应关系
GUA_WUXING_MAP = {
    "乾宫": "金",
    "兑宫": "金",
    "离宫": "火",
    "震宫": "木",
    "巽宫": "木",
    "坎宫": "水",
    "艮宫": "土",
    "坤宫": "土"
}

# 卦宫世应爻位置
GUA_SHI = {
    "乾宫": [
        {"gua_type": "本宫卦", "shi_yao": 6, "ying_yao": 3},  # 乾为天
        {"gua_type": "一世卦", "shi_yao": 1, "ying_yao": 4},  # 天风姤
        {"gua_type": "二世卦", "shi_yao": 2, "ying_yao": 5},  # 天山遁
        {"gua_type": "三世卦", "shi_yao": 3, "ying_yao": 6},  # 天地否
        {"gua_type": "四世卦", "shi_yao": 4, "ying_yao": 1},  # 风地观
        {"gua_type": "五世卦", "shi_yao": 5, "ying_yao": 2},  # 山地剥
        {"gua_type": "游魂卦", "shi_yao": 4, "ying_yao": 1},  # 火地晋
        {"gua_type": "归魂卦", "shi_yao": 3, "ying_yao": 6}   # 火天大有
    ],
    "坎宫": [
        {"gua_type": "本宫卦", "shi_yao": 6, "ying_yao": 3},  # 坎为水
        {"gua_type": "一世卦", "shi_yao": 1, "ying_yao": 4},  # 水泽节
        {"gua_type": "二世卦", "shi_yao": 2, "ying_yao": 5},  # 水雷屯
        {"gua_type": "三世卦", "shi_yao": 3, "ying_yao": 6},  # 水火既济
        {"gua_type": "四世卦", "shi_yao": 4, "ying_yao": 1},  # 泽火革
        {"gua_type": "五世卦", "shi_yao": 5, "ying_yao": 2},  # 雷火丰
        {"gua_type": "游魂卦", "shi_yao": 4, "ying_yao": 1},  # 地火明夷
        {"gua_type": "归魂卦", "shi_yao": 3, "ying_yao": 6}   # 地水师
    ],
    "艮宫": [
        {"gua_type": "本宫卦", "shi_yao": 6, "ying_yao": 3},  # 艮为山
        {"gua_type": "一世卦", "shi_yao": 1, "ying_yao": 4},  # 山火贲
        {"gua_type": "二世卦", "shi_yao": 2, "ying_yao": 5},  # 山天大畜
        {"gua_type": "三世卦", "shi_yao": 3, "ying_yao": 6},  # 山泽损
        {"gua_type": "四世卦", "shi_yao": 4, "ying_yao": 1},  # 火泽睽
        {"gua_type": "五世卦", "shi_yao": 5, "ying_yao": 2},  # 天泽履
        {"gua_type": "游魂卦", "shi_yao": 4, "ying_yao": 1},  # 风泽中孚
        {"gua_type": "归魂卦", "shi_yao": 3, "ying_yao": 6}   # 风山渐
    ],
    "震宫": [
        {"gua_type": "本宫卦", "shi_yao": 6, "ying_yao": 3},  # 震为雷
        {"gua_type": "一世卦", "shi_yao": 1, "ying_yao": 4},  # 雷地豫
        {"gua_type": "二世卦", "shi_yao": 2, "ying_yao": 5},  # 雷水解
        {"gua_type": "三世卦", "shi_yao": 3, "ying_yao": 6},  # 雷风恒
        {"gua_type": "四世卦", "shi_yao": 4, "ying_yao": 1},  # 地风升
        {"gua_type": "五世卦", "shi_yao": 5, "ying_yao": 2},  # 水风井
        {"gua_type": "游魂卦", "shi_yao": 4, "ying_yao": 1},  # 泽风大过
        {"gua_type": "归魂卦", "shi_yao": 3, "ying_yao": 6}   # 泽雷随
    ],
    "巽宫": [
        {"gua_type": "本宫卦", "shi_yao": 6, "ying_yao": 3},  # 巽为风
        {"gua_type": "一世卦", "shi_yao": 1, "ying_yao": 4},  # 风天小畜
        {"gua_type": "二世卦", "shi_yao": 2, "ying_yao": 5},  # 风火家人
        {"gua_type": "三世卦", "shi_yao": 3, "ying_yao": 6},  # 风雷益
        {"gua_type": "四世卦", "shi_yao": 4, "ying_yao": 1},  # 天雷无妄
        {"gua_type": "五世卦", "shi_yao": 5, "ying_yao": 2},  # 火雷噬嗑
        {"gua_type": "游魂卦", "shi_yao": 4, "ying_yao": 1},  # 山雷颐
        {"gua_type": "归魂卦", "shi_yao": 3, "ying_yao": 6}   # 山风蛊
    ],
    "离宫": [
        {"gua_type": "本宫卦", "shi_yao": 6, "ying_yao": 3},  # 离为火
        {"gua_type": "一世卦", "shi_yao": 1, "ying_yao": 4},  # 火山旅
        {"gua_type": "二世卦", "shi_yao": 2, "ying_yao": 5},  # 火风鼎
        {"gua_type": "三世卦", "shi_yao": 3, "ying_yao": 6},  # 火水未济
        {"gua_type": "四世卦", "shi_yao": 4, "ying_yao": 1},  # 山水蒙
        {"gua_type": "五世卦", "shi_yao": 5, "ying_yao": 2},  # 风水涣
        {"gua_type": "游魂卦", "shi_yao": 4, "ying_yao": 1},  # 天水讼
        {"gua_type": "归魂卦", "shi_yao": 3, "ying_yao": 6}   # 天火同人
    ],
    "坤宫": [
        {"gua_type": "本宫卦", "shi_yao": 6, "ying_yao": 3},  # 坤为地
        {"gua_type": "一世卦", "shi_yao": 1, "ying_yao": 4},  # 地雷复
        {"gua_type": "二世卦", "shi_yao": 2, "ying_yao": 5},  # 地泽临
        {"gua_type": "三世卦", "shi_yao": 3, "ying_yao": 6},  # 地天泰
        {"gua_type": "四世卦", "shi_yao": 4, "ying_yao": 1},  # 雷天大壮
        {"gua_type": "五世卦", "shi_yao": 5, "ying_yao": 2},  # 泽天夬
        {"gua_type": "游魂卦", "shi_yao": 4, "ying_yao": 1},  # 水天需
        {"gua_type": "归魂卦", "shi_yao": 3, "ying_yao": 6}   # 水地比
    ],
    "兑宫": [
        {"gua_type": "本宫卦", "shi_yao": 6, "ying_yao": 3},  # 兑为泽
        {"gua_type": "一世卦", "shi_yao": 1, "ying_yao": 4},  # 泽水困
        {"gua_type": "二世卦", "shi_yao": 2, "ying_yao": 5},  # 泽地萃
        {"gua_type": "三世卦", "shi_yao": 3, "ying_yao": 6},  # 泽山咸
        {"gua_type": "四世卦", "shi_yao": 4, "ying_yao": 1},  # 水山蹇
        {"gua_type": "五世卦", "shi_yao": 5, "ying_yao": 2},  # 地山谦
        {"gua_type": "游魂卦", "shi_yao": 4, "ying_yao": 1},  # 雷山小过
        {"gua_type": "归魂卦", "shi_yao": 3, "ying_yao": 6}   # 雷泽归妹
    ]
}