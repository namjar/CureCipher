# CureCipher 中医命理分析工具包

CureCipher是一个中医诊断和命理分析工具包，主要包括八字排盘、紫微斗数、六爻等功能。目前已经实现了八字排盘功能，支持大运、神煞、命宫、胎元等计算和分析。

## 功能特点

- 支持阳历和阴历日期的八字计算
- 支持大运计算功能
- 支持神煞计算功能
- 支持命宫和胎元计算功能
- 提供全面的八字分析功能
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

### 命令行工具

```bash
# 使用命令行工具计算八字
python bazi_cli.py 1990 5 15 12 -g male

# 指定出生城市
python bazi_cli.py 1990 5 15 12 -g female -c "北京"

# 输出JSON格式
python bazi_cli.py 1990 5 15 12 -g male -f json
```

### Python API

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

## 项目结构

```
├── models/             # 模型目录
│   ├── bazi/          # 八字模块
│   │   ├── bazi_calculator.py   # 八字计算器
│   │   ├── lunar_extension.py   # lunar_python扩展功能
│   │   └── calculator.py        # 基础计算函数
├── tests/             # 测试目录
│   ├── test_lunar_extension.py  # 测试lunar扩展功能
│   └── test_bazi_calculator_full.py  # 测试八字计算器
├── bazi_cli.py        # 命令行工具
└── requirements.txt   # 依赖项
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
