""" 真太阳时计算模块 """
import datetime
import math
import warnings
from typing import Optional, Tuple, Union

from .location import location_service


class SolarTimeCalculator:
    """真太阳时计算类"""
    
    def calculate_true_solar_time(self, solar_date: datetime.date, time_hour: float,
                               longitude: Optional[float]=None, latitude: Optional[float]=None) -> float:
        """
        计算真太阳时
        
        此方法使用改进的算法计算真太阳时，包括：
        1. 更精确的儒略日计算，正确处理闰年
        2. 更精确的时差方程计算，考虑太阳黄经和地球自转倾斜角
        3. 增强的参数验证和异常处理
        
        参数:
            solar_date (datetime.date): 阳历日期
            time_hour (float): 时辰（24小时制，0-23.999），可以包含小数部分表示分钟和秒
            longitude (float, optional): 经度，东经为正，西经为负，默认通过IP获取
            latitude (float, optional): 纬度，北纬为正，南纬为负，默认通过IP获取
            
        返回:
            float: 真太阳时（小时），包含小数部分（0-24范围内）
            
        异常:
            TypeError: 当参数类型不正确时
            ValueError: 当参数值不在有效范围内时
        """
        # 参数验证
        if not isinstance(solar_date, datetime.date):
            raise TypeError("solar_date必须是datetime.date类型")
        
        if not isinstance(time_hour, (int, float)):
            raise TypeError("time_hour必须是数值类型（int或float）")
            
        if time_hour < 0 or time_hour >= 24:
            raise ValueError("time_hour必须在0到24之间")

        # 如果未提供经纬度，通过IP地址获取
        if longitude is None or latitude is None:
            longitude, latitude = self._get_validated_location()
            
        # 标准时区的时区差（以小时为单位）
        timezone = round(longitude / 15)
        
        # 计算儒略日 (使用更精确的算法)
        julian_day = self._calculate_julian_day(solar_date, time_hour - timezone)
        
        # 计算相对于J2000.0的天数
        t = (julian_day - 2451545.0) / 36525.0  # 世纪数
        
        # 计算平太阳时与真太阳时之差（使用更精确的时差方程）
        eq_time = self._calculate_equation_of_time(t)
        
        # 计算真太阳时（小时）
        true_solar_time = time_hour + (eq_time / 60) + ((longitude - (timezone * 15)) / 15)
        
        # 确保真太阳时在0-24之间
        true_solar_time = true_solar_time % 24
        
        return true_solar_time
    
    def _get_validated_location(self) -> Tuple[float, float]:
        """
        获取并验证位置信息
        
        返回:
            Tuple[float, float]: 验证后的经度和纬度
        """
        longitude, latitude = location_service.get_location_from_ip()
        
        # 验证经纬度的有效性
        if (not isinstance(longitude, (int, float)) or 
            not isinstance(latitude, (int, float)) or
            longitude < -180 or longitude > 180 or
            latitude < -90 or latitude > 90):
            
            # 使用默认值
            default_longitude, default_latitude = 116.4, 39.9  # 北京的经纬度作为默认值
            warnings.warn(
                f"无效的经纬度: ({longitude}, {latitude})，使用默认值: ({default_longitude}, {default_latitude})",
                UserWarning
            )
            return default_longitude, default_latitude
            
        return longitude, latitude
    
    def _calculate_julian_day(self, date: datetime.date, hour: float) -> float:
        """
        计算儒略日
        
        使用更精确的算法计算儒略日，正确处理闰年和日期边界
        
        参数:
            date (datetime.date): 日期
            hour (float): 小时（包含小数部分）
            
        返回:
            float: 儒略日
        """
        y = date.year
        m = date.month
        d = date.day
        
        # 调整1月和2月为前一年的13月和14月
        if m <= 2:
            y -= 1
            m += 12
            
        # 处理格里高利历法修正
        a = y // 100
        b = 2 - a + a // 4
        
        # 计算儒略日
        jd = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + b - 1524.5 + hour / 24.0
        
        return jd
    
    def _calculate_equation_of_time(self, t: float) -> float:
        """
        计算时差方程（太阳时差）
        
        使用更精确的算法计算时差方程，考虑太阳黄经和地球自转倾斜角
        
        参数:
            t (float): 世纪数，相对于J2000.0
            
        返回:
            float: 时差（分钟）
        """
        # 计算太阳的平黄经
        l0 = 280.46646 + 36000.76983 * t + 0.0003032 * t**2
        l0 = l0 % 360
        
        # 计算太阳的平近点角
        m = 357.52911 + 35999.05029 * t - 0.0001537 * t**2
        m = m % 360
        m_rad = math.radians(m)
        
        # 计算地球轨道离心率
        e = 0.016708634 - 0.000042037 * t - 0.0000001267 * t**2
        
        # 计算太阳的中心差
        c = (1.914602 - 0.004817 * t - 0.000014 * t**2) * math.sin(m_rad)
        c += (0.019993 - 0.000101 * t) * math.sin(2 * m_rad)
        c += 0.000289 * math.sin(3 * m_rad)
        
        # 计算太阳的真黄经
        true_long = l0 + c
        true_long_rad = math.radians(true_long)
        
        # 计算太阳的视黄经
        omega = 125.04 - 1934.136 * t
        apparent_long = true_long - 0.00569 - 0.00478 * math.sin(math.radians(omega))
        apparent_long_rad = math.radians(apparent_long)
        
        # 计算平赤经和赤纬
        oblique = 23.439291 - 0.0130042 * t - 0.00000016 * t**2 + 0.000000504 * t**3
        oblique_rad = math.radians(oblique)
        
        # 计算时差（分钟）
        y = math.tan(oblique_rad / 2) ** 2
        eq_time = y * math.sin(2 * math.radians(l0))
        eq_time -= 2 * e * math.sin(m_rad)
        eq_time += 4 * e * y * math.sin(m_rad) * math.cos(2 * math.radians(l0))
        eq_time -= 0.5 * y**2 * math.sin(4 * math.radians(l0))
        eq_time -= 1.25 * e**2 * math.sin(2 * m_rad)
        
        # 转换为分钟
        eq_time = eq_time * 4  # 度转分钟
        
        return eq_time
        
    def hour_to_shichen_num(self, hour: float) -> int:
        """
        将小时（24小时制）转换为时辰数字
        
        参数:
            hour (float): 小时（24小时制，0-23.999）
            
        返回:
            int: 时辰对应的数字（1-12）
        """
        # 将小时转换为整数时辰
        hour_int = int(hour)
        
        # 时辰对照表（24小时制转中国传统时辰）
        shichen_map = {
            0: 1, 1: 1,    # 子时 23:00-01:00
            2: 2, 3: 2,    # 丑时 01:00-03:00
            4: 3, 5: 3,    # 寅时 03:00-05:00
            6: 4, 7: 4,    # 卯时 05:00-07:00
            8: 5, 9: 5,    # 辰时 07:00-09:00
            10: 6, 11: 6,  # 巳时 09:00-11:00
            12: 7, 13: 7,  # 午时 11:00-13:00
            14: 8, 15: 8,  # 未时 13:00-15:00
            16: 9, 17: 9,  # 申时 15:00-17:00
            18: 10, 19: 10,  # 酉时 17:00-19:00
            20: 11, 21: 11,  # 戌时 19:00-21:00
            22: 12, 23: 12   # 亥时 21:00-23:00
        }
        
        # 返回时辰数字，默认为1（子时）
        return shichen_map.get(hour_int, 1)


# 导出单例实例
solar_time_calculator = SolarTimeCalculator()
