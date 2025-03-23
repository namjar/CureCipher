"""
六爻纳甲计算模块
使用najia库计算六爻卦象，结合农历日期、八字和神煞信息分析健康问题

主要功能：
1. 根据阳历/农历起卦，计算六爻卦象（64卦）
2. 计算爻位、纳甲（天干地支）、六亲、六神、世应、动爻、变卦、空亡
3. 结合八字和神煞，分析健康问题，特别关注日建、月建影响
4. 支持真太阳时计算，根据用户IP地址自动判断经纬度
"""

import json
import os
import sys
import datetime
import math
import random
import requests
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent))

# 导入子模块 - 使用绝对导入而非相对导入
from models.liuyao.modules.location import location_service
from models.liuyao.modules.solar_time import solar_time_calculator
from models.liuyao.modules.yao_components import yao_components
from models.liuyao.modules.health_analyzer import health_analyzer
from models.liuyao.modules.gua_calculator import gua_calculator

from models.bazi.calculator import get_element

# 导入 najia 库进行六爻计算
try:
    import najia
except ImportError:
    print("请安装 najia 库: pip install najia")
    sys.exit(1)

# 导入 lunar_python 库进行日期转换
from lunar_python import Solar, Lunar


class LiuYaoNaJia:
    """六爻纳甲计算类"""
    
    def __init__(self):
        """初始化方法"""
        # 初始化纳甲处理器 - 修正属性名称
        try:
            self.najia_processor = najia.Najia()  # 由NaJia改为Najia
        except Exception as e:
            print(f"初始化 najia 处理器失败: {e}")
            self.najia_processor = None
            
        # 流年信息（2025年为乙巳年）
        self.flow_year = {"year": 2025, "gz": "乙巳", "element": "木火"}
        
    def calculate_gua(self, solar_date: datetime.date, time_hour: float, 
                      longitude: Optional[float]=None, latitude: Optional[float]=None, 
                      day_master: Optional[str]=None, yong_shen: Optional[str]=None,
                      use_true_solar_time: bool=False, ip: Optional[str]=None) -> Dict:
        """
        计算六爻卦象
        
        参数:
            solar_date (datetime.date): 阳历日期
            time_hour (float): 时辰（24小时制，0-23），可以包含小数部分表示分钟
            longitude (float, optional): 经度，东经为正，西经为负，默认通过IP获取
            latitude (float, optional): 纬度，北纬为正，南纬为负，默认通过IP获取
            day_master (str, optional): 八字日主天干，例如'甲'
            yong_shen (str, optional): 八字用神五行，例如'水'
            use_true_solar_time (bool): 是否使用真太阳时，默认False
            ip (str, optional): 用户IP地址，用于自动获取位置，默认None
            
        返回:
            Dict: 包含六爻卦象的相关信息
        """
        # 如果未提供经纬度，通过IP地址获取
        if longitude is None or latitude is None:
            longitude, latitude = location_service.get_location_from_ip(ip)
        
        # 如果使用真太阳时，计算真太阳时
        adjusted_time_hour = time_hour
        if use_true_solar_time:
            adjusted_time_hour = solar_time_calculator.calculate_true_solar_time(
                solar_date, time_hour, longitude
            )
        
        # 将阳历日期转换为datetime对象 - 修复Solar.fromDate的参数问题
        int_hour = int(adjusted_time_hour)
        int_minute = int((adjusted_time_hour % 1) * 60)
        solar_datetime = datetime.datetime(
            solar_date.year, solar_date.month, solar_date.day,
            int_hour, int_minute
        )
        
        # 将阳历转换为农历
        solar = Solar.fromYmd(solar_date.year, solar_date.month, solar_date.day)  # 使用fromYmd而非fromDate
        lunar = solar.getLunar()
        
        # 获取四柱干支
        year_gz = lunar.getYearInGanZhi()
        month_gz = lunar.getMonthInGanZhi()
        day_gz = lunar.getDayInGanZhi()
        hour_gz = self._get_hour_gz(adjusted_time_hour, day_gz[0])
        
        # 从干支提取天干地支
        year_gan, year_zhi = year_gz[0], year_gz[1:]
        month_gan, month_zhi = month_gz[0], month_gz[1:]
        day_gan, day_zhi = day_gz[0], day_gz[1:]
        hour_gan, hour_zhi = hour_gz[0], hour_gz[1:]
        
        # 使用najia库计算卦象
        gua_data = self.najia_processor.parse_gua_by_datetime(
            solar_date.year, solar_date.month, solar_date.day, 
            adjusted_time_hour, longitude, latitude
        )
        
        # 计算动爻（改进算法：日干支数 + 时辰数，取余6）
        day_ganzhi_num = yao_components.ganzhi_order.get(day_gz, 1)
        hour_num = solar_time_calculator.hour_to_shichen_num(adjusted_time_hour)
        
        dong_yao = (day_ganzhi_num + hour_num) % 6
        if dong_yao == 0:
            dong_yao = 6  # 如果整除，则动第六爻
        
        # 获取本卦和变卦信息
        ben_gua = gua_data['ben_gua']
        ben_gua_name = ben_gua['name']
        ben_gua_element = ben_gua['element']
        
        # 获取变卦信息
        bian_gua = gua_data['bian_gua']
        
        # 获取纳甲信息
        najia_info = gua_data['najia']
        
        # 计算六亲、六神、空亡
        liuqin = yao_components.calculate_liuqin(najia_info, day_master, day_zhi)
        liushen = yao_components.calculate_liushen(day_gan)
        kongwang = yao_components.calculate_kongwang(day_gz, self.najia_processor)
        
        # 获取世应信息
        shi_yao = gua_data['shi_yao']
        ying_yao = gua_data['ying_yao']
        
        # 整合结果
        result = {
            "ben_gua": {
                "name": ben_gua_name,
                "element": ben_gua_element,
                "number": ben_gua.get('number', 0)
            },
            "najia": najia_info,
            "liuqin": liuqin,
            "liushen": liushen,
            "kongwang": kongwang,
            "shi_yao": shi_yao,
            "ying_yao": ying_yao,
            "dong_yao": dong_yao,
            "bian_gua": {
                "name": bian_gua['name'],
                "element": bian_gua['element'],
                "number": bian_gua.get('number', 0)
            },
            "date_info": {
                "solar_date": solar_date.strftime("%Y-%m-%d"),
                "lunar_date": f"{lunar.getYearInChinese()}年{lunar.getMonthInChinese()}月{lunar.getDayInChinese()}",
                "time_hour": time_hour,
                "adjusted_time_hour": adjusted_time_hour if use_true_solar_time else time_hour,
                "use_true_solar_time": use_true_solar_time,
                "year_gz": year_gz,
                "month_gz": month_gz,
                "day_gz": day_gz,
                "hour_gz": hour_gz
            },
            "bazi_info": {
                "day_master": day_master,
                "day_master_element": self._get_element(day_master) if day_master else None,
                "yong_shen": yong_shen
            },
            "location": {
                "longitude": longitude,
                "latitude": latitude
            }
        }
        
        # 分析健康问题
        health_analysis = self._analyze_health(result, day_master, yong_shen)
        result["health_analysis"] = health_analysis
        
        return result
    
    def _get_hour_gz(self, hour: float, day_gan: str) -> str:
        """
        根据小时和日干获取时辰干支
        
        参数:
            hour (float): 小时（24小时制）
            day_gan (str): 日干
            
        返回:
            str: 时辰干支
        """
        # 使用 najia 库计算
        int_hour = int(hour)
        return self.najia_processor.get_hour_ganzhi(int_hour, day_gan)
    
    def _get_element(self, gan: Optional[str]) -> Optional[str]:
        """
        获取天干的五行属性
        
        参数:
            gan (str, optional): 天干
            
        返回:
            str, optional: 五行属性
        """
        if not gan:
            return None
            
        element_map = {
            "甲": "木", "乙": "木",
            "丙": "火", "丁": "火",
            "戊": "土", "己": "土",
            "庚": "金", "辛": "金",
            "壬": "水", "癸": "水"
        }
        
        return element_map.get(gan)
    
    def get_location_from_ip(self, ip: Optional[str]=None) -> Tuple[float, float]:
        """
        根据IP地址获取经纬度，优先在线API，失败则用离线DB-IP数据库
        
        参数:
            ip (str, optional): 用户IP地址，默认None（自动获取）
            
        返回:
            Tuple[float, float]: 经度（longitude），纬度（latitude）
        """
        return location_service.get_location_from_ip(ip)
    
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
        return solar_time_calculator.calculate_true_solar_time(solar_date, time_hour, longitude)
    
    def _analyze_health(self, gua_result: Dict, day_master: Optional[str], 
                      yong_shen: Optional[str]) -> Dict:
        """
        分析健康问题
        
        参数:
            gua_result (Dict): 卦象结果
            day_master (str, optional): 日主天干
            yong_shen (str, optional): 用神五行
            
        返回:
            Dict: 健康分析结果
        """
        return health_analyzer.analyze_health(gua_result, day_master, yong_shen)
    
    def format_result(self, result: Dict) -> str:
        """
        格式化卦象结果为可读字符串
        
        参数:
            result (Dict): 卦象计算结果
            
        返回:
            str: 格式化后的结果字符串
        """
        output = []
        
        # 日期和时间信息
        output.append(f"测算日期: {result['date_info']['solar_date']} {result['date_info']['time_hour']}时")
        if result['date_info']['use_true_solar_time']:
            output.append(f"真太阳时: {result['date_info']['adjusted_time_hour']:.2f}时")
        output.append(f"农历: {result['date_info']['lunar_date']}")
        output.append(f"四柱: {result['date_info']['year_gz']} {result['date_info']['month_gz']} {result['date_info']['day_gz']} {result['date_info']['hour_gz']}")
        
        # 位置信息
        output.append(f"经度: {result['location']['longitude']:.2f}，纬度: {result['location']['latitude']:.2f}")
        
        # 八字信息
        if result['bazi_info']['day_master']:
            output.append(f"日主: {result['bazi_info']['day_master']}（五行{result['bazi_info']['day_master_element']}）")
        if result['bazi_info']['yong_shen']:
            output.append(f"用神: {result['bazi_info']['yong_shen']}")
        
        # 卦象信息
        output.append("")
        output.append(f"本卦: {result['ben_gua']['name']} ({result['ben_gua']['element']})")
        
        # 纳甲信息
        najia_str = ", ".join([
            f"初爻{result['najia'][0]}" if i == 0 else 
            f"六爻{result['najia'][-1]}" if i == 5 else 
            f"第{i+1}爻{result['najia'][i]}" 
            for i in range(6)
        ])
        output.append(f"纳甲: {najia_str}")
        
        # 六亲信息
        liuqin_str = ", ".join([
            f"初爻{result['liuqin'][0]}" if i == 0 else 
            f"六爻{result['liuqin'][-1]}" if i == 5 else 
            f"第{i+1}爻{result['liuqin'][i]}" 
            for i in range(6)
        ])
        output.append(f"六亲: {liuqin_str}")
        
        # 六神信息
        liushen_str = ", ".join([
            f"初爻{result['liushen'][0]}" if i == 0 else 
            f"六爻{result['liushen'][-1]}" if i == 5 else 
            f"第{i+1}爻{result['liushen'][i]}" 
            for i in range(6)
        ])
        output.append(f"六神: {liushen_str}")
        
        # 空亡信息
        kongwang_str = ", ".join(result['kongwang']) if result['kongwang'] else "无"
        output.append(f"空亡: {kongwang_str}")
        
        # 世应爻
        output.append(f"世爻: 第{result['shi_yao']}爻 ({result['liuqin'][result['shi_yao']-1]})")
        output.append(f"应爻: 第{result['ying_yao']}爻 ({result['liuqin'][result['ying_yao']-1]})")
        
        # 动爻
        output.append(f"动爻: 第{result['dong_yao']}爻")
        
        # 变卦
        output.append(f"变卦: {result['bian_gua']['name']} ({result['bian_gua']['element']})")
        
        # 健康分析
        output.append("")
        output.append(f"健康影响: {result['health_analysis']['overall']}")
        
        if result['health_analysis']['specific_issues']:
            output.append(f"具体问题: {' '.join(result['health_analysis']['specific_issues'])}")
        
        if result['health_analysis']['recommendations']:
            output.append(f"健康建议: {' '.join(result['health_analysis']['recommendations'])}")
        
        return "\n".join(output)


def get_bazi(birth_datetime, day_master=None, yong_shen=None):
    """
    从八字模块导入的函数，用于获取八字信息
    这里简化处理，实际应该从models.bazi.calculator模块导入
    
    参数:
        birth_datetime (datetime.datetime): 出生日期时间
        day_master (str, optional): 日主天干
        yong_shen (str, optional): 用神五行
        
    返回:
        Dict: 八字信息
    """
    from models.bazi.calculator import calculate_bazi
    result = calculate_bazi(
        birth_datetime.year, birth_datetime.month, birth_datetime.day, 
        birth_datetime.hour, "male"  # 性别参数在这里不重要
    )
    return result["result"]


if __name__ == "__main__":
    """测试代码"""
    # 初始化六爻纳甲计算类
    liu_yao = LiuYaoNaJia()
    
    # 测试用例1
    test_date_1 = datetime.date(1990, 5, 15)
    test_hour_1 = 8
    day_master_1 = "丙"  # 火
    yong_shen_1 = "水"
    
    # 测试用例2
    test_date_2 = datetime.date(2025, 3, 22)
    test_hour_2 = 14
    day_master_2 = "甲"  # 木
    yong_shen_2 = "水"
    
    # 计算六爻卦象 - 暂时关闭真太阳时避免IP定位错误
    for test_date, test_hour, day_master, yong_shen in [
        (test_date_1, test_hour_1, day_master_1, yong_shen_1),
        (test_date_2, test_hour_2, day_master_2, yong_shen_2)
    ]:
        result = liu_yao.calculate_gua(
            test_date, test_hour, day_master=day_master, yong_shen=yong_shen,
            use_true_solar_time=False,  # 设为False以避免IP定位问题
            longitude=-100, latitude=40  # 直接提供固定的经纬度
        )
        
        # 打印格式化结果
        print(liu_yao.format_result(result))
        print("\n" + "-" * 80 + "\n")
