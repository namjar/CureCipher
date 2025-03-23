"""
六爻纳甲计算模块
使用纳甲计算六爻卦象，结合农历日期、八字和神煞信息分析健康问题

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
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    # 尝试导入子模块
    from models.liuyao.modules.location import location_service
    from models.liuyao.modules.solar_time import solar_time_calculator
    from models.liuyao.modules.yao_components import yao_components
    from models.liuyao.modules.health_analyzer import health_analyzer
    from models.liuyao.modules.gua_calculator import gua_calculator
    from models.liuyao.modules.najia_analyzer import najia_analyzer
except ImportError as e:
    print(f"导入子模块失败: {e}")
    print("请确认子模块文件存在并且路径正确")
    # 如果子模块导入失败，这里可以提供一个简化的实现或者直接退出程序
    sys.exit(1)

# 导入八字计算器模块
from models.bazi.calculator import get_element


class LiuYaoNaJia:
    """六爻纳甲计算类 - 主类"""
    
    def __init__(self):
        """初始化方法"""
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
        # 如果未提供经纬度，且IP可用，则通过IP获取位置
        if (longitude is None or latitude is None) and ip is not None:
            try:
                longitude, latitude = location_service.get_location_from_ip(ip)
            except Exception as e:
                print(f"通过IP获取位置失败: {e}")
                # 使用默认值
                longitude = longitude or 116.4  # 默认北京经度
                latitude = latitude or 39.9    # 默认北京纬度
        elif longitude is None or latitude is None:
            # 使用默认值
            longitude = longitude or 116.4  # 默认北京经度
            latitude = latitude or 39.9     # 默认北京纬度
        
        # 调用卦象计算器计算卦象
        result = gua_calculator.calculate_gua(
            solar_date, time_hour, longitude, latitude,
            day_master, yong_shen, use_true_solar_time
        )
        
        return result
    
    def get_location_from_ip(self, ip: Optional[str]=None) -> Tuple[float, float]:
        """
        根据IP地址获取经纬度，委托给location_service
        
        参数:
            ip (str, optional): 用户IP地址，默认None（自动获取）
            
        返回:
            Tuple[float, float]: 经度（longitude），纬度（latitude）
        """
        return location_service.get_location_from_ip(ip)
    
    def calculate_true_solar_time(self, solar_date: datetime.date, time_hour: float, 
                                  longitude: float) -> float:
        """
        计算真太阳时，委托给solar_time_calculator
        
        参数:
            solar_date (datetime.date): 阳历日期
            time_hour (float): 时辰（24小时制，0-23），可以包含小数部分表示分钟
            longitude (float): 经度，东经为正，西经为负
            
        返回:
            float: 真太阳时（小时），包含小数部分
        """
        return solar_time_calculator.calculate_true_solar_time(solar_date, time_hour, longitude)
    
    def format_result(self, result: Dict) -> str:
        """
        格式化卦象结果为可读字符串，委托给gua_calculator
        
        参数:
            result (Dict): 卦象计算结果
            
        返回:
            str: 格式化后的结果字符串
        """
        return gua_calculator.format_gua_result(result)


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
    
    # 计算六爻卦象 - 为避免IP定位错误，使用固定经纬度
    for test_date, test_hour, day_master, yong_shen in [
        (test_date_1, test_hour_1, day_master_1, yong_shen_1),
        (test_date_2, test_hour_2, day_master_2, yong_shen_2)
    ]:
        # 提供固定经纬度，使用真太阳时
        result = liu_yao.calculate_gua(
            test_date, test_hour, 
            longitude=None, latitude=None,  # 让系统通过IP自动获取经纬度
            day_master=day_master, 
            yong_shen=yong_shen,
            use_true_solar_time=True  # 默认开启真太阳时
        )
        
        # 打印格式化结果
        print(liu_yao.format_result(result))
        print("\n" + "-" * 80 + "\n")
