#!/usr/bin/env python3
"""
最小八字排盘服务器
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
import sys
import os

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services.bazi_calculator import calculate_bazi_data
from app.schemas.bazi import BaziCalculateRequest, BaziCalculateResponse

app = FastAPI(title="八字排盘API", version="1.0.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "八字排盘API服务正在运行"}

@app.post("/api/v1/bazi/calculate", response_model=BaziCalculateResponse)
async def calculate_bazi(request: BaziCalculateRequest):
    """计算八字排盘"""
    try:
        result = await calculate_bazi_data(request, quick_mode=False)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)
