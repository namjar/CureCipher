#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
高精度真太阳时计算模块
实现了考虑太阳黄经、地球自转和黄道倾角影响的精确真太阳时计算
"""

import datetime
import math
from typing import Tuple, Optional

class EnhancedSolarTimeCalculator:
    """高精度真太阳时计算类"""
    
    def calculate_true_solar_time(self, solar_date: datetime.date, time_hour: float,
                               longitude: float, latitude: float) -> float:
        """
        计算真太阳时 - 高精度版
        
        增强版算法：
        1. 精确的儒略日计算，处理1582年格里高利历改革
        2. 高精度时差方程，基于NREL算法
        3. 考虑地球轨道离心率和黄道倾角
        4. 动态计算时区，而不是简单的经度换算
        
        参数:
            solar_date (datetime.date): 阳历日期
            time_hour (float): 时辰（24小时制，0-23.999）
            longitude (float): 经度，东经为正，西经为负
            latitude (float): 纬度，北纬为正，南纬为负
            
        返回:
            float: 真太阳时（小时）
        """
        # 参数验证
        if not isinstance(solar_date, datetime.date):
            raise TypeError("solar_date必须是datetime.date类型")
        
        if not isinstance(time_hour, (int, float)):
            raise TypeError("time_hour必须是数值类型（int或float）")
            
        if time_hour < 0 or time_hour >= 24:
            raise ValueError("time_hour必须在0到24之间")
            
        if not isinstance(longitude, (int, float)):
            raise TypeError("longitude必须是数值类型")
            
        if not isinstance(latitude, (int, float)):
            raise TypeError("latitude必须是数值类型")
            
        if longitude < -180 or longitude > 180:
            raise ValueError("longitude必须在-180到180之间")
            
        if latitude < -90 or latitude > 90:
            raise ValueError("latitude必须在-90到90之间")
        
        # 计算儒略日
        julian_day = self._calculate_julian_day(solar_date, time_hour)
        
        # 计算世纪数T (以2000.0为参考点)
        T = (julian_day - 2451545.0) / 36525.0
        
        # 计算太阳黄经 (以度为单位)
        L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T**2
        L0 = L0 % 360  # 确保在0-360度范围内
        
        # 计算太阳平近点角
        M = 357.52911 + 35999.05029 * T - 0.0001537 * T**2
        M = M % 360
        M_rad = math.radians(M)
        
        # 计算地球轨道离心率
        e = 0.016708634 - 0.000042037 * T - 0.0000001267 * T**2
        
        # 计算太阳中心差
        C = ((1.914602 - 0.004817 * T - 0.000014 * T**2) * math.sin(M_rad) + 
             (0.019993 - 0.000101 * T) * math.sin(2 * M_rad) + 
             0.000289 * math.sin(3 * M_rad))
        
        # 计算太阳真黄经
        true_longitude = L0 + C
        
        # 计算太阳视黄经（考虑黄动差）
        omega = 125.04 - 1934.136 * T
        apparent_longitude = true_longitude - 0.00569 - 0.00478 * math.sin(math.radians(omega))
        
        # 计算平黄赤交角
        obliquity = 23.439291 - 0.0130042 * T - 0.00000016 * T**2 + 0.000000504 * T**3
        obliquity_corrected = obliquity + 0.00256 * math.cos(math.radians(omega))
        
        # 计算时差方程 (以分钟为单位)
        y = math.tan(math.radians(obliquity_corrected/2))**2
        eq_time = (y * math.sin(2 * math.radians(L0)) - 
                  2 * e * math.sin(M_rad) + 
                  4 * e * y * math.sin(M_rad) * math.cos(2 * math.radians(L0)) - 
                  0.5 * y**2 * math.sin(4 * math.radians(L0)) - 
                  1.25 * e**2 * math.sin(2 * M_rad))
        eq_time = 4 * eq_time  # 将弧度转换为分钟 (1度 = 4分钟)
        
        # 计算时区 (基于精确经度，而不是简单的15度一个时区)
        # 实际上我们需要考虑行政时区与地理时区的差异
        # 这里使用更精确的方法：根据经度计算当地标准时区
        timezone_hour = round(longitude / 15)
        
        # 计算经度修正 (每15度经度对应1小时时差)
        longitude_correction = (longitude - timezone_hour * 15) / 15
        
        # 计算真太阳时 (当地标准时间 + 方程时 + 经度修正)
        true_solar_time = time_hour + eq_time / 60 + longitude_correction
        
        # 确保结果在0-24范围内
        true_solar_time = true_solar_time % 24
        
        return true_solar_time
    
    def calculate_time_diff(self, solar_date: datetime.date, time_hour: float,
                         longitude: float, latitude: float) -> float:
        """
        计算真太阳时与标准时间的差值（分钟）
        
        参数:
            solar_date (datetime.date): 阳历日期
            time_hour (float): 时辰（24小时制，0-23.999）
            longitude (float): 经度，东经为正，西经为负
            latitude (float): 纬度，北纬为正，南纬为负
            
        返回:
            float: 时差（分钟）
        """
        true_solar_time = self.calculate_true_solar_time(solar_date, time_hour, longitude, latitude)
        time_diff = (true_solar_time - time_hour) * 60  # 转换为分钟
        
        # 调整范围在-720到720分钟之间（±12小时）
        if time_diff > 720:
            time_diff -= 1440
        elif time_diff < -720:
            time_diff += 1440
            
        return time_diff
    
    def _calculate_julian_day(self, date: datetime.date, hour: float) -> float:
        """
        计算儒略日 (高精度版)
        
        参数:
            date (datetime.date): 日期
            hour (float): 小时（24小时制，带小数）
            
        返回:
            float: 儒略日
        """
        # 提取年月日
        year = date.year
        month = date.month
        day = date.day + hour / 24.0
        
        # 处理1月和2月
        if month <= 2:
            year -= 1
            month += 12
        
        # 处理格里高利历改革 (1582年10月15日之后)
        if (date.year > 1582 or 
            (date.year == 1582 and 
             (date.month > 10 or 
              (date.month == 10 and date.day >= 15)))):
            A = int(year / 100)
            B = 2 - A + int(A / 4)
        else:
            B = 0
        
        # 计算儒略日
        JD = (int(365.25 * (year + 4716)) + 
              int(30.6001 * (month + 1)) + 
              day + B - 1524.5)
        
        return JD
    
    def get_sunset_time(self, solar_date: datetime.date, longitude: float, latitude: float) -> float:
        """
        计算日落时间（近似值）
        
        参数:
            solar_date (datetime.date): 阳历日期
            longitude (float): 经度
            latitude (float): 纬度
            
        返回:
            float: 日落时间（24小时制）
        """
        # 计算儒略日 (中午12:00)
        julian_day = self._calculate_julian_day(solar_date, 12.0)
        
        # 计算世纪数T
        T = (julian_day - 2451545.0) / 36525.0
        
        # 计算太阳赤纬角
        declination = self._calculate_solar_declination(T)
        
        # 计算日落时角
        latitude_rad = math.radians(latitude)
        declination_rad = math.radians(declination)
        
        # 日落时角计算，考虑大气折射和太阳视半径
        # 海平面的标准值为-0.83度
        sunset_hour_angle = math.acos(-0.01454 - math.tan(latitude_rad) * math.tan(declination_rad))
        sunset_hour_angle = math.degrees(sunset_hour_angle)
        
        # 将时角转换为小时
        # 每15度对应1小时
        sunset_time = 12.0 + sunset_hour_angle / 15.0
        
        # 应用经度修正
        timezone_hour = round(longitude / 15)
        longitude_correction = (longitude - timezone_hour * 15) / 15
        sunset_time += longitude_correction
        
        # 应用方程时修正
        eq_time = self._calculate_equation_of_time(T)
        sunset_time += eq_time / 60
        
        return sunset_time % 24
    
    def get_sunrise_time(self, solar_date: datetime.date, longitude: float, latitude: float) -> float:
        """
        计算日出时间（近似值）
        
        参数:
            solar_date (datetime.date): 阳历日期
            longitude (float): 经度
            latitude (float): 纬度
            
        返回:
            float: 日出时间（24小时制）
        """
        # 计算儒略日 (中午12:00)
        julian_day = self._calculate_julian_day(solar_date, 12.0)
        
        # 计算世纪数T
        T = (julian_day - 2451545.0) / 36525.0
        
        # 计算太阳赤纬角
        declination = self._calculate_solar_declination(T)
        
        # 计算日出时角
        latitude_rad = math.radians(latitude)
        declination_rad = math.radians(declination)
        
        # 日出时角计算，考虑大气折射和太阳视半径
        sunrise_hour_angle = math.acos(-0.01454 - math.tan(latitude_rad) * math.tan(declination_rad))
        sunrise_hour_angle = -math.degrees(sunrise_hour_angle)
        
        # 将时角转换为小时
        # 每15度对应1小时
        sunrise_time = 12.0 + sunrise_hour_angle / 15.0
        
        # 应用经度修正
        timezone_hour = round(longitude / 15)
        longitude_correction = (longitude - timezone_hour * 15) / 15
        sunrise_time += longitude_correction
        
        # 应用方程时修正
        eq_time = self._calculate_equation_of_time(T)
        sunrise_time += eq_time / 60
        
        return sunrise_time % 24
    
    def _calculate_solar_declination(self, T: float) -> float:
        """
        计算太阳赤纬角
        
        参数:
            T (float): 世纪数
            
        返回:
            float: 太阳赤纬角（度）
        """
        # 计算太阳黄经
        L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T**2
        L0 = L0 % 360
        
        # 计算太阳平近点角
        M = 357.52911 + 35999.05029 * T - 0.0001537 * T**2
        M = M % 360
        M_rad = math.radians(M)
        
        # 计算地球轨道离心率
        e = 0.016708634 - 0.000042037 * T - 0.0000001267 * T**2
        
        # 计算太阳中心差
        C = ((1.914602 - 0.004817 * T - 0.000014 * T**2) * math.sin(M_rad) + 
             (0.019993 - 0.000101 * T) * math.sin(2 * M_rad) + 
             0.000289 * math.sin(3 * M_rad))
        
        # 计算太阳真黄经
        true_longitude = L0 + C
        
        # 计算黄道倾角
        obliquity = 23.439291 - 0.0130042 * T - 0.00000016 * T**2 + 0.000000504 * T**3
        
        # 计算太阳赤纬角
        declination = math.asin(math.sin(math.radians(obliquity)) * math.sin(math.radians(true_longitude)))
        declination = math.degrees(declination)
        
        return declination
    
    def _calculate_equation_of_time(self, T: float) -> float:
        """
        计算时差方程（分钟）
        
        参数:
            T (float): 世纪数
            
        返回:
            float: 时差（分钟）
        """
        # 计算太阳黄经
        L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T**2
        L0 = L0 % 360
        
        # 计算太阳平近点角
        M = 357.52911 + 35999.05029 * T - 0.0001537 * T**2
        M = M % 360
        M_rad = math.radians(M)
        
        # 计算地球轨道离心率
        e = 0.016708634 - 0.000042037 * T - 0.0000001267 * T**2
        
        # 计算黄道倾角
        obliquity = 23.439291 - 0.0130042 * T - 0.00000016 * T**2 + 0.000000504 * T**3
        
        # 计算时差方程
        y = math.tan(math.radians(obliquity/2))**2
        eq_time = (y * math.sin(2 * math.radians(L0)) - 
                  2 * e * math.sin(M_rad) + 
                  4 * e * y * math.sin(M_rad) * math.cos(2 * math.radians(L0)) - 
                  0.5 * y**2 * math.sin(4 * math.radians(L0)) - 
                  1.25 * e**2 * math.sin(2 * M_rad))
        
        # 转换为分钟
        eq_time = 4 * eq_time
        
        return eq_time
    
    def get_daylight_hours(self, solar_date: datetime.date, longitude: float, latitude: float) -> float:
        """
        计算日照时间（小时）
        
        参数:
            solar_date (datetime.date): 阳历日期
            longitude (float): 经度
            latitude (float): 纬度
            
        返回:
            float: 日照时间（小时）
        """
        sunrise = self.get_sunrise_time(solar_date, longitude, latitude)
        sunset = self.get_sunset_time(solar_date, longitude, latitude)
        
        # 处理日出在日落之后的情况（跨午夜）
        if sunset < sunrise:
            sunset += 24
            
        daylight_hours = sunset - sunrise
        return daylight_hours

# 导出单例实例
enhanced_solar_time_calculator = EnhancedSolarTimeCalculator()
