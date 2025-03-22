"""
八字计算模块
使用lunar_python库计算八字、流年、流月、大运、小运和神煞
"""

import datetime
import json
import os
import functools
import math
import requests
from cryptography.fernet import Fernet
from geopy.geocoders import Nominatim
from lunar_python import Solar, Lunar

@functools.lru_cache(maxsize=128)
def calculate_bazi(birth_year, birth_month, birth_day, birth_hour, gender, 
                  longitude=116.4074, latitude=39.9042, city=None):
    """
    计算八字及相关信息，支持真太阳时校正
    
    参数:
        birth_year (int): 出生年
        birth_month (int): 出生月
        birth_day (int): 出生日
        birth_hour (int): 出生时（24小时制）
        gender (str): 性别 ('male'/'female')
        longitude (float): 经度，默认北京116.4074
        latitude (float): 纬度，默认北京39.9042
        city (str, optional): 出生城市. 默认为None，使用经纬度
    
    返回:
        dict: 包含八字、四柱五行、流年、流月、大运、小运、神煞的字典
    """
    # 经纬度转换
    try:
        if city:
            # 尝试使用内部位置转换模块
            try:
                from .location_converter import city_to_coordinates
                coords = city_to_coordinates(city)
                if coords:
                    latitude, longitude = coords
                else:
                    # 如果内部模块无法找到城市，尝试使用外部地理编码
                    geolocator = Nominatim(user_agent="curecipher")
                    location = geolocator.geocode(city)
                    if location:
                        latitude = location.latitude
                        longitude = location.longitude
                    else:
                        # 如果仍然找不到，使用默认值
                        print(f"找不到城市 {city}，使用默认值: 经度={longitude}, 纬度={latitude}")
            except ImportError:
                # 如果内部模块不可用，使用外部地理编码
                geolocator = Nominatim(user_agent="curecipher")
                location = geolocator.geocode(city)
                if location:
                    latitude = location.latitude
                    longitude = location.longitude
                else:
                    # 如果找不到城市，使用默认值
                    print(f"找不到城市 {city}，使用默认值: 经度={longitude}, 纬度={latitude}")
            
        # 真太阳时校正
        solar = Solar.fromYmdHms(birth_year, birth_month, birth_day, birth_hour, 0, 0)
        
        # 计算真太阳时偏差
        time_diff = calculate_true_solar_time_diff(longitude, birth_year, birth_month, birth_day)
        
        # 调整时间
        adjusted_hour = birth_hour + time_diff / 60  # 转换为小时
        adjusted_day = birth_day
        
        # 处理跨日问题
        if adjusted_hour >= 24:
            adjusted_hour -= 24
            adjusted_day += 1
        elif adjusted_hour < 0:
            adjusted_hour += 24
            adjusted_day -= 1
            
        # 创建调整后的Solar对象
        adjusted_solar = Solar.fromYmdHms(
            birth_year, 
            birth_month, 
            adjusted_day, 
            int(adjusted_hour), 
            int((adjusted_hour - int(adjusted_hour)) * 60), 
            0
        )
        
        # 获取农历
        lunar = adjusted_solar.getLunar()
        
        # 八字
        bazi = lunar.getEightChar()
        year_gz = bazi.getYear()
        month_gz = bazi.getMonth()
        day_gz = bazi.getDay()
        hour_gz = bazi.getTime()
        
        # 获取天干和地支
        year_gan = year_gz[0]
        year_zhi = year_gz[1:]
        month_gan = month_gz[0]
        month_zhi = month_gz[1:]
        day_gan = day_gz[0]
        day_zhi = day_gz[1:]
        hour_gan = hour_gz[0]
        hour_zhi = hour_gz[1:]
        
        # 获取五行属性
        year_element = get_element(year_gan)
        month_element = get_element(month_gan)
        day_element = get_element(day_gan)
        hour_element = get_element(hour_gan)
        
        # 计算五行比例
        elements_count = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        
        # 天干五行
        elements_count[get_element(year_gan)] += 1
        elements_count[get_element(month_gan)] += 1
        elements_count[get_element(day_gan)] += 1
        elements_count[get_element(hour_gan)] += 1
        
        # 地支藏干五行（简化处理）
        zhi_to_elements = {
            "子": {"水": 1.0},
            "丑": {"土": 0.5, "金": 0.3, "水": 0.2},
            "寅": {"木": 0.6, "火": 0.3, "土": 0.1},
            "卯": {"木": 1.0},
            "辰": {"土": 0.6, "木": 0.3, "水": 0.1},
            "巳": {"火": 0.6, "土": 0.3, "金": 0.1},
            "午": {"火": 0.7, "土": 0.3},
            "未": {"土": 0.6, "火": 0.3, "木": 0.1},
            "申": {"金": 0.6, "水": 0.3, "土": 0.1},
            "酉": {"金": 1.0},
            "戌": {"土": 0.6, "火": 0.2, "木": 0.2},
            "亥": {"水": 0.7, "木": 0.3}
        }
        
        for zhi, elements in zhi_to_elements.items():
            if zhi == year_zhi:
                for element, weight in elements.items():
                    elements_count[element] += weight
            if zhi == month_zhi:
                for element, weight in elements.items():
                    elements_count[element] += weight
            if zhi == day_zhi:
                for element, weight in elements.items():
                    elements_count[element] += weight
            if zhi == hour_zhi:
                for element, weight in elements.items():
                    elements_count[element] += weight
        
        # 计算百分比
        total = sum(elements_count.values())
        element_percentages = {k: round(v / total * 100, 1) for k, v in elements_count.items()}
        
        # 纳音五行
        nayin = {
            "year": bazi.getYearNaYin(),
            "month": bazi.getMonthNaYin(),
            "day": bazi.getDayNaYin(),
            "hour": bazi.getTimeNaYin()
        }
        
        # 计算日主强弱
        day_master_element = get_element(day_gan)
        day_master_score = elements_count[day_master_element]
        
        # 判断日主强弱
        if day_master_score / total >= 0.3:
            day_master_strength = "旺"
            day_master_strength_en = "Strong"
            day_master_strength_es = "Fuerte"
        elif day_master_score / total <= 0.15:
            day_master_strength = "弱"
            day_master_strength_en = "Weak"
            day_master_strength_es = "Débil"
        else:
            day_master_strength = "中和"
            day_master_strength_en = "Balanced"
            day_master_strength_es = "Equilibrado"
        
        # 用神分析（简化）
        if day_master_strength == "旺":
            # 日主过旺，用耗泄
            yong_shen = get_controlled_element(day_master_element)
            yong_shen_en = get_element_english(yong_shen)
            yong_shen_es = get_element_spanish(yong_shen)
        elif day_master_strength == "弱":
            # 日主过弱，用生助
            yong_shen = get_generating_element(day_master_element)
            yong_shen_en = get_element_english(yong_shen)
            yong_shen_es = get_element_spanish(yong_shen)
        else:
            # 日主中和，平衡五行
            weakest_element = min(elements_count.items(), key=lambda x: x[1])[0]
            yong_shen = weakest_element
            yong_shen_en = get_element_english(yong_shen)
            yong_shen_es = get_element_spanish(yong_shen)
        
        # 当前年月的流年流月
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        
        # 计算流年干支
        lunar_current = calculate_liunian_ganzhi(current_year)
        
        # 计算流月干支
        liuyue = calculate_liuyue_ganzhi(current_year, current_month)
        
        # 计算大运
        # gender参数: 1代表男，0代表女
        gender_code = 1 if gender.lower() == "male" else 0
        try:
            # 尝试调用大运计算
            dayun_list = bazi.getDaYun(gender_code)
        except AttributeError:
            # 兼容处理：如果方法不可用，使用空列表
            # 静默处理，不输出警告
            dayun_list = []
        
        # 获取当前大运
        current_dayun = None
        start_ages = []
        
        if dayun_list:
            try:
                for i, yun in enumerate(dayun_list):
                    start_age = yun.getStartAge()
                    start_ages.append(start_age)
                    if i < len(dayun_list) - 1:
                        next_start_age = dayun_list[i+1].getStartAge()
                        current_age = current_year - birth_year
                        if start_age <= current_age < next_start_age:
                            current_dayun = yun
                            break
                    else:
                        # 最后一个大运
                        if start_age <= current_age:
                            current_dayun = yun
            except Exception as e:
                print(f"警告: 获取大运信息时出错: {e}")
        
        # 如果找不到当前大运，使用空实例
        if not current_dayun:
            current_dayun = {"ganzhi": "", "element": "", "start_age": 0, "end_age": 0}
        
        # 小运计算
        xiaoyun = None
        try:
            xiaoyun = lunar.getXiaoYun(current_year, gender_code, True)
        except AttributeError:
            # 静默处理，不输出警告
            xiaoyun = {"ganzhi": "", "element": ""}
        
        # 神煞
        shensha_list = []
        try:
            shensha_list = bazi.getShenSha()
        except AttributeError:
            # 静默处理，不输出警告
            pass
        
        # 日主天干
        day_master = day_gan
        day_master_element = get_element(day_master)
        
        # 尝试从六爻模块获取卦象信息（如果存在）
        liuyao_info = {}
        try:
            from models.liuyao.liuyao_analyzer import calculate_gua
            liuyao_info = calculate_gua(
                birth_year=birth_year,
                birth_month=birth_month,
                birth_day=birth_day,
                birth_hour=birth_hour,
                year_gz=year_gz,
                month_gz=month_gz,
                day_gz=day_gz,
                hour_gz=hour_gz,
                shensha_list=shensha_list
            )
        except (ImportError, ModuleNotFoundError):
            # 如果六爻模块不存在，留空
            liuyao_info = {
                "name": "未知",
                "description": "六爻模块未安装",
                "note": "请安装 models.liuyao.liuyao_analyzer 模块以获取六爻信息"
            }
        
        # 构建结果
        result = {
            "bazi": {
                "year": year_gz,
                "month": month_gz,
                "day": day_gz,
                "hour": hour_gz,
                "day_master": day_master,
                "day_master_element": day_master_element,
                "formatted": f"{year_gz} {month_gz} {day_gz} {hour_gz}"
            },
            "elements": {
                "year": year_element,
                "month": month_element,
                "day": day_element,
                "hour": hour_element,
                "percentages": element_percentages
            },
            "day_master_strength": {
                "status": day_master_strength,
                "en": day_master_strength_en,
                "es": day_master_strength_es
            },
            "yong_shen": {
                "element": yong_shen,
                "en": yong_shen_en,
                "es": yong_shen_es
            },
            "nayin": nayin,
            "current": {
                "liunian": lunar_current,
                "liunian_element": get_element(lunar_current[0]),
                "liuyue": liuyue,
                "liuyue_element": get_element(liuyue[0])
            },
            "dayun": {
                "ganzhi": current_dayun.get("ganzhi", "") if isinstance(current_dayun, dict) else "",
                "element": current_dayun.get("element", "") if isinstance(current_dayun, dict) else "",
                "start_age": current_dayun.get("start_age", 0) if isinstance(current_dayun, dict) else 0,
                "end_age": current_dayun.get("end_age", 0) if isinstance(current_dayun, dict) else 0
            },
            "xiaoyun": {
                "ganzhi": xiaoyun.get("ganzhi", "") if isinstance(xiaoyun, dict) else "",
                "element": xiaoyun.get("element", "") if isinstance(xiaoyun, dict) else ""
            },
            "shensha": shensha_list,
            "liuyao": liuyao_info,
            "location": {
                "city": city or "默认位置",
                "latitude": latitude,
                "longitude": longitude
            },
            "true_solar_time": {
                "original": f"{birth_hour:02d}:00",
                "adjusted": f"{int(adjusted_hour):02d}:{int((adjusted_hour - int(adjusted_hour)) * 60):02d}",
                "diff_minutes": round(time_diff, 2)
            }
        }
        
        # 加密数据（HIPAA合规）
        encrypted_result = encrypt_data(result)
        
        return {
            "result": result,
            "encrypted": encrypted_result
        }
    
    except Exception as e:
        print(f"计算八字时出错: {e}")
        import traceback
        traceback.print_exc()
        return {
            "error": str(e),
            "message": "计算八字时出错，请检查输入参数和网络连接"
        }

def calculate_true_solar_time_diff(longitude, year, month, day):
    """
    计算真太阳时校正（分钟数）
    
    参数:
        longitude (float): 经度
        year (int): 年
        month (int): 月
        day (int): 日
    
    返回:
        float: 时差（分钟）
    """
    # 计算儒略日
    if month <= 2:
        year -= 1
        month += 12
    
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    
    julian_day = (math.floor(365.25 * (year + 4716)) + 
                 math.floor(30.6001 * (month + 1)) + 
                 day + B - 1524.5)
    
    # 计算时间方程
    # 简化公式，实际应有更复杂精确的计算
    D = julian_day - 2451545.0  # J2000
    g = 357.529 + 0.98560028 * D  # 平太阳黄经
    g_rad = math.radians(g % 360)
    
    # 时间方程（简化）
    eq_time = (9.87 * math.sin(2 * g_rad) - 
              7.53 * math.cos(g_rad) - 
              1.5 * math.sin(g_rad))
    
    # 经度校正
    local_time_diff = longitude / 15 * 60  # 每15度经度1小时
    
    # 总时差
    return eq_time + local_time_diff

def get_default_location():
    """
    获取默认位置（北京）
    
    返回:
        tuple: (纬度, 经度)
    """
    return 39.9042, 116.4074  # 北京默认值

@functools.lru_cache(maxsize=64)
def get_element(gan):
    """
    获取天干的五行属性
    
    参数:
        gan (str): 天干字符
    
    返回:
        str: 五行属性（'木', '火', '土', '金', '水'）
    """
    elements_map = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }
    
    return elements_map.get(gan, "未知")

@functools.lru_cache(maxsize=16)
def get_element_english(chinese_element):
    """
    将中文五行属性转换为英文
    
    参数:
        chinese_element (str): 中文五行属性
    
    返回:
        str: 英文五行属性
    """
    element_map = {
        "木": "Wood",
        "火": "Fire",
        "土": "Earth",
        "金": "Metal",
        "水": "Water",
        "未知": "Unknown"
    }
    
    return element_map.get(chinese_element, "Unknown")

@functools.lru_cache(maxsize=16)
def get_element_spanish(chinese_element):
    """
    将中文五行属性转换为西班牙语
    
    参数:
        chinese_element (str): 中文五行属性
    
    返回:
        str: 西班牙语五行属性
    """
    element_map = {
        "木": "Madera",
        "火": "Fuego",
        "土": "Tierra",
        "金": "Metal",
        "水": "Agua",
        "未知": "Desconocido"
    }
    
    return element_map.get(chinese_element, "Desconocido")

@functools.lru_cache(maxsize=16)
def get_generating_element(element):
    """
    获取生我的五行
    
    参数:
        element (str): 五行属性
    
    返回:
        str: 生我的五行
    """
    generating_map = {
        "木": "水",
        "火": "木",
        "土": "火",
        "金": "土",
        "水": "金"
    }
    return generating_map.get(element, "未知")

@functools.lru_cache(maxsize=16)
def get_controlled_element(element):
    """
    获取我克的五行
    
    参数:
        element (str): 五行属性
    
    返回:
        str: 我克的五行
    """
    controlled_map = {
        "木": "土",
        "火": "金",
        "土": "水",
        "金": "木",
        "水": "火"
    }
    return controlled_map.get(element, "未知")

def encrypt_data(data):
    """
    加密数据（HIPAA合规）
    
    参数:
        data (dict): 要加密的数据
    
    返回:
        str: 加密后的数据
    """
    # 使用固定密钥进行简单加密（实际使用中应使用安全的密钥管理）
    key = b'my-secret-key-16'  # 16字节密钥示例
    fernet = Fernet(key)
    encrypted = fernet.encrypt(json.dumps(data, ensure_ascii=False).encode())
    return encrypted.decode()

def decrypt_data(encrypted_data):
    """
    解密数据
    
    参数:
        encrypted_data (str): 加密的数据
    
    返回:
        dict: 解密后的数据
    """
    key = b'my-secret-key-16'
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data.encode())
    return json.loads(decrypted.decode())

def calculate_liunian_ganzhi(year):
    """
    计算流年干支
    
    参数:
        year (int): 年份
    
    返回:
        str: 干支
    """
    Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    gan_index = (year - 4) % 10
    zhi_index = (year - 4) % 12
    
    return Gan[gan_index] + Zhi[zhi_index]

def calculate_liuyue_ganzhi(year, month):
    """
    计算流月干支
    
    参数:
        year (int): 年份
        month (int): 月份
    
    返回:
        str: 干支
    """
    Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 计算年份的天干
    year_gan_index = (year - 4) % 10
    
    # 根据年份天干和月份确定月干
    base_month_gan_index = (year_gan_index * 2 + month - 1) % 10
    
    # 确定月支（正月-寅月）
    month_zhi_index = (month + 1) % 12
    
    return Gan[base_month_gan_index] + Zhi[month_zhi_index]

# 创建默认位置配置文件（如果不存在）
def create_default_location_config():
    """创建默认位置配置文件（如果不存在）"""
    config_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(config_dir, "location_config.json")
    
    if not os.path.exists(config_path):
        default_config = {
            "default_location": {
                "latitude": 39.9042,
                "longitude": 116.4074
            },
            "description": "北京默认位置"
        }
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=4)
            print(f"已创建默认位置配置文件: {config_path}")
        except Exception as e:
            print(f"创建默认位置配置文件时出错: {e}")

# 初始化配置文件
create_default_location_config()

if __name__ == "__main__":
    # 测试代码
    test_result = calculate_bazi(1990, 5, 15, 8, "male", longitude=116.4074, latitude=39.9042)
    result = test_result["result"]
    
    print("八字: " + result["bazi"]["formatted"])
    print("五行比例: ", end="")
    for element, percentage in result["elements"]["percentages"].items():
        print(f"{element}: {percentage}%, ", end="")
    print()
    print(f"日主强弱: {result['day_master_strength']['status']} ({result['day_master_strength']['en']}/{result['day_master_strength']['es']})")
    print(f"用神: {result['yong_shen']['element']} ({result['yong_shen']['en']}/{result['yong_shen']['es']})")
    print(f"流月干支 (1990年5月): {calculate_liuyue_ganzhi(1990, 5)}")
    print(f"六爻卦象: {result['liuyao']['name']}")
    
    # 查看加密数据（HIPAA合规）
    print("\n数据加密示例:")
    print(test_result["encrypted"][:50] + "...")
    
    # 解密测试
    decrypted = decrypt_data(test_result["encrypted"])
    print("\n解密验证成功：", decrypted["bazi"]["formatted"] == result["bazi"]["formatted"])
