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
    from models.bazi.calculator import calculate_true_solar_time_diff
except ImportError:
    def calculate_liunian_ganzhi(year):
        Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        gan_idx = (year - 4) % 10
        zhi_idx = (year - 4) % 12
        return Gan[gan_idx] + Zhi[zhi_idx]
    
    def calculate_liuyue_ganzhi(year, month):
        Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        year_gan_index = (year - 4) % 10
        base_month_gan_index = (year_gan_index * 2 + month - 1) % 10
        month_zhi_index = (month + 1) % 12
        return Gan[base_month_gan_index] + Zhi[month_zhi_index]
    
    def calculate_true_solar_time_diff(longitude, year, month, day):
        import math
        return longitude / 15 * 60

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

class Najia(object):
    def __init__(self, verbose=None):
        self.verbose = (verbose, 2)[verbose > 2] or 0
        self.bian = None
        self.hide = None
        self.data = None

    @staticmethod
    def _gz(gan, zhi):
        return GANS[gan] + ZHIS[zhi]

    @staticmethod
    def _daily(date=None, longitude=116.4074, latitude=39.9042):
        if date is None:
            date = datetime.datetime.now()
        else:
            date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M') if isinstance(date, str) else date

        year = date.year
        month = date.month
        day = date.day
        hour = date.hour

        try:
            from lunar_python import Solar, Lunar
            time_diff = calculate_true_solar_time_diff(longitude, year, month, day)
            adjusted_hour = hour + time_diff / 60
            adjusted_day = day
            if adjusted_hour >= 24:
                adjusted_hour -= 24
                adjusted_day += 1
            elif adjusted_hour < 0:
                adjusted_hour += 24
                adjusted_day -= 1
            solar = Solar.fromYmdHms(year, month, adjusted_day, int(adjusted_hour), int((adjusted_hour - int(adjusted_hour)) * 60), 0)
            lunar = solar.getLunar()
            bazi = lunar.getEightChar()
            year_gz = bazi.getYear()
            month_gz = bazi.getMonth()
            day_gz = bazi.getDay()
            hour_gz = bazi.getTime()
            day_gan = day_gz[0]
            day_zhi = day_gz[1:]
            gan_idx = GANS.index(day_gan)
            zhi_idx = ZHIS.index(day_zhi)
            if zhi_idx < gan_idx:
                zhi_idx += 12
            xk_idx = (zhi_idx - gan_idx) // 2
            xk_start = (xk_idx * 2 + 10) % 12
            xkong = ZHIS[xk_start] + ZHIS[(xk_start + 1) % 12]
        except (ImportError, ModuleNotFoundError):
            try:
                from models.bazi.calculator import calculate_day_gz, calculate_hour_gz, calculate_xunkong
                year_gz = calculate_liunian_ganzhi(year)
                month_gz = calculate_liuyue_ganzhi(year, month)
                day_gz = calculate_day_gz(year, month, day)
                hour_gz = calculate_hour_gz(day_gz, hour)
                xkong = calculate_xunkong(day_gz)
            except (ImportError, ModuleNotFoundError):
                logger.warning("无法导入lunar_python和bazi模块，使用简化计算")
                year_gz = calculate_liunian_ganzhi(year)
                month_gz = calculate_liuyue_ganzhi(year, month)
                def simple_day_gz(year, month, day):
                    month_gan = month_gz[0]
                    gan_base = {"甲": 0, "己": 5, "乙": 2, "庚": 7, "丙": 4, "辛": 9, "丁": 6, "壬": 1, "戊": 8, "癸": 3}
                    gan_idx = (gan_base.get(month_gan, 0) + day - 1) % 10
                    zhi_idx = (day + 1) % 12
                    return GANS[gan_idx] + ZHIS[zhi_idx]
                def simple_hour_gz(day_gz, hour):
                    day_gan = day_gz[0]
                    gan_offset = {"甲": 0, "己": 5, "乙": 2, "庚": 7, "丙": 4, "辛": 9, "丁": 6, "壬": 1, "戊": 8, "癸": 3}
                    zhi_hour = hour // 2
                    if zhi_hour >= 12:
                        zhi_hour = 0
                    gan_idx = (gan_offset.get(day_gan, 0) + zhi_hour) % 10
                    return GANS[gan_idx] + ZHIS[zhi_hour]
                def simple_xunkong(day_gz):
                    day_gan = day_gz[0]
                    day_zhi = day_gz[1:]
                    gan_idx = GANS.index(day_gan)
                    zhi_idx = ZHIS.index(day_zhi)
                    if zhi_idx < gan_idx:
                        zhi_idx += 12
                    xk_idx = (zhi_idx - gan_idx) // 2
                    xk_start = (xk_idx * 2 + 10) % 12
                    return ZHIS[xk_start] + ZHIS[(xk_start + 1) % 12]
                day_gz = simple_day_gz(year, month, day)
                hour_gz = simple_hour_gz(day_gz, hour)
                xkong = simple_xunkong(day_gz)

        adj_info = f"{hour:02d}:00"
        try:
            time_diff = calculate_true_solar_time_diff(longitude, year, month, day)
            adj_hour = hour + time_diff / 60
            adj_hour_int = int(adj_hour)
            adj_min = int((adj_hour - adj_hour_int) * 60)
            adj_info = f"{adj_hour_int:02d}:{adj_min:02d} (校正{time_diff:.1f}分)"
        except Exception as e:
            logger.warning(f"计算真太阳时失败: {e}")

        result = {
            'xkong': xkong,
            'gz': {
                'year': year_gz,
                'month': month_gz,
                'day': day_gz,
                'hour': hour_gz,
            },
            'true_solar': adj_info
        }
        return result

    @staticmethod
    def _hidden(gong=None, qins=None):
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

    def compile(self, params=None, gender=None, date=None, title=None, guaci=False, longitude=116.4074, latitude=39.9042, **kwargs):
        if params is None or not isinstance(params, list) or len(params) != 6:
            raise ValueError("六爻参数(params)必须是长度为6的列表，例如[1,2,2,2,2,2]")
        for i, p in enumerate(params):
            if not isinstance(p, (int, float)) or p < 1 or p > 4:
                raise ValueError(f"第{i+1}爻参数无效，应为1-4之间的整数: {p}")
        title = title or ''
        solar = datetime.datetime.now() if date is None else date
        lunar = self._daily(solar, longitude, latitude)
        gender = '' if gender is None else gender
        mark = ''.join([str(int(p) % 2) for p in params])
        try:
            shiy = set_shi_yao(mark)
            if shiy is None or len(shiy) < 2:
                raise ValueError(f"无法确定世应爻: {mark}")
            gong = palace(mark, shiy[0])
            if gong is None:
                raise ValueError(f"无法确定卦宫: {mark}")
            name = GUA64.get(mark)
            if name is None:
                raise ValueError(f"无效的卦码: {mark}")
            qin6 = [get_qin6(XING5[int(GUA5[gong])], ZHI5[ZHIS.index(x[1])]) for x in get_najia(mark)]
            qinx = [GZ5X(x) for x in get_najia(mark)]
            god6 = get_god6(lunar['gz']['day'])
            dong = [i for i, x in enumerate(params) if x > 2]
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
        except Exception as e:
            logger.error(f"编译卦象时出错: {e}")
            raise ValueError(f"编译卦象时出错: {e}")

    def render(self):
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
        try:
            rows['main']['gong_type'] = self._get_bagong_type(self.data['mark'], rows['gong'])
            logger.info(f"本卦类型: {rows['main']['gong_type']}")
        except Exception as e:
            logger.warning(f"确定本卦类型出错: {e}")
            rows['main']['gong_type'] = rows['gong'] + "宫"

        # 动态计算缩进，确保“兑”与六亲对齐
        # 六神（白虎）占2个字符，空格2个，六亲（兄弟癸酉金）占5个字符，总共9个字符
        main_gua_title = f"{rows['gong']}:{rows['name']} ({rows['main']['gong_type']})"
        main_indent_spaces = 15 - len(main_gua_title) // 2  # 每个中文字符占2个宽度
        if main_indent_spaces < 0:
            main_indent_spaces = 0
        rows['main']['indent'] = '\u3000' * main_indent_spaces

        if rows.get('hide'):
            rows['hide']['qin6'] = [' %s%s ' % (rows['hide']['qin6'][x], rows['hide']['qinx'][x]) if x in rows['hide']['seat'] else empty for x in range(0, 6)]
        else:
            rows['hide'] = {'qin6': ['  ' for _ in range(0, 6)]}

        if rows.get('bian'):
            rows['bian']['type'] = get_type(rows['bian']['mark'])
            try:
                rows['bian']['gong_type'] = self._get_bagong_type(self.data['mark'], rows['gong'])
                logger.info(f"变卦类型: {rows['bian']['gong_type']}")
            except Exception as e:
                logger.warning(f"确定变卦类型出错: {e}")
                rows['bian']['gong_type'] = rows['bian'].get('gong', "") + "宫"

            # 变卦缩进
            bian_gua_title = f"{rows['bian']['gong']}:{rows['bian']['name']} ({rows['bian']['gong_type']})"
            # 变卦六亲前的固定宽度：六神2 + 空格2 + 六亲5 + 空格2 + 爻位5 + 空格2 = 18
            fixed_width_before_bian_qin = 8
            bian_indent_spaces = fixed_width_before_bian_qin - len(bian_gua_title) // 2
            if bian_indent_spaces < 0:
                bian_indent_spaces = 0
            rows['bian']['indent'] = '\u3000' * bian_indent_spaces

            if rows['bian']['qin6']:
                rows['bian']['qin6'] = [f'{rows["bian"]["qin6"][x]}{rows["bian"]["qinx"][x]}' if x in self.data['dong'] else f'  {rows["bian"]["qin6"][x]}{rows["bian"]["qinx"][x]}'
                                        for x in range(0, 6)]
            if rows['bian']['mark']:
                rows['bian']['mark'] = [symbal[int(x)] for x in rows['bian']['mark']]
        else:
            rows['bian'] = {
                'qin6': [' ' for _ in range(0, 6)], 
                'mark': [' ' for _ in range(0, 6)],
                'gong_type': ""
            }

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

        if 'lunar' in rows and 'true_solar' in rows['lunar']:
            pass
        else:
            if 'lunar' not in rows:
                rows['lunar'] = {}
            rows['lunar']['true_solar'] = rows.get('true_solar', '')

        # 移除调试信息，但仍生成debug字段以防后续需要
        rows['debug'] = {
            'main_mark': self.data['mark'],
            'main_name': rows['name'],
            'main_gong': rows['gong']
        }
        if rows.get('bian'):
            rows['debug']['bian_mark'] = rows['bian'].get('mark', '')
            rows['debug']['bian_name'] = rows['bian'].get('name', '')
            rows['debug']['bian_gong'] = rows['bian'].get('gong', '')

        template = Template(tpl)
        return template.render(**rows)

    def _get_bagong_type(self, mark, gong):
        if isinstance(mark, str) and (len(mark) == 6) and all(c in '01' for c in mark):
            pass
        else:
            try:
                if not isinstance(mark, str) and len(mark) == 6:
                    mark = ''.join(['1' if int(x) % 2 == 1 else '0' for x in mark])
                elif len(mark) != 6 or not all(c in '01' for c in mark):
                    return f"{gong}宫"
            except Exception as e:
                logger.warning(f"卦码格式错误: {mark}, {e}")
                return f"{gong}宫"
        
        bagong_map = {
            '乾': {
                '111111': '本宫卦', '111100': '一世卦', '111010': '二世卦', '111001': '三世卦',
                '001111': '四世卦', '010111': '五世卦', '101111': '游魂卦', '101100': '归魂卦'
            },
            '坎': {
                '010010': '本宫卦', '010011': '一世卦', '010001': '二世卦', '010101': '三世卦',
                '110010': '四世卦', '100010': '五世卦', '000010': '游魂卦', '000011': '归魂卦'
            },
            '艮': {
                '001001': '本宫卦', '001101': '一世卦', '001111': '二世卦', '001011': '三世卦',
                '101001': '四世卦', '111001': '五世卦', '011001': '游魂卦', '011101': '归魂卦'
            },
            '震': {
                '100100': '本宫卦', '100000': '一世卦', '100010': '二世卦', '100011': '三世卦',
                '000100': '四世卦', '010100': '五世卦', '011100': '游魂卦', '011000': '归魂卦'
            },
            '巽': {
                '011011': '本宫卦', '011111': '一世卦', '011101': '二世卦', '011100': '三世卦',
                '111011': '四世卦', '101011': '五世卦', '001011': '游魂卦', '001111': '归魂卦'
            },
            '离': {
                '101101': '本宫卦', '101001': '一世卦', '101011': '二世卦', '101010': '三世卦',
                '001101': '四世卦', '011101': '五世卦', '111101': '游魂卦', '111001': '归魂卦'
            },
            '坤': {
                '000000': '本宫卦', '000100': '一世卦', '000011': '二世卦', '000111': '三世卦',
                '100000': '四世卦', '011000': '五世卦', '010000': '游魂卦', '010100': '归魂卦'
            },
            '兑': {
                '110110': '本宫卦', '110010': '一世卦', '110000': '二世卦', '110001': '三世卦',
                '010110': '四世卦', '001000': '五世卦', '100110': '游魂卦', '100010': '归魂卦'
            }
        }
        if gong in bagong_map and mark in bagong_map[gong]:
            return bagong_map[gong][mark]
        return f"{gong}宫"

    def export(self):
        solar, params = self.data['solar'], self.data['params']
        return solar, params

    def predict(self):
        return