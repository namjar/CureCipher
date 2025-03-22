"""
八字计算模块
使用lunar_python库计算八字、流年、流月、大运、小运和神煞
"""

import datetime
import requests
from geopy.geocoders import Nominatim
from lunar_python import Solar, Lunar, Gan, Zhi

def calculate_bazi(birth_year, birth_month, birth_day, birth_hour, gender, city=None):
    """
    计算八字及相关信息
    
    参数:
        birth_year (int): 出生年
        birth_month (int): 出生月
        birth_day (int): 出生日
        birth_hour (int): 出生时（24小时制）
        gender (str): 性别 ('male'/'female')
        city (str, optional): 出生城市. 默认为None，将通过IP获取当前位置
    
    返回:
        dict: 包含八字、四柱五行、流年、流月、大运、小运、神煞的字典
    """
    # 经纬度转换
    try:
        geolocator = Nominatim(user_agent="curecipher")
        if city:
            location = geolocator.geocode(city)
            if location:
                latitude = location.latitude
                longitude = location.longitude
            else:
                # 如果找不到城市，使用默认值
                print(f"找不到城市 {city}，使用默认值")
                latitude, longitude = get_default_location()
        else:
            latitude, longitude = get_default_location()
            
        # 真太阳时校正
        solar = Solar.fromYmdHms(birth_year, birth_month, birth_day, birth_hour, 0, 0)
        solar.setLongitude(longitude)
        solar.setLatitude(latitude)
        lunar = solar.getLunar()
        
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
        
        # 纳音五行
        nayin = {
            "year": bazi.getYearNaYin(),
            "month": bazi.getMonthNaYin(),
            "day": bazi.getDayNaYin(),
            "hour": bazi.getTimeNaYin()
        }
        
        # 当前年月的流年流月
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        
        lunar_current = Lunar.fromYmd(current_year, current_month, 1)
        liunian = lunar_current.getYearInGanZhi()
        liuyue = lunar_current.getMonthInGanZhi()
        
        # 计算大运
        # gender参数: 1代表男，0代表女
        gender_code = 1 if gender.lower() == "male" else 0
        dayun_list = bazi.getDaYun(gender_code)
        
        # 获取当前大运
        current_dayun = None
        start_ages = []
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
        
        # 如果找不到当前大运，使用第一个
        if not current_dayun and dayun_list:
            current_dayun = dayun_list[0]
        
        # 小运计算
        xiaoyun = lunar.getXiaoYun(current_year, gender_code, True)
        
        # 神煞
        shensha_list = bazi.getShenSha()
        
        # 日主天干
        day_master = day_gan
        day_master_element = get_element(day_master)
        
        result = {
            "bazi": {
                "year": year_gz,
                "month": month_gz,
                "day": day_gz,
                "hour": hour_gz,
                "day_master": day_master,
                "day_master_element": day_master_element
            },
            "elements": {
                "year": year_element,
                "month": month_element,
                "day": day_element,
                "hour": hour_element
            },
            "nayin": nayin,
            "current": {
                "liunian": liunian,
                "liunian_element": get_element(liunian[0]),
                "liuyue": liuyue,
                "liuyue_element": get_element(liuyue[0])
            },
            "dayun": {
                "ganzhi": current_dayun.getGanZhi() if current_dayun else "",
                "element": get_element(current_dayun.getGanZhi()[0]) if current_dayun else "",
                "start_age": current_dayun.getStartAge() if current_dayun else 0,
                "end_age": current_dayun.getEndAge() if current_dayun else 0
            },
            "xiaoyun": {
                "ganzhi": xiaoyun.getGanZhi(),
                "element": get_element(xiaoyun.getGanZhi()[0])
            },
            "shensha": shensha_list,
            "location": {
                "city": city or "默认位置",
                "latitude": latitude,
                "longitude": longitude
            }
        }
        
        return result
    
    except Exception as e:
        print(f"计算八字时出错: {e}")
        return {
            "error": str(e),
            "message": "计算八字时出错，请检查输入参数和网络连接"
        }

def get_default_location():
    """
    获取默认位置（通过IP地址）
    
    返回:
        tuple: (纬度, 经度)
    """
    try:
        response = requests.get("http://ipinfo.io/json")
        data = response.json()
        city = data.get("city", "New York")
        
        geolocator = Nominatim(user_agent="curecipher")
        location = geolocator.geocode(city)
        
        if location:
            return location.latitude, location.longitude
        else:
            # 如果无法定位城市，则返回北京的坐标
            default_location = geolocator.geocode("Beijing")
            return default_location.latitude, default_location.longitude
    
    except Exception as e:
        print(f"获取默认位置时出错: {e}")
        # 返回北京的默认坐标
        return 39.9042, 116.4074

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

def get_element_english(chinese_element):
    """
    将中文五行属性转换为英文
    
    参数:
        chinese_element (str): 中文五行属性
    
    返回:
        str: 英文五行属性 ('wood', 'fire', 'earth', 'metal', 'water')
    """
    element_map = {
        "木": "wood",
        "火": "fire",
        "土": "earth",
        "金": "metal",
        "水": "water"
    }
    
    return element_map.get(chinese_element, "unknown")

if __name__ == "__main__":
    # 测试代码
    result = calculate_bazi(1990, 5, 15, 12, "male", "Beijing")
    print(result)
