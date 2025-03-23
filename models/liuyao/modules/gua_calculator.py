# /Users/ericw/Documents/GitHub/CureCipher/models/liuyao/modules/gua_calculator.py
"""
卦象计算模块 - 计算六爻卦象并整合各种信息
"""

import datetime
from typing import Dict, Optional

from lunar_python import Solar, Lunar

from .location import location_service
from .solar_time import solar_time_calculator
from .yao_components import yao_components
from .AccurateNajia import accurate_najia
from .health_analyzer import health_analyzer
from .shensha_data import get_shensha_by_zhi, get_liushen
from .gua_display import generate_full_gua_display, gua_to_image_text

class GuaCalculator:
    """卦象计算类，整合各组件计算六爻卦象"""
    
    def __init__(self):
        """初始化卦象计算器"""
        pass  # 已经通过单例模式导入依赖，无需额外初始化
    
    def calculate_gua(self, solar_date: datetime.date, time_hour: float, 
                      longitude: Optional[float]=None, latitude: Optional[float]=None, 
                      day_master: Optional[str]=None, yong_shen: Optional[str]=None,
                      use_true_solar_time: bool=True, ip: Optional[str]=None) -> Dict:
        """
        计算六爻卦象
        
        参数:
            solar_date (datetime.date): 阳历日期
            time_hour (float): 时辰（24小时制，0-23），可以包含小数部分表示分钟
            longitude (float, optional): 经度，东经为正，西经为负，默认通过IP获取
            latitude (float, optional): 纬度，北纬为正，南纬为负，默认通过IP获取
            day_master (str, optional): 八字日主天干，例如'甲'
            yong_shen (str, optional): 八字用神五行，例如'水'
            use_true_solar_time (bool): 是否使用真太阳时，默认True
            ip (str, optional): 用户IP地址，用于自动获取位置，默认None
            
        返回:
            Dict: 包含六爻卦象的相关信息
        """
        # 输入验证
        if not isinstance(solar_date, datetime.date):
            raise ValueError(f"solar_date 必须是 datetime.date 类型，当前为 {type(solar_date)}")
        if not isinstance(time_hour, (int, float)) or time_hour < 0 or time_hour >= 24:
            raise ValueError(f"time_hour 必须在 0-23.99 范围内，当前为 {time_hour}")

        # 如果未提供经纬度，尝试通过IP地址获取
        if (longitude is None or latitude is None) and ip is not None:
            try:
                longitude, latitude = location_service.get_location_from_ip(ip)
            except Exception as e:
                print(f"通过IP获取位置失败: {e}")
                longitude = longitude or 116.4  # 默认北京经度
                latitude = latitude or 39.9     # 默认北京纬度
        elif longitude is None or latitude is None:
            longitude = longitude or 116.4  # 默认北京经度
            latitude = latitude or 39.9     # 默认北京纬度
        
        # 如果使用真太阳时，计算真太阳时
        adjusted_time_hour = time_hour
        if use_true_solar_time:
            adjusted_time_hour = solar_time_calculator.calculate_true_solar_time(
                solar_date, time_hour, longitude, latitude
            )
        
        # 将阳历转换为农历
        solar = Solar.fromYmd(solar_date.year, solar_date.month, solar_date.day)
        lunar = solar.getLunar()
        
        # 获取四柱干支
        year_gz = lunar.getYearInGanZhi()
        month_gz = lunar.getMonthInGanZhi()
        day_gz = lunar.getDayInGanZhi()
        hour_gz = yao_components.get_hour_ganzhi(int(adjusted_time_hour), day_gz[0])
        
        # 从干支提取天干地支
        year_gan, year_zhi = year_gz[0], year_gz[1:]
        month_gan, month_zhi = month_gz[0], month_gz[1:]
        day_gan, day_zhi = day_gz[0], day_gz[1:]
        hour_gan, hour_zhi = hour_gz[0], hour_gz[1:]
        
        # 使用accurate_najia计算卦象
        gua_data = accurate_najia.parse_gua_by_datetime(
            solar_date.year, solar_date.month, solar_date.day, 
            adjusted_time_hour, longitude, latitude
        )
        
        # 动爻直接从gua_data获取
        dong_yao_pos = gua_data['dong_yao']
        
        # 获取本卦和变卦信息
        ben_gua = gua_data['ben_gua']
        ben_gua_name = ben_gua['name']
        ben_gua_element = ben_gua['element']
        ben_yao_array = gua_data['ben_gua'].get('yao', [])
        
        bian_gua = gua_data['bian_gua']
        bian_gua_name = bian_gua['name']
        bian_gua_element = bian_gua['element']
        bian_yao_array = gua_data['bian_gua'].get('yao', [])
        
        # 获取纳甲信息
        najia_info = gua_data['najia']
        bian_najia_info = gua_data.get('bian_najia', [])
        
        # 验证卦象数据完整性
        if not najia_info or len(najia_info) != 6:
            raise ValueError("本卦纳甲信息不完整")
        if not bian_najia_info or len(bian_najia_info) != 6:
            raise ValueError("变卦纳甲信息不完整")
        if not ben_yao_array or not bian_yao_array:
            raise ValueError("本卦或变卦爻位信息缺失")
        
        # 计算六亲、六神、空亡
        liuqin = yao_components.calculate_liuqin(najia_info, day_master, day_zhi)
        liushen = get_liushen(day_gan)
        kongwang = yao_components.calculate_kongwang(day_gz)
        bian_liuqin = yao_components.calculate_liuqin(bian_najia_info, day_master, day_zhi)
        
        # 获取世应信息
        shi_yao = gua_data['shi_yao']
        ying_yao = gua_data['ying_yao']
        
        # 使用神煞数据模块获取神煞信息
        shenshas_info = get_shensha_by_zhi(year_zhi, month_zhi, day_zhi, hour_zhi)
        
        # 整合结果
        result = {
            "ben_gua": {
                "name": ben_gua_name,
                "element": ben_gua_element,
                "number": ben_gua.get('number', 0),
                "yao": ben_yao_array
            },
            "najia": najia_info,
            "liuqin": liuqin,
            "liushen": liushen,
            "kongwang": kongwang,
            "shi_yao": shi_yao,
            "ying_yao": ying_yao,
            "dong_yao": dong_yao_pos,
            "bian_gua": {
                "name": bian_gua_name,
                "element": bian_gua_element,
                "number": bian_gua.get('number', 0),
                "yao": bian_yao_array
            },
            "bian_najia": bian_najia_info,
            "bian_liuqin": bian_liuqin,
            "shenshas": shenshas_info,
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
        
        # 生成卦象ASCII图
        result["gua_ascii"] = generate_full_gua_display(result)
        
        # 生成图像文本
        result["gua_image_text"] = gua_to_image_text(ben_yao_array, bian_yao_array, dong_yao_pos, ben_gua_name, bian_gua_name)
        
        return result
    
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
        output.append(f"测算日期: {result['date_info']['solar_date']}")
        output.append(f"当地时间: {result['date_info']['time_hour']:.2f}时")
        output.append(f"真太阳时: {result['date_info']['adjusted_time_hour']:.2f}时") if result['date_info']['use_true_solar_time'] else output.append("真太阳时: 未开启")
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
        
        # 添加卦象图形（确保与本卦和变卦名称一致）
        if "gua_image_text" in result:
            output.append("\n" + result["gua_image_text"])
        
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
        
        # 变卦纳甲信息
        if 'bian_najia' in result and result['bian_najia']:
            bian_najia_str = ", ".join([
                f"初爻{result['bian_najia'][0]}" if i == 0 else 
                f"六爻{result['bian_najia'][-1]}" if i == 5 else 
                f"第{i+1}爻{result['bian_najia'][i]}" 
                for i in range(len(result['bian_najia']))
            ])
            output.append(f"变卦纳甲: {bian_najia_str}")
        
        # 变卦六亲信息
        if 'bian_liuqin' in result and result['bian_liuqin']:
            bian_liuqin_str = ", ".join([
                f"初爻{result['bian_liuqin'][0]}" if i == 0 else 
                f"六爻{result['bian_liuqin'][-1]}" if i == 5 else 
                f"第{i+1}爻{result['bian_liuqin'][i]}" 
                for i in range(len(result['bian_liuqin']))
            ])
            output.append(f"变卦六亲: {bian_liuqin_str}")
        
        # 神煞信息
        if 'shenshas' in result and result['shenshas']:
            output.append("")
            output.append("神煞信息:")
            
            # 年柱神煞
            if 'year' in result['shenshas'] and result['shenshas']['year']:
                year_shenshas = [
                    f"{name}(第{pos}爻)" for name, pos in result['shenshas']['year']
                ]
                output.append(f"  年柱神煞: {', '.join(year_shenshas)}")
            
            # 月柱神煞
            if 'month' in result['shenshas'] and result['shenshas']['month']:
                month_shenshas = [
                    f"{name}(第{pos}爻)" for name, pos in result['shenshas']['month']
                ]
                output.append(f"  月柱神煞: {', '.join(month_shenshas)}")
            
            # 日柱神煞
            if 'day' in result['shenshas'] and result['shenshas']['day']:
                day_shenshas = [
                    f"{name}(第{pos}爻)" for name, pos in result['shenshas']['day']
                ]
                output.append(f"  日柱神煞: {', '.join(day_shenshas)}")
            
            # 时柱神煞
            if 'hour' in result['shenshas'] and result['shenshas']['hour']:
                hour_shenshas = [
                    f"{name}(第{pos}爻)" for name, pos in result['shenshas']['hour']
                ]
                output.append(f"  时柱神煞: {', '.join(hour_shenshas)}")
        
        # 健康分析
        if 'health_analysis' in result:
            output.append("")
            output.append(f"健康影响: {result['health_analysis']['overall']}")
            if result['health_analysis']['specific_issues']:
                output.append(f"具体问题: {' '.join(result['health_analysis']['specific_issues'])}")
            if result['health_analysis']['recommendations']:
                output.append(f"健康建议: {', '.join(result['health_analysis']['recommendations'])}")
        
        return "\n".join(output)

# 导出单例实例
gua_calculator = GuaCalculator()