from pathlib import Path
import json
from .najia import Najia

def load_shensha_data():
    base_dir = Path(__file__).parent.parent.parent
    data_file = base_dir / "data" / "shensha_impacts.json"
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def diagnose_health(params, date, gender=None, day_master_strength="neutral"):
    najia = Najia(verbose=2).compile(params=params, date=date, gender=gender)
    gua_data = najia.data
    gua_name = gua_data['name']
    gua_element_map = {
        '乾为天': '金', '兑为泽': '金', '离为火': '火', '震为雷': '木',
        '巽为风': '木', '坎为水': '水', '艮为山': '土', '坤为地': '土'
    }
    gua_element = gua_element_map.get(gua_name, '未知')
    shensha_data = load_shensha_data()
    shensha_list = [s for s in shensha_data["positive"] if shensha_data["positive"][s]["element"] == gua_element] + \
                   [s for s in shensha_data["negative"] if shensha_data["negative"][s]["element"] == gua_element]
    print(f"加载的神煞: {shensha_list}")  # 添加调试信息
    health_impacts = []
    remedies = []
    for shensha in shensha_list:
        data = shensha_data["positive"].get(shensha, shensha_data["negative"].get(shensha))
        aspects = data["health_aspects"][f"day_master_{day_master_strength}"]
        if gua_element in data.get("flow_year_boost", []):
            aspects = [f"{a} (流年增强)" for a in aspects]
        health_impacts.extend(aspects)
        if "remedy" in data:
            remedies.extend(data["remedy"])
    god6 = gua_data['god6']
    dong = gua_data['dong']
    god6_impacts = []
    for idx in dong:
        god = god6[idx]
        if god == "白虎":
            god6_impacts.append("白虎动，疾病或意外风险加重")
        elif god == "青龙":
            god6_impacts.append("青龙动，健康有利")
    return {
        "gua_name": gua_name,
        "gua_element": gua_element,
        "health_impacts": health_impacts,
        "remedies": remedies,
        "shensha": shensha_list,
        "god6_impacts": god6_impacts,
        "render": najia.render()
    }