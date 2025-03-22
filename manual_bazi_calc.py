"""
直接计算八字的脚本

男性  阳历1977年2月25日晚上8点50分出生于北京
"""

import sys
from datetime import datetime
from lunar_python import Solar, Lunar, Gan, Zhi
import json
from pathlib import Path

# 将计算结果直接打印输出

# 设置出生数据
birth_year = 1977
birth_month = 2
birth_day = 25
birth_hour = 21  # 8:50pm 四舍五入到9点
birth_gender = "male"  # 男性
birth_city = "Beijing"  # 北京

# 使用lunar_python进行计算
solar = Solar.fromYmdHms(birth_year, birth_month, birth_day, birth_hour, 0, 0)

# 设置经纬度（北京的经纬度）
solar.setLongitude(116.4074)
solar.setLatitude(39.9042)

# 获取农历和八字信息
lunar = solar.getLunar()
bazi = lunar.getEightChar()

# 获取四柱
year_gz = bazi.getYear()
month_gz = bazi.getMonth()
day_gz = bazi.getDay()
hour_gz = bazi.getTime()

# 获取干支和纳音
year_gan = year_gz[0]
year_zhi = year_gz[1:]
month_gan = month_gz[0]
month_zhi = month_gz[1:]
day_gan = day_gz[0]
day_zhi = day_gz[1:]
hour_gan = hour_gz[0]
hour_zhi = hour_gz[1:]

# 纳音五行
year_nayin = bazi.getYearNaYin()
month_nayin = bazi.getMonthNaYin()
day_nayin = bazi.getDayNaYin()
hour_nayin = bazi.getTimeNaYin()

# 获取五行属性
elements_map = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}
year_element = elements_map.get(year_gan, "未知")
month_element = elements_map.get(month_gan, "未知")
day_element = elements_map.get(day_gan, "未知")
hour_element = elements_map.get(hour_gan, "未知")

# 当前年月的流年流月
current_year = datetime.now().year
current_month = datetime.now().month
lunar_current = Lunar.fromYmd(current_year, current_month, 1)
liunian = lunar_current.getYearInGanZhi()
liuyue = lunar_current.getMonthInGanZhi()
liunian_element = elements_map.get(liunian[0], "未知")
liuyue_element = elements_map.get(liuyue[0], "未知")

# 大运
gender_code = 1 if birth_gender.lower() == "male" else 0
dayun_list = bazi.getDaYun(gender_code)

# 获取当前大运
current_age = current_year - birth_year
current_dayun = None
for i, yun in enumerate(dayun_list):
    start_age = yun.getStartAge()
    if i < len(dayun_list) - 1:
        next_start_age = dayun_list[i+1].getStartAge()
        if start_age <= current_age < next_start_age:
            current_dayun = yun
            break
    else:
        # 最后一个大运
        if start_age <= current_age:
            current_dayun = yun

if not current_dayun and dayun_list:
    current_dayun = dayun_list[0]

# 小运
xiaoyun = lunar.getXiaoYun(current_year, gender_code, True)

# 神煞
shensha_list = bazi.getShenSha()

# 打印结果
print("=" * 60)
print(f"出生日期：阳历 {birth_year}年{birth_month}月{birth_day}日 {birth_hour}时")
print(f"出生地点：{birth_city}")
print(f"性别：{'男' if birth_gender.lower() == 'male' else '女'}")
print("=" * 60)
print("八字四柱：")
print(f"年柱：{year_gz} ({year_element})")
print(f"月柱：{month_gz} ({month_element})")
print(f"日柱：{day_gz} ({day_element}) - 日主")
print(f"时柱：{hour_gz} ({hour_element})")
print("=" * 60)
print("纳音五行：")
print(f"年柱：{year_nayin}")
print(f"月柱：{month_nayin}")
print(f"日柱：{day_nayin}")
print(f"时柱：{hour_nayin}")
print("=" * 60)
print("大运信息：")
if current_dayun:
    print(f"当前大运：{current_dayun.getGanZhi()} ({elements_map.get(current_dayun.getGanZhi()[0], '未知')})")
    print(f"大运起始年龄：{current_dayun.getStartAge()}")
    print(f"大运结束年龄：{current_dayun.getEndAge()}")
else:
    print("未能计算当前大运")

print("=" * 60)
print("小运信息：")
print(f"当前小运：{xiaoyun.getGanZhi()} ({elements_map.get(xiaoyun.getGanZhi()[0], '未知')})")

print("=" * 60)
print("当前流年流月：")
print(f"流年：{liunian} ({liunian_element})")
print(f"流月：{liuyue} ({liuyue_element})")

print("=" * 60)
print("神煞信息：")
if shensha_list:
    for i, shensha in enumerate(shensha_list):
        print(f"{i+1}. {shensha}")
else:
    print("未获取到神煞信息")

print("=" * 60)
print("五行统计：")
element_count = {
    "木": 0,
    "火": 0,
    "土": 0,
    "金": 0,
    "水": 0
}
# 四柱天干的五行
element_count[year_element] += 1
element_count[month_element] += 1
element_count[day_element] += 1
element_count[hour_element] += 1

print(f"木：{element_count['木']}个")
print(f"火：{element_count['火']}个")
print(f"土：{element_count['土']}个")
print(f"金：{element_count['金']}个")
print(f"水：{element_count['水']}个")

print("=" * 60)
print("日主五行分析：")
day_master = day_gan
day_master_element = day_element

# 获取生我和克我的五行
generating_map = {
    "木": "水",
    "火": "木",
    "土": "火",
    "金": "土",
    "水": "金"
}
controlling_map = {
    "木": "金",
    "火": "水",
    "土": "木",
    "金": "火",
    "水": "土"
}
generated_map = {
    "木": "火",
    "火": "土",
    "土": "金",
    "金": "水",
    "水": "木"
}
controlled_map = {
    "木": "土",
    "火": "金",
    "土": "水",
    "金": "木",
    "水": "火"
}

sheng_wo = generating_map[day_master_element]
ke_wo = controlling_map[day_master_element]
wo_sheng = generated_map[day_master_element]
wo_ke = controlled_map[day_master_element]

print(f"日主五行：{day_master} ({day_master_element})")
print(f"生我者：{sheng_wo}")
print(f"克我者：{ke_wo}")
print(f"我生者：{wo_sheng}")
print(f"我克者：{wo_ke}")

# 保存计算结果到JSON文件
result = {
    "basic_info": {
        "birth_date": f"{birth_year}年{birth_month}月{birth_day}日 {birth_hour}时",
        "birth_place": birth_city,
        "gender": "男" if birth_gender.lower() == "male" else "女"
    },
    "bazi": {
        "year": year_gz,
        "month": month_gz,
        "day": day_gz,
        "hour": hour_gz,
        "elements": {
            "year": year_element,
            "month": month_element,
            "day": day_element,
            "hour": hour_element
        },
        "nayin": {
            "year": year_nayin,
            "month": month_nayin,
            "day": day_nayin,
            "hour": hour_nayin
        }
    },
    "dayun": {
        "ganzhi": current_dayun.getGanZhi() if current_dayun else "",
        "element": elements_map.get(current_dayun.getGanZhi()[0], "未知") if current_dayun else "",
        "start_age": current_dayun.getStartAge() if current_dayun else 0,
        "end_age": current_dayun.getEndAge() if current_dayun else 0
    },
    "xiaoyun": {
        "ganzhi": xiaoyun.getGanZhi(),
        "element": elements_map.get(xiaoyun.getGanZhi()[0], "未知")
    },
    "current": {
        "liunian": liunian,
        "liunian_element": liunian_element,
        "liuyue": liuyue,
        "liuyue_element": liuyue_element
    },
    "shensha": shensha_list,
    "element_count": element_count,
    "day_master_analysis": {
        "day_master": day_master,
        "day_master_element": day_master_element,
        "sheng_wo": sheng_wo,
        "ke_wo": ke_wo,
        "wo_sheng": wo_sheng,
        "wo_ke": wo_ke
    }
}

# 保存到文件
with open('/Users/ericw/Documents/GitHub/CureCipher/manual_bazi_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("=" * 60)
print("计算结果已保存到 manual_bazi_result.json 文件")
