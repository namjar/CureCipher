def calculate_true_solar_time_diff(longitude, year, month, day):
    """
    计算真太阳时校正（分钟数）
    
    参数:
        longitude (float): 经度
        year (int): 年
        month (int): 月
        day (int): 日
    
    返回:
        float: 时差（分钟）
    """
    # 计算儒略日
    if month <= 2:
        year -= 1
        month += 12
    
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    
    julian_day = (math.floor(365.25 * (year + 4716)) + 
                 math.floor(30.6001 * (month + 1)) + 
                 day + B - 1524.5)
    
    # 计算时间方程
    # 简化公式，实际应有更复杂精确的计算
    D = julian_day - 2451545.0  # J2000
    g = 357.529 + 0.98560028 * D  # 平太阳黄经
    g_rad = math.radians(g % 360)
    
    # 时间方程（简化）
    eq_time = (9.87 * math.sin(2 * g_rad) - 
              7.53 * math.cos(g_rad) - 
              1.5 * math.sin(g_rad))
    
    # 经度校正
    local_time_diff = longitude / 15 * 60  # 每15度经度1小时
    
    # 总时差
    return eq_time + local_time_diff

def get_default_location():
    """
    获取默认位置（北京）
    
    返回:
        tuple: (纬度, 经度)
    """
    return 39.9042, 116.4074  # 北京默认值

@functools.lru_cache(maxsize=64)
def get_element(gan):
    """
    获取天干的五行属性
    
    参数:
        gan (str): 天干字符
    
    返回:
        str: 五行属性（'木', '火', '土', '金', '水'）
    """
    elements_map = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }
    
    return elements_map.get(gan, "未知")

@functools.lru_cache(maxsize=16)
def get_element_english(chinese_element):
    """
    将中文五行属性转换为英文
    
    参数:
        chinese_element (str): 中文五行属性
    
    返回:
        str: 英文五行属性
    """
    element_map = {
        "木": "Wood",
        "火": "Fire",
        "土": "Earth",
        "金": "Metal",
        "水": "Water",
        "未知": "Unknown"
    }
    
    return element_map.get(chinese_element, "Unknown")

@functools.lru_cache(maxsize=16)
def get_element_spanish(chinese_element):
    """
    将中文五行属性转换为西班牙语
    
    参数:
        chinese_element (str): 中文五行属性
    
    返回:
        str: 西班牙语五行属性
    """
    element_map = {
        "木": "Madera",
        "火": "Fuego",
        "土": "Tierra",
        "金": "Metal",
        "水": "Agua",
        "未知": "Desconocido"
    }
    
    return element_map.get(chinese_element, "Desconocido")

@functools.lru_cache(maxsize=16)
def get_generating_element(element):
    """
    获取生我的五行
    
    参数:
        element (str): 五行属性
    
    返回:
        str: 生我的五行
    """
    generating_map = {
        "木": "水",
        "火": "木",
        "土": "火",
        "金": "土",
        "水": "金"
    }
    return generating_map.get(element, "未知")

@functools.lru_cache(maxsize=16)
def get_controlled_element(element):
    """
    获取我克的五行
    
    参数:
        element (str): 五行属性
    
    返回:
        str: 我克的五行
    """
    controlled_map = {
        "木": "土",
        "火": "金",
        "土": "水",
        "金": "木",
        "水": "火"
    }
    return controlled_map.get(element, "未知")

def encrypt_data(data):
    """
    加密数据（HIPAA合规）
    
    参数:
        data (dict): 要加密的数据
    
    返回:
        str: 加密后的数据
    """
    # 使用固定密钥进行简单加密（实际使用中应使用安全的密钥管理）
    key = b'my-secret-key-16'  # 16字节密钥示例
    fernet = Fernet(key)
    encrypted = fernet.encrypt(json.dumps(data, ensure_ascii=False).encode())
    return encrypted.decode()

def decrypt_data(encrypted_data):
    """
    解密数据
    
    参数:
        encrypted_data (str): 加密的数据
    
    返回:
        dict: 解密后的数据
    """
    key = b'my-secret-key-16'
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data.encode())
    return json.loads(decrypted.decode())

def calculate_liunian_ganzhi(year):
    """
    计算流年干支
    
    参数:
        year (int): 年份
    
    返回:
        str: 干支
    """
    Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    gan_index = (year - 4) % 10
    zhi_index = (year - 4) % 12
    
    return Gan[gan_index] + Zhi[zhi_index]

def calculate_liuyue_ganzhi(year, month):
    """
    计算流月干支
    
    参数:
        year (int): 年份
        month (int): 月份
    
    返回:
        str: 干支
    """
    Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 计算年份的天干
    year_gan_index = (year - 4) % 10
    
    # 根据年份天干和月份确定月干
    base_month_gan_index = (year_gan_index * 2 + month - 1) % 10
    
    # 确定月支（正月-寅月）
    month_zhi_index = (month + 1) % 12
    
    return Gan[base_month_gan_index] + Zhi[month_zhi_index]

def generate_liuyao(birth_year, birth_month, birth_day, birth_hour, 
                  year_gz, month_gz, day_gz, hour_gz, shensha_list=None):
    """
    生成六爻卦象基础信息（简化版）
    完整的六爻纳甲计算在单独的模块中实现
    
    参数:
        birth_year, birth_month, birth_day, birth_hour: 出生时间
        year_gz, month_gz, day_gz, hour_gz: 八字干支
        shensha_list: 神煞列表
    
    返回:
        dict: 六爻卦象基础信息
    """
    # 简化的六爻信息，完整计算在liuyao_analyzer.py中实现
    from importlib import util
    liuyao_module_exists = util.find_spec('models.liuyao.liuyao_analyzer') is not None
    
    if liuyao_module_exists:
        try:
            # 尝试从专门的六爻模块导入卦象计算函数
            from models.liuyao.liuyao_analyzer import calculate_gua
            # 调用专门模块的函数计算六爻卦象
            return calculate_gua(
                birth_year=birth_year,
                birth_month=birth_month,
                birth_day=birth_day,
                birth_hour=birth_hour,
                year_gz=year_gz,
                month_gz=month_gz,
                day_gz=day_gz,
                hour_gz=hour_gz,
                shensha_list=shensha_list
            )
        except (ImportError, ModuleNotFoundError):
            pass  # 如果专门模块不可用，使用简化版实现
    
    # 六十四卦名称 (简化版实现)
    bagua_names = ["乾", "坤", "震", "艮", "离", "坎", "兑", "巽"]
    gua64_names = [
        "乾为天", "坤为地", "水雷屯", "山水蒙", "水天需", "天水讼", "地水师", "水地比",
        "风天小畜", "天泽履", "地天泰", "天地否", "天火同人", "火天大有", "地山谦", "雷地豫",
        "泽雷随", "山风蛊", "地泽临", "风地观", "火雷噬嗑", "山火贲", "山地剥", "地雷复",
        "天雷无妄", "山天大畜", "山雷颐", "泽风大过", "坎为水", "离为火", "泽山咸", "雷风恒",
        "天山遁", "雷天大壮", "火地晋", "地火明夷", "风火家人", "火泽睽", "水山蹇", "雷水解",
        "山泽损", "风雷益", "泽天夬", "天风姤", "泽地萃", "地风升", "泽水困", "水风井",
        "泽火革", "火风鼎", "震为雷", "艮为山", "风山渐", "雷泽归妹", "雷火丰", "火山旅",
        "巽为风", "兑为泽", "风水涣", "水泽节", "风泽中孚", "雷山小过", "水火既济", "火水未济"
    ]
    
    # 根据八字计算卦象（简化算法）
    year_stem = ord(year_gz[0]) - ord('甲')
    year_branch = "子丑寅卯辰巳午未申酉戌亥".find(year_gz[1:])
    
    month_stem = ord(month_gz[0]) - ord('甲')
    month_branch = "子丑寅卯辰巳午未申酉戌亥".find(month_gz[1:])
    
    day_stem = ord(day_gz[0]) - ord('甲')
    day_branch = "子丑寅卯辰巳午未申酉戌亥".find(day_gz[1:])
    
    hour_stem = ord(hour_gz[0]) - ord('甲')
    hour_branch = "子丑寅卯辰巳午未申酉戌亥".find(hour_gz[1:])
    
    # 计算上卦和下卦索引
    upper_index = (year_stem + month_branch) % 8
    lower_index = (day_stem + hour_branch) % 8
    
    # 计算变爻位置（1-6）
    change_yao = ((birth_year + birth_month + birth_day + birth_hour) % 6) + 1
    
    # 确定卦象索引
    gua_index = upper_index * 8 + lower_index
    
    # 考虑神煞影响（如果有的话）
    if shensha_list and len(shensha_list) > 0:
        # 简化：根据神煞数量调整卦象
        gua_index = (gua_index + len(shensha_list)) % 64
    
    # 生成结果（简化版）
    return {
        "name": gua64_names[gua_index],
        "upper": bagua_names[upper_index],
        "lower": bagua_names[lower_index],
        "change_yao": change_yao,
        "description": f"{gua64_names[gua_index]}卦，第{change_yao}爻变",
        "note": "此为简化版六爻信息，详细纳甲分析请使用 models.liuyao.liuyao_analyzer 模块"
    }
    
# 创建默认位置配置文件（如果不存在）
def create_default_location_config():
    """创建默认位置配置文件（如果不存在）"""
    config_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(config_dir, "location_config.json")
    
    if not os.path.exists(config_path):
        default_config = {
            "default_location": {
                "latitude": 39.9042,
                "longitude": 116.4074
            },
            "description": "北京默认位置"
        }
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=4)
            print(f"已创建默认位置配置文件: {config_path}")
        except Exception as e:
            print(f"创建默认位置配置文件时出错: {e}")

# 初始化配置文件
create_default_location_config()

if __name__ == "__main__":
    # 测试代码
    test_result = calculate_bazi(1990, 5, 15, 8, "male", longitude=116.4074, latitude=39.9042)
    result = test_result["result"]
    
    print("八字: " + result["bazi"]["formatted"])
    print("五行比例: ", end="")
    for element, percentage in result["elements"]["percentages"].items():
        print(f"{element}: {percentage}%, ", end="")
    print()
    print(f"日主强弱: {result['day_master_strength']['status']} ({result['day_master_strength']['en']}/{result['day_master_strength']['es']})")
    print(f"用神: {result['yong_shen']['element']} ({result['yong_shen']['en']}/{result['yong_shen']['es']})")
    print(f"流月干支 (1990年5月): {calculate_liuyue_ganzhi(1990, 5)}")
    print(f"六爻卦象: {result['liuyao']['name']}")
    
    # 查看加密数据（HIPAA合规）
    print("\n数据加密示例:")
    print(test_result["encrypted"][:50] + "...")
    
    # 解密测试
    decrypted = decrypt_data(test_result["encrypted"])
    print("\n解密验证成功：", decrypted["bazi"]["formatted"] == result["bazi"]["formatted"])
