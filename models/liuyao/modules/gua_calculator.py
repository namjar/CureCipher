"""
卦象计算模块 - 计算六爻卦象并整合各种信息
"""

import datetime
import random
from typing import Dict, List, Optional, Tuple

from lunar_python import Solar, Lunar

from .location import location_service
from .solar_time import solar_time_calculator
from .yao_components import yao_components
from .health_analyzer import health_analyzer

class SimpleNajia:
    """简单的纳甲处理器，用于替代najia库"""
    
    def __init__(self):
        """初始化方法"""
        self.gua_elements = {
            "乾": "金", "坤": "土", "震": "木", "艮": "土",
            "离": "火", "坎": "水", "兑": "金", "巽": "木",
            "中": "土"  # 中爻为土
        }
        
    def parse_gua_by_datetime(self, year, month, day, hour, longitude, latitude):
        """简单实现六爻卦象计算"""
        # 简化实现，根据日期生成伪随机的卦象
        seed = year * 10000 + month * 100 + day + int(hour)
        random.seed(seed)
        
        # 本卦 - 简化处理，随机选择一个卦
        ben_gua_names = ["乾", "坤", "震", "艮", "离", "坎", "兑", "巽"]
        ben_gua_name = random.choice(ben_gua_names)
        ben_gua_element = self.gua_elements[ben_gua_name]
        
        # 变卦 - 简化处理，随机选择一个卦（不同于本卦）
        other_guas = [g for g in ben_gua_names if g != ben_gua_name]
        bian_gua_name = random.choice(other_guas)
        bian_gua_element = self.gua_elements[bian_gua_name]
        
        # 纳甲 - 简化处理，生成六个随机的天干地支
        tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        najia = []
        for _ in range(6):
            gan = random.choice(tiangan)
            zhi = random.choice(dizhi)
            najia.append(f"{gan}{zhi}")
        
        # 世应爻 - 简化处理，随机选择世应爻位置
        shi_yao = random.randint(1, 6)
        ying_yao = 7 - shi_yao  # 世应相对
        
        return {
            "ben_gua": {
                "name": ben_gua_name,
                "element": ben_gua_element,
                "number": random.randint(1, 64)
            },
            "bian_gua": {
                "name": bian_gua_name,
                "element": bian_gua_element,
                "number": random.randint(1, 64)
            },
            "najia": najia,
            "shi_yao": shi_yao,
            "ying_yao": ying_yao
        }
    
    def get_hour_ganzhi(self, hour, day_gan):
        """根据小时和日干获取时辰干支"""
        # 时辰对照表（24小时制）
        hour_to_zhi_map = {
            0: "子", 1: "子",  # 23:00-01:00
            2: "丑", 3: "丑",  # 01:00-03:00
            4: "寅", 5: "寅",  # 03:00-05:00
            6: "卯", 7: "卯",  # 05:00-07:00
            8: "辰", 9: "辰",  # 07:00-09:00
            10: "巳", 11: "巳",  # 09:00-11:00
            12: "午", 13: "午",  # 11:00-13:00
            14: "未", 15: "未",  # 13:00-15:00
            16: "申", 17: "申",  # 15:00-17:00
            18: "酉", 19: "酉",  # 17:00-19:00
            20: "戌", 21: "戌",  # 19:00-21:00
            22: "亥", 23: "亥"   # 21:00-23:00
        }
        
        # 确定地支
        zhi = hour_to_zhi_map.get(hour, "子")
                
        # 根据日干确定时干
        gan_idx = {"甲": 0, "乙": 2, "丙": 4, "丁": 6, "戊": 8, 
                   "己": 0, "庚": 2, "辛": 4, "壬": 6, "癸": 8}
        
        # 时干顺序
        gans = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        
        # 地支序号
        zhi_idx = {"子": 0, "丑": 1, "寅": 2, "卯": 3, "辰": 4, "巳": 5,
                   "午": 6, "未": 7, "申": 8, "酉": 9, "戌": 10, "亥": 11}
        
        # 计算时干
        start_idx = gan_idx.get(day_gan, 0)
        gan_idx = (start_idx + zhi_idx.get(zhi, 0)) % 10
        gan = gans[gan_idx]
        
        return f"{gan}{zhi}"
        
    def get_najia_by_yao_number(self, yao_number):
        """根据爻序获取纳甲信息"""
        # 简化实现，固定生成天干地支
        tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        # 保证相同爻位返回一致的结果
        gan = tiangan[(yao_number * 2) % 10]
        zhi = dizhi[yao_number % 12]
        
        return f"{gan}{zhi}"

class GuaCalculator:
    """卦象计算类，整合各组件计算六爻卦象"""
    
    def __init__(self):
        """初始化卦象计算器"""
        # 初始化自己的简易纳甲处理器
        self.najia_processor = SimpleNajia()
    
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
        # 如果未提供经纬度，使用默认值
        if longitude is None:
            longitude = -100  # 默认北美经度
        if latitude is None:
            latitude = 40     # 默认北美纬度
        
        # 如果使用真太阳时，计算真太阳时
        adjusted_time_hour = time_hour
        if use_true_solar_time:
            adjusted_time_hour = solar_time_calculator.calculate_true_solar_time(
                solar_date, time_hour, longitude
            )
        
        # 将阳历转换为农历 - 使用正确的方法
        solar = Solar.fromYmd(solar_date.year, solar_date.month, solar_date.day)
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
        result["health_analysis"] = health_analyzer.analyze_health(result, day_master, yong_shen)
        
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
    
    def format_gua_result(self, result: Dict) -> str:
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

# 单例模式，导出一个实例
gua_calculator = GuaCalculator()
