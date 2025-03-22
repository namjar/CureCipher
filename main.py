from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

# 导入API路由
from services.api import create_app
from services.api.routes import api_router

# 创建FastAPI应用
app = create_app()

# 注册API路由
app.include_router(api_router, prefix="")

@app.get("/")
async def root():
    return {"message": "欢迎使用CureCipher健康管理系统"}

@app.get("/api")
async def api_info():
    return {
        "name": "CureCipher API",
        "version": "0.1.0",
        "description": "中医与现代科技结合的健康管理平台API",
        "endpoints": [
            "/api/bazi/calculate",
            "/api/bazi/summary",
            "/api/bazi/health_advice"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
