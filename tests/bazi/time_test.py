"""
测试时辰计算
"""
import sys
import os
import traceback

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from lunar_python import Solar, Lunar

def test_time_conversion():
    """测试时辰计算"""
    try:
        print("测试时辰计算...")
        
        # 测试案例：1977年2月25日20:50（晚上8点50分）在北京出生
        solar = Solar.fromYmdHms(1977, 2, 25, 20, 50, 0)
        
        # 转换为农历
        lunar = solar.getLunar()
        
        # 获取八字
        bazi = lunar.getEightChar()
        
        # 提取时柱
        hour_gz = bazi.getTime()
        
        print(f"阳历时间: 1977年2月25日 20:50")
        print(f"对应时柱: {hour_gz}")
        print(f"天干: {hour_gz[0]}")
        print(f"地支: {hour_gz[1]}")
        
        # 测试不同的小时
        test_hours = [19, 20, 21]
        for hour in test_hours:
            solar_test = Solar.fromYmdHms(1977, 2, 25, hour, 0, 0)
            lunar_test = solar_test.getLunar()
            bazi_test = lunar_test.getEightChar()
            hour_gz_test = bazi_test.getTime()
            print(f"测试时间 {hour}:00 对应时柱: {hour_gz_test}")
        
        print("时辰测试完成！")
        
    except Exception as e:
        print(f"时辰测试失败: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_time_conversion()
