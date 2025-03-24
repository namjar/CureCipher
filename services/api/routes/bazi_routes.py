"""
八字API路由

提供八字计算和分析的REST API端点
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import datetime

from models.bazi.calculator import calculate_bazi
from models.bazi.five_elements import analyze_five_elements
from models.bazi.shensha import analyze_shensha

# 创建路由
router = APIRouter(
    prefix="/api/bazi",
    tags=["bazi"],
    responses={404: {"description": "Not found"}},
)

# 请求模型
class BaziRequest(BaseModel):
    birth_year: int = Field(..., gt=1900, lt=2100, description="出生年份")
    birth_month: int = Field(..., ge=1, le=12, description="出生月份")
    birth_day: int = Field(..., ge=1, le=31, description="出生日期")
    birth_hour: int = Field(..., ge=0, le=23, description="出生小时（24小时制）")
    birth_minute: int = Field(0, ge=0, le=59, description="出生分钟")
    gender: str = Field(..., description="性别，male或female")
    city: Optional[str] = Field(None, description="出生城市")
    
    class Config:
        schema_extra = {
            "example": {
                "birth_year": 1977,
                "birth_month": 2,
                "birth_day": 25,
                "birth_hour": 20,
                "birth_minute": 50,
                "gender": "male",
                "city": "Beijing"
            }
        }

# 响应模型
class BaziResponse(BaseModel):
    bazi_result: Dict[str, Any]
    elements_result: Dict[str, Any]
    shensha_result: Dict[str, Any]
    
    class Config:
        schema_extra = {
            "example": {
                "bazi_result": {
                    "bazi": {
                        "year": "丁巳",
                        "month": "丙寅",
                        "day": "癸巳",
                        "hour": "辛亥"
                    }
                },
                "elements_result": {
                    "element_percentages": {
                        "木": 12.5,
                        "火": 31.25,
                        "土": 12.5,
                        "金": 12.5,
                        "水": 31.25
                    }
                },
                "shensha_result": {
                    "positive_impacts": [
                        {"name": "天乙"},
                        {"name": "文昌"}
                    ],
                    "negative_impacts": [
                        {"name": "劫煞"}
                    ]
                }
            }
        }

class BaziSummaryResponse(BaseModel):
    four_pillars: str
    day_master: str
    element_balance: str
    health_advice: str
    
    class Config:
        schema_extra = {
            "example": {
                "four_pillars": "丁巳 丙寅 癸巳 辛亥",
                "day_master": "癸水",
                "element_balance": "火水偏旺，土金木偏弱",
                "health_advice": "注意肾脏和泌尿系统健康，保持充足的睡眠，避免过度劳累，补充足够水分。"
            }
        }

@router.post("/calculate", response_model=BaziResponse, summary="计算八字并分析")
async def calc_bazi(request: BaziRequest):
    """
    计算八字并进行五行和神煞分析
    
    - **birth_year**: 出生年份
    - **birth_month**: 出生月份
    - **birth_day**: 出生日期
    - **birth_hour**: 出生小时（24小时制）
    - **birth_minute**: 出生分钟（可选，默认为0）
    - **gender**: 性别（male/female）
    - **city**: 出生城市（可选，默认为Beijing）
    
    返回八字计算结果、五行分析和神煞分析。
    """
    try:
        # 四舍五入小时
        rounded_hour = request.birth_hour
        if request.birth_minute >= 30:
            rounded_hour += 1
        
        if rounded_hour >= 24:
            rounded_hour = 0
        
        # 计算八字
        bazi_result = calculate_bazi(
            request.birth_year,
            request.birth_month,
            request.birth_day,
            rounded_hour,
            request.gender,
            city=request.city or "Beijing"
        )
        
        # 处理返回结果
        if isinstance(bazi_result, dict):
            if 'error' in bazi_result:
                # 如果出错，直接抛出异常
                raise HTTPException(status_code=500, detail=bazi_result['message'] if 'message' in bazi_result else bazi_result['error'])
            elif 'result' in bazi_result:
                # 提取结果数据
                bazi_result = bazi_result['result']
        
        # 分析五行
        elements_result = analyze_five_elements(bazi_result)
        
        # 分析神煞
        shensha_result = analyze_shensha(
            bazi_result.get("shensha", []),
            bazi_result["bazi"]["day_master_element"]
        )
        
        return {
            "bazi_result": bazi_result,
            "elements_result": elements_result,
            "shensha_result": shensha_result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算八字时出错: {str(e)}")

@router.post("/summary", response_model=BaziSummaryResponse, summary="获取八字简要分析")
async def get_bazi_summary(request: BaziRequest):
    """
    获取八字的简要分析
    
    - **birth_year**: 出生年份
    - **birth_month**: 出生月份
    - **birth_day**: 出生日期
    - **birth_hour**: 出生小时（24小时制）
    - **birth_minute**: 出生分钟（可选，默认为0）
    - **gender**: 性别（male/female）
    - **city**: 出生城市（可选，默认为Beijing）
    
    返回八字四柱、日主、五行平衡状况和健康建议的简要概述。
    """
    try:
        # 四舍五入小时
        rounded_hour = request.birth_hour
        if request.birth_minute >= 30:
            rounded_hour += 1
        
        if rounded_hour >= 24:
            rounded_hour = 0
        
        # 计算八字
        bazi_result = calculate_bazi(
            request.birth_year,
            request.birth_month,
            request.birth_day,
            rounded_hour,
            request.gender,
            city=request.city or "Beijing"
        )
        
        # 处理返回结果
        if isinstance(bazi_result, dict):
            if 'error' in bazi_result:
                # 如果出错，直接抛出异常
                raise HTTPException(status_code=500, detail=bazi_result['message'] if 'message' in bazi_result else bazi_result['error'])
            elif 'result' in bazi_result:
                # 提取结果数据
                bazi_result = bazi_result['result']
        
        # 分析五行
        elements_result = analyze_five_elements(bazi_result)
        
        # 构建四柱字符串
        four_pillars = f"{bazi_result['bazi']['year']} {bazi_result['bazi']['month']} {bazi_result['bazi']['day']} {bazi_result['bazi']['hour']}"
        
        # 构建日主字符串
        day_master = f"{bazi_result['bazi']['day_master']}{bazi_result['bazi']['day_master_element']}"
        
        # 构建五行平衡描述
        element_balance = elements_result['balance_analysis']['description']
        
        # 提取健康建议
        health_advice = elements_result['health_advice']['general_advice']
        
        return {
            "four_pillars": four_pillars,
            "day_master": day_master,
            "element_balance": element_balance,
            "health_advice": health_advice
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取八字简要分析时出错: {str(e)}")

@router.get("/health_advice", summary="获取基于八字的健康建议")
async def get_health_advice(
    birth_year: int = Query(..., gt=1900, lt=2100, description="出生年份"),
    birth_month: int = Query(..., ge=1, le=12, description="出生月份"),
    birth_day: int = Query(..., ge=1, le=31, description="出生日期"),
    birth_hour: int = Query(..., ge=0, le=23, description="出生小时（24小时制）"),
    birth_minute: int = Query(0, ge=0, le=59, description="出生分钟"),
    gender: str = Query(..., regex="^(male|female)$", description="性别，male或female"),
    city: Optional[str] = Query(None, description="出生城市")
):
    """
    获取基于八字的健康建议
    
    - **birth_year**: 出生年份
    - **birth_month**: 出生月份
    - **birth_day**: 出生日期
    - **birth_hour**: 出生小时（24小时制）
    - **birth_minute**: 出生分钟（可选，默认为0）
    - **gender**: 性别（male/female）
    - **city**: 出生城市（可选，默认为Beijing）
    
    返回基于八字的健康建议，包括饮食和运动指导。
    """
    try:
        # 四舍五入小时
        rounded_hour = birth_hour
        if birth_minute >= 30:
            rounded_hour += 1
        
        if rounded_hour >= 24:
            rounded_hour = 0
        
        # 计算八字
        bazi_result = calculate_bazi(
            birth_year,
            birth_month,
            birth_day,
            rounded_hour,
            gender,
            city=city or "Beijing"
        )
        
        # 处理返回结果
        if isinstance(bazi_result, dict):
            if 'error' in bazi_result:
                # 如果出错，直接抛出异常
                raise HTTPException(status_code=500, detail=bazi_result['message'] if 'message' in bazi_result else bazi_result['error'])
            elif 'result' in bazi_result:
                # 提取结果数据
                bazi_result = bazi_result['result']
        
        # 分析五行
        elements_result = analyze_five_elements(bazi_result)
        
        # 提取健康建议
        health_advice = elements_result['health_advice']
        diet_advice = elements_result['diet_advice']
        exercise_advice = elements_result['exercise_advice']
        
        # 组合返回结果
        result = {
            "general_advice": health_advice['general_advice'],
            "seasonal_advice": health_advice['seasonal_advice'],
            "health_risks": health_advice['health_risks'],
            "diet_recommendations": {
                "recommended_flavors": [
                    f"{flavor['flavor']}({flavor['effect']})" for flavor in diet_advice['recommended_flavors']
                ],
                "foods_to_avoid": [
                    f"{flavor['flavor']}({flavor['reason']})" for flavor in diet_advice['avoid_flavors']
                ],
                "seasonal_recipes": [
                    f"{recipe['name']}({recipe['effect']})" for recipe in diet_advice['seasonal_recipes']
                ]
            },
            "exercise_recommendations": [
                f"{exercise['exercise_types'][0]}({exercise['effect']})" for exercise in exercise_advice['recommended_exercises']
            ],
            "frequency_advice": exercise_advice['frequency_advice']
        }
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取健康建议时出错: {str(e)}")
