#!/usr/bin/env python
"""
简单测试脚本，测试六爻纳甲模块是否正常工作
"""

import sys
import os
from pathlib import Path
import datetime

# 确保项目根目录在 sys.path 中
project_root = str(Path(__file__).resolve().parent)
print(f"当前工作目录: {os.getcwd()}")
print(f"添加路径: {project_root}")
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 显示当前路径
print("\n当前Python路径:")
for p in sys.path:
    print(f"  {p}")

# 导入模块
try:
    print("\n尝试导入六爻纳甲模块...")
    from models.liuyaonajia.najia import Najia
    print("导入Najia类成功!")
    from models.liuyaonajia.diagnosis import diagnose_health
    print("导入diagnose_health成功!")
except Exception as e:
    print(f"导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 运行测试
try:
    print("\n运行测试...")
    # 创建参数和日期
    params = [2, 2, 1, 2, 4, 2]
    date = datetime.datetime.now()
    
    # 测试Najia类
    najia = Najia(verbose=1)
    result = najia.compile(params=params, date=date).render()
    print("\n纳甲排盘结果:")
    print(result)
    
    # 测试健康诊断
    health = diagnose_health(params=params, date=date, day_master_strength="neutral")
    print("\n健康诊断结果:")
    print(f"卦名: {health['gua_name']}")
    print(f"五行: {health['gua_element']}")
    print(f"健康影响: {health['health_impacts']}")
    print(f"调理建议: {health['remedies']}")
    
    print("\n测试成功完成!")
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
