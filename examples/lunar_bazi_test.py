"""
使用lunar_python计算八字的测试脚本
"""

import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到系统路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入适配当前lunar_python版本的计算器
from models.bazi.calculator_lunar import calculate_bazi, get_element

def test_bazi_calculation():
    """测试八字计算"""
    print("=" * 60)
    print("八字计算测试 - 1977年2月25日晚上8点50分出生于北京的男性")
    print("=" * 60)
    
    # 将8点50分四舍五入到9点(21时)
    birth_hour = 21
    
    # 计算八字
    result = calculate_bazi(1977, 2, 25, birth_hour, "male", "Beijing")
    
    # 打印结果
    print("\n基本八字信息:")
    print(f"四柱: {result['bazi']['year']} {result['bazi']['month']} {result['bazi']['day']} {result['bazi']['hour']}")
    print(f"日主: {result['bazi']['day_master']} ({result['bazi']['day_master_element']})")
    
    print("\n四柱五行:")
    print(f"年柱: {result['bazi']['year']} - {result['elements']['year']}")
    print(f"月柱: {result['bazi']['month']} - {result['elements']['month']}")
    print(f"日柱: {result['bazi']['day']} - {result['elements']['day']}")
    print(f"时柱: {result['bazi']['hour']} - {result['elements']['hour']}")
    
    print("\n纳音:")
    print(f"年柱: {result['nayin']['year']}")
    print(f"月柱: {result['nayin']['month']}")
    print(f"日柱: {result['nayin']['day']}")
    print(f"时柱: {result['nayin']['hour']}")
    
    print("\n当前运势:")
    print(f"流年: {result['current']['liunian']} ({result['current']['liunian_element']})")
    print(f"流月: {result['current']['liuyue']} ({result['current']['liuyue_element']})")
    print(f"大运: {result['dayun']['ganzhi']} ({result['dayun']['element']})")
    print(f"小运: {result['xiaoyun']['ganzhi']} ({result['xiaoyun']['element']})")
    
    print("\n神煞:")
    if result.get('shensha'):
        for i, shensha in enumerate(result['shensha'], 1):
            print(f"  {i}. {shensha}")
    else:
        print("  无神煞信息")
    
    print("\n位置信息:")
    print(f"城市: {result['location']['city']}")
    print(f"经纬度: {result['location']['longitude']}, {result['location']['latitude']}")
    
    return result

def test_lunar_python_version():
    """测试lunar_python版本功能"""
    print("\n" + "=" * 60)
    print("测试lunar_python库基本功能")
    print("=" * 60)
    
    try:
        from lunar_python import Solar, Lunar
        
        # 创建一个阳历日期
        solar = Solar.fromYmd(1977, 2, 25)
        print(f"阳历: {solar.toYmd()}")
        
        # 转换为农历
        lunar = solar.getLunar()
        print(f"农历: {lunar.toYmd()}")
        
        # 获取八字
        bazi = lunar.getEightChar()
        year_gz = bazi.getYear()
        month_gz = bazi.getMonth()
        day_gz = bazi.getDay()
        hour_gz = bazi.getTime()
        
        print(f"八字: {year_gz} {month_gz} {day_gz} {hour_gz}")
        
        # 测试纳音
        print(f"纳音: {bazi.getYearNaYin()} {bazi.getMonthNaYin()} {bazi.getDayNaYin()} {bazi.getTimeNaYin()}")
        
        # 测试大运
        dayuns = bazi.getDaYun(1)  # 男性
        print("\n大运:")
        for i, dayun in enumerate(dayuns[:5]):  # 只显示前5个大运
            print(f"  大运{i+1}: {dayun.getGanZhi()}, 年龄: {dayun.getStartAge()}-{dayun.getEndAge()}")
        
        print("\nlunar_python库测试成功!")
        return True
    
    except Exception as e:
        print(f"lunar_python库测试失败: {e}")
        return False

if __name__ == "__main__":
    # 测试lunar_python库
    test_lunar_python_version()
    
    # 计算八字
    result = test_bazi_calculation()
    
    print("\n" + "=" * 60)
    print(f"测试完成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
