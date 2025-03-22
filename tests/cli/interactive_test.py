# /Users/ericw/Documents/GitHub/CureCipher/tests/cli/interactive_test.py
"""
交互式测试工具
"""
import sys
import os
import textwrap

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from models.bazi.bazi_calculator import calculate_bazi, generate_bazi_report

def format_text(text, width=80):
    """格式化文本输出"""
    return "\n".join(textwrap.wrap(text, width))

def interactive_test():
    """交互式测试工具"""
    print("\n" + "="*60)
    print(" "*20 + "八字排盘测试工具")
    print("="*60 + "\n")
    
    while True:
        try:
            print("\n请输入出生信息:")
            year = int(input("出生年份(如1990): "))
            month = int(input("出生月份(1-12): "))
            day = int(input("出生日期(1-31): "))
            hour = int(input("出生时辰(0-23): "))
            gender = input("性别(male/female): ")
            city = input("出生城市(可选): ") or None
            
            print("\n正在计算...")
            bazi_result = calculate_bazi(year, month, day, hour, gender, city)
            
            if "error" in bazi_result:
                print(f"\n计算出错: {bazi_result['message']}")
                continue
                
            report = generate_bazi_report(bazi_result)
            
            print("\n" + "="*60)
            print(" "*20 + "八字命盘解读结果")
            print("="*60 + "\n")
            
            print(report["text_report"])
            
            print("\n" + "="*60)
            again = input("\n是否继续测试?(y/n): ")
            if again.lower() != 'y':
                break
        except KeyboardInterrupt:
            print("\n\n已退出测试")
            break
        except Exception as e:
            print(f"\n发生错误: {str(e)}")
            again = input("\n是否继续测试?(y/n): ")
            if again.lower() != 'y':
                break

if __name__ == "__main__":
    interactive_test()