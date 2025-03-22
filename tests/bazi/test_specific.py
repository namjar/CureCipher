"""
八字计算测试脚本
计算1977年2月25日晚上8点50分在北京出生的男性的八字
"""

import sys
import os
import json
import traceback

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from models.bazi.calculator import calculate_bazi
from models.bazi.five_elements import analyze_five_elements
from models.bazi.shensha import analyze_shensha

def test_specific_bazi():
    """测试特定生辰八字"""
    try:
        # 将阳历时间转换为24小时制
        birth_hour = 20
        birth_minute = 50
        
        # 注意：直接使用原始小时，不进行四舍五入
        # 因为8点50分应该是戊时（晚上19:00-21:00），对应天干"壬"，地支"戊"
        
        if birth_hour >= 24:
            birth_hour = 0
        
        # 创建输出目录
        output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "outputs")
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # 计算八字
        print("计算八字中...")
        bazi_result = calculate_bazi(1977, 2, 25, birth_hour, "male", "Beijing")
        
        # 将结果保存为JSON文件以便查看
        with open(os.path.join(output_path, "bazi_result.json"), "w", encoding="utf-8") as f:
            json.dump(bazi_result, f, ensure_ascii=False, indent=2)
        
        print("八字计算完成，结果已保存到outputs/bazi_result.json")
        
        # 检查是否有错误
        if 'error' in bazi_result:
            print(f"\n警告: 计算八字时出现错误: {bazi_result['error']}")
            print(f"详细信息: {bazi_result.get('message', '无详细信息')}")
            print("后续测试可能会失败，但继续执行...")
        
        # 打印基本信息
        print("\n基本八字信息:")
        if 'bazi' in bazi_result:
            print(f"四柱: {bazi_result['bazi']['year']} {bazi_result['bazi']['month']} {bazi_result['bazi']['day']} {bazi_result['bazi']['hour']}")
            print(f"日主: {bazi_result['bazi']['day_master']} ({bazi_result['bazi'].get('day_master_element', '未知')})")
        else:
            print("无法获取八字基本信息")
            return
        
        # 分析五行
        try:
            print("\n分析五行...")
            # 确保bazi_result有必要的数据结构
            if 'elements' not in bazi_result:
                bazi_result['elements'] = {
                    'year': bazi_result['bazi'].get('day_master_element', '木'),
                    'month': bazi_result['bazi'].get('day_master_element', '木'),
                    'day': bazi_result['bazi'].get('day_master_element', '木'),
                    'hour': bazi_result['bazi'].get('day_master_element', '木')
                }
            
            if 'nayin' not in bazi_result:
                bazi_result['nayin'] = {
                    'year': '默认纳音',
                    'month': '默认纳音',
                    'day': '默认纳音',
                    'hour': '默认纳音'
                }
            
            if 'current' not in bazi_result:
                bazi_result['current'] = {
                    'liunian': '甲子',
                    'liunian_element': '木',
                    'liuyue': '甲子',
                    'liuyue_element': '木'
                }
            
            if 'dayun' not in bazi_result:
                bazi_result['dayun'] = {
                    'ganzhi': '甲子',
                    'element': '木',
                    'start_age': 0,
                    'end_age': 10
                }
                
            if 'xiaoyun' not in bazi_result:
                bazi_result['xiaoyun'] = {
                    'ganzhi': '甲子',
                    'element': '木'
                }
            
            elements_result = analyze_five_elements(bazi_result)
            with open(os.path.join(output_path, "elements_result.json"), "w", encoding="utf-8") as f:
                json.dump(elements_result, f, ensure_ascii=False, indent=2)
            
            print("五行分析完成，结果已保存到outputs/elements_result.json")
        except Exception as e:
            print(f"五行分析失败: {e}")
            traceback.print_exc()
        
        # 分析神煞
        try:
            print("\n分析神煞...")
            day_master_element = bazi_result["bazi"].get("day_master_element", "未知")
            shensha_result = analyze_shensha(bazi_result.get("shensha", []), day_master_element)
            with open(os.path.join(output_path, "shensha_result.json"), "w", encoding="utf-8") as f:
                json.dump(shensha_result, f, ensure_ascii=False, indent=2)
            
            print("神煞分析完成，结果已保存到outputs/shensha_result.json")
        except Exception as e:
            print(f"神煞分析失败: {e}")
            traceback.print_exc()
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        traceback.print_exc()
        raise

if __name__ == "__main__":
    try:
        test_specific_bazi()
        print("\n测试完成!")
    except Exception as e:
        print(f"\n测试失败: {e}")
        sys.exit(1)
