"""
简化版八字计算示例

不依赖geopy，可以直接运行
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到系统路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入简化版计算器
from models.bazi.calculator_simple import calculate_bazi

def main():
    """主函数"""
    print("=" * 60)
    print("八字计算示例 - 1977年2月25日晚上8点50分出生于北京的男性")
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
    
    print("\n=" * 60)
    print("计算完成!")

if __name__ == "__main__":
    main()
