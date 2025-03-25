        # 参数验证
        if params is None or not isinstance(params, list) or len(params) != 6:
            raise ValueError("六爪参数(params)必须是长度为6的列表，例如[1,2,2,2,2,2]")
            
        for i, p in enumerate(params):
            if not isinstance(p, (int, float)) or p < 1 or p > 4:
                raise ValueError(f"第{i+1}爪参数无效，应为1-4之间的整数: {p}")import sys
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
    # 优先使用八字模块中的干支计算函数
    from models.bazi.calculator import calculate_liunian_ganzhi, calculate_liuyue_ganzhi
    from models.bazi.calculator import calculate_true_solar_time_diff
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
        # 简化版流月干支计算
        Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        # 计算年份的天干
        year_gan_index = (year - 4) % 10
        
        # 根据年份天干和月份确定月干
        base_month_gan_index = (year_gan_index * 2 + month - 1) % 10
        
        # 确定月支（正月-寅月）
        month_zhi_index = (month + 1) % 12
        
        return Gan[base_month_gan_index] + Zhi[month_zhi_index]
    
    def calculate_true_solar_time_diff(longitude, year, month, day):
        """简化版真太阳时差计算"""
        import math
        # 经度校正（粗略计算）
        return longitude / 15 * 60  # 每15度经度1小时（换算成分钟）

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
    def _daily(date=None, longitude=116.4074, latitude=39.9042):
        """
        计算日期的干支信息，支持真太阳时校正
        
        参数:
            date (datetime/str): 日期对象或字符串(格式:'%Y-%m-%d %H:%M')
            longitude (float): 经度，默认北京116.4074
            latitude (float): 纬度，默认北京39.9042
            
        返回:
            dict: 包含年月日时干支和旬空信息的字典
        """
        if date is None:
            date = datetime.datetime.now()
        else:
            date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M') if isinstance(date, str) else date

        year = date.year
        month = date.month
        day = date.day
        hour = date.hour

        # 尝试使用lunar_python库
        try:
            from lunar_python import Solar, Lunar
            
            # 计算真太阳时偏差
            time_diff = calculate_true_solar_time_diff(longitude, year, month, day)
            
            # 调整时间
            adjusted_hour = hour + time_diff / 60  # 转换为小时
            adjusted_day = day
            
            # 处理跨日问题
            if adjusted_hour >= 24:
                adjusted_hour -= 24
                adjusted_day += 1
            elif adjusted_hour < 0:
                adjusted_hour += 24
                adjusted_day -= 1
                
            # 创建调整后的Solar对象
            solar = Solar.fromYmdHms(
                year, 
                month, 
                adjusted_day, 
                int(adjusted_hour), 
                int((adjusted_hour - int(adjusted_hour)) * 60), 
                0
            )
            
            # 获取农历
            lunar = solar.getLunar()
            
            # 八字
            bazi = lunar.getEightChar()
            year_gz = bazi.getYear()
            month_gz = bazi.getMonth()
            day_gz = bazi.getDay()
            hour_gz = bazi.getTime()
            
            # 计算旬空
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
            # 尝试使用bazi模块中其他函数
            try:
                from models.bazi.calculator import calculate_day_gz, calculate_hour_gz, calculate_xunkong
                year_gz = calculate_liunian_ganzhi(year)
                month_gz = calculate_liuyue_ganzhi(year, month)
                day_gz = calculate_day_gz(year, month, day)
                hour_gz = calculate_hour_gz(day_gz, hour)
                xkong = calculate_xunkong(day_gz)
            except (ImportError, ModuleNotFoundError):
                # 使用简化计算
                logger.warning("无法导入lunar_python和bazi模块，使用简化计算")
                year_gz = calculate_liunian_ganzhi(year)
                month_gz = calculate_liuyue_ganzhi(year, month)
                
                # 简化日干支计算 - 使用五虎遁日诀近似计算
                def simple_day_gz(year, month, day):
                    # 这是极简版本，实际需要精确计算
                    month_gan = month_gz[0]
                    gan_base = {"甲": 0, "己": 5, "乙": 2, "庚": 7, "丙": 4, "辛": 9, "丁": 6, "壬": 1, "戊": 8, "癸": 3}
                    gan_idx = (gan_base.get(month_gan, 0) + day - 1) % 10
                    zhi_idx = (day + 1) % 12  # 简化计算，不精确
                    return GANS[gan_idx] + ZHIS[zhi_idx]
                
                # 简化时干支计算
                def simple_hour_gz(day_gz, hour):
                    # 根据日干五虎遁时计算
                    day_gan = day_gz[0]
                    gan_offset = {"甲": 0, "己": 5, "乙": 2, "庚": 7, "丙": 4, "辛": 9, "丁": 6, "壬": 1, "戊": 8, "癸": 3}
                    # 时辰转换
                    zhi_hour = hour // 2
                    if zhi_hour >= 12:  # 处理午夜12点
                        zhi_hour = 0
                    gan_idx = (gan_offset.get(day_gan, 0) + zhi_hour) % 10
                    return GANS[gan_idx] + ZHIS[zhi_hour]
                
                # 简化旬空计算
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
                
                # 计算各项干支
                day_gz = simple_day_gz(year, month, day)
                hour_gz = simple_hour_gz(day_gz, hour)
                xkong = simple_xunkong(day_gz)
                
        # 计算调整后的真太阳时时间
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

    def compile(self, params=None, gender=None, date=None, title=None, guaci=False, longitude=116.4074, latitude=39.9042, **kwargs):
        """
        根据参数编译卦
        
        参数:
            params (list): 六爪参数，例如[1,2,2,2,2,2]
            gender (str): 性别，'male'或'female'
            date (datetime/str): 日期对象或字符串
            title (str): 标题
            guaci (bool): 是否显示卦词
            longitude (float): 经度，默认北京116.4074
            latitude (float): 纬度，默认北京39.9042
            
        返回:
            Najia: 当前实例，支持链式调用
            
        异常:
            ValueError: 当参数无效或不完整时
        """
        title = title or ''
        solar = datetime.datetime.now() if date is None else date
        
        # 传递经纬度参数
        lunar = self._daily(solar, longitude, latitude)

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