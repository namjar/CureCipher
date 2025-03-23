"""
卦象图形化显示模块 - 提供六爻卦象的ASCII和Unicode图形表示
"""

from typing import List, Dict, Tuple, Optional, Union

# 爻符号定义
YANG_YAO = "———"  # 阳爻
YIN_YAO = "— —"   # 阴爻
DONG_YANG = "⚊○⚊"  # 动阳爻
DONG_YIN = "⚋○⚋"   # 动阴爻

# 卦象映射
GUA_MAP = {
    "乾": [1, 1, 1, 1, 1, 1], "坤": [0, 0, 0, 0, 0, 0], 
    "震": [1, 0, 0, 0, 0, 0], "艮": [0, 0, 0, 0, 0, 1],
    "离": [1, 0, 1, 0, 1, 0], "坎": [0, 1, 0, 1, 0, 1],
    "兑": [1, 0, 0, 0, 1, 0], "巽": [0, 1, 0, 0, 0, 1]
}

GUA_NAMES = {
    "111111": "乾", "000000": "坤", 
    "100000": "震", "000001": "艮",
    "101010": "离", "010101": "坎",
    "100010": "兑", "010001": "巽"
}

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

def generate_gua_ascii(ben_gua: List[int], dong_yao_pos: Optional[int] = None) -> str:
    """
    生成本卦的ASCII图形
    
    参数:
        ben_gua (List[int]): 本卦爻值列表，从下到上6爻，1表示阳爻，0表示阴爻
        dong_yao_pos (int, optional): 动爻位置，1-6，默认None表示无动爻
        
    返回:
        str: 格式化的ASCII卦象图
    """
    lines = []
    for i in range(5, -1, -1):  # 从上到下遍历爻
        is_dong = dong_yao_pos == i + 1 if dong_yao_pos else False
        lines.append(f"{i+1}: {yao_to_string(ben_gua[i], is_dong)}")
    
    # 组合成卦象图
    return "\n".join(lines)

def generate_gua_summary(ben_gua: List[int], bian_gua: List[int], dong_yao_pos: int) -> str:
    """
    生成完整的卦象变化摘要
    
    参数:
        ben_gua (List[int]): 本卦爻值列表
        bian_gua (List[int]): 变卦爻值列表
        dong_yao_pos (int): 动爻位置，1-6
        
    返回:
        str: 卦象变化摘要
    """
    # 获取卦名
    ben_code = "".join(str(y) for y in ben_gua)
    bian_code = "".join(str(y) for y in bian_gua)
    
    ben_name = GUA_NAMES.get(ben_code, "未知卦")
    bian_name = GUA_NAMES.get(bian_code, "未知卦")
    
    # 生成本卦和变卦的ASCII图
    ben_ascii = generate_gua_ascii(ben_gua, dong_yao_pos)
    bian_ascii = generate_gua_ascii(bian_gua)
    
    # 组合成摘要
    summary = [
        f"本卦：{ben_name}卦",
        ben_ascii,
        f"变爻：第{dong_yao_pos}爻",
        f"变卦：{bian_name}卦",
        bian_ascii
    ]
    
    return "\n".join(summary)

def generate_full_gua_display(result: Dict) -> str:
    """
    根据计算结果生成完整的卦象显示
    
    参数:
        result (Dict): 卦象计算结果
        
    返回:
        str: 格式化的卦象显示字符串
    """
    # 提取本卦和变卦信息
    ben_gua_name = result['ben_gua']['name']
    ben_gua_yao = result['ben_gua'].get('yao', GUA_MAP.get(ben_gua_name, [1, 1, 1, 0, 0, 0]))
    
    bian_gua_name = result['bian_gua']['name']
    bian_gua_yao = result['bian_gua'].get('yao', GUA_MAP.get(bian_gua_name, [0, 0, 0, 1, 1, 1]))
    
    dong_yao_pos = result['dong_yao']
    
    # 生成卦象ASCII图
    gua_display = generate_gua_summary(ben_gua_yao, bian_gua_yao, dong_yao_pos)
    
    # 添加六亲、六神信息
    if 'liuqin' in result and 'liushen' in result:
        gua_display += "\n\n六亲六神对照表："
        for i in range(6):
            yao_name = "初爻" if i == 0 else "六爻" if i == 5 else f"第{i+1}爻"
            liuqin = result['liuqin'][i] if i < len(result['liuqin']) else "未知"
            liushen = result['liushen'][i] if i < len(result['liushen']) else "未知"
            gua_display += f"\n{yao_name}: {liuqin} {liushen}"
    
    # 添加世应信息
    if 'shi_yao' in result and 'ying_yao' in result:
        gua_display += f"\n\n世爻：第{result['shi_yao']}爻"
        gua_display += f"\n应爻：第{result['ying_yao']}爻"
    
    return gua_display

# 用于生成图像的字符表示
def gua_to_image_text(ben_gua: List[int], bian_gua: List[int], dong_yao_pos: int) -> str:
    """
    生成用于图像渲染的字符表示
    
    参数:
        ben_gua (List[int]): 本卦爻值列表
        bian_gua (List[int]): 变卦爻值列表
        dong_yao_pos (int): 动爻位置，1-6
        
    返回:
        str: 用于生成图像的文本表示
    """
    # 获取卦名
    ben_code = "".join(str(y) for y in ben_gua)
    bian_code = "".join(str(y) for y in bian_gua)
    
    ben_name = GUA_NAMES.get(ben_code, "未知卦")
    bian_name = GUA_NAMES.get(bian_code, "未知卦")
    
    # 符号定义
    yang = "▅▅▅▅▅"
    yin = "▅▅ ▅▅"
    dong_yang = "▅▅○▅▅"
    dong_yin = "▅▅○ ▅"
    
    # 构建本卦
    ben_lines = ["本卦：" + ben_name]
    for i in range(5, -1, -1):  # 从上到下
        is_dong = dong_yao_pos == i + 1
        if ben_gua[i] == 1:  # 阳爻
            line = dong_yang if is_dong else yang
        else:  # 阴爻
            line = dong_yin if is_dong else yin
        ben_lines.append(line)
    
    # 构建变卦
    bian_lines = ["变卦：" + bian_name]
    for i in range(5, -1, -1):  # 从上到下
        line = yang if bian_gua[i] == 1 else yin
        bian_lines.append(line)
    
    # 合并
    all_lines = []
    for i in range(len(ben_lines)):
        all_lines.append(f"{ben_lines[i]}     {bian_lines[i] if i < len(bian_lines) else ''}")
    
    return "\n".join(all_lines)
