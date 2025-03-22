# 八字计算模块使用说明

本文档介绍如何使用CureCipher项目中的八字计算模块。

## 模块功能

八字计算模块可以：

1. 计算出生八字（年月日时四柱干支）
2. 分析五行比例和生克关系
3. 提供健康建议和饮食运动指导
4. 分析吉凶神煞对健康的影响

## 使用方法

### 使用Python代码调用

```python
from models.bazi.calculator import calculate_bazi
from models.bazi.five_elements import analyze_five_elements
from models.bazi.shensha import analyze_shensha

# 计算八字
bazi_result = calculate_bazi(
    birth_year=1977,   # 出生年
    birth_month=2,     # 出生月
    birth_day=25,      # 出生日
    birth_hour=21,     # 出生时辰（24小时制，这里是晚上9点）
    gender="male",     # 性别（"male"或"female"）
    city="Beijing"     # 出生城市（可选，默认为"Beijing"）
)

# 分析五行
elements_result = analyze_five_elements(bazi_result)

# 分析神煞
shensha_result = analyze_shensha(
    bazi_result.get("shensha", []),
    bazi_result["bazi"]["day_master_element"]
)

# 使用结果
print(f"四柱: {bazi_result['bazi']['year']} {bazi_result['bazi']['month']} {bazi_result['bazi']['day']} {bazi_result['bazi']['hour']}")
print(f"日主: {bazi_result['bazi']['day_master']} ({bazi_result['bazi']['day_master_element']})")
```

### 使用命令行工具

项目提供了命令行工具，可以直接计算八字：

```bash
python scripts/calculate_bazi.py -y 1977 -m 2 -d 25 -H 20 -M 50 -g male -c Beijing
```

参数说明：
- `-y, --year`: 出生年份
- `-m, --month`: 出生月份
- `-d, --day`: 出生日期
- `-H, --hour`: 出生小时（24小时制）
- `-M, --minute`: 出生分钟（可选，默认为0）
- `-g, --gender`: 性别（male/female）
- `-c, --city`: 出生城市（可选，默认为Beijing）
- `-o, --output`: 输出文件路径（可选）

计算结果会保存为JSON文件，默认保存在`outputs`目录下。

### 运行测试用例

项目包含预定义的测试用例，可以直接运行：

```bash
python tests/bazi/test_specific_bazi.py
```

这将计算特定出生日期（1977年2月25日晚上8点50分，男性，北京）的八字，并输出详细分析结果。

## 返回结果说明

### 基本八字信息

```json
{
  "bazi": {
    "year": "丁巳",
    "month": "丙寅",
    "day": "癸巳",
    "hour": "辛亥",
    "day_master": "癸",
    "day_master_element": "水"
  }
}
```

### 五行分析结果

```json
{
  "element_percentages": {
    "木": 20.5,
    "火": 35.2,
    "土": 15.0,
    "金": 10.1,
    "水": 19.2
  },
  "balance_analysis": {
    "balance_state": "稍有不平衡",
    "description": "火偏强，金偏弱，可能需要适当调整。"
  }
}
```

### 神煞分析结果

```json
{
  "positive_impacts": [
    {
      "name": "天乙",
      "description": "天乙贵人",
      "impact": "吉神，主贵人相助，逢凶化吉"
    }
  ],
  "negative_impacts": [
    {
      "name": "劫煞",
      "description": "劫煞",
      "impact": "凶神，主遭遇意外或损失"
    }
  ]
}
```

## 注意事项

1. 时间使用24小时制，如晚上8点表示为20时
2. 时辰计算会自动四舍五入到整点
3. 如果不提供城市，默认使用北京的经纬度
4. 命令行工具会自动四舍五入小时，根据分钟数

## 自定义和扩展

如果需要扩展神煞的健康影响数据，可以修改`data/shensha_impacts.json`文件。

如果需要自定义五行调理方案，可以修改`data/five_elements_flavors.json`和`data/five_elements_exercises.json`文件。
