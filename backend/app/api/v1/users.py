# bazi_app/backend/app/api/v1/users.py

from fastapi import APIRouter

# 定义用户路由
router = APIRouter(prefix="/users", tags=["用户管理"])