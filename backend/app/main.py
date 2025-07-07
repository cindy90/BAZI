from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import uvicorn # 仅用于本地运行入口点
from dotenv import load_dotenv
import os

# 加载 .env 文件中的环境变量
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

from .api.v1.router import api_router

app = FastAPI(
    title="Bazi App API",
    description="A FastAPI backend for Bazi fortune-telling application.",
    version="0.1.0",
)
# 注册 API 路由
app.include_router(api_router, prefix="/api/v1") # 新增这行
# 配置 CORS (跨域资源共享)
# 允许前端在开发阶段访问后端

# 开发环境：允许所有源，支持完整的CORS功能
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有源
    allow_credentials=False,  # 当allow_origins=["*"]时，必须设为False
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],  # 明确列出支持的方法
    allow_headers=["*"],  # 允许所有头部
    expose_headers=["*"],  # 暴露所有响应头部
)

# 添加全局OPTIONS处理
@app.options("/{path:path}")
async def options_handler(path: str, request: Request):
    """处理所有路由的OPTIONS预检请求"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "86400",  # 24小时缓存
        }
    )

@app.get("/")
async def read_root():
    """
    根路径，简单的欢迎消息。
    """
    return {"message": "Welcome to Bazi App API!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)