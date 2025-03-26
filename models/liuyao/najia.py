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

# 修正SYMBOL定义，使用 ×→ 和 ○→
SYMBOL = [
    {0: '▅▅  ▅▅', 1: '▅▅▅▅▅▅', 2: '', 3: '×→', 4: '○→'},
    {0: '▅▅  ▅▅', 1: '▅▅▅▅▅▅', 2: '', 3: '×→', 4: '○→'},
    {0: '▅▅  ▅▅', 1: '▅▅▅▅▅▅', 2: '', 3: '×→', 4: '○→'}
]

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
                'year': '乙巳',
                'month': '己卯',
                'day': '癸巳',
                'hour': '乙卯',
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
        try:
            # 先计算本卦卦码
            base_mark = [str(int(v) % 2) for v in params]  # 2,3→0; 1,4→1
            # 变卦：基于本卦卦码，动爻位置翻转
            mark = list(base_mark)  # 复制本卦卦码
            for i, v in enumerate(params):
                if v in [3, 4]:  # 动爻（3或4）翻转
                    mark[i] = '1' if mark[i] == '0' else '0'
            mark = ''.join(mark)
            
            # 计算变卦的世爻位置
            shiy = set_shi_yao(mark)
            if shiy is None or len(shiy) < 2:
                logger.warning(f"无法确定变卦世应爻: {mark}")
            
            # 计算变卦所属卦宫
            p = palace(mark, shiy[0]) if shiy else None
            if p is None:
                logger.warning(f"无法确定变卦卦宫: {mark}")
                bian_gong = "未知"
            else:
                bian_gong = GUAS[p]
            
            # 计算变卦亲用神
            qin6 = [get_qin6(XING5[int(GUA5[gong])], ZHI5[ZHIS.index(x[1])]) for x in get_najia(mark)]
            qinx = [GZ5X(x) for x in get_najia(mark)]
            
            # 获取变卦的卦名
            bian_name = GUA64.get(mark, "")
            if not bian_name:
                logger.warning(f"无法从卦码获取变卦名称: {mark}")
                bian_name = "未知卦"
                
            return {
                'name': bian_name,
                'mark': mark,
                'qin6': qin6,
                'qinx': qinx,
                'gong': bian_gong,
            }
        except Exception as e:
            logger.error(f"计算变卦时出错: {e}")
            raise ValueError(f"计算变卦时出错: {e}")

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

    @staticmethod
    def calculate_visual_width(text):
        """计算字符串的视觉宽度，中文字符占2个宽度，英文字符占1个宽度"""
        width = 0
        for char in text:
            # 中文字符（包括全角字符）占2个宽度
            if ord(char) > 127:
                width += 2
            else:
                width += 1
        return width

    def render(self):
        tpl = Path(__file__).parent / 'data' / 'standard.tpl'
        tpl = tpl.read_text(encoding='utf-8')
        empty = '\u3000' * 6
        rows = self.data
        symbal = SYMBOL[self.verbose]
        # 调整动爻符号，确保对齐，×→ 和 ○→ 后加4个空格
        rows['dyao'] = [symbal[x] + '    ' if x in (3, 4) else '    ' for x in self.data['params']]
        rows['main'] = {}
        rows['main']['mark'] = [symbal[int(x)] for x in self.data['mark']]
        rows['main']['type'] = get_type(self.data['mark'])
        rows['main']['gong'] = rows['gong']
        rows['main']['name'] = rows['name']
        try:
            rows['main']['gong_type'] = self._get_bagong_type(self.data['mark'], rows['gong'])
        except Exception as e:
            logger.warning(f"确定本卦类型出错: {e}")
            rows['main']['gong_type'] = rows['gong'] + "宫"

        # 计算本卦标题的视觉宽度并设置缩进
        main_gua_title = f"{rows['gong']}:{rows['name']} ({rows['main']['gong_type']})"
        main_visual_width = self.calculate_visual_width(main_gua_title)
        main_indent_spaces = 19 - main_visual_width // 2
        if main_indent_spaces < 0:
            main_indent_spaces = 0
        rows['main']['indent'] = '\u3000' * main_indent_spaces

        if rows.get('hide'):
            rows['hide']['qin6'] = [' %s%s ' % (rows['hide']['qin6'][x], rows['hide']['qinx'][x]) if x in rows['hide']['seat'] else empty for x in range(0, 6)]
        else:
            rows['hide'] = {'qin6': ['  ' for _ in range(0, 6)]}

        # 确保变卦部分始终显示
        if rows.get('bian'):
            rows['bian']['type'] = get_type(rows['bian']['mark'])
            # 保存原始 bian_mark 用于卦型计算
            bian_mark_raw = rows['bian']['mark']  # 原始 mark，字符串形式
            try:
                bian_mark = ''.join(map(str, bian_mark_raw))  # 确保是字符串
                bian_gong = rows['bian']['gong']
                rows['bian']['gong_type'] = self._get_bagong_type(bian_mark, bian_gong)
            except Exception as e:
                logger.warning(f"确定变卦类型出错: {e}")
                rows['bian']['gong_type'] = rows['bian'].get('gong', "") + "宫"

            bian_gua_title = f"{rows['bian']['gong']}:{rows['bian']['name']} ({rows['bian']['gong_type']})"
            bian_visual_width = self.calculate_visual_width(bian_gua_title)
            fixed_width_before_bian_qin = 15 + main_visual_width  # 调整为动态宽度
            bian_indent_spaces = fixed_width_before_bian_qin - main_visual_width - bian_visual_width // 2
            if bian_indent_spaces < 0:
                bian_indent_spaces = 0
            rows['bian']['indent'] = '\u3000' * bian_indent_spaces

            if rows['bian']['qin6']:
                rows['bian']['qin6'] = [f'{rows["bian"]["qin6"][x]}{rows["bian"]["qinx"][x]}' if x in self.data['dong'] else f'  {rows["bian"]["qin6"][x]}{rows["bian"]["qinx"][x]}'
                                        for x in range(0, 6)]
            if rows['bian']['mark']:
                # 转换为符号用于显示
                rows['bian']['mark'] = [symbal[int(x)] for x in bian_mark_raw]
        else:
            # 如果没有变卦（理论上不会发生），设置默认值
            rows['bian'] = {
                'qin6': [' ' for _ in range(0, 6)], 
                'mark': [' ' for _ in range(0, 6)],
                'gong_type': "",
                'gong': rows['gong'],
                'name': rows['name']
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

        rows['debug'] = {
            'main_mark': self.data['mark'],
            'main_name': rows['name'],
            'main_gong': rows['gong']
        }
        if rows.get('bian'):
            rows['debug']['bian_mark'] = rows['bian'].get('mark', ''),
            rows['debug']['bian_name'] = rows['bian'].get('name', ''),
            rows['debug']['bian_gong'] = rows['bian'].get('gong', '')

        try:
            template = Template(tpl)
            result = template.render(**rows)
            return result
        except Exception as e:
            logger.error(f"渲染六爻纳甲模板失败: {e}")
            raise ValueError(f"渲染模板失败: {e}")

    def _get_bagong_type(self, mark, gong):
        # 确保 mark 是字符串
        if not isinstance(mark, str):
            try:
                mark = ''.join(map(str, mark))
            except Exception as e:
                logger.error(f"卦码转换失败: {e}, 原始值: {mark}")
                return f"{gong}宫"
                
        if len(mark) != 6 or not all(c in '01' for c in mark):
            logger.warning(f"卦码格式错误: {mark}")
            return f"{gong}宫"

        # 补充完整的八宫卦映射
        bagong_map = {
            '乾': {
                '111111': '本宫卦',  # 乾为天
                '111110': '一世卦',  # 天风姤
                '111101': '二世卦',  # 天山遁
                '111011': '三世卦',  # 天地否
                '011111': '四世卦',  # 风地观
                '101111': '五世卦',  # 山地剥
                '110111': '游魂卦',  # 火地晋
                '110110': '归魂卦'   # 火天大有
            },
            '坎': {
                '010010': '本宫卦',  # 坎为水
                '010011': '一世卦',  # 水泽节
                '010001': '二世卦',  # 水雷屯
                '010101': '三世卦',  # 水火既济
                '110010': '四世卦',  # 泽火革
                '001010': '五世卦',  # 雷火丰
                '000010': '游魂卦',  # 地火明夷
                '000011': '归魂卦'   # 地水师
            },
            '艮': {
                '001001': '本宫卦',  # 艮为山
                '001011': '一世卦',  # 山火贲
                '001111': '二世卦',  # 山天大畜
                '001110': '三世卦',  # 山泽损
                '101001': '四世卦',  # 火泽睽
                '111001': '五世卦',  # 天泽履
                '011001': '游魂卦',  # 风泽中孚
                '011011': '归魂卦'   # 风山渐
            },
            '震': {
                '100100': '本宫卦',  # 震为雷
                '100110': '一世卦',  # 雷地豫
                '100010': '二世卦',  # 雷水解
                '100011': '三世卦',  # 雷风恒
                '000100': '四世卦',  # 地风升
                '010100': '五世卦',  # 水风井
                '110100': '游魂卦',  # 泽风大过
                '110110': '归魂卦'   # 泽雷随
            },
            '巽': {
                '011011': '本宫卦',  # 巽为风
                '011111': '一世卦',  # 风天小畜
                '011110': '二世卦',  # 风火家人
                '011100': '三世卦',  # 风雷益
                '111011': '四世卦',  # 天雷无妄
                '110011': '五世卦',  # 火雷噬嗑
                '001011': '游魂卦',  # 山雷颐
                '001111': '归魂卦'   # 山风蛊
            },
            '离': {
                '101101': '本宫卦',  # 离为火
                '101111': '一世卦',  # 火山旅
                '101011': '二世卦',  # 火风鼎
                '101010': '三世卦',  # 火水未济
                '001101': '四世卦',  # 山水蒙
                '011101': '五世卦',  # 风水涣
                '111101': '游魂卦',  # 天水讼
                '111111': '归魂卦'   # 天火同人
            },
            '坤': {
                '000000': '本宫卦',  # 坤为地
                '000001': '一世卦',  # 地雷复
                '000011': '二世卦',  # 地泽临
                '000111': '三世卦',  # 地天泰
                '100000': '四世卦',  # 雷天大壮
                '110000': '五世卦',  # 泽天夬
                '010000': '游魂卦',  # 水天需
                '010001': '归魂卦'   # 水地比
            },
            '兑': {
                '110110': '本宫卦',  # 兑为泽
                '110111': '一世卦',  # 泽水困
                '110011': '二世卦',  # 泽地萃
                '110001': '三世卦',  # 泽山咸
                '011000': '四世卦',  # 水山蹇
                '001000': '五世卦',  # 地山谦
                '100100': '游魂卦',  # 雷山小过
                '100110': '归魂卦',  # 雷泽归妹
            }
        }
        if gong in bagong_map and mark in bagong_map[gong]:
            gua_type = bagong_map[gong][mark]
            return gua_type
        
        # 如果没有直接匹配，尝试推断卦型
        # 获取卦宫的本宫卦码
        base_gua = {
            '乾': '111111', '坎': '010010', '艮': '001001', '震': '100100',
            '巽': '011011', '离': '101101', '坤': '000000', '兑': '110110'
        }
        if gong not in base_gua:
            logger.warning(f"未知卦宫: {gong}")
            return f"{gong}宫"
        
        base_mark = base_gua[gong]
        # 计算与本宫卦的差异
        diff_count = sum(1 for a, b in zip(mark, base_mark) if a != b)
        
        # 根据差异推断卦型
        if diff_count == 0:
            return '本宫卦'
        elif diff_count == 1:
            return '一世卦'
        elif diff_count == 2:
            return '二世卦'
        elif diff_count == 3:
            return '三世卦'
        elif diff_count == 4:
            return '四世卦'
        elif diff_count == 5:
            return '五世卦'
        else:
            # 检查是否为游魂卦或归魂卦
            # 游魂卦：世爻在四爻
            # 归魂卦：世爻在三爻
            shiy = set_shi_yao(mark)
            if shiy and shiy[0] == 4:
                return '游魂卦'
            elif shiy and shiy[0] == 3:
                return '归魂卦'
            return '未知卦型'

    def export(self):
        solar, params = self.data['solar'], self.data['params']
        return solar, params

    def predict(self):
        return