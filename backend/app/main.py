from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn # 仅用于本地运行入口点
from app.api.v1.router import api_router

app = FastAPI(
    title="Bazi App API",
    description="A FastAPI backend for Bazi fortune-telling application.",
    version="0.1.0",
)
# 注册 API 路由
app.include_router(api_router, prefix="/api/v1") # 新增这行
# 配置 CORS (跨域资源共享)
# 允许前端在开发阶段访问后端

origins = [
    "http://localhost",
    "http://localhost:5173", # 你的前端开发服务器地址
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    """
    根路径，简单的欢迎消息。
    """
    return {"message": "Welcome to Bazi App API!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)