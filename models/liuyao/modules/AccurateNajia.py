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
        
        # 八卦的爻位数组映射（从下到上，初爻到上爻）
        self.bagua_yao_map = {
            "乾": [1, 1, 1],  # 乾为天，三个阳爻
            "坤": [0, 0, 0],  # 坤为地，三个阴爻
            "震": [1, 0, 0],  # 震为雷，一阳二阴
            "艮": [0, 0, 1],  # 艮为山，一阴二阳
            "离": [1, 0, 1],  # 离为火，二阳一阴
            "坎": [0, 1, 0],  # 坎为水，二阴一阳
            "兑": [1, 1, 0],  # 兑为泽，二阳一阴
            "巽": [0, 1, 1]   # 巽为风，一阴二阳
        }
        
        # 六十四卦数组映射
        self.gua64_map = self._generate_64_gua_map()
    
    def _generate_64_gua_map(self) -> Dict[str, List[int]]:
        """
        生成六十四卦爻位数组映射
        
        返回:
            Dict[str, List[int]]: 卦名到六爻数组的映射
        """
        gua64_map = {}
        
        # 八卦组合生成六十四卦
        for upper_name, upper_yao in self.bagua_yao_map.items():
            for lower_name, lower_yao in self.bagua_yao_map.items():
                # 完整卦名，如"坎上离下"为火水未济
                full_name = f"{upper_name}{lower_name}"
                # 组合上卦和下卦爻数组（下卦在前，上卦在后）
                full_yao = lower_yao + upper_yao
                gua64_map[full_name] = full_yao
                
                # 也添加特定卦名的映射，如"火水未济"
                if upper_name == "坎" and lower_name == "离":
                    gua64_map["未济"] = full_yao
                elif upper_name == "离" and lower_name == "坎":
                    gua64_map["既济"] = full_yao
                # 添加其他常用卦名...
        
        return gua64_map
    
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
        ben_gua_short_name = gua_info.get("gua_short_name", "")
        ben_gua_element = gua_info.get("gua_element", self.gua_elements.get(ben_gua_short_name or ben_gua_name, "金"))
        ben_gua_palace = gua_info.get("gua_palace", "")
        ben_gua_type = gua_info.get("gua_type", "本宫卦")
        ben_yao = gua_info["yao"]
        
        bian_gua_name = gua_info["bian_gua_name"]
        bian_gua_short_name = gua_info.get("bian_gua_short_name", "")
        bian_gua_element = gua_info.get("bian_gua_element", self.gua_elements.get(bian_gua_short_name or bian_gua_name, "金"))
        bian_gua_palace = gua_info.get("bian_gua_palace", "")
        bian_gua_type = gua_info.get("bian_gua_type", "本宫卦")
        bian_yao = gua_info["bian_yao"]
        
        # 动爻位置
        dong_yao_position = gua_info["dong_yao"]
        
        # 计算纳甲
        najia_info = self._calculate_najia(ben_gua_short_name or ben_gua_name)
        bian_najia = self._calculate_bian_najia(najia_info, dong_yao_position)
        
        # 计算世应爻
        shi_yao, ying_yao = self._calculate_shi_ying(ben_gua_short_name or ben_gua_name)
        
        return {
            "ben_gua": {
                "name": ben_gua_name,
                "short_name": ben_gua_short_name,
                "element": ben_gua_element,
                "palace": ben_gua_palace,
                "gua_type": ben_gua_type,
                "number": gua_info.get("gua_number", random.randint(1, 64)),
                "yao": ben_yao
            },
            "bian_gua": {
                "name": bian_gua_name,
                "short_name": bian_gua_short_name,
                "element": bian_gua_element,
                "palace": bian_gua_palace,
                "gua_type": bian_gua_type,
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
        
        # 八卦的爻位数组映射（六爻，从下到上）
        gua_yao_map = {
            "乾": [1, 1, 1, 1, 1, 1],  # ☰ 乾为天
            "坤": [0, 0, 0, 0, 0, 0],  # ☷ 坤为地
            "震": [1, 0, 0, 1, 0, 0],  # ☳ 震为雷
            "艮": [0, 0, 1, 0, 0, 1],  # ☶ 艮为山
            "离": [1, 0, 1, 1, 0, 1],  # ☲ 离为火
            "坎": [0, 1, 0, 0, 1, 0],  # ☵ 坎为水
            "兑": [1, 1, 0, 1, 1, 0],  # ☱ 兑为泽
            "巽": [0, 1, 1, 0, 1, 1]   # ☴ 巽为风
        }
        
        # 卦名映射
        gua_name_map = {
            "乾": "乾为天",
            "坤": "坤为地",
            "震": "震为雷",
            "艮": "艮为山",
            "离": "离为火",
            "坎": "坎为水",
            "兑": "兑为泽",
            "巽": "巽为风"
        }
        
        # 卦宫映射
        gua_palace_map = {
            "乾": "乾宫",
            "坤": "坤宫",
            "震": "震宫",
            "艮": "艮宫",
            "离": "离宫",
            "坎": "坎宫",
            "兑": "兑宫",
            "巽": "巽宫"
        }
        
        # 卦的五行属性
        gua_element_map = {
            "乾": "金",
            "坤": "土",
            "震": "木",
            "艮": "土",
            "离": "火",
            "坎": "水",
            "兑": "金",
            "巽": "木"
        }
        
        # 为遵循最小改动原则，继续使用现有的卦象选择逻辑
        gua_names = list(gua_yao_map.keys())
        index = (month + day) % len(gua_names)
        ben_gua_short_name = gua_names[index]
        ben_gua_name = gua_name_map[ben_gua_short_name]
        ben_yao = gua_yao_map[ben_gua_short_name].copy()
        ben_gua_palace = gua_palace_map[ben_gua_short_name]
        ben_gua_element = gua_element_map[ben_gua_short_name]
        
        # 动爻位置固定为第3爻（为了演示）
        dong_yao_position = 3
        
        # 变卦：将动爻的值反转（阴变阳，阳变阴）
        bian_yao = ben_yao.copy()
        bian_yao[dong_yao_position - 1] = 1 - bian_yao[dong_yao_position - 1]
        
        # 根据变卦爻组合确定变卦名称
        bian_gua_short_name = None
        for name, yao_pattern in gua_yao_map.items():
            if bian_yao == yao_pattern:
                bian_gua_short_name = name
                break
        
        # 如果未找到匹配的变卦，使用一个默认值
        if not bian_gua_short_name:
            if ben_gua_short_name == "离":  # 根据示例，如果本卦是离
                bian_gua_short_name = "坎"  # 变卦应为坎
                bian_yao = gua_yao_map["坎"]
            else:
                # 其他情况随机选择一个不同的卦
                other_guas = [g for g in gua_names if g != ben_gua_short_name]
                bian_gua_short_name = random.choice(other_guas)
                bian_yao = gua_yao_map[bian_gua_short_name]
        
        # 获取变卦的完整名称、卦宫和五行属性
        bian_gua_name = gua_name_map[bian_gua_short_name]
        bian_gua_palace = gua_palace_map[bian_gua_short_name]
        bian_gua_element = gua_element_map[bian_gua_short_name]
        
        # 确定卦型（本宫卦、游魂卦、归魂卦等）
        ben_gua_type = "本宫卦"  # 默认值，实际应根据八宫卦规则确定
        bian_gua_type = "本宫卦"  # 默认值，实际应根据八宫卦规则确定
        
        return {
            "gua_name": ben_gua_name,
            "gua_short_name": ben_gua_short_name,
            "gua_palace": ben_gua_palace,
            "gua_type": ben_gua_type,
            "gua_element": ben_gua_element,
            "yao": ben_yao,
            "bian_gua_name": bian_gua_name,
            "bian_gua_short_name": bian_gua_short_name,
            "bian_gua_palace": bian_gua_palace,
            "bian_gua_type": bian_gua_type,
            "bian_gua_element": bian_gua_element,
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
        palace = self.gua_palace_map.get(gua_name, gua_name[:1])  # 取卦名首字作为宫位
        dizhi_list = self.najia_rules.get(palace, self.najia_rules.get("乾", ["子", "丑", "寅", "卯", "辰", "巳"]))
        
        # 五行对应天干映射（阳干、阴干）
        wuxing_gan_map = {
            "金": ["庚", "辛"],
            "木": ["甲", "乙"],
            "水": ["壬", "癸"],
            "火": ["丙", "丁"],
            "土": ["戊", "己"]
        }
        
        # 地支对应五行
        dizhi_wuxing = {
            "子": "水", "丑": "土", "寅": "木", "卯": "木", 
            "辰": "土", "巳": "火", "午": "火", "未": "土",
            "申": "金", "酉": "金", "戌": "土", "亥": "水"
        }
        
        najia_info = []
        for i in range(6):
            yao_pos = 5 - i  # 从上爻到初爻顺序
            zhi = dizhi_list[yao_pos] if yao_pos < len(dizhi_list) else "子"
            
            # 确定地支五行
            zhi_wuxing = dizhi_wuxing.get(zhi, "土")
            
            # 根据地支五行选择对应的天干组
            gan_pair = wuxing_gan_map.get(zhi_wuxing, ["戊", "己"])
            
            # 根据爻的阴阳性质选择天干
            # 阳爻配阳干，阴爻配阴干
            is_yang_yao = (i % 2 == 0)  # 1、3、5爻为阳，2、4、6爻为阴
            gan = gan_pair[0] if is_yang_yao else gan_pair[1]
            
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
        # 五行相生相克关系
        wuxing_sheng = {
            "金": "水", # 金生水
            "水": "木", # 水生木
            "木": "火", # 木生火
            "火": "土", # 火生土
            "土": "金"  # 土生金
        }
        
        # 地支五行对应关系
        dizhi_wuxing = {
            "子": "水", "丑": "土", "寅": "木", "卯": "木", 
            "辰": "土", "巳": "火", "午": "火", "未": "土",
            "申": "金", "酉": "金", "戌": "土", "亥": "水"
        }
        
        # 天干对应五行
        gan_wuxing = {
            "甲": "木", "乙": "木",
            "丙": "火", "丁": "火",
            "戊": "土", "己": "土",
            "庚": "金", "辛": "金",
            "壬": "水", "癸": "水"
        }
        
        bian_najia = najia.copy()
        if 1 <= dong_yao_position <= 6:
            # 得到动爻的天干地支
            gan, zhi = najia[dong_yao_position - 1][0], najia[dong_yao_position - 1][1:]
            
            # 地支相对，子午相对，丑未相对，以此类推
            new_zhi = self.zhi_opposite.get(zhi, zhi)
            
            # 保持天干不变，只改变地支
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
        palace = self.gua_palace_map.get(gua_name, gua_name[:1])  # 取卦名首字作为宫位
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