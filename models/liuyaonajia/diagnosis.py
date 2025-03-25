import sys
from pathlib import Path
import json
import datetime

# 清理 sys.modules 以避免重复导入
module_name = 'models.liuyaonajia.diagnosis'
if module_name in sys.modules:
    del sys.modules[module_name]

# 动态添加项目根目录到 sys.path
project_root = str(Path(__file__).resolve().parents[3])  # 指向 CureCipher 根目录
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from models.liuyaonajia.najia import Najia
    from models.bazi.shensha import analyze_shensha
except ImportError as e:
    print(f"ImportError in diagnosis.py: {e}")
    raise

def load_shensha_data():
    base_dir = Path(__file__).parent.parent.parent
    data_file = base_dir / "data" / "shensha_impacts.json"
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        raise
    except Exception as e:
        print(f"Error loading shensha_impacts.json: {e}")
        raise

def calculate_flow_year_element(year):
    """根据年份计算流年五行（基于天干）"""
    gan_elements = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }
    Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    gan_idx = (year - 4) % 10
    gan = Gan[gan_idx]
    flow_year_element = gan_elements[gan]
    return flow_year_element

def diagnose_health(params, date, gender=None, day_master_strength="neutral", flow_year_element=None, longitude=-100, latitude=40):
    try:
        najia = Najia(verbose=2).compile(params=params, date=date, gender=gender, longitude=longitude, latitude=latitude)
    except Exception as e:
        print(f"Error compiling Najia: {e}")
        raise

    gua_data = najia.data
    gua_name = gua_data['name']  # 本卦名称
    day_gz = gua_data['lunar']['gz']['day']
    dong = gua_data['dong']
    bian_gua_name = gua_data['bian']['name'] if gua_data['bian']['name'] else gua_name  # 变卦名称

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
    gua_element = gua_element_map.get(gua_name, '未知')  # 本卦五行
    bian_gua_element = gua_element_map.get(bian_gua_name, gua_element)  # 变卦五行

    try:
        shensha_data = load_shensha_data()
    except Exception as e:
        print(f"Error in load_shensha_data: {e}")
        raise

    # 加载六爻相关的神煞
    liuyao_shensha = [
        "天乙贵人", "文昌贵人", "太极贵人", "月德贵人", "天德贵人", "福星贵人",
        "国印贵人", "禄神", "金舆", "华盖", "三奇贵人", "天医",
        "白虎", "羊刃", "劫煞", "亡神", "阴煞", "元辰", "咸池", "飞刃",
        "灾煞", "吊客", "大耗", "丧门"
    ]

    # 五行映射
    element_map = {'金': 'metal', '木': 'wood', '水': 'water', '火': 'fire', '土': 'earth'}
    gua_element_mapped = element_map.get(gua_element, gua_element.lower())
    bian_gua_element_mapped = element_map.get(bian_gua_element, bian_gua_element.lower())

    # 筛选与本卦五行匹配的神煞
    shensha_list = [
        s for s in shensha_data["positive"]
        if s in liuyao_shensha and gua_element_mapped in shensha_data["positive"][s]["element_affinity"]
    ] + [
        s for s in shensha_data["negative"]
        if s in liuyao_shensha and gua_element_mapped in shensha_data["negative"][s]["element_affinity"]
    ]
    print(f"加载的神煞: {shensha_list}")

    # 准备 najia_data，包含 shensha_data
    gua_data["shensha_data"] = shensha_data

    # 动态计算流年五行
    if flow_year_element is None:
        year = date.year
        flow_year_element = calculate_flow_year_element(year)
        print(f"动态计算流年五行: {year}年 -> {flow_year_element}")

    # 调用 shensha.py 进行健康分析
    try:
        shensha_result = analyze_shensha(
            shensha_list,
            gua_element,
            day_master_strength=day_master_strength,
            flow_year_element=flow_year_element,
            mode="liuyao",
            najia_data=gua_data
        )
    except Exception as e:
        print(f"Error in analyze_shensha: {e}")
        raise

    # 提取健康影响和调理建议
    health_impacts = []
    remedies = []
    for impact in shensha_result["positive_impacts"]:
        if impact["health"] != ["无特定影响"]:
            health_impacts.extend(impact["health"])
    for impact in shensha_result["negative_impacts"]:
        if impact["health"] != ["无特定影响"]:
            health_impacts.extend(impact["health"])
        if impact["remedy"]:
            remedies.extend(impact["remedy"])

    return {
        "gua_name": gua_name,
        "gua_element": gua_element,
        "bian_gua_name": bian_gua_name,
        "bian_gua_element": bian_gua_element,
        "health_impacts": list(set(health_impacts)),  # 去重
        "remedies": list(set(remedies)),  # 去重
        "shensha": shensha_list,
        "god6_impacts": shensha_result["god6_impacts"],
        "render": najia.render(),
        "shensha_analysis": shensha_result
    }

if __name__ == "__main__":
    # 测试与用户一致的参数
    params = [4, 1, 1, 1, 1, 1]  # 泽天夬变乾为天
    date = "2025-03-24 22:00"
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
    result = diagnose_health(params=params, date=date_obj, day_master_strength="neutral")
    print(result['render'])
    print("\n健康分析：")
    print(f"本卦名：{result['gua_name']}")
    print(f"本卦五行：{result['gua_element']}")
    print(f"变卦名：{result['bian_gua_name']}")
    print(f"变卦五行：{result['bian_gua_element']}")
    print(f"健康影响：{result['health_impacts']}")
    print(f"调理建议：{result['remedies']}")
    print(f"六神影响：{result['god6_impacts']}")
    print("\n神煞分析结果 (完整版):")
    print(json.dumps(result['shensha_analysis'], ensure_ascii=False, indent=2))