"""
扩展lunar_python库的功能，添加八字大运、命宫、胎元计算等功能
"""

from lunar_python import Solar, Lunar

# 因为lunar_python库中没有Gan和Zhi，我们需要自己定义
Gan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
Zhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

class LunarExtension:
    """扩展Lunar类的功能"""
    
    def __init__(self, lunar=None, solar=None, year=None, month=None, day=None, hour=None):
        """
        初始化，可以通过以下方式：
        1. 直接传入lunar对象
        2. 传入solar对象
        3. 传入年月日时(公历)
        """
        if lunar:
            self.lunar = lunar
        elif solar:
            self.lunar = solar.getLunar()
        elif year and month and day:
            # 默认小时为0
            hour = hour if hour is not None else 0
            solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
            self.lunar = solar.getLunar()
        else:
            raise ValueError("必须提供lunar对象、solar对象或年月日时")
            
        self.bazi = self.lunar.getEightChar()
        
    def get_day_un(self, gender_code=1):
        """
        计算大运
        
        参数:
            gender_code (int): 1代表男，0代表女
        
        返回:
            list: 大运列表
        """
        # 获取月支
        month_zhi = self.bazi.getMonthZhi()
        # 获取年干
        year_gan = self.bazi.getYearGan()
        
        # 男阳女阴顺推，男阴女阳逆推
        month_zhi_index = Zhi.index(month_zhi)
        year_gan_index = Gan.index(year_gan)
        
        # 判断顺逆
        is_forward = True
        if gender_code == 1:  # 男
            is_forward = year_gan_index % 2 == 0  # 阳干顺推
        else:  # 女
            is_forward = year_gan_index % 2 == 1  # 阴干顺推
            
        # 计算大运开始年龄
        start_age = self._calculate_start_age()
        
        # 生成大运列表
        day_un_list = []
        gan_index = Gan.index(self.bazi.getMonthGan())
        zhi_index = month_zhi_index
        
        for i in range(8):  # 生成8个大运
            # 计算干支索引
            if is_forward:
                gan_index = (gan_index + 1) % 10
                zhi_index = (zhi_index + 1) % 12
            else:
                gan_index = (gan_index - 1) % 10
                zhi_index = (zhi_index - 1) % 12
                
            # 干支
            gan = Gan[gan_index]
            zhi = Zhi[zhi_index]
            
            # 开始年龄
            start_age_i = start_age + i * 10
            
            # 结束年龄
            end_age = start_age_i + 10
            
            # 添加到列表
            day_un_list.append({
                "gan_zhi": gan + zhi,
                "start_age": start_age_i,
                "end_age": end_age - 1,
                "is_current": False
            })
            
        return day_un_list
    
    def _calculate_start_age(self):
        """
        计算大运起运年龄
        
        返回:
            int: 起运年龄
        """
        # 具体年龄计算略复杂，这里简化处理
        # 真实计算需要考虑出生时辰、节气等因素
        # 标准算法: 计算出生日期到下一个节气的天数，然后每3天为1岁
        
        # 获取农历月
        lunar_month = self.lunar.getMonth()
        
        # 获取出生时辰
        hour = self.lunar.getHour()
        
        # 简化算法:
        # 男阳女阴，阳男在冬天出生(10-12月)，起运较晚，反之较早
        # 阴男在夏天出生(4-9月)，起运较晚，反之较早
        # 阴男在阴月(2,4,6,8,10,12)出生，起运较晚，反之较早
        # 计算出生时间距离节气的天数，按照3天计1岁
        
        # 简化版本
        # 出生月份对应的大致起运年龄
        start_age_map = {
            1: 6, 2: 4, 3: 3, 4: 2, 
            5: 2, 6: 1, 7: 1, 8: 2,
            9: 4, 10: 6, 11: 8, 12: 9
        }
        
        # 基于月份获取大致起运年龄
        lunar_month_abs = abs(lunar_month)  # 考虑闰月情况
        start_age = start_age_map.get(lunar_month_abs, 3)
        
        # 时辰调整
        if hour >= 12:
            start_age -= 1
            
        # 确保最小为1岁
        return max(1, start_age)
    
    def get_ming_gong(self):
        """
        计算命宫
        
        返回:
            str: 命宫地支
        """
        # 命宫公式: 子午卯酉的对宫，顺数到生时
        month_zhi = self.bazi.getMonthZhi()
        hour_zhi = self.bazi.getTimeZhi()
        
        # 找出月支
        month_zhi_index = Zhi.index(month_zhi)
        
        # 卯酉为一组，寻找宫位并从此处顺时针数到生时
        # 简化算法: 以正月寅月为例，寅逆数起，数至卯对宫酉；命宫在酉，再由酉顺数至生时
        
        # 计算命宫起点
        start_index = (12 - month_zhi_index) % 12
        
        # 计算生时的索引
        hour_index = Zhi.index(hour_zhi)
        
        # 从起点顺数到生时的地支
        ming_gong_index = (start_index + hour_index) % 12
        
        return Zhi[ming_gong_index]
    
    def get_tai_yuan(self):
        """
        计算胎元
        
        返回:
            str: 胎元干支
        """
        # 胎元公式: 年支加月支，取天干地支
        year_zhi = self.bazi.getYearZhi()
        month_zhi = self.bazi.getMonthZhi()
        
        # 计算地支索引
        year_zhi_index = Zhi.index(year_zhi)
        month_zhi_index = Zhi.index(month_zhi)
        
        # 计算胎元支
        tai_yuan_zhi_index = (year_zhi_index + month_zhi_index) % 12
        tai_yuan_zhi = Zhi[tai_yuan_zhi_index]
        
        # 计算胎元干
        # 根据地支推算天干
        # 子(0)-> 癸(9), 丑(1)-> 己(5), 寅(2)-> 甲(0), ...
        zhi_to_gan_offset = {
            0: 9, 1: 5, 2: 0, 3: 1, 4: 5, 5: 2, 
            6: 3, 7: 5, 8: 4, 9: 5, 10: 5, 11: 6
        }
        
        tai_yuan_gan_index = (zhi_to_gan_offset[tai_yuan_zhi_index]) % 10
        tai_yuan_gan = Gan[tai_yuan_gan_index]
        
        # 返回胎元干支
        return tai_yuan_gan + tai_yuan_zhi
    
    def get_shen_sha(self):
        """
        计算神煞
        
        返回:
            list: 神煞列表
        """
        day_gan = self.bazi.getDayGan()
        year_zhi = self.bazi.getYearZhi()
        month_zhi = self.bazi.getMonthZhi()
        day_zhi = self.bazi.getDayZhi()
        hour_zhi = self.bazi.getTimeZhi()
        
        # 日主天干
        me = day_gan
        
        # 四柱地支
        zhis = [year_zhi, month_zhi, day_zhi, hour_zhi]
        
        # 神煞列表
        shen_sha_list = []
        
        # 年支神煞
        year_shens = {
            "太岁": {"子": "子", "丑": "丑", "寅": "寅", "卯": "卯", "辰": "辰", "巳": "巳", 
                   "午": "午", "未": "未", "申": "申", "酉": "酉", "戌": "戌", "亥": "亥"},
            "劫煞": {"子": "未", "丑": "申", "寅": "酉", "卯": "戌", "辰": "亥", "巳": "子", 
                   "午": "丑", "未": "寅", "申": "卯", "酉": "辰", "戌": "巳", "亥": "午"},
            "灾煞": {"子": "酉", "丑": "戌", "寅": "亥", "卯": "子", "辰": "丑", "巳": "寅", 
                   "午": "卯", "未": "辰", "申": "巳", "酉": "午", "戌": "未", "亥": "申"},
            "岁煞": {"子": "戌", "丑": "辰", "寅": "丑", "卯": "未", "辰": "寅", "巳": "申", 
                   "午": "巳", "未": "亥", "申": "午", "酉": "寅", "戌": "酉", "亥": "辰"}
        }
        
        # 月支神煞
        month_shens = {
            "天德": {"子": "巳", "丑": "庚", "寅": "丁", "卯": "申", "辰": "壬", "巳": "辛", 
                   "午": "亥", "未": "甲", "申": "癸", "酉": "寅", "戌": "丙", "亥": "乙"},
            "月德": {"子": "壬", "丑": "庚", "寅": "丙", "卯": "甲", "辰": "壬", "巳": "庚", 
                   "午": "丙", "未": "甲", "申": "壬", "酉": "庚", "戌": "丙", "亥": "甲"},
        }
        
        # 日干神煞
        day_shens = {
            "日德": {"甲": ["巳"], "乙": ["午"], "丙": ["申"], "丁": ["酉"], "戊": ["申"], "己": ["酉"], 
                   "庚": ["亥"], "辛": ["子"], "壬": ["寅"], "癸": ["卯"]},
            "福神": {"甲": ["寅", "卯", "辰"], "乙": ["寅", "卯", "辰"], "丙": ["巳", "午", "未"], 
                   "丁": ["巳", "午", "未"], "戊": ["巳", "午", "未"], "己": ["巳", "午", "未"], 
                   "庚": ["申", "酉", "戌"], "辛": ["申", "酉", "戌"], "壬": ["亥", "子", "丑"], "癸": ["亥", "子", "丑"]},
            "喜神": {"甲": ["寅", "卯", "辰"], "乙": ["亥", "子", "丑"], "丙": ["巳", "午", "未"], 
                   "丁": ["寅", "卯", "辰"], "戊": ["申", "酉", "戌"], "己": ["巳", "午", "未"], 
                   "庚": ["亥", "子", "丑"], "辛": ["申", "酉", "戌"], "壬": ["寅", "卯", "辰"], "癸": ["亥", "子", "丑"]}
        }
        
        # 计算年支神煞
        for shen_name, shen_dict in year_shens.items():
            if year_zhi in shen_dict:
                target = shen_dict[year_zhi]
                for i, zhi in enumerate(zhis):
                    if zhi == target:
                        shen_sha_list.append({
                            "name": shen_name,
                            "position": ["年", "月", "日", "时"][i],
                            "description": f"{year_zhi}年{shen_name}{target}在{['年', '月', '日', '时'][i]}柱"
                        })
                        
        # 计算月支神煞
        for shen_name, shen_dict in month_shens.items():
            if month_zhi in shen_dict:
                target = shen_dict[month_zhi]
                if isinstance(target, str):  # 处理单个目标
                    if target in day_gan:  # 准确判断日干与目标的匹配
                        shen_sha_list.append({
                            "name": shen_name,
                            "position": "日",
                            "description": f"{month_zhi}月{shen_name}{target}在日干"
                        })
                    for i, zhi in enumerate(zhis):
                        if target == zhi:
                            shen_sha_list.append({
                                "name": shen_name,
                                "position": ["年", "月", "日", "时"][i],
                                "description": f"{month_zhi}月{shen_name}{target}在{['年', '月', '日', '时'][i]}柱"
                            })
                elif isinstance(target, list):  # 处理多个目标
                    for t in target:
                        if t in day_gan:  # 同样准确判断日干与目标的匹配
                            shen_sha_list.append({
                                "name": shen_name,
                                "position": "日",
                                "description": f"{month_zhi}月{shen_name}{t}在日干"
                            })
                        for i, zhi in enumerate(zhis):
                            if t == zhi:
                                shen_sha_list.append({
                                    "name": shen_name,
                                    "position": ["年", "月", "日", "时"][i],
                                    "description": f"{month_zhi}月{shen_name}{t}在{['年', '月', '日', '时'][i]}柱"
                                })
        
        # 计算日干神煞
        for shen_name, shen_dict in day_shens.items():
            if day_gan in shen_dict:
                targets = shen_dict[day_gan]
                for target in targets:
                    for i, zhi in enumerate(zhis):
                        if zhi == target:
                            shen_sha_list.append({
                                "name": shen_name,
                                "position": ["年", "月", "日", "时"][i],
                                "description": f"{day_gan}日{shen_name}{target}在{['年', '月', '日', '时'][i]}柱"
                            })
        
        return shen_sha_list

# 测试代码
if __name__ == "__main__":
    solar = Solar.fromYmdHms(1990, 5, 15, 12, 0, 0)
    lunar_ext = LunarExtension(solar=solar)
    
    # 获取大运
    day_uns = lunar_ext.get_day_un(gender_code=1)
    print("大运列表:", day_uns)
    
    # 获取命宫
    ming_gong = lunar_ext.get_ming_gong()
    print("命宫:", ming_gong)
    
    # 获取胎元
    tai_yuan = lunar_ext.get_tai_yuan()
    print("胎元:", tai_yuan)
    
    # 获取神煞
    shen_sha = lunar_ext.get_shen_sha()
    print("神煞:", shen_sha)
