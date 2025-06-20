from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router # 暂时是空的，但我们先准备好

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)