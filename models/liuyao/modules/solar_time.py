"""
真太阳时模块 - 计算真太阳时与时辰
"""

import math
import datetime
from typing import Tuple, Optional, Dict

class SolarTimeCalculator:
    """真太阳时计算类"""
    
    def __init__(self):
        """初始化真太阳时计算器"""
        # 时辰映射
        self.shichen_map = {
            "子时": 1, "丑时": 2, "寅时": 3, "卯时": 4, "辰时": 5, "巳时": 6,
            "午时": 7, "未时": 8, "申时": 9, "酉时": 10, "戌时": 11, "亥时": 12
        }
        
        # 时辰对照表（24小时制）
        self.shichen_ranges = [
            (23, 1, "子时"),  # 23:00-01:00
            (1, 3, "丑时"),   # 01:00-03:00
            (3, 5, "寅时"),   # 03:00-05:00
            (5, 7, "卯时"),   # 05:00-07:00
            (7, 9, "辰时"),   # 07:00-09:00
            (9, 11, "巳时"),  # 09:00-11:00
            (11, 13, "午时"), # 11:00-13:00
            (13, 15, "未时"), # 13:00-15:00
            (15, 17, "申时"), # 15:00-17:00
            (17, 19, "酉时"), # 17:00-19:00
            (19, 21, "戌时"), # 19:00-21:00
            (21, 23, "亥时")  # 21:00-23:00
        ]
    
    def calculate_true_solar_time(self, solar_date: datetime.date, time_hour: float,
                                  longitude: float) -> float:
        """
        计算真太阳时
        
        参数:
            solar_date (datetime.date): 阳历日期
            time_hour (float): 时辰（24小时制，0-23），可以包含小数部分表示分钟
            longitude (float): 经度，东经为正，西经为负
            
        返回:
            float: 真太阳时（小时），包含小数部分
        """
        # 标准时区的时区差（以小时为单位）
        timezone = round(longitude / 15)
        
        # 计算儒略日
        year, month, day = solar_date.year, solar_date.month, solar_date.day
        if month <= 2:
            year -= 1
            month += 12
        
        a = year // 100
        b = 2 - a + a // 4
        
        julian_day = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5
        
        # 计算时角（单位：弧度）
        D = julian_day - 2451545.0 + (time_hour - timezone) / 24.0
        
        # 计算平太阳时与真太阳时之差（以分钟为单位）
        g = 357.529 + 0.98560028 * D  # 太阳的平近点角（单位：度）
        g_rad = math.radians(g % 360)  # 转换为弧度
        
        # 太阳赤经方程（简化版）
        eq_time = 9.87 * math.sin(2 * g_rad) - 7.53 * math.cos(g_rad) - 1.5 * math.sin(g_rad)
        
        # 计算真太阳时（小时）
        true_solar_time = time_hour + (eq_time / 60) + ((longitude - (timezone * 15)) / 15)
        
        # 确保真太阳时在0-24之间
        true_solar_time = true_solar_time % 24
        
        return true_solar_time
    
    def hour_to_shichen_num(self, hour: float) -> int:
        """
        将24小时制的小时转换为时辰序号
        
        参数:
            hour (float): 小时（24小时制，0-23.99）
            
        返回:
            int: 时辰序号（1-12）
        """
        # 处理子时跨天的特殊情况
        hour_24 = hour % 24
        
        # 遍历时辰范围，找到对应的时辰
        for start, end, shichen in self.shichen_ranges:
            # 处理子时跨天的特殊情况
            if start == 23:  # 子时
                if hour_24 >= 23 or hour_24 < 1:
                    return self.shichen_map[shichen]
            else:  # 其他时辰
                if start <= hour_24 < end:
                    return self.shichen_map[shichen]
        
        # 默认返回子时
        return 1
    
    def hour_to_shichen_name(self, hour: float) -> str:
        """
        将24小时制的小时转换为时辰名称
        
        参数:
            hour (float): 小时（24小时制，0-23.99）
            
        返回:
            str: 时辰名称（子时、丑时等）
        """
        for start, end, shichen in self.shichen_ranges:
            hour_24 = hour % 24
            if start == 23:  # 子时特殊处理
                if hour_24 >= 23 or hour_24 < 1:
                    return shichen
            else:
                if start <= hour_24 < end:
                    return shichen
        
        return "子时"  # 默认返回子时

# 单例模式，导出一个实例
solar_time_calculator = SolarTimeCalculator()
