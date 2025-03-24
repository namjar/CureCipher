"""
特定测算类型解释模块 - 主要针对健康问题分析
"""

from typing import Dict, List, Optional
from .base_interpreter import BaseInterpreter

from ...health_analyzer import health_analyzer


class SpecificQueryInterpreter(BaseInterpreter):
    """特定测算类型解释器，根据不同的测算类型提供针对性解释，主要关注健康方面"""
    
    def __init__(self):
        """初始化特定测算类型解释器"""
        # 卦象与健康状况的关联
        self.health_gua_relations = {
            "有利卦象": [
                "乾为天", "天地否", "地天泰", "天雷无妄", "天火同人", 
                "坤为地", "地雷复", "雷地豫", "地水师", "水地比",
                "震为雷", "雷水解", "雷风恒", "雷地豫", "兑为泽",
                "坎为水", "水天需", "水地比", "水山蹇", "离为火"
            ],
            "不利卦象": [
                "水山蹇", "山水蒙", "山火贲", "水雷屯", "雷水解",
                "水火既济", "火水未济", "火山旅", "山火贲", "火风鼎",
                "天风姤", "风天小畜", "风雷益", "风山渐", "风水涣",
                "坎为水", "水雷屯", "天水讼", "水火既济", "火水未济"
            ]
        }
        
        # 各爻位与健康系统的关联
        self.yao_health_relations = {
            1: "初爻代表健康基础，表示体质条件和先天健康状况",
            2: "二爻代表日常生活习惯，表示饮食起居和保健行为",
            3: "三爻代表健康环境，表示生活和工作环境对健康的影响",
            4: "四爻代表疾病变化，表示病情发展趋势和康复情况",
            5: "五爻代表医疗条件，表示治疗方式和医疗资源",
            6: "上爻代表健康远景，表示长期健康趋势和预后"
        }
        
        # 六亲与健康系统的关联
        self.liuqin_health_relations = {
            "官鬼": {
                "健康含义": "代表压力、制约，健康中的疾病或问题",
                "相关系统": "中枢神经系统、内分泌系统、自律神经",
                "症状表现": "压力症状、紧张、焦虑、失眠、内分泌紊乱",
                "治疗建议": "减轻压力，放松身心，规律作息，避免过度劳累"
            },
            "父母": {
                "健康含义": "代表调养、保护，健康中的养生或医护",
                "相关系统": "消化系统、呼吸系统、内分泌系统",
                "症状表现": "脾胃不适、消化不良、呼吸系统问题、能量不足",
                "治疗建议": "加强调养，增强饮食调理，重视医疗干预，改善作息"
            },
            "子孙": {
                "健康含义": "代表恢复、改善，健康中的康复或缓解",
                "相关系统": "生殖系统、免疫系统、精神状态",
                "症状表现": "免疫力下降、情绪不稳、生殖系统问题",
                "治疗建议": "增强免疫力，保持心情愉快，关注生殖健康，适当运动"
            },
            "财星": {
                "健康含义": "代表能量、活力，健康中的精力或体力",
                "相关系统": "循环系统、代谢系统、内分泌系统",
                "症状表现": "疲劳、乏力、代谢异常、营养不良",
                "治疗建议": "均衡营养，增强代谢，适度锻炼，调整饮食结构"
            },
            "兄弟": {
                "健康含义": "代表平衡、协调，健康中的身心平衡",
                "相关系统": "肌肉骨骼系统、免疫系统、外周神经",
                "症状表现": "身体不协调、肌肉酸痛、关节问题、免疫力波动",
                "治疗建议": "保持身体平衡，加强肌肉锻炼，调整姿势，增强免疫力"
            },
            "妻财": {
                "健康含义": "代表调节、适应，健康中的适应能力",
                "相关系统": "泌尿系统、内分泌系统、皮肤系统",
                "症状表现": "水液代谢异常、皮肤问题、适应能力下降",
                "治疗建议": "增强适应能力，保持水分平衡，关注皮肤护理，调节内分泌"
            }
        }
        
        # 六神与健康的关联
        self.liushen_health_relations = {
            "青龙": {
                "健康含义": "代表生机、活力、恢复力",
                "相关系统": "肝胆系统、血液循环、肌腱韧带",
                "健康影响": "有助于促进血液循环，增强身体活力，加速恢复和愈合",
                "注意事项": "情绪波动可能导致肝火上升，需注意控制情绪"
            },
            "朱雀": {
                "健康含义": "代表热力、代谢、精神活动",
                "相关系统": "心脏系统、神经系统、消化系统",
                "健康影响": "提高新陈代谢，促进体温调节，但也可能引起情绪不稳",
                "注意事项": "口舌生疮，心火过旺，易引起失眠和消化不良"
            },
            "勾陈": {
                "健康含义": "代表稳定、缓慢、积累",
                "相关系统": "脾胃系统、内分泌系统、淋巴系统",
                "健康影响": "有利于稳定情绪，增强消化功能，但进展缓慢",
                "注意事项": "消化不良，胃部不适，体重增加，需注意饮食规律"
            },
            "腾蛇": {
                "健康含义": "代表变动、适应、波动",
                "相关系统": "神经系统、免疫系统、皮肤系统",
                "健康影响": "有利于排毒，改善血液循环，但可能使症状反复",
                "注意事项": "皮肤问题，过敏反应，神经紧张，需保持平稳状态"
            },
            "白虎": {
                "健康含义": "代表劲力、清肃、破坏",
                "相关系统": "肺部系统、骨骼系统、免疫系统",
                "健康影响": "有利于呼吸系统，增强免疫力，但可能引起疼痛和损伤",
                "注意事项": "慢性疼痛，肺部问题，骨骼损伤，需注意保护身体"
            },
            "玄武": {
                "健康含义": "代表潜藏、隐秘、收藏",
                "相关系统": "肾脏系统、泌尿系统、生殖系统",
                "健康影响": "有利于肾脏功能，改善水液代谢，但可能隐藏问题",
                "注意事项": "泌尿系统问题，水肿，腰背疼痛，需注意保暖和水分平衡"
            }
        }
        
        # 五行与健康系统的关联
        self.wuxing_health_relations = {
            "木": {
                "健康含义": "代表生长、舒展、柔韧",
                "相关系统": "肝胆系统、肌腱、眼睛",
                "常见病症": "肝炎、胆囊炎、眼疾、肌腱炎、偏头痛",
                "情绪表现": "易怒、抑郁、情绪波动",
                "饮食调理": "绿色蔬菜、柑橘类水果、五谷杂粮",
                "运动建议": "伸展运动、瑜伽、太极"
            },
            "火": {
                "健康含义": "代表温热、激发、活动",
                "相关系统": "心脏系统、小肠、血管、舌头",
                "常见病症": "心脑血管疾病、高血压、心律不齐、失眠",
                "情绪表现": "焦虑、兴奋、激动、喜悦",
                "饮食调理": "苦味食物、红色水果、菊花茶、莲子",
                "运动建议": "有氧运动、步行、慢跑、游泳"
            },
            "土": {
                "健康含义": "代表稳定、转化、吸收",
                "相关系统": "脾胃系统、肌肉组织、口腔",
                "常见病症": "消化不良、胃炎、肥胖、糖尿病",
                "情绪表现": "思虑过度、担忧、固执",
                "饮食调理": "甜味食物、山药、南瓜、薏米",
                "运动建议": "缓和步行、八段锦、健胃操"
            },
            "金": {
                "健康含义": "代表收敛、坚固、清洁",
                "相关系统": "肺部系统、大肠、皮肤、鼻子",
                "常见病症": "呼吸系统疾病、过敏、皮肤病、便秘",
                "情绪表现": "悲伤、忧郁、敏感",
                "饮食调理": "辛辣食物、白色食物、梨、百合",
                "运动建议": "呼吸练习、胸部拓展运动、大肠按摩"
            },
            "水": {
                "健康含义": "代表滋润、流动、潜藏",
                "相关系统": "肾脏系统、膀胱、骨髓、耳朵",
                "常见病症": "肾炎、尿路感染、骨质疏松、耳鸣",
                "情绪表现": "恐惧、忧虑、畏寒",
                "饮食调理": "咸味食物、黑色食物、豆类、海产品",
                "运动建议": "水中运动、太极、肾区按摩"
            }
        }
        
        # 疾病类型与卦象的关联
        self.disease_gua_relations = {
            "急性疾病": {
                "相关卦象": ["天火同人", "火雷噬嗑", "雷地豫", "雷水解", "风雷益"],
                "特点": "发病急、变化快、症状明显",
                "对策": "及时就医、控制症状、消除病因"
            },
            "慢性疾病": {
                "相关卦象": ["山地剥", "地山谦", "山水蒙", "水山蹇", "坎为水"],
                "特点": "病程长、起伏缓、反复性强",
                "对策": "长期调理、生活规律、避免诱因"
            },
            "外感疾病": {
                "相关卦象": ["风天小畜", "天风姤", "风水涣", "风雷益", "巽为风"],
                "特点": "受外邪影响、气候相关、传染性",
                "对策": "增强抵抗力、防止感染、适应气候"
            },
            "内伤疾病": {
                "相关卦象": ["坎为水", "水火既济", "火水未济", "水地比", "地水师"],
                "特点": "内脏功能失调、代谢异常、慢性发展",
                "对策": "调理脏腑、均衡饮食、情志调节"
            },
            "心理疾病": {
                "相关卦象": ["火风鼎", "风山渐", "山火贲", "火天大有", "离为火"],
                "特点": "情绪异常、认知偏差、行为改变",
                "对策": "心理疏导、情绪管理、必要时药物治疗"
            }
        }

    def interpret(self, gua_result: Dict, day_master: Optional[str] = None, 
                 query_type: Optional[str] = None) -> str:
        """
        根据测算类型提供针对性解释
        
        参数:
            gua_result (Dict): 卦象计算结果
            day_master (str, optional): 日主天干
            query_type (str, optional): 测算类型
            
        返回:
            str: 解释结果
        """
        # 如果未指定测算类型，默认为健康分析
        if not query_type:
            query_type = "健康"
        
        # 确保测算类型是健康相关的
        if query_type != "健康":
            return f"当前专题分析主要支持健康领域，暂不提供「{query_type}」类型的专业解释。"
        
        # 提取卦象信息
        ben_gua = gua_result["ben_gua"]
        bian_gua = gua_result["bian_gua"]
        dong_yao = gua_result["dong_yao"]
        shi_yao = gua_result["shi_yao"]
        najia = gua_result.get("najia", ["未知"] * 6)
        liuqin = gua_result.get("liuqin", ["未知"] * 6)
        liushen = gua_result.get("liushen", ["未知"] * 6)
        
        # 获取健康分析结果
        health_result = health_analyzer.analyze_health(
            gua_result, day_master=day_master, yong_shen=None
        )
        
        # 组合解释
        explanation = "【健康专题分析】\n\n"
        
        # 添加卦象概述
        explanation += "一、卦象健康概述\n"
        
        # 获取卦名
        ben_gua_name = ben_gua["name"]
        bian_gua_name = bian_gua["name"]
        
        # 判断卦象健康吉凶
        ben_health_state = "有利" if ben_gua_name in self.health_gua_relations["有利卦象"] else "不利" if ben_gua_name in self.health_gua_relations["不利卦象"] else "中性"
        bian_health_state = "有利" if bian_gua_name in self.health_gua_relations["有利卦象"] else "不利" if bian_gua_name in self.health_gua_relations["不利卦象"] else "中性"
        
        explanation += f"本卦「{ben_gua_name}」对健康{ben_health_state}，变卦「{bian_gua_name}」对健康{bian_health_state}。\n"
        
        # 健康整体评估
        if health_result.get("overall"):
            explanation += f"整体评估：{health_result['overall']}\n"
        
        # 添加动爻健康解析
        explanation += "\n二、动爻健康分析\n"
        
        # 动爻爻位信息
        dong_yao_idx = dong_yao - 1
        explanation += f"{self.yao_health_relations.get(dong_yao, '未知爻位')}\n"
        
        # 动爻六亲信息
        if dong_yao_idx < len(liuqin):
            dong_liuqin = liuqin[dong_yao_idx]
            if dong_liuqin in self.liuqin_health_relations:
                liuqin_info = self.liuqin_health_relations[dong_liuqin]
                explanation += f"动爻六亲为「{dong_liuqin}」：{liuqin_info['健康含义']}\n"
                explanation += f"相关系统：{liuqin_info['相关系统']}\n"
                explanation += f"可能症状：{liuqin_info['症状表现']}\n"
                explanation += f"调理建议：{liuqin_info['治疗建议']}\n"
        
        # 动爻六神信息
        if dong_yao_idx < len(liushen):
            dong_liushen = liushen[dong_yao_idx]
            if dong_liushen in self.liushen_health_relations:
                liushen_info = self.liushen_health_relations[dong_liushen]
                explanation += f"动爻六神为「{dong_liushen}」：{liushen_info['健康含义']}\n"
                explanation += f"影响：{liushen_info['健康影响']}\n"
                explanation += f"注意：{liushen_info['注意事项']}\n"
        
        # 添加纳甲五行健康分析
        explanation += "\n三、五行健康分析\n"
        
        if dong_yao_idx < len(najia):
            dong_yao_najia = najia[dong_yao_idx]
            if len(dong_yao_najia) >= 2:
                dong_gan, dong_zhi = dong_yao_najia[0], dong_yao_najia[1:]
                
                # 分析天干五行
                from models.bazi.calculator import get_element
                dong_gan_element = get_element(dong_gan)
                
                if dong_gan_element in self.wuxing_health_relations:
                    wuxing_info = self.wuxing_health_relations[dong_gan_element]
                    explanation += f"动爻天干五行为「{dong_gan_element}」\n"
                    explanation += f"相关系统：{wuxing_info['相关系统']}\n"
                    explanation += f"常见病症：{wuxing_info['常见病症']}\n"
                    explanation += f"饮食调理：宜食用{wuxing_info['饮食调理']}\n"
                    explanation += f"运动建议：适合{wuxing_info['运动建议']}\n"
        
        # 添加疾病类型分析
        explanation += "\n四、疾病类型分析\n"
        
        # 判断最可能的疾病类型
        disease_types = []
        for disease_type, info in self.disease_gua_relations.items():
            if ben_gua_name in info["相关卦象"] or bian_gua_name in info["相关卦象"]:
                disease_types.append(disease_type)
        
        if disease_types:
            explanation += f"根据卦象分析，疾病可能属于{'、'.join(disease_types)}类型。\n"
            for disease_type in disease_types:
                info = self.disease_gua_relations[disease_type]
                explanation += f"• {disease_type}：{info['特点']}\n"
                explanation += f"  对策：{info['对策']}\n"
        else:
            explanation += "卦象未明确指示特定疾病类型，需结合具体症状进一步分析。\n"
        
        # 添加健康建议
        explanation += "\n五、健康建议\n"
        
        # 来自健康分析器的建议
        if "recommendations" in health_result:
            for i, rec in enumerate(health_result["recommendations"], 1):
                if i <= 5:  # 最多显示5条建议
                    explanation += f"{i}. {rec}\n"
        
        # 根据卦象变化趋势提供建议
        explanation += "\n六、健康趋势\n"
        
        if ben_health_state == "有利" and bian_health_state == "有利":
            explanation += "健康状况良好，保持现有生活习惯和保健方式。\n"
            explanation += "建议：定期体检，均衡饮食，保持适度运动，充足休息。\n"
        elif ben_health_state == "不利" and bian_health_state == "有利":
            explanation += "健康状况有望改善，当前治疗或调理方向正确。\n"
            explanation += "建议：坚持医嘱，保持良好心态，循序渐进恢复，避免操之过急。\n"
        elif ben_health_state == "有利" and bian_health_state == "不利":
            explanation += "健康状况可能走下坡路，需警惕潜在健康问题。\n"
            explanation += "建议：增强预防意识，避免过度劳累，及时就医检查，调整生活方式。\n"
        elif ben_health_state == "不利" and bian_health_state == "不利":
            explanation += "健康状况不佳，病情可能持续或加重。\n"
            explanation += "建议：积极寻求专业医疗帮助，调整治疗方案，改善生活环境，保持良好心态。\n"
        else:
            explanation += "健康状况变化不明显，需结合具体情况判断。\n"
            explanation += "建议：关注身体变化，保持健康生活方式，有异常及时就医。\n"
        
        # 添加日常保健建议
        explanation += "\n七、日常保健建议\n"
        
        explanation += "1. 生活规律：保持规律作息，充足睡眠，避免熬夜。\n"
        explanation += "2. 均衡饮食：多样化饮食，控制油盐糖摄入，适量蛋白质，丰富蔬果。\n"
        explanation += "3. 适度运动：每周3-5次，每次30分钟以上的有氧运动。\n"
        explanation += "4. 心理调节：保持积极心态，适当减压，培养兴趣爱好。\n"
        explanation += "5. 环境调适：保持居住环境干净整洁，空气流通，避免有害物质。\n"
        
        return explanation


# 单例模式，导出一个实例
specific_query_interpreter = SpecificQueryInterpreter()
