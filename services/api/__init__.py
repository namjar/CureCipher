"""
CureCipher API 包初始化文件
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def create_app():
    """创建并配置FastAPI应用"""
    app = FastAPI(
        title="CureCipher API",
        description="中医与现代科技结合的健康管理平台API",
        version="0.1.0"
    )
    
    # 添加CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 上线后替换为具体域名
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app
