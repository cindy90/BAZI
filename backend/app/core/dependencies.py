from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud import user as crud_user
from app.schemas import user as user_schemas
from app.core.config import settings

# 定义 OAuth2 方案，tokenUrl 指向我们获取 token 的 API 路径
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> user_schemas.UserResponse:
    """
    依赖函数：从 JWT Token 中获取当前用户。
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解码 JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if not isinstance(username, str) or not username:
            raise credentials_exception
        token_data = user_schemas.UserBase(
            username=username,
            email="test@example.com",   # 合法邮箱
            phone="+8613800138000"      # 合法手机号
        ) # 使用 UserBase 来验证 sub
    except JWTError:
        raise credentials_exception

    # 从数据库获取用户
    user = crud_user.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    if not bool(getattr(user, "is_active", False)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用",
        )
    # 返回 Pydantic 模型，不包含敏感信息
    return user_schemas.UserResponse.model_validate(user)