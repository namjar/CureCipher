import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 导入API路由
from services.api import create_app
from services.api.routes import api_router

# 创建FastAPI应用
app = create_app()

# 确保前端目录存在
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend", "public")
logger.debug(f"前端目录路径: {frontend_dir}")

# 确保目录存在
if not os.path.exists(frontend_dir):
    logger.warning(f"前端目录不存在，创建目录: {frontend_dir}")
    os.makedirs(frontend_dir, exist_ok=True)
    
    # 确保CSS和JS目录存在
    css_dir = os.path.join(frontend_dir, "css")
    js_dir = os.path.join(frontend_dir, "js")
    os.makedirs(css_dir, exist_ok=True)
    os.makedirs(js_dir, exist_ok=True)
    
    # 创建基本的index.html文件
    index_html_path = os.path.join(frontend_dir, "index.html")
    if not os.path.exists(index_html_path):
        with open(index_html_path, 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CureCipher</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
        }
        .container {
            margin-top: 80px;
        }
        h1 {
            color: #1890ff;
            font-size: 2.5em;
        }
        .btn {
            display: inline-block;
            margin: 10px;
            padding: 12px 24px;
            background-color: #1890ff;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        .btn:hover {
            background-color: #096dd9;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>CureCipher 中医健康管理系统</h1>
        <p>系统已成功启动!</p>
        
        <div class="buttons">
            <a href="/bazi" class="btn">八字分析</a>
            <a href="/liuyao" class="btn">六爻排盘</a>
            <a href="/api" class="btn">API信息</a>
        </div>
        
        <p style="margin-top: 40px;">
            <small>这是一个简化版页面，仅用于测试服务器连接</small>
        </p>
    </div>
</body>
</html>
""")
        logger.info(f"创建了默认index.html: {index_html_path}")

# 输出前端文件列表
if os.path.exists(frontend_dir):
    logger.debug("前端目录存在，列出文件:")
    for root, dirs, files in os.walk(frontend_dir):
        for file in files:
            logger.debug(f"  - {os.path.join(root, file)}")
else:
    logger.error(f"前端目录仍然不存在: {frontend_dir}")

# 注册API路由
app.include_router(api_router, prefix="")

# 挂载静态文件
app.mount("/static", StaticFiles(directory="frontend/public"), name="static")

# 根路径路由 - 这个必须在通配符路由之前定义
@app.get("/")
async def root():
    frontend_path = os.path.join("frontend", "public", "index.html")
    logger.debug(f"根路径请求: 检查index.html路径: {frontend_path}")
    
    if os.path.exists(frontend_path):
        logger.debug("根路径: 返回index.html")
        return FileResponse(frontend_path)
    else:
        logger.error(f"根路径: index.html文件不存在: {frontend_path}")
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>CureCipher</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; text-align: center; }
        .container { max-width: 800px; margin: 100px auto; }
        .btn { display: inline-block; margin: 10px; padding: 10px 20px; background: #1890ff; color: white; 
              text-decoration: none; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>CureCipher 中医健康管理系统</h1>
        <p>系统已成功启动!</p>
        <div>
            <a href="/bazi" class="btn">八字分析</a>
            <a href="/liuyao" class="btn">六爻排盘</a>
            <a href="/api" class="btn">API信息</a>
        </div>
    </div>
</body>
</html>
"""
        return HTMLResponse(content=html_content)

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

# 前端路由处理 - 这个必须在最后定义
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    logger.debug(f"请求路径: {full_path}")
    
    # API路由不走前端路由
    if full_path.startswith("api/"):
        logger.debug(f"API路由不处理: {full_path}")
        raise HTTPException(status_code=404, detail="API path not found")
    
    # 先检查是否是静态文件
    static_file_path = os.path.join("frontend", "public", full_path)
    logger.debug(f"检查静态文件路径: {static_file_path}")
    
    if os.path.exists(static_file_path) and os.path.isfile(static_file_path):
        logger.debug(f"返回静态文件: {static_file_path}")
        return FileResponse(static_file_path)
    
    # 如果不是静态文件，返回index.html，由前端路由处理
    frontend_path = os.path.join("frontend", "public", "index.html")
    logger.debug(f"检查index.html路径: {frontend_path}")
    
    if os.path.exists(frontend_path):
        logger.debug("返回index.html")
        return FileResponse(frontend_path)
    else:
        logger.error(f"index.html文件不存在: {frontend_path}")
        html_content = """<!DOCTYPE html>
<html>
<head>
    <title>CureCipher</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; text-align: center; }
        .container { max-width: 800px; margin: 100px auto; }
        .btn { display: inline-block; margin: 10px; padding: 10px 20px; background: #1890ff; color: white; 
              text-decoration: none; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>CureCipher 中医健康管理系统</h1>
        <p>页面加载错误: index.html文件不存在</p>
        <p>请检查前端文件是否已正确安装</p>
    </div>
</body>
</html>
"""
        return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
