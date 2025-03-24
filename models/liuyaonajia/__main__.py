import random
import sys
import datetime
from pathlib import Path

# 确保项目根目录在 sys.path 中
project_root = str(Path(__file__).resolve().parents[2])  # 指向 CureCipher 根目录
print(f"Adding to sys.path: {project_root}")
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 打印 sys.path 调试
print("sys.path:")
for p in sys.path:
    print(f"  {p}")

try:
    import click
    from models.liuyaonajia import __version__
    from models.liuyaonajia.najia import Najia
    from models.liuyaonajia.diagnosis import diagnose_health
except ImportError as e:
    print(f"Import error: {e}")
    # 基本功能版本，没有click
    if "click" in str(e):
        print("Click module not found. Running basic version.")
        click = None
        from models.liuyaonajia import __version__
        from models.liuyaonajia.najia import Najia
        from models.liuyaonajia.diagnosis import diagnose_health

# 主函数
def run_najia(params=None, gender=None, date=None, title=None, guaci=False, verbose=0):
    # 默认值处理
    params = [random.randint(1, 4) for _ in range(0, 6)] if params is None else params
    params = [int(x) for x in params.replace(',', '')] if isinstance(params, str) else params
    params = [int(str(x).replace('0', '4')) for x in params]

    date = datetime.datetime.now() if date is None else date
    if isinstance(date, str):
        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
        except ValueError:
            print("Date format error, using current time")
            date = datetime.datetime.now()

    # 六爻排盘
    gua = Najia(verbose).compile(params=params, gender=gender, date=date, title=title, guaci=guaci)
    res = gua.render()
    print("卦象：")
    print(res)

    # 健康诊断
    health_result = diagnose_health(params=params, date=date, gender=gender, day_master_strength="neutral")
    print("\n健康分析：")
    print(f"卦名：{health_result['gua_name']}")
    print(f"五行：{health_result['gua_element']}")
    print(f"健康影响：{health_result['health_impacts']}")
    print(f"调理建议：{health_result['remedies']}")
    print(f"六神影响：{health_result['god6_impacts']}")

    return 0

# 判断是否有click
if 'click' in globals() and click is not None:
    @click.command()
    @click.help_option('-h', '--help')
    @click.version_option(__version__, '-V', '--version', prog_name='liuyaonajia', message='%(prog)s: v%(version)s')
    @click.option('-v', '--verbose', count=True, help='卦爻样式')
    @click.option('-p', '--params', default=None, help='摇卦参数')
    @click.option('-g', '--gender', default='', help='摇卦人性别')
    @click.option('-t', '--title', default='', help='求卦问卜事情')
    @click.option('-c', '--guaci', is_flag=True, help='是否显示卦辞')
    @click.option('-d', '--date', default=None, help='日期 YYYY-MM-DD hh:mm')
    def main(params, gender, date, title, guaci, verbose):
        return run_najia(params, gender, date, title, guaci, verbose)

    if __name__ == "__main__":
        sys.exit(main())
else:
    # 简单版本，无click依赖
    if __name__ == "__main__":
        print("Running basic version without click")
        sys.exit(run_najia())