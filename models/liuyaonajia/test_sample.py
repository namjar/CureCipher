import sys
import os
from pathlib import Path

# 修正父目录层级
project_root = str(Path(__file__).resolve().parents[2])  # 指向 CureCipher 根目录
print(f"Adding to sys.path: {project_root}")
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 打印 sys.path 调试
print("sys.path:")
for p in sys.path:
    print(f"  {p}")

from models.liuyaonajia.najia import Najia
from models.liuyaonajia.diagnosis import diagnose_health
import datetime

if __name__ == "__main__":
    params = [2, 2, 1, 2, 4, 2]
    date = "2019-12-25 00:20"
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')

    # 六爻排盘
    result = Najia(verbose=2).compile(params=params, date=date_obj).render()
    print("卦象：")
    print(result)

    # 健康诊断
    health_result = diagnose_health(params=params, date=date_obj, day_master_strength="neutral")
    print("\n健康分析：")
    print(f"卦名：{health_result['gua_name']}")
    print(f"五行：{health_result['gua_element']}")
    print(f"健康影响：{health_result['health_impacts']}")
    print(f"调理建议：{health_result['remedies']}")
    print(f"六神影响：{health_result['god6_impacts']}")