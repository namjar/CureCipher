import sys
import os
from pathlib import Path
import datetime

# 确保项目根目录在 sys.path 中
project_root = str(Path(__file__).resolve().parent)  # CureCipher 根目录
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 测试 Najia 类是否正常工作
from models.liuyaonajia.najia import Najia
from models.liuyaonajia.diagnosis import diagnose_health

def main():
    # 创建参数
    params = [2, 2, 1, 2, 4, 2]
    date = datetime.datetime.now()
    
    print("测试 Najia 类")
    najia = Najia(verbose=2)
    najia_result = najia.compile(params=params, date=date)
    render_result = najia_result.render()
    print(render_result)
    
    print("\n测试 diagnose_health 函数")
    health_result = diagnose_health(params=params, date=date)
    print(f"卦名：{health_result['gua_name']}")
    print(f"五行：{health_result['gua_element']}")
    print(f"健康影响：{health_result['health_impacts']}")
    print(f"调理建议：{health_result['remedies']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
