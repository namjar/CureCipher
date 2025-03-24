import sys
import json
import logging
import os
from pathlib import Path
import datetime
from jinja2 import Template

# 导入路径处理
sys_path = str(Path(__file__).resolve().parents[2])  # 指向项目根目录
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)

from .const import GANS
from .const import GUA5
from .const import GUA64
from .const import GUAS
from .const import SYMBOL
from .const import XING5
from .const import YAOS
from .const import ZHI5
from .const import ZHIS
from .utils import get_god6
from .utils import get_guaci
from .utils import get_najia
from .utils import get_qin6
from .utils import get_type
from .utils import GZ5X
from .utils import palace
from .utils import set_shi_yao

# 绝对导入替代相对导入
try:
    from models.bazi.calculator import calculate_liunian_ganzhi, calculate_liuyue_ganzhi
except ImportError:
    # 提供一个备用实现
    def calculate_liunian_ganzhi(year):
        """简化版流年干支计算"""
        Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        gan_idx = (year - 4) % 10
        zhi_idx = (year - 4) % 12
        return Gan[gan_idx] + Zhi[zhi_idx]
    
    def calculate_liuyue_ganzhi(year, month):
        """简化版流月干支计算"""
        return "甲子"  # 简单返回一个默认值

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

class Najia(object):
    def __init__(self, verbose=None):
        self.verbose = (verbose, 2)[verbose > 2] or 0
        self.bian = None  # 变卦
        self.hide = None  # 伏神
        self.data = None

    @staticmethod
    def _gz(gan, zhi):
        """获取干支"""
        return GANS[gan] + ZHIS[zhi]

    @staticmethod
    def _daily(date=None):
        """计算日期"""
        if date is None:
            date = datetime.datetime.now()
        else:
            date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M') if isinstance(date, str) else date

        year = date.year
        month = date.month
        day = date.day
        hour = date.hour

        # 使用 /bazi/calculator.py 的函数计算干支
        year_gz = calculate_liunian_ganzhi(year)
        month_gz = calculate_liuyue_ganzhi(year, month)
        # 日干支和时干支简化处理，实际需更精确计算
        day_gz = calculate_liunian_ganzhi(year)  # 占位，需补充日干支逻辑
        hour_gz = "未知"  # 占位，需补充时干支逻辑

        result = {
            'xkong': '未知',  # 旬空待补充
            'gz': {
                'year': year_gz,
                'month': month_gz,
                'day': day_gz,
                'hour': hour_gz,
            }
        }
        return result

    @staticmethod
    def _hidden(gong=None, qins=None):
        """计算伏神卦"""
        if gong is None or qins is None:
            raise Exception('参数缺失')

        if len(set(qins)) < 5:
            mark = YAOS[gong] * 2
            qin6 = [get_qin6(XING5[int(GUA5[gong])], ZHI5[ZHIS.index(x[1])]) for x in get_najia(mark)]
            qinx = [GZ5X(x) for x in get_najia(mark)]
            seat = [qin6.index(x) for x in list(set(qin6).difference(set(qins)))]
            return {
                'name': GUA64.get(mark),
                'mark': mark,
                'qin6': qin6,
                'qinx': qinx,
                'seat': seat,
            }
        return None

    @staticmethod
    def _transform(params=None, gong=None):
        """计算变卦"""
        if params is None or len(params) < 6:
            raise Exception('参数缺失')

        if 3 in params or 4 in params:
            mark = ''.join(['1' if v in [1, 4] else '0' for v in params])
            qin6 = [get_qin6(XING5[int(GUA5[gong])], ZHI5[ZHIS.index(x[1])]) for x in get_najia(mark)]
            qinx = [GZ5X(x) for x in get_najia(mark)]
            return {
                'name': GUA64.get(mark),
                'mark': mark,
                'qin6': qin6,
                'qinx': qinx,
                'gong': GUAS[palace(mark, set_shi_yao(mark)[0])],
            }
        return None

    def compile(self, params=None, gender=None, date=None, title=None, guaci=False, **kwargs):
        """根据参数编译卦"""
        title = title or ''
        solar = datetime.datetime.now() if date is None else date
        lunar = self._daily(solar)

        gender = '' if gender is None else gender

        # 卦码
        mark = ''.join([str(int(p) % 2) for p in params])
        shiy = set_shi_yao(mark)  # 世应爻
        gong = palace(mark, shiy[0])  # 卦宫
        name = GUA64[mark]  # 卦名
        qin6 = [get_qin6(XING5[int(GUA5[gong])], ZHI5[ZHIS.index(x[1])]) for x in get_najia(mark)]
        qinx = [GZ5X(x) for x in get_najia(mark)]
        god6 = get_god6(lunar['gz']['day'])  # 六神
        dong = [i for i, x in enumerate(params) if x > 2]  # 动爻位置

        # 伏神和变卦
        hide = self._hidden(gong, qin6)
        bian = self._transform(params=params, gong=gong)

        self.data = {
            'params': params,
            'gender': gender,
            'title': title,
            'guaci': guaci,
            'solar': solar,
            'lunar': lunar,
            'god6': god6,
            'dong': dong,
            'name': name,
            'mark': mark,
            'gong': GUAS[gong],
            'shiy': shiy,
            'qin6': qin6,
            'qinx': qinx,
            'bian': bian,
            'hide': hide,
        }
        return self

    def render(self):
        """渲染卦象"""
        tpl = Path(__file__).parent / 'data' / 'standard.tpl'
        tpl = tpl.read_text(encoding='utf-8')

        empty = '\u3000' * 6
        rows = self.data
        symbal = SYMBOL[self.verbose]

        rows['dyao'] = [symbal[x] if x in (3, 4) else '' for x in self.data['params']]
        rows['main'] = {}
        rows['main']['mark'] = [symbal[int(x)] for x in self.data['mark']]
        rows['main']['type'] = get_type(self.data['mark'])
        rows['main']['gong'] = rows['gong']
        rows['main']['name'] = rows['name']
        rows['main']['indent'] = '\u3000' * 2

        if rows.get('hide'):
            rows['hide']['qin6'] = [' %s%s ' % (rows['hide']['qin6'][x], rows['hide']['qinx'][x]) if x in rows['hide']['seat'] else empty for x in range(0, 6)]
            rows['main']['indent'] += empty
        else:
            rows['main']['indent'] += '\u3000' * 1
            rows['hide'] = {'qin6': ['  ' for _ in range(0, 6)]}

        rows['main']['display'] = '{indent}{name} ({gong}-{type})'.format(**rows['main'])

        if rows.get('bian'):
            hide = (8, 19)[bool(rows.get('hide'))]
            rows['bian']['type'] = get_type(rows['bian']['mark'])
            rows['bian']['indent'] = (hide - len(rows['main']['display'])) * '\u3000'
            if rows['bian']['qin6']:
                rows['bian']['qin6'] = [f'{rows["bian"]["qin6"][x]}{rows["bian"]["qinx"][x]}' if x in self.data['dong'] else f'  {rows["bian"]["qin6"][x]}{rows["bian"]["qinx"][x]}'
                                        for x in range(0, 6)]
            if rows['bian']['mark']:
                rows['bian']['mark'] = [symbal[int(rows['bian']['mark'][x])] for x in range(0, 6)]
        else:
            rows['bian'] = {'qin6': [' ' for _ in range(0, 6)], 'mark': [' ' for _ in range(0, 6)]}

        shiy = []
        for x in range(0, 6):
            if x == self.data['shiy'][0] - 1:
                shiy.append('世')
            elif x == self.data['shiy'][1] - 1:
                shiy.append('应')
            else:
                shiy.append('  ')
        rows['shiy'] = shiy

        if self.data['guaci']:
            rows['guaci'] = get_guaci(rows['name'])

        template = Template(tpl)
        return template.render(**rows)

    def export(self):
        solar, params = self.data['solar'], self.data['params']
        return solar, params

    def predict(self):
        return