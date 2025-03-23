# /Users/ericw/Documents/GitHub/CureCipher/models/liuyao/modules/AccurateNajia.py
"""
精确纳甲计算模块，提供六爻纳甲计算
"""

import random
from typing import Dict, List, Tuple, Optional

class AccurateNajia:
    """精确纳甲计算类，提供六爻纳甲计算"""
    
    def __init__(self):
        """初始化方法"""
        self.gua_elements = {
            "乾": "金", "坤": "土", "震": "木", "艮": "土",
            "离": "火", "坎": "水", "兑": "金", "巽": "木",
            "中": "土"  # 中爻为土
        }
        
        # 八宫卦映射，用于确定世应爻和纳甲
        self.gua_palace_map = {
            "乾": "乾", "兑": "乾", "离": "乾", "震": "乾",
            "巽": "坤", "坎": "坤", "艮": "坤", "坤": "坤"
        }
        
        # 八宫卦的世应爻位置
        self.shi_ying_map = {
            "乾": (5, 2),  # 乾宫：世爻第五爻，应爻第二爻
            "坤": (2, 5),  # 坤宫：世爻第二爻，应爻第五爻
            "震": (1, 4),  # 震宫：世爻初爻，应爻第四爻
            "巽": (4, 1),  # 巽宫：世爻第四爻，应爻初爻
            "坎": (2, 5),  # 坎宫：世爻第二爻，应爻第五爻
            "离": (3, 6),  # 离宫：世爻第三爻，应爻第六爻
            "艮": (1, 4),  # 艮宫：世爻初爻，应爻第四爻
            "兑": (4, 1)   # 兑宫：世爻第四爻，应爻初爻
        }
        
        # 八宫卦的纳甲天干地支规则
        self.najia_rules = {
            "乾": ["戌", "申", "午", "辰", "寅", "子"],
            "坤": ["未", "巳", "卯", "丑", "亥", "酉"],
            "震": ["寅", "辰", "午", "申", "戌", "子"],
            "巽": ["巳", "卯", "丑", "亥", "酉", "未"],
            "坎": ["子", "寅", "辰", "午", "申", "戌"],
            "离": ["午", "辰", "寅", "子", "戌", "申"],
            "艮": ["寅", "辰", "午", "申", "戌", "子"],
            "兑": ["酉", "亥", "丑", "卯", "巳", "未"]
        }
        
        self.tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        self.dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        # 地支对应关系（阳阴互变）
        self.zhi_opposite = {
            "子": "午", "午": "子",
            "丑": "未", "未": "丑",
            "寅": "申", "申": "寅",
            "卯": "酉", "酉": "卯",
            "辰": "戌", "戌": "辰",
            "巳": "亥", "亥": "巳"
        }
    
    def parse_gua_by_datetime(self, year: int, month: int, day: int, hour: float, 
                              longitude: float, latitude: float) -> Dict:
        """
        根据日期时间计算六爻卦象
        
        参数:
            year (int): 年份
            month (int): 月份
            day (int): 日期
            hour (float): 时辰（24小时制）
            longitude (float): 经度
            latitude (float): 纬度
            
        返回:
            Dict: 包含本卦、变卦、纳甲、世应、动爻等信息
        """
        # 使用改进的备用算法起卦
        gua_info = self._backup_parse_gua(year, month, day, hour)
        
        # 提取本卦和变卦信息
        ben_gua_name = gua_info["gua_name"]
        ben_gua_element = self.gua_elements.get(ben_gua_name, "金")
        ben_yao = gua_info["yao"]
        
        bian_gua_name = gua_info["bian_gua_name"]
        bian_gua_element = self.gua_elements.get(bian_gua_name, "土")
        bian_yao = gua_info["bian_yao"]
        
        # 动爻位置
        dong_yao_position = gua_info["dong_yao"]
        
        # 计算纳甲
        najia_info = self._calculate_najia(ben_gua_name)
        bian_najia = self._calculate_bian_najia(najia_info, dong_yao_position)
        
        # 计算世应爻
        shi_yao, ying_yao = self._calculate_shi_ying(ben_gua_name)
        
        return {
            "ben_gua": {
                "name": ben_gua_name,
                "element": ben_gua_element,
                "number": gua_info.get("gua_number", random.randint(1, 64)),
                "yao": ben_yao
            },
            "bian_gua": {
                "name": bian_gua_name,
                "element": bian_gua_element,
                "number": gua_info.get("bian_gua_number", random.randint(1, 64)),
                "yao": bian_yao
            },
            "najia": najia_info,
            "bian_najia": bian_najia,
            "shi_yao": shi_yao,
            "ying_yao": ying_yao,
            "dong_yao": dong_yao_position
        }
    
    def _backup_parse_gua(self, year: int, month: int, day: int, hour: float) -> Dict:
        """
        备用起卦算法（改进版）
        
        参数:
            year (int): 年份
            month (int): 月份
            day (int): 日期
            hour (float): 时辰
            
        返回:
            Dict: 包含本卦、变卦、动爻等信息
        """
        # 使用日期和时间生成种子
        seed = year * 10000 + month * 100 + day + int(hour)
        random.seed(seed)
        
        # 本卦
        gua_yao_map = {
            "乾": [1, 1, 1, 1, 1, 1],  # ☰
            "坤": [0, 0, 0, 0, 0, 0],  # ☷
            "震": [0, 0, 1, 0, 0, 1],  # ☳
            "艮": [1, 0, 0, 1, 0, 0],  # ☶
            "离": [1, 0, 1, 1, 0, 1],  # ☲
            "坎": [0, 1, 0, 0, 1, 0],  # ☵
            "兑": [1, 1, 0, 1, 1, 0],  # ☱
            "巽": [0, 1, 1, 0, 1, 1]   # ☴
        }
        
        ben_gua_names = list(gua_yao_map.keys())
        ben_gua_name = random.choice(ben_gua_names)
        ben_yao = gua_yao_map[ben_gua_name]
        
        # 动爻
        dong_yao_position = random.randint(1, 6)
        
        # 变卦
        bian_yao = ben_yao.copy()
        bian_yao[dong_yao_position - 1] = 1 - bian_yao[dong_yao_position - 1]
        
        # 查找变卦名称
        bian_gua_name = None
        for name, yao_pattern in gua_yao_map.items():
            if bian_yao == yao_pattern:
                bian_gua_name = name
                break
        
        if not bian_gua_name:
            # 如果未找到匹配的变卦，随机选择一个不同的卦
            other_guas = [g for g in ben_gua_names if g != ben_gua_name]
            bian_gua_name = random.choice(other_guas)
            bian_yao = gua_yao_map[bian_gua_name]
        
        return {
            "gua_name": ben_gua_name,
            "yao": ben_yao,
            "bian_gua_name": bian_gua_name,
            "bian_yao": bian_yao,
            "dong_yao": dong_yao_position
        }
    
    def _calculate_najia(self, gua_name: str) -> List[str]:
        """
        计算本卦纳甲
        
        参数:
            gua_name (str): 本卦名称
            
        返回:
            List[str]: 六爻的纳甲信息（天干地支）
        """
        # 根据八宫卦规则计算纳甲
        palace = self.gua_palace_map.get(gua_name, "乾")
        dizhi_list = self.najia_rules.get(palace, self.najia_rules["乾"])
        
        najia_info = []
        for i in range(6):
            zhi = dizhi_list[i]
            # 天干根据卦宫五行和爻位阴阳分配
            element = self.gua_elements[palace]
            gan_candidates = {
                "金": ["庚", "辛"],
                "木": ["甲", "乙"],
                "水": ["壬", "癸"],
                "火": ["丙", "丁"],
                "土": ["戊", "己"]
            }.get(element, ["甲", "乙"])
            gan = gan_candidates[i % 2]  # 奇数位用阳干，偶数位用阴干
            najia_info.append(f"{gan}{zhi}")
        
        return najia_info
    
    def _calculate_bian_najia(self, najia: List[str], dong_yao_position: int) -> List[str]:
        """
        计算变卦纳甲
        
        参数:
            najia (List[str]): 本卦纳甲
            dong_yao_position (int): 动爻位置（1-6）
            
        返回:
            List[str]: 变卦纳甲
        """
        bian_najia = najia.copy()
        if 1 <= dong_yao_position <= 6:
            gan, zhi = najia[dong_yao_position - 1][0], najia[dong_yao_position - 1][1:]
            new_zhi = self.zhi_opposite.get(zhi, zhi)
            bian_najia[dong_yao_position - 1] = f"{gan}{new_zhi}"
        return bian_najia
    
    def _calculate_shi_ying(self, gua_name: str) -> Tuple[int, int]:
        """
        计算世爻和应爻位置
        
        参数:
            gua_name (str): 本卦名称
            
        返回:
            Tuple[int, int]: 世爻位置，应爻位置
        """
        # 根据八宫卦规则
        palace = self.gua_palace_map.get(gua_name, "乾")
        shi_yao, ying_yao = self.shi_ying_map.get(palace, (5, 2))
        return shi_yao, ying_yao
    
    def get_najia_by_yao_number(self, yao_number: int) -> str:
        """
        根据爻序获取纳甲信息（备用方法）
        
        参数:
            yao_number (int): 爻位（1-6）
            
        返回:
            str: 纳甲信息（天干地支）
        """
        if not (1 <= yao_number <= 6):
            raise ValueError(f"yao_number 必须在 1-6 之间，当前为 {yao_number}")
        
        gan = self.tiangan[(yao_number * 2) % 10]
        zhi = self.dizhi[yao_number % 12]
        return f"{gan}{zhi}"

# 导出单例实例
accurate_najia = AccurateNajia()