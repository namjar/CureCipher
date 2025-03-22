"""
测试时辰计算，检查八字时柱是否正确
"""
import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from lunar_python import Solar, Lunar

def main():
    """检查1977年2月25日不同时间对应的时柱"""
    print("===== 八字时柱测试 =====")
    print("测试1977年2月25日不同时间对应的八字时柱\n")
    
    # 创建报告目录
    hours_data = []
    
    # 测试整点时间
    for hour in range(0, 24):
        solar = Solar.fromYmdHms(1977, 2, 25, hour, 0, 0)
        lunar = solar.getLunar()
        bazi = lunar.getEightChar()
        hour_gz = bazi.getTime()
        
        hour_data = {
            "hour": hour,
            "time_str": f"{hour:02d}:00",
            "hour_gz": hour_gz,
            "gan": hour_gz[0],
            "zhi": hour_gz[1]
        }
        hours_data.append(hour_data)
        
        print(f"时间 {hour:02d}:00 对应时柱: {hour_gz}")
        
        # 特别检查20:00 (8点)
        if hour == 20:
            solar_8pm = Solar.fromYmdHms(1977, 2, 25, 20, 50, 0)
            lunar_8pm = solar_8pm.getLunar()
            bazi_8pm = lunar_8pm.getEightChar()
            hour_gz_8pm = bazi_8pm.getTime()
            print(f"\n特别检查 - 时间 20:50 对应时柱: {hour_gz_8pm}")
    
    # 分析结果
    print("\n===== 分析结果 =====")
    
    # 1. 按时辰划分
    time_mapping = {}
    for data in hours_data:
        gz = data["hour_gz"]
        if gz not in time_mapping:
            time_mapping[gz] = []
        time_mapping[gz].append(data["hour"])
    
    print("时辰对应的小时:")
    for gz, hours in time_mapping.items():
        hour_ranges = [f"{h:02d}:00" for h in hours]
        print(f"{gz}: {', '.join(hour_ranges)}")
    
    # 检查晚上8点50分
    solar_check = Solar.fromYmdHms(1977, 2, 25, 20, 50, 0)
    lunar_check = solar_check.getLunar()
    bazi_check = lunar_check.getEightChar()
    
    # 获取完整八字
    year_gz = bazi_check.getYear()
    month_gz = bazi_check.getMonth()
    day_gz = bazi_check.getDay()
    hour_gz = bazi_check.getTime()
    
    print(f"\n1977年2月25日 20:50 的八字:")
    print(f"年柱: {year_gz}")
    print(f"月柱: {month_gz}")
    print(f"日柱: {day_gz}")
    print(f"时柱: {hour_gz}")
    print(f"完整八字: {year_gz} {month_gz} {day_gz} {hour_gz}")
    
    # 输出判断结果
    correct_hour_gz = "壬戌"  # 根据您提供的正确八字
    if hour_gz == correct_hour_gz:
        print(f"\n✅ 八字时柱计算正确: {hour_gz}")
    else:
        print(f"\n❌ 八字时柱计算不正确!")
        print(f"   计算得到: {hour_gz}")
        print(f"   应该为: {correct_hour_gz}")
        print("   可能是时辰划分或lunar_python库的实现问题。")

if __name__ == "__main__":
    main()
