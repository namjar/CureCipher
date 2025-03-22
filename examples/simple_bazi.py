"""
使用lunar_python库计算八字的简单示例
基于实际可用的API
"""

from lunar_python import Solar, Lunar

def calculate_simple_bazi(birth_year, birth_month, birth_day, birth_hour=0):
    """使用lunar_python库计算八字"""
    # 创建阳历对象
    solar = Solar.fromYmdHms(birth_year, birth_month, birth_day, birth_hour, 0, 0)
    print(f"阳历: {solar.toString()}")
    
    # 转换为农历
    lunar = solar.getLunar()
    print(f"农历: {lunar.toString()}")
    
    # 获取八字对象
    bazi = lunar.getEightChar()
    
    # 获取四柱
    year_gz = bazi.getYear()
    month_gz = bazi.getMonth()
    day_gz = bazi.getDay()
    time_gz = bazi.getTime()  # 使用getTime而不是getHour
    
    # 获取纳音
    year_nayin = bazi.getYearNaYin()
    month_nayin = bazi.getMonthNaYin()
    day_nayin = bazi.getDayNaYin()
    time_nayin = bazi.getTimeNaYin()
    
    # 获取五行属性
    year_element = get_element_from_gan(year_gz[0])
    month_element = get_element_from_gan(month_gz[0])
    day_element = get_element_from_gan(day_gz[0])
    time_element = get_element_from_gan(time_gz[0])
    
    print("\n八字四柱:")
    print(f"年柱: {year_gz} ({year_element})")
    print(f"月柱: {month_gz} ({month_element})")
    print(f"日柱: {day_gz} ({day_element}) - 日主")
    print(f"时柱: {time_gz} ({time_element})")
    
    print("\n纳音五行:")
    print(f"年柱: {year_nayin}")
    print(f"月柱: {month_nayin}")
    print(f"日柱: {day_nayin}")
    print(f"时柱: {time_nayin}")
    
    # 尝试计算大运（如果可能）
    try:
        print("\n大运:")
        gender_code = 1  # 男性
        dayun_list = bazi.getDaYun(gender_code)
        for i, yun in enumerate(dayun_list[:5]):  # 只显示前5个大运
            print(f"  大运{i+1}: {yun.getGanZhi()}, 年龄: {yun.getStartAge()}-{yun.getEndAge()}")
    except Exception as e:
        print(f"计算大运时出错: {e}")
    
    return {
        "year": year_gz,
        "month": month_gz,
        "day": day_gz,
        "time": time_gz,
        "day_master": day_gz[0],
        "day_master_element": day_element
    }

def get_element_from_gan(gan):
    """获取天干的五行属性"""
    elements_map = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }
    return elements_map.get(gan, "未知")

if __name__ == "__main__":
    print("=" * 60)
    print("八字计算 - 1977年2月25日晚上8点50分出生于北京的男性")
    print("=" * 60)
    
    # 测试不同的时辰
    print("\n测试21时（晚上9点）:")
    birth_hour = 21
    result = calculate_simple_bazi(1977, 2, 25, birth_hour)
    
    print("\n全部四柱: {0} {1} {2} {3}".format(
        result["year"], result["month"], result["day"], result["time"]
    ))
    print(f"日主五行: {result['day_master']} ({result['day_master_element']})")
