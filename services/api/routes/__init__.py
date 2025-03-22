"""
API 路由包初始化文件
"""

from fastapi import APIRouter
from .bazi_routes import router as bazi_router

# 创建主路由
api_router = APIRouter()

# 注册子路由
api_router.include_router(bazi_router)

# 后续可以添加更多路由
# api_router.include_router(health_router)
# api_router.include_router(liuyao_router)
# 等等
