"""
卦象图形化显示模块 - 提供六爻卦象的ASCII和Unicode图形表示
增强版 - 支持八宫卦信息、六亲、六神、世应爻位置等详细显示
"""

import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Union

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

# 导入卦宫处理模块
from models.liuyao.modules.gua_palace import gua_palace
from models.liuyao.data.bagong_data import LIUSHEN_DATA, LIUQIN_DATA, WUXING_DATA

# 爻符号定义 - 使用与参考图完全匹配的符号
YANG_YAO = "▅▅▅▅▅▅▅▅"  # 阳爻
YIN_YAO = "▅▅▅  ▅▅▅"   # 阴爻
DONG_YANG = "▅▅▅▅▅▅▅▅ ×→"  # 动阳爻
DONG_YIN = "▅▅▅  ▅▅▅ ×→"   # 动阴爻

# 爻位名称
YAO_NAMES = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]

def yao_to_string(yao: int, is_dong: bool = False) -> str:
    """
    将爻数值转换为字符串表示
    
    参数:
        yao (int): 爻值，1表示阳爻，0表示阴爻
        is_dong (bool): 是否为动爻
        
    返回:
        str: 爻的字符串表示
    """
    if is_dong:
        return DONG_YANG if yao == 1 else DONG_YIN
    else:
        return YANG_YAO if yao == 1 else YIN_YAO

def remove_duplicate_gong(palace_name: str) -> str:
    """
    修复卦宫显示中的重复问题
    
    参数:
        palace_name (str): 卦宫名称
        
    返回:
        str: 修复后的卦宫名称
    """
    if palace_name.endswith("宫宫"):
        return palace_name[:-1]
    return palace_name

def generate_gua_ascii(ben_gua: List[int], dong_yao_pos: Optional[int] = None, 
                       shi_yao: Optional[int] = None, ying_yao: Optional[int] = None) -> str:
    """
    生成本卦的ASCII图形
    
    参数:
        ben_gua (List[int]): 本卦爻值列表，从下到上6爻，1表示阳爻，0表示阴爻
        dong_yao_pos (int, optional): 动爻位置，1-6，默认None表示无动爻
        shi_yao (int, optional): 世爻位置，1-6
        ying_yao (int, optional): 应爻位置，1-6
        
    返回:
        str: 格式化的ASCII卦象图
    """
    lines = []
    for i in range(5, -1, -1):  # 从上到下遍历爻
        yao_num = i + 1
        is_dong = dong_yao_pos == yao_num if dong_yao_pos else False
        shi_mark = " 世" if shi_yao == yao_num else ""
        ying_mark = " 应" if ying_yao == yao_num else ""
        
        lines.append(f"{yao_num}: {yao_to_string(ben_gua[i], is_dong)}{shi_mark}{ying_mark}")
    
    # 组合成卦象图
    return "\n".join(lines)

def generate_full_gua_display(result: Dict) -> str:
    """
    根据计算结果生成完整的卦象显示，符合传统六爻排盘格式
    
    参数:
        result (Dict): 卦象计算结果
        
    返回:
        str: 格式化的卦象显示字符串
    """
    # 提取本卦和变卦信息
    ben_gua_name = result['ben_gua']['name']
    ben_gua_yao = result['ben_gua'].get('yao', [])
    
    bian_gua_name = result['bian_gua']['name']
    bian_gua_yao = result['bian_gua'].get('yao', [])
    
    dong_yao_pos = result['dong_yao']
    shi_yao_pos = result['shi_yao']
    ying_yao_pos = result['ying_yao']
    
    # 提取日期信息
    date_info = result.get('date_info', {})
    solar_date = date_info.get('solar_date', '')
    solar_time = date_info.get('solar_time', '')
    lunar_date = date_info.get('lunar_date', '')
    year_gz = date_info.get('year_gz', '')
    month_gz = date_info.get('month_gz', '')
    day_gz = date_info.get('day_gz', '')
    hour_gz = date_info.get('hour_gz', '')
    
    # 尝试解析年月日和时间成更标准的格式
    if isinstance(solar_date, str) and '-' in solar_date:
        parts = solar_date.split('-')
        if len(parts) == 3:
            year, month, day = parts
            solar_date_str = f"{year}年 {month}月 {day}日"
        else:
            solar_date_str = solar_date
    else:
        solar_date_str = str(solar_date)
        
    if isinstance(solar_time, float) or isinstance(solar_time, int):
        hour = int(solar_time)
        minute = int((solar_time - hour) * 60)
        solar_time_str = f"{hour}时 {minute}分"
    else:
        solar_time_str = str(solar_time)
    
    # 空亡信息
    kongwang = "、".join(result.get('kongwang', []))
    
    # 识别卦宫和卦型
    ben_palace = remove_duplicate_gong(result['ben_gua'].get('palace', '未知宫'))
    ben_type = result['ben_gua'].get('gua_type', '未知')
    
    bian_palace = remove_duplicate_gong(result['bian_gua'].get('palace', '未知宫'))
    bian_type = result['bian_gua'].get('gua_type', '未知')
    
    # 准备六亲、六神和纳甲信息
    liuqin = result.get('liuqin', [''] * 6)
    liushen = result.get('liushen', [''] * 6)
    najia = result.get('najia', [''] * 6)
    
    # 六神名称，按顺序排列
    liushen_names = ["青龙", "玄武", "白虎", "螣蛇", "勾陈", "朱雀"]
    
    # 构建传统排盘格式的头部信息 - 优化日期时间格式
    header = f"公历：{solar_date_str} {solar_time_str}\n"
    header += f"干支：{year_gz}年 {month_gz}月 {day_gz}日 {hour_gz}时 （旬空：{kongwang})\n"
    header += f"得「{ben_gua_name}」之「{bian_gua_name}」卦\n"
    
    # 构建卦宫和卦名行 - 优化为官方排盘检格式
    gua_info = f"{ben_palace}宫:{ben_gua_name}" + "　" * 6 + f"{bian_palace}宫:{bian_gua_name}\n"
    
    # 构建爻位显示
    yaos_display = ""
    
    # 世应标记数组
    shi_ying_marks = [""] * 6
    if shi_yao_pos and 1 <= shi_yao_pos <= 6:
        shi_ying_marks[shi_yao_pos-1] = "世"
    if ying_yao_pos and 1 <= ying_yao_pos <= 6:
        shi_ying_marks[ying_yao_pos-1] = "应"
    
    # 动爻标记数组
    dong_marks = [""] * 6
    if dong_yao_pos and 1 <= dong_yao_pos <= 6:
        dong_marks[dong_yao_pos-1] = " ×→"
    
    # 从上爻到初爻逐行显示
    for i in range(5, -1, -1):
        yao_num = i + 1
        
        # 使用固定的六神名称提高对齐性
        liushen_display = liushen_names[i] if i < len(liushen_names) else "　　"
        
        # 添加六神 - 使用固定宽度的黑体显示
        yaos_display += f"{liushen_display}　　　　　　"
        
        # 为六亲和纳甲信息确保固定宽度，提高对齐性
        liuqin_najia = f"{liuqin[i]}{najia[i]}"
        
        # 添加六亲和纳甲（本卦）
        yaos_display += f"{liuqin_najia} "
        
        # 添加爻符
        yao_symbol = yao_to_string(ben_gua_yao[i], False)
        yaos_display += yao_symbol
        
        # 添加世应标记
        shi_ying_mark = shi_ying_marks[i]
        if shi_ying_mark:
            yaos_display += f" {shi_ying_mark}"
        else:
            yaos_display += "  "
        
        # 添加动爻标记
        dong_mark = dong_marks[i]
        if dong_mark:
            yaos_display += dong_mark
        else:
            yaos_display += "    "
        
        # 添加变卦信息
        yaos_display += f" {liuqin_najia} {yao_to_string(bian_gua_yao[i], False)}\n"
    
    # 组合完整排盘信息
    full_display = header + gua_info + yaos_display
    
    return full_display

def generate_najia_style_display(result: Dict) -> str:
    """
    根据计算结果生成完全符合najia库样式的排盘显示
    
    参数:
        result (Dict): 卦象计算结果
        
    返回:
        str: 格式化的卦象显示字符串
    """
    # 提取各个必要的数据
    date_info = result.get('date_info', {})
    # 尝试从solar_date解析年月日
    solar_date = date_info.get('solar_date', '')
    if solar_date:
        parts = solar_date.split('-')
        if len(parts) == 3:
            year, month, day = parts
        else:
            year, month, day = '', '', ''
    else:
        year, month, day = '', '', ''
    
    # 尝试从time_hour获取小时和分钟
    time_hour = date_info.get('time_hour', 0)
    hour = int(time_hour)
    minute = int((time_hour - hour) * 60)
    
    year_gz = date_info.get('year_gz', '')
    month_gz = date_info.get('month_gz', '')
    day_gz = date_info.get('day_gz', '')
    hour_gz = date_info.get('hour_gz', '')
    
    # 空亡信息
    kongwang = "、".join(result.get('kongwang', []))
    
    # 卦象信息
    ben_gua_name = result['ben_gua']['name']
    ben_gua_yao = result['ben_gua'].get('yao', [])
    ben_palace = remove_duplicate_gong(result['ben_gua'].get('palace', '未知宫'))
    ben_type = result['ben_gua'].get('gua_type', '未知')
    
    bian_gua_name = result['bian_gua']['name'] if 'bian_gua' in result else ''
    bian_gua_yao = result['bian_gua'].get('yao', []) if 'bian_gua' in result else []
    bian_palace = remove_duplicate_gong(result['bian_gua'].get('palace', '未知宫')) if 'bian_gua' in result else ''
    bian_type = result['bian_gua'].get('gua_type', '未知') if 'bian_gua' in result else ''
    
    # 获取六神、六亲、纳甲信息
    liuqin = result.get('liuqin', [''] * 6)
    liushen = result.get('liushen', [''] * 6)
    najia = result.get('najia', [''] * 6)
    
    # 动爻位置
    dong_yao_pos = result.get('dong_yao', None)
    shi_yao_pos = result.get('shi_yao', None)
    ying_yao_pos = result.get('ying_yao', None)
    
    # 与参考图匹配的符号定义 - 使用方块字符
    yang_symbol = "▅▅▅▅▅▅▅▅"  # 阳爻符号
    yin_symbol = "▅▅▅  ▅▅▅"  # 阴爻符号
    dong_symbol = " ×→"  # 动爻标记
    
    # 头部信息 - 优化日期和时间格式
    header = f"公历：{year}年 {month}月 {day}日 {hour}时 {minute}分\n"
    header += f"干支：{year_gz}年 {month_gz}月 {day_gz}日 {hour_gz}时 （旬空：{kongwang})\n"
    header += f"得「{ben_gua_name}」之「{bian_gua_name}」卦\n"
    
    # 卦宫行 - 添加更清晰的对齐和分隔
    gua_info = f"{ben_palace}宫:{ben_gua_name}" + "　" * 6 + f"{bian_palace}宫:{bian_gua_name}\n"
    
    # 构建六爻显示
    yaos_display = ""
    
    # 六神名称对齐
    liushen_names = ["青龙", "玄武", "白虎", "螣蛇", "勾陈", "朱雀"]
    
    # 逐行生成六爻显示
    for i in range(5, -1, -1):
        yao_num = i + 1
        is_dong = yao_num == dong_yao_pos
        is_shi = yao_num == shi_yao_pos
        is_ying = yao_num == ying_yao_pos
        
        # 使用固定的六神名称提高对齐性
        liushen_display = liushen_names[i] if i < len(liushen_names) else "　　"
        
        # 本卦爻符号
        ben_yao_value = ben_gua_yao[i] if i < len(ben_gua_yao) else 0
        ben_symbol = yang_symbol if ben_yao_value == 1 else yin_symbol
        
        # 变卦爻符号
        bian_yao_value = bian_gua_yao[i] if i < len(bian_gua_yao) else 0
        bian_symbol = yang_symbol if bian_yao_value == 1 else yin_symbol
        
        # 为六亲和纳甲信息确保固定宽度，提高对齐性
        liuqin_najia = f"{liuqin[i]}{najia[i]}"
        
        # 创建世应标记和动爻标记
        shi_ying_mark = ""
        if is_shi:
            shi_ying_mark = " 世"
        elif is_ying:
            shi_ying_mark = " 应"
        
        # 动爻标记
        dong_mark = ""
        if is_dong:
            dong_mark = dong_symbol
        
        # 三种不同的行类型：无标记、世应爻、动爻
        line = ""
        
        # 根据不同类型调整间距以保持对齐
        if dong_mark and shi_ying_mark:  # 既是动爻又是世应爻
            line = f"{liushen_display}　　　　　　{liuqin_najia} {ben_symbol}{shi_ying_mark}{dong_mark} {liuqin_najia} {bian_symbol}\n"
        elif shi_ying_mark:  # 只有世应爻
            line = f"{liushen_display}　　　　　　{liuqin_najia} {ben_symbol}{shi_ying_mark}    {liuqin_najia} {bian_symbol}\n"
        elif dong_mark:  # 只有动爻
            line = f"{liushen_display}　　　　　　{liuqin_najia} {ben_symbol}{dong_mark}   {liuqin_najia} {bian_symbol}\n"
        else:  # 无标记
            line = f"{liushen_display}　　　　　　{liuqin_najia} {ben_symbol}　　　{liuqin_najia} {bian_symbol}\n"
        
        yaos_display += line
    
    # 组合完整显示
    full_display = header + gua_info + yaos_display
    
    return full_display

def gua_to_image_text(ben_yao: List[int], bian_yao: List[int], dong_yao_pos: Optional[int] = None,
                   ben_gua_name: str = "", bian_gua_name: str = "",
                   ben_palace: str = "", bian_palace: str = "",
                   shi_yao: Optional[int] = None, ying_yao: Optional[int] = None) -> str:
    """
    生成卦象的图像文本表示
    
    参数:
        ben_yao (List[int]): 本卦爻值数组
        bian_yao (List[int]): 变卦爻值数组
        dong_yao_pos (int, optional): 动爻位置
        ben_gua_name (str): 本卦名称
        bian_gua_name (str): 变卦名称
        ben_palace (str): 本卦卦宫
        bian_palace (str): 变卦卦宫
        shi_yao (int, optional): 世爻位置
        ying_yao (int, optional): 应爻位置
        
    返回:
        str: 格式化的卦象图像文本
    """
    ben_palace = remove_duplicate_gong(ben_palace)
    bian_palace = remove_duplicate_gong(bian_palace)
    
    header = f"本卦：{ben_palace} {ben_gua_name}    变卦：{bian_palace} {bian_gua_name}\n"
    
    lines = []
    for i in range(5, -1, -1):  # 从上爻到初爻
        yao_num = i + 1
        ben_symbol = YANG_YAO if ben_yao[i] == 1 else YIN_YAO
        bian_symbol = YANG_YAO if bian_yao[i] == 1 else YIN_YAO
        
        # 世应爻标记
        shi_mark = " 世" if yao_num == shi_yao else ""
        ying_mark = " 应" if yao_num == ying_yao else ""
        
        # 动爻标记
        dong_mark = " ×→" if yao_num == dong_yao_pos else ""
        
        lines.append(f"{yao_num}爻: {ben_symbol}{shi_mark}{ying_mark}{dong_mark} → {bian_symbol}")
    
    return header + "\n".join(lines)

def generate_enhanced_gua_display(result: Dict) -> str:
    """
    生成增强版的卦象显示
    
    参数:
        result (Dict): 卦象计算结果
        
    返回:
        str: 格式化的增强版卦象显示
    """
    ben_gua_name = result['ben_gua']['name']
    ben_gua_yao = result['ben_gua'].get('yao', [])
    ben_palace = remove_duplicate_gong(result['ben_gua'].get('palace', '未知宫'))
    ben_type = result['ben_gua'].get('gua_type', '未知')
    
    bian_gua_name = result['bian_gua']['name']
    bian_gua_yao = result['bian_gua'].get('yao', [])
    bian_palace = remove_duplicate_gong(result['bian_gua'].get('palace', '未知宫'))
    bian_type = result['bian_gua'].get('gua_type', '未知')
    
    dong_yao_pos = result['dong_yao']
    shi_yao_pos = result['shi_yao']
    ying_yao_pos = result['ying_yao']
    
    liuqin = result.get('liuqin', [''] * 6)
    liushen = result.get('liushen', [''] * 6)
    najia = result.get('najia', [''] * 6)
    
    header = f"本卦：{ben_palace} {ben_gua_name}（{ben_type}）    变卦：{bian_palace} {bian_gua_name}（{bian_type}）\n"
    
    lines = []
    for i in range(5, -1, -1):  # 从上爻到初爻
        yao_num = i + 1
        is_dong = yao_num == dong_yao_pos
        is_shi = yao_num == shi_yao_pos
        is_ying = yao_num == ying_yao_pos
        
        # 处理本卦爻
        ben_symbol = YANG_YAO if ben_gua_yao[i] == 1 else YIN_YAO
        if is_dong:
            ben_symbol = DONG_YANG if ben_gua_yao[i] == 1 else DONG_YIN
        
        # 处理变卦爻
        bian_symbol = YANG_YAO if bian_gua_yao[i] == 1 else YIN_YAO
        
        # 生成标记
        marks = []
        if is_shi:
            marks.append("世")
        if is_ying:
            marks.append("应")
        
        mark_str = f"({','.join(marks)})" if marks else ""
        
        # 添加六神、六亲和纳甲信息
        liushen_str = liushen[i] if i < len(liushen) else ""
        liuqin_str = liuqin[i] if i < len(liuqin) else ""
        najia_str = najia[i] if i < len(najia) else ""
        
        lines.append(f"{liushen_str}\u3000{liuqin_str}{najia_str}\u3000{ben_symbol}\u3000{mark_str}\u3000→\u3000{bian_symbol}")
    
    # 添加空亡信息
    kongwang_str = "、".join(result.get('kongwang', [])) or "无"
    footer = f"\n空亡：{kongwang_str}"
    
    # 添加世应爻位置
    if shi_yao_pos:
        footer += f"\n世爻：第{shi_yao_pos}爻（{liuqin[shi_yao_pos-1] if shi_yao_pos-1 < len(liuqin) else ''}）"
    if ying_yao_pos:
        footer += f"\n应爻：第{ying_yao_pos}爻（{liuqin[ying_yao_pos-1] if ying_yao_pos-1 < len(liuqin) else ''}）"
    if dong_yao_pos:
        footer += f"\n动爻：第{dong_yao_pos}爻（{liuqin[dong_yao_pos-1] if dong_yao_pos-1 < len(liuqin) else ''}）"
    
    return header + "\n".join(lines) + footer

def format_for_print(result: Dict) -> str:
    """
    格式化卦象结果为适合打印的格式
    
    参数:
        result (Dict): 卦象计算结果
        
    返回:
        str: 格式化后的打印字符串
    """
    # 提取日期时间信息
    date_info = result.get('date_info', {})
    solar_date = date_info.get('solar_date', '')
    adjusted_time_hour = date_info.get('adjusted_time_hour', 0)
    lunar_date = date_info.get('lunar_date', '')
    year_gz = date_info.get('year_gz', '')
    month_gz = date_info.get('month_gz', '')
    day_gz = date_info.get('day_gz', '')
    hour_gz = date_info.get('hour_gz', '')
    
    # 解析年月日格式
    if isinstance(solar_date, str) and '-' in solar_date:
        parts = solar_date.split('-')
        if len(parts) == 3:
            year, month, day = parts
            solar_date_str = f"{year}年 {month}月 {day}日"
        else:
            solar_date_str = solar_date
    else:
        solar_date_str = str(solar_date)
        
    # 格式化时间
    if isinstance(adjusted_time_hour, float) or isinstance(adjusted_time_hour, int):
        hour = int(adjusted_time_hour)
        minute = int((adjusted_time_hour - hour) * 60)
        time_str = f"{hour}时 {minute}分"
    else:
        time_str = f"{adjusted_time_hour:.2f}时"
    
    # 提取卦象信息
    ben_gua_name = result['ben_gua']['name']
    bian_gua_name = result['bian_gua']['name']
    ben_palace = remove_duplicate_gong(result['ben_gua'].get('palace', '未知宫'))
    bian_palace = remove_duplicate_gong(result['bian_gua'].get('palace', '未知宫'))
    
    # 构建头部信息 - 使用优化的日期时间格式
    header = f"公历：{solar_date_str} {time_str}\n"
    header += f"农历：{lunar_date}\n"
    header += f"干支：{year_gz}年 {month_gz}月 {day_gz}日 {hour_gz}时\n"
    
    # 选择哪个格式的排盘信息
    # 尝试使用 generate_najia_style_display 如果函数可用
    header += f"得「{ben_gua_name}」之「{bian_gua_name}」卦\n"
    
    # 使用改进后的 najia_style 排盘格式
    gua_display = generate_najia_style_display(result)
    
    # 组合完整显示
    return header + gua_display
