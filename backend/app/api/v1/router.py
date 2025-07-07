# backend/app/api/v1/router.py
from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .bazi import router as bazi_router
from .iching import router as iching_router  # 新增易经算卦路由

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(bazi_router)
api_router.include_router(iching_router)  # 新增易经算卦路由