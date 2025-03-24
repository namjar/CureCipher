from pathlib import Path
import json
import os
from .najia import Najia

def load_shensha_data():
    """加载神煞数据"""
    # 尝试多个可能的路径
    possible_paths = [
        Path(__file__).parent.parent.parent / "data" / "shensha_impacts.json",  # 项目根目录data文件夹
        Path(__file__).parent / "data" / "shensha_impacts.json",  # 当前模块data文件夹
        Path(__file__).resolve().parents[2] / "data" / "shensha_impacts.json"  # 绝对路径
    ]
    
    for path in possible_paths:
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    # 如果找不到文件，创建一个基本结构
    print("警告: 未找到神煞数据文件，使用基本结构")
    return {
        "positive": {"天医": {"element": "水", "health_aspects": {"day_master_strong": ["健康"], "day_master_weak": ["健康"], "day_master_neutral": ["健康"]}}},
        "negative": {"白虎": {"element": "金", "health_aspects": {"day_master_strong": ["警惕"], "day_master_weak": ["警惕"], "day_master_neutral": ["警惕"]}, "remedy": ["调养"]}}
    }

def diagnose_health(params, date, gender=None, day_master_strength="neutral"):
    """
    六爻健康诊断

    参数:
        params (list): 六爻参数（比如[2, 2, 1, 2, 4, 2]）
        date (str/datetime): 日期（比如'2019-12-25 00:20'）
        gender (str): 性别
        day_master_strength (str): 日主强弱（strong/weak/neutral）

    返回:
        dict: 卦象、健康影响、调理建议
    """
    # 六爻排盘
    najia = Najia(verbose=2).compile(params=params, date=date, gender=gender)
    gua_data = najia.data

    # 卦象五行
    gua_name = gua_data.get('name', '未知卦')
    gua_element_map = {
        '乾为天': '金', '兑为泽': '金', '离为火': '火', '震为雷': '木',
        '巽为风': '木', '坎为水': '水', '艮为山': '土', '坤为地': '土'
    }
    gua_element = gua_element_map.get(gua_name, '土')  # 默认土

    # 加载神煞
    shensha_data = load_shensha_data()
    shensha_list = [s for s in shensha_data["positive"] if shensha_data["positive"][s]["element"] == gua_element] + \
                   [s for s in shensha_data["negative"] if shensha_data["negative"][s]["element"] == gua_element]

    # 健康影响
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

    # 六神辅助判断
    god6 = gua_data.get('god6', [])
    dong = gua_data.get('dong', [])  # 动爻位置
    god6_impacts = []
    
    for idx in dong:
        if 0 <= idx < len(god6):  # 确保索引有效
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
        "render": najia.render()  # 字符画输出
    }