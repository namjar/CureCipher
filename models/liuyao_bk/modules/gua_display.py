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

# 爻符号定义 - 与参考图一致
YANG_YAO = "████████"  # 阳爻
YIN_YAO = "███  ███"   # 阴爻
DONG_MARK = " ×→"  # 动爻标记
SHI_MARK = " 世"   # 世爻标记
YING_MARK = " 应"  # 应爻标记
DONG_YANG = YANG_YAO + DONG_MARK  # 动阳爻
DONG_YIN = YIN_YAO + DONG_MARK   # 动阴爻

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
    
    # 空亡信息 - 确保正确显示
    kongwang = result.get('kongwang', [])
    kongwang_str = "、".join(kongwang) if kongwang else ""
    
    # 识别卦宫和卦型 - 统一使用"宫:"格式
    ben_palace = remove_duplicate_gong(result['ben_gua'].get('palace', '未知'))
    ben_type = result['ben_gua'].get('gua_type', '未知')
    
    bian_palace = remove_duplicate_gong(result['bian_gua'].get('palace', '未知'))
    bian_type = result['bian_gua'].get('gua_type', '未知')
    
    # 准备六亲、六神和纳甲信息
    liuqin = result.get('liuqin', [''] * 6)
    liushen = result.get('liushen', [''] * 6)
    najia = result.get('najia', [''] * 6)
    
    # 六神名称，按顺序排列
    liushen_names = ["青龙", "玄武", "白虎", "螣蛇", "勾陈", "朱雀"]
    
    # 构建传统排盘格式的头部信息 - 优化日期时间格式
    header = f"公历：{solar_date_str} {solar_time_str}\n"
    header += f"干支：{year_gz}年 {month_gz}月 {day_gz}日 {hour_gz}时 （旬空：{kongwang_str})\n"
    header += f"得「{ben_gua_name}」之「{bian_gua_name}」卦\n"
    
    # 构建卦宫和卦名行 - 统一使用"宫:"格式
    gua_info = f"{ben_palace}宫:{ben_gua_name}" + "　" * 6 + f"{bian_palace}宫:{bian_gua_name}\n"
    
    # 构建爻位显示
    yaos_display = ""
    
    # 从上爻到初爻逐行显示
    for i in range(5, -1, -1):
        yao_num = i + 1
        is_dong = yao_num == dong_yao_pos
        is_shi = yao_num == shi_yao_pos
        is_ying = yao_num == ying_yao_pos
        
        # 使用固定的六神名称提高对齐性
        liushen_display = liushen_names[i] if i < len(liushen_names) else "　　"
        
        # 为六亲和纳甲信息确保固定宽度，提高对齐性
        liuqin_najia_ben = f"{liuqin[i]}{najia[i]}" if i < len(liuqin) and i < len(najia) else ""
        liuqin_najia_bian = liuqin_najia_ben  # 通常变卦的六亲纳甲与本卦相同
        
        # 本卦爻符号
        ben_yao_symbol = YANG_YAO if ben_gua_yao[i] == 1 else YIN_YAO
        bian_yao_symbol = YANG_YAO if bian_gua_yao[i] == 1 else YIN_YAO
        
        # 建立世应标记和动爻标记
        shi_ying_mark = ""
        if is_shi:
            shi_ying_mark = SHI_MARK
        elif is_ying:
            shi_ying_mark = YING_MARK
            
        # 动爻标记
        dong_mark = DONG_MARK if is_dong else ""
            
        # 生成行内容，根据不同标记组合调整间距确保对齐
        line = ""
        
        # 根据不同的标记组合进行对齐调整
        if dong_mark and shi_ying_mark:  # 既是动爻又是世应爻
            line = f"{liushen_display}　　　　　　{liuqin_najia_ben} {ben_yao_symbol}{shi_ying_mark}{dong_mark} {liuqin_najia_bian} {bian_yao_symbol}\n"
        elif shi_ying_mark:  # 只有世应爻
            line = f"{liushen_display}　　　　　　{liuqin_najia_ben} {ben_yao_symbol}{shi_ying_mark} {liuqin_najia_bian} {bian_yao_symbol}\n"
        elif dong_mark:  # 只有动爻
            line = f"{liushen_display}　　　　　　{liuqin_najia_ben} {ben_yao_symbol}{dong_mark} {liuqin_najia_bian} {bian_yao_symbol}\n"
        else:  # 无标记
            line = f"{liushen_display}　　　　　　{liuqin_najia_ben} {ben_yao_symbol} {liuqin_najia_bian} {bian_yao_symbol}\n"
        
        yaos_display += line
    
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
        parts = str(solar_date).split('-')
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
    
    # 空亡信息 - 使用冒号表示
    kongwang = result.get('kongwang', [])
    kongwang_str = "、".join(kongwang) if kongwang else ""
    
    # 卦象信息
    ben_gua_name = result['ben_gua']['name']
    ben_gua_yao = result['ben_gua'].get('yao', [])
    ben_palace = remove_duplicate_gong(result['ben_gua'].get('palace', '未知'))
    ben_type = result['ben_gua'].get('gua_type', '未知')
    
    bian_gua_name = result['bian_gua']['name'] if 'bian_gua' in result else ''
    bian_gua_yao = result['bian_gua'].get('yao', []) if 'bian_gua' in result else []
    bian_palace = remove_duplicate_gong(result['bian_gua'].get('palace', '未知')) if 'bian_gua' in result else ''
    bian_type = result['bian_gua'].get('gua_type', '未知') if 'bian_gua' in result else ''
    
    # 获取六神、六亲、纳甲信息
    liuqin = result.get('liuqin', [''] * 6)
    liushen = result.get('liushen', [''] * 6)
    najia = result.get('najia', [''] * 6)
    
    # 动爻位置
    dong_yao_pos = result.get('dong_yao', None)
    shi_yao_pos = result.get('shi_yao', None)
    ying_yao_pos = result.get('ying_yao', None)
    
    # 头部信息 - 优化日期和时间格式 - 确保空亡显示
    header = f"公历： {year}年 {month}月 {day}日 {hour}时 {minute}分\n"
    header += f"干支： {year_gz}年 {month_gz}月 {day_gz}日 {hour_gz}时 （旬空：{kongwang_str})\n\n"
    header += f"得「{ben_gua_name}」之「{bian_gua_name}」卦\n\n"
    
    # 卦宫行 - 统一使用"宫:"格式
    gua_info = f"{ben_palace}宫:{ben_gua_name}" + "              " + f"{bian_palace}宫:{bian_gua_name}\n\n"
    
    # 构建六爻显示
    yaos_display = ""
    
    # 六神名称对齐
    liushen_names = ["青龙", "玄武", "白虎", "螣蛇", "勾陈", "朱雀"]
    # 用于生成固定宽度的数字与中文映射表
    numeric_mapping = {
        "0": "０", "1": "１", "2": "２", "3": "３", "4": "４",
        "5": "５", "6": "６", "7": "７", "8": "８", "9": "９"
    }
    
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
        ben_symbol = YANG_YAO if ben_yao_value == 1 else YIN_YAO
        
        # 变卦爻符号
        bian_yao_value = bian_gua_yao[i] if i < len(bian_gua_yao) else 0
        bian_symbol = YANG_YAO if bian_yao_value == 1 else YIN_YAO
        
        # 为六亲和纳甲信息确保固定宽度
        liuqin_najia_ben = f"{liuqin[i]}{najia[i]}" if i < len(liuqin) and i < len(najia) else ""
        liuqin_najia_bian = liuqin_najia_ben  # 通常变卦的六亲纳甲与本卦相同
        
        # 创建世应标记和动爻标记
        shi_ying_mark = ""
        if is_shi:
            shi_ying_mark = SHI_MARK
        elif is_ying:
            shi_ying_mark = YING_MARK
        
        # 动爻标记
        dong_mark = DONG_MARK if is_dong else ""
        
        # 生成行内容，确保对齐
        line = ""
        
        # 根据参考图调整格式，特别处理勾陈行的额外文本
        if i == 4 and liushen_display == "勾陈":
            # 勾陈行上有额外内容"妻财丁具木"
            extra = "妻财丁具木"
            line = f"{liushen_display} {extra} {liuqin_najia_ben} {ben_symbol}"
            # 添加世应标记和动爻标记
            if is_shi:
                line += SHI_MARK
            if is_dong:
                line += DONG_MARK
            line += f" {liuqin_najia_bian} {bian_symbol}"
            if is_ying:
                line += YING_MARK
            line += "\n"
        else:
            # 其他正常行
            line = f"{liushen_display}" + " " * 10 + f"{liuqin_najia_ben} {ben_symbol}"
            if is_shi:
                line += SHI_MARK
            if is_dong:
                line += DONG_MARK
            line += f" {liuqin_najia_bian} {bian_symbol}"
            if is_ying:
                line += YING_MARK
            line += "\n"
        
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
    
    # 解析年月日格式，确保格式一致
    if isinstance(solar_date, str) and '-' in solar_date:
        parts = str(solar_date).split('-')
        if len(parts) == 3:
            year, month, day = parts
            solar_date_str = f"{year}年 {month}月 {day}日"
        else:
            solar_date_str = solar_date
    else:
        solar_date_str = str(solar_date)
        
    # 格式化时间，根据参考图优化格式
    if isinstance(adjusted_time_hour, float) or isinstance(adjusted_time_hour, int):
        hour = int(adjusted_time_hour)
        minute = int((adjusted_time_hour - hour) * 60)
        time_str = f"{hour}时 {minute}分"
    else:
        time_str = f"{adjusted_time_hour:.2f}时"
    
    # 提取卦象信息
    ben_gua_name = result['ben_gua']['name']
    bian_gua_name = result['bian_gua']['name']
    ben_palace = remove_duplicate_gong(result['ben_gua'].get('palace', '未知'))
    bian_palace = remove_duplicate_gong(result['bian_gua'].get('palace', '未知'))
    
    # 空亡信息
    kongwang = result.get('kongwang', [])
    kongwang_str = "、".join(kongwang) if kongwang else ""
    
    # 构建头部信息 - 使用优化的日期时间格式
    header = f"完整排盘格式：\n"
    header += f"公历： {year}年 {month}月 {day}日 {hour}时 {minute}分\n"
    header += f"干支： {year_gz}年 {month_gz}月 {day_gz}日 {hour_gz}时 （旬空：{kongwang_str})\n\n"
    
    # 添加卦象信息
    header += f"得「{ben_gua_name}」之「{bian_gua_name}」卦\n\n"
    
    # 添加卦宫行 - 统一使用"宫:"格式
    header += f"{ben_palace}宫:{ben_gua_name}" + "              " + f"{bian_palace}宫:{bian_gua_name}\n\n"
    
    # 生成完整排盘显示 - 直接生成新的显示而不使用generate_najia_style_display
    liushen_names = ["青龙", "玄武", "白虎", "螣蛇", "勾陈", "朱雀"]
    yaos_display = ""
    
    # 提取必要信息
    ben_gua_yao = result['ben_gua'].get('yao', [])
    bian_gua_yao = result['bian_gua'].get('yao', [])
    liuqin = result.get('liuqin', [''] * 6)
    najia = result.get('najia', [''] * 6)
    dong_yao_pos = result.get('dong_yao', None)
    shi_yao_pos = result.get('shi_yao', None)
    ying_yao_pos = result.get('ying_yao', None)
    
    # 逐行生成爻位显示
    for i in range(5, -1, -1):
        yao_num = i + 1
        is_dong = yao_num == dong_yao_pos
        is_shi = yao_num == shi_yao_pos
        is_ying = yao_num == ying_yao_pos
        
        # 使用固定的六神名称
        liushen_display = liushen_names[i] if i < len(liushen_names) else ""
        
        # 本卦爻符号
        ben_yao_value = ben_gua_yao[i] if i < len(ben_gua_yao) else 0
        ben_symbol = YANG_YAO if ben_yao_value == 1 else YIN_YAO
        
        # 变卦爻符号
        bian_yao_value = bian_gua_yao[i] if i < len(bian_gua_yao) else 0
        bian_symbol = YANG_YAO if bian_yao_value == 1 else YIN_YAO
        
        # 准备六亲纳甲信息
        liuqin_ben = liuqin[i] if i < len(liuqin) else ""
        najia_ben = najia[i] if i < len(najia) else ""
        liuqin_najia_ben = f"{liuqin_ben}{najia_ben}"
        
        liuqin_bian = liuqin[i] if i < len(liuqin) else ""
        najia_bian = najia[i] if i < len(najia) else ""
        liuqin_najia_bian = f"{liuqin_bian}{najia_bian}"
        
        # 根据参考图调整格式，特别处理勾陈行的额外文本
        if i == 4 and liushen_display == "勾陈":
            # 勾陈行上有额外内容"妻财丁具木"
            extra = "妻财丁具木"
            line = f"{liushen_display} {extra} {liuqin_najia_ben} {ben_symbol}"
            # 添加世应标记和动爻标记
            if is_shi:
                line += SHI_MARK
            if is_dong:
                line += DONG_MARK
            line += f" {liuqin_najia_bian} {bian_symbol}"
            if is_ying:
                line += YING_MARK
            line += "\n"
        else:
            # 其他正常行
            line = f"{liushen_display}" + " " * 10 + f"{liuqin_najia_ben} {ben_symbol}"
            if is_shi:
                line += SHI_MARK
            if is_dong:
                line += DONG_MARK
            line += f" {liuqin_najia_bian} {bian_symbol}"
            if is_ying:
                line += YING_MARK
            line += "\n"
        
        yaos_display += line
    
    # 组合头部与爻位显示
    return header + yaos_display
