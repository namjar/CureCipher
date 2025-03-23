# CureCipher 中医命理分析工具包

CureCipher是一个中医诊断和命理分析工具包，主要包括八字排盘、紫微斗数、六爻等功能。目前已经实现了八字排盘功能和六爻纳甲排盘功能，支持大运、神煞、命宫、胎元等计算和分析。

## 功能特点

### 八字

- 支持阳历和阴历日期的八字计算
- 支持大运计算功能
- 支持神煞计算功能
- 支持命宫和胎元计算功能
- 提供全面的八字分析功能

### 六爻

- 支持六爻纳甲排盘功能
- 支持六亲、六神、纳甲信息显示
- 支持世应爻位计算
- 支持传统六爻排盘格式
- 支持真太阳时计算

- 命令行工具支持，方便与其他程序集成

## 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖项：
- lunar_python (农历、八字基础计算)
- colorama (终端彩色输出)
- geopy (地理位置解析)

## 使用方法

### 八字命令行工具

```bash
# 使用命令行工具计算八字
python bazi_cli.py 1990 5 15 12 -g male

# 指定出生城市
python bazi_cli.py 1990 5 15 12 -g female -c "北京"

# 输出JSON格式
python bazi_cli.py 1990 5 15 12 -g male -f json
```

### 六爻纳甲命令行工具

```bash
# 使用命令行工具计算六爻纳甲
python liuyao_najia.py

# 然后按提示输入信息，如日期、时间、经纬度等信息
```

### Python API

#### 八字计算

```python
from models.bazi.bazi_calculator import calculate_bazi, generate_bazi_report

# 计算八字
bazi_result = calculate_bazi(1990, 5, 15, 12, "male", "北京")

# 生成报告
report = generate_bazi_report(bazi_result)

# 显示四柱八字
print(f"四柱八字: {report['basic_info']['four_pillars']}")

# 显示五行得分
print(f"五行得分: {report['five_elements']['scores']}")

# 显示文本报告
print(report['text_report'])
```

#### 六爻纳甲计算

```python
from models.liuyao.modules.gua_calculator import gua_calculator
from models.liuyao.modules.gua_display import generate_najia_style_display

# 计算六爻卦象
result = gua_calculator.calculate_gua(
    solar_date=date_obj,    # 阳历日期对象
    time_hour=hour,         # 小时数（可以24小时制小数）
    longitude=longitude,    # 经度
    latitude=latitude,      # 纬度
    use_true_solar_time=True,  # 是否使用真太阳时
)

# 生成排盘显示
display = generate_najia_style_display(result)
print(display)
```

## 项目结构

```
└─ models/             # 模型目录
    ├─ bazi/          # 八字模块
    │   ├─ bazi_calculator.py   # 八字计算器
    │   ├─ lunar_extension.py   # lunar_python扩展功能
    │   └─ calculator.py        # 基础计算函数
    └─ liuyao/        # 六爻模块
        ├─ modules/     # 模块目录
        │   ├─ gua_calculator.py  # 卦象计算程序
        │   ├─ gua_display.py     # 卦象显示模块
        │   ├─ gua_palace.py      # 卦宫信息处理
        │   ├─ AccurateNajia.py   # 精确纳甲计算
        │   └─ enhanced_solar_time.py  # 真太阳时计算
        └─ data/       # 数据目录
            └─ bagong_data.py      # 八宫卦数据
├─ tests/             # 测试目录
├─ bazi_cli.py        # 八字命令行工具
├─ liuyao_najia.py    # 六爻纳甲命令行工具
└─ requirements.txt   # 依赖项
```

## 运行测试

```bash
# 运行单元测试
python -m unittest tests.test_lunar_extension
python -m unittest tests.test_bazi_calculator_full

# 或者使用pytest
python -m pytest tests/
```

## 功能说明

### 八字计算

支持阳历和阴历日期的八字计算，可以得到天干地支、十神、五行、大运、流年等信息。

### 大运计算

基于性别和出生日期计算大运，支持起运年龄、大运干支、十神等信息。

### 命宫和胎元

计算命宫和胎元信息，用于推断命主的个性特征和先天禀赋。

### 神煞计算

计算各种神煞信息，如驿马、桃花、劫煞等，用于辅助八字分析。

### 八字分析

提供全面的八字分析功能，包括日主强弱、五行平衡、用神等信息，生成详细的文本报告。

### 六爻纳甲

支持传统六爻排盘，包括：
- 本卦和变卦的计算
- 六亲、六神和纳甲的显示
- 世应爻位的确定
- 卦宫和卦型的判断
- 真太阳时的计算
- 多种排盘格式

### 六爻解卦

计算六爻动爻变化，自动识别卦宫，确定世应爻位，提供六亲六神纳甲信息，辅助解卦分析。
