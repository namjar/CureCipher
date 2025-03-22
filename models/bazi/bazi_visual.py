#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字命盘可视化模块 - 将八字命盘数据转换为可视化表示
"""

def generate_text_grid(report):
    """
    生成文本网格形式的八字命盘
    
    参数:
        report (dict): 八字报告数据
    
    返回:
        str: 文本形式的命盘网格
    """
    # 获取基本信息
    bazi = report['basic_info']['four_pillars'].split()
    gans = report['basic_info']['gans'].split()
    zhis = report['basic_info']['zhis'].split()
    
    # 获取十神信息（如果有）
    gan_shens = report.get('ten_gods', {}).get('gans', ['', '', '', ''])
    zhi_shens = report.get('ten_gods', {}).get('zhis', ['', '', '', ''])
    
    # 获取纳音信息
    nayins = [report['nayin'][pos] for pos in ['year', 'month', 'day', 'hour']]
    
    # 获取空亡信息（如果有）
    empties = report.get('relations', {}).get('empties', ['', '', '', ''])
    
    # 生成表头
    lines = []
    lines.append("┏━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓")
    lines.append("┃   年柱   ┃   月柱   ┃   日柱   ┃   时柱   ┃")
    lines.append("┣━━━━━━━━━━╋━━━━━━━━━━╋━━━━━━━━━━╋━━━━━━━━━━┫")
    
    # 天干行
    gan_line = "┃"
    for i in range(4):
        gan = gans[i]
        shen = gan_shens[i] if i < len(gan_shens) and gan_shens[i] else ""
        shen_str = f"({shen})" if shen else "    "
        gan_line += f" {gan}  {shen_str} ┃"
    lines.append(gan_line)
    
    # 地支行
    zhi_line = "┃"
    for i in range(4):
        zhi = zhis[i]
        shen = zhi_shens[i] if i < len(zhi_shens) and zhi_shens[i] else ""
        shen_str = f"({shen})" if shen else "    "
        zhi_line += f" {zhi}  {shen_str} ┃"
    lines.append(zhi_line)
    
    # 纳音行
    nayin_line = "┃"
    for i in range(4):
        nayin = nayins[i] if i < len(nayins) else ""
        nayin_line += f" {nayin[:4]}.. ┃" if len(nayin) > 4 else f" {nayin.ljust(8)} ┃"
    lines.append(nayin_line)
    
    # 空亡行（如果有）
    if any(empties):
        empty_line = "┃"
        for i in range(4):
            empty = "空亡" if empties[i] else "    "
            empty_line += f" {empty.ljust(8)} ┃"
        lines.append(empty_line)
    
    # 表尾
    lines.append("┗━━━━━━━━━━┻━━━━━━━━━━┻━━━━━━━━━━┻━━━━━━━━━━┛")
    
    # 添加五行得分
    lines.append("\n五行得分：")
    scores = report['five_elements']['scores']
    score_line = "  ".join([f"{element}: {score:.1f}" for element, score in scores.items()])
    lines.append(score_line)
    
    # 添加日主信息
    lines.append(f"\n日主: {report['basic_info']['day_master']} ({report['pattern_analysis']['day_master_strength']} {report['pattern_analysis']['day_master_percentage']:.1f}%)")
    
    # 添加用神信息
    lines.append(f"用神: {report['pattern_analysis']['yong_shen']}")
    
    # 添加特殊信息
    lines.append(f"命宫: {report['special']['ming_gong']}   胎元: {report['special']['tai_yuan']}")
    
    return "\n".join(lines)

def generate_html_grid(report):
    """
    生成HTML格式的八字命盘
    
    参数:
        report (dict): 八字报告数据
    
    返回:
        str: HTML格式的命盘网格
    """
    # 获取基本信息
    bazi = report['basic_info']['four_pillars'].split()
    gans = report['basic_info']['gans'].split()
    zhis = report['basic_info']['zhis'].split()
    
    # 获取十神信息（如果有）
    gan_shens = report.get('ten_gods', {}).get('gans', ['', '', '', ''])
    zhi_shens = report.get('ten_gods', {}).get('zhis', ['', '', '', ''])
    
    # 获取纳音信息
    nayins = [report['nayin'][pos] for pos in ['year', 'month', 'day', 'hour']]
    
    # 获取空亡信息（如果有）
    empties = report.get('relations', {}).get('empties', ['', '', '', ''])
    
    # 生成CSS样式
    css = """
    <style>
        .bazi-table {
            border-collapse: collapse;
            font-family: "Microsoft YaHei", "宋体", sans-serif;
            margin: 20px 0;
            width: 100%;
            max-width: 800px;
        }
        .bazi-table th, .bazi-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }
        .bazi-table th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        .bazi-table .gan {
            background-color: #f9f9f9;
        }
        .bazi-table .zhi {
            background-color: #f0f0f0;
        }
        .bazi-table .nayin {
            background-color: #e9e9e9;
            font-size: 0.9em;
        }
        .bazi-table .empty {
            color: red;
            font-size: 0.9em;
        }
        .bazi-info {
            margin-top: 20px;
            font-family: "Microsoft YaHei", "宋体", sans-serif;
        }
        .bazi-info p {
            margin: 5px 0;
        }
        .scores {
            display: flex;
            justify-content: space-between;
            max-width: 500px;
            margin: 10px 0;
        }
        .score-item {
            text-align: center;
            padding: 5px;
            border-radius: 4px;
            min-width: 60px;
        }
        .score-item.wood {
            background-color: #a5d6a7;
        }
        .score-item.fire {
            background-color: #ffcdd2;
        }
        .score-item.earth {
            background-color: #ffe0b2;
        }
        .score-item.metal {
            background-color: #e1f5fe;
        }
        .score-item.water {
            background-color: #d1c4e9;
        }
    </style>
    """
    
    # 生成HTML表格
    html = f"{css}\n<div class='bazi-container'>\n"
    html += "<table class='bazi-table'>\n"
    html += "  <tr><th>年柱</th><th>月柱</th><th>日柱</th><th>时柱</th></tr>\n"
    
    # 天干行
    html += "  <tr class='gan'>\n"
    for i in range(4):
        gan = gans[i]
        shen = gan_shens[i] if i < len(gan_shens) and gan_shens[i] else ""
        shen_str = f"<small>({shen})</small>" if shen else ""
        html += f"    <td>{gan} {shen_str}</td>\n"
    html += "  </tr>\n"
    
    # 地支行
    html += "  <tr class='zhi'>\n"
    for i in range(4):
        zhi = zhis[i]
        shen = zhi_shens[i] if i < len(zhi_shens) and zhi_shens[i] else ""
        shen_str = f"<small>({shen})</small>" if shen else ""
        html += f"    <td>{zhi} {shen_str}</td>\n"
    html += "  </tr>\n"
    
    # 纳音行
    html += "  <tr class='nayin'>\n"
    for i in range(4):
        nayin = nayins[i] if i < len(nayins) else ""
        html += f"    <td>{nayin}</td>\n"
    html += "  </tr>\n"
    
    # 空亡行（如果有）
    if any(empties):
        html += "  <tr class='empty'>\n"
        for i in range(4):
            empty = "空亡" if empties[i] else ""
            html += f"    <td>{empty}</td>\n"
        html += "  </tr>\n"
    
    html += "</table>\n"
    
    # 添加五行得分
    html += "<div class='bazi-info'>\n"
    html += "  <div class='scores'>\n"
    
    # 映射中文五行到英文类名
    element_class = {'木': 'wood', '火': 'fire', '土': 'earth', '金': 'metal', '水': 'water'}
    
    scores = report['five_elements']['scores']
    for element, score in scores.items():
        class_name = element_class.get(element, '')
        html += f"    <div class='score-item {class_name}'>{element}: {score:.1f}</div>\n"
    html += "  </div>\n"
    
    # 添加日主信息
    html += f"  <p>日主: {report['basic_info']['day_master']} ({report['pattern_analysis']['day_master_strength']} {report['pattern_analysis']['day_master_percentage']:.1f}%)</p>\n"
    
    # 添加用神信息
    html += f"  <p>用神: {report['pattern_analysis']['yong_shen']}</p>\n"
    
    # 添加特殊信息
    html += f"  <p>命宫: {report['special']['ming_gong']}   胎元: {report['special']['tai_yuan']}</p>\n"
    html += "</div>\n"
    html += "</div>"
    
    return html

def generate_markdown_grid(report):
    """
    生成Markdown格式的八字命盘
    
    参数:
        report (dict): 八字报告数据
    
    返回:
        str: Markdown格式的命盘网格
    """
    # 获取基本信息
    bazi = report['basic_info']['four_pillars'].split()
    gans = report['basic_info']['gans'].split()
    zhis = report['basic_info']['zhis'].split()
    
    # 获取十神信息（如果有）
    gan_shens = report.get('ten_gods', {}).get('gans', ['', '', '', ''])
    zhi_shens = report.get('ten_gods', {}).get('zhis', ['', '', '', ''])
    
    # 获取纳音信息
    nayins = [report['nayin'][pos] for pos in ['year', 'month', 'day', 'hour']]
    
    # 生成表格
    lines = []
    lines.append("## 八字命盘")
    lines.append("")
    lines.append("| 年柱 | 月柱 | 日柱 | 时柱 |")
    lines.append("|------|------|------|------|")
    
    # 天干行
    gan_line = "|"
    for i in range(4):
        gan = gans[i]
        shen = gan_shens[i] if i < len(gan_shens) and gan_shens[i] else ""
        shen_str = f"({shen})" if shen else ""
        gan_line += f" {gan} {shen_str} |"
    lines.append(gan_line)
    
    # 地支行
    zhi_line = "|"
    for i in range(4):
        zhi = zhis[i]
        shen = zhi_shens[i] if i < len(zhi_shens) and zhi_shens[i] else ""
        shen_str = f"({shen})" if shen else ""
        zhi_line += f" {zhi} {shen_str} |"
    lines.append(zhi_line)
    
    # 纳音行
    nayin_line = "|"
    for i in range(4):
        nayin = nayins[i] if i < len(nayins) else ""
        nayin_line += f" {nayin} |"
    lines.append(nayin_line)
    
    # 添加五行得分
    lines.append("")
    lines.append("### 五行得分")
    scores = report['five_elements']['scores']
    for element, score in scores.items():
        lines.append(f"- {element}: {score:.1f}")
    
    # 添加日主信息
    lines.append("")
    lines.append(f"### 日主: {report['basic_info']['day_master']} ({report['pattern_analysis']['day_master_strength']} {report['pattern_analysis']['day_master_percentage']:.1f}%)")
    
    # 添加用神信息
    lines.append(f"### 用神: {report['pattern_analysis']['yong_shen']}")
    
    # 添加特殊信息
    lines.append(f"### 特殊信息")
    lines.append(f"- 命宫: {report['special']['ming_gong']}")
    lines.append(f"- 胎元: {report['special']['tai_yuan']}")
    
    return "\n".join(lines)

def generate_visual_report(report, format='text'):
    """
    生成可视化的命盘报告
    
    参数:
        report (dict): 八字报告数据
        format (str): 输出格式，可选 'text', 'html', 'markdown'
    
    返回:
        str: 指定格式的可视化报告
    """
    if format == 'html':
        return generate_html_grid(report)
    elif format == 'markdown':
        return generate_markdown_grid(report)
    else:  # 默认为text
        return generate_text_grid(report)

# 测试代码
if __name__ == "__main__":
    # 创建一个示例报告用于测试
    sample_report = {
        'basic_info': {
            'four_pillars': '甲子 乙丑 丙寅 丁卯',
            'gans': '甲 乙 丙 丁',
            'zhis': '子 丑 寅 卯',
            'day_master': '丙(火)'
        },
        'ten_gods': {
            'gans': ['偏印', '印', '--', '食'],
            'zhis': ['正印', '偏财', '比肩', '伤官']
        },
        'five_elements': {
            'scores': {'木': 25.5, '火': 15.0, '土': 10.0, '金': 5.0, '水': 20.0}
        },
        'nayin': {
            'year': '海中金',
            'month': '海中金',
            'day': '炉中火',
            'hour': '炉中火'
        },
        'relations': {
            'empties': [False, True, False, False]
        },
        'pattern_analysis': {
            'day_master_strength': '中和',
            'day_master_percentage': 25.0,
            'yong_shen': '木 (生身)'
        },
        'special': {
            'ming_gong': '酉',
            'tai_yuan': '丙午'
        }
    }
    
    # 测试不同格式的输出
    print(generate_text_grid(sample_report))
    print("\n" + "="*50 + "\n")
    
    html_output = generate_html_grid(sample_report)
    with open('bazi_chart.html', 'w', encoding='utf-8') as f:
        f.write(html_output)
    print("HTML输出已保存到 bazi_chart.html")
    
    print("\n" + "="*50 + "\n")
    print(generate_markdown_grid(sample_report))
