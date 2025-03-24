"""
六爻纳甲简单测试
"""

import sys
import os
from pathlib import Path
import datetime

# 确保项目根目录在 sys.path 中
project_root = str(Path(__file__).resolve().parent)
print(f"Adding to sys.path: {project_root}")
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 显示 sys.path
print("Current sys.path:")
for p in sys.path:
    print(f"  {p}")

# 导入模块
try:
    print("测试导入...")
    from models.liuyaonajia.najia import Najia
    from models.liuyaonajia.diagnosis import diagnose_health
    print("导入成功!")
except Exception as e:
    print(f"导入失败: {e}")
    sys.exit(1)

# 测试纳甲类初始化
try:
    print("\n测试Najia类初始化...")
    najia = Najia(verbose=1)
    print("初始化成功!")
except Exception as e:
    print(f"初始化失败: {e}")
    sys.exit(1)

# 测试编译和渲染
try:
    print("\n测试编译和渲染...")
    params = [2, 2, 1, 2, 4, 2]
    date = datetime.datetime.now()
    najia_result = najia.compile(params=params, date=date, gender="male")
    render_result = najia_result.render()
    print("编译和渲染成功:")
    print(render_result)
except Exception as e:
    print(f"编译或渲染失败: {e}")
    sys.exit(1)

# 测试健康诊断
try:
    print("\n测试健康诊断...")
    health_result = diagnose_health(params=params, date=date, gender="male")
    print("健康诊断成功:")
    print(f"卦名：{health_result['gua_name']}")
    print(f"五行：{health_result['gua_element']}")
    print(f"健康影响：{health_result['health_impacts']}")
    print(f"调理建议：{health_result['remedies']}")
    print(f"六神影响：{health_result['god6_impacts']}")
except Exception as e:
    print(f"健康诊断失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n所有测试通过!")
