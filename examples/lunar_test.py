"""
测试lunar_python库的基本功能
"""

try:
    print("尝试导入lunar_python...")
    from lunar_python import Solar, Lunar
    
    print("成功导入lunar_python库!")
    
    # 测试基本功能
    birth_year = 1977
    birth_month = 2
    birth_day = 25
    
    print(f"\n测试阳历日期: {birth_year}年{birth_month}月{birth_day}日")
    
    # 创建阳历对象
    solar = Solar.fromYmd(birth_year, birth_month, birth_day)
    print(f"阳历: {solar.toString()}")
    
    # 转换为农历
    lunar = solar.getLunar()
    print(f"农历: {lunar.toString()}")
    
    # 获取干支纪年
    print(f"\n干支纪年:")
    print(f"年柱: {lunar.getYearInGanZhi()}")
    print(f"月柱: {lunar.getMonthInGanZhi()}")
    print(f"日柱: {lunar.getDayInGanZhi()}")
    
    # 尝试获取八字
    print("\n尝试获取八字...")
    
    try:
        # 方法1: 使用getEightChar()
        bazi = lunar.getEightChar()
        print("成功获取八字对象!")
        
        # 尝试获取年月日时柱
        print("\n四柱:")
        try:
            print(f"年柱: {bazi.getYear()}")
            print(f"月柱: {bazi.getMonth()}")
            print(f"日柱: {bazi.getDay()}")
            print(f"时柱: {bazi.getHour() if hasattr(bazi, 'getHour') else bazi.getTime()}")
        except Exception as e:
            print(f"获取四柱时出错: {e}")
        
        # 尝试获取纳音
        print("\n纳音:")
        try:
            print(f"年柱纳音: {bazi.getYearNaYin()}")
            print(f"月柱纳音: {bazi.getMonthNaYin()}")
            print(f"日柱纳音: {bazi.getDayNaYin()}")
            print(f"时柱纳音: {bazi.getTimeNaYin()}")
        except Exception as e:
            print(f"获取纳音时出错: {e}")
        
    except Exception as e:
        print(f"获取八字对象时出错: {e}")
    
    # 查看可用方法
    print("\n查看Lunar对象的可用方法:")
    lunar_methods = [method for method in dir(lunar) if callable(getattr(lunar, method)) and not method.startswith('_')]
    print(', '.join(lunar_methods[:10]) + "... (已截断)")
    
    if hasattr(lunar, 'getEightChar'):
        print("\n查看EightChar对象的可用方法:")
        bazi = lunar.getEightChar()
        bazi_methods = [method for method in dir(bazi) if callable(getattr(bazi, method)) and not method.startswith('_')]
        print(', '.join(bazi_methods[:10]) + "... (已截断)")
    
    print("\nluar_python库测试完成!")

except ImportError as e:
    print(f"导入lunar_python库失败: {e}")
except Exception as e:
    print(f"测试lunar_python时出错: {e}")
