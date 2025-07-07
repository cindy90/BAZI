from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.session import get_db
from app.schemas import auth as auth_schemas
from app.schemas import user as user_schemas
from app.crud import user as crud_user
from app.core.security import verify_password, create_access_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["认证"])

@router.post("/register", response_model=user_schemas.UserResponse)
def register_user(user_in: auth_schemas.RegisterRequest, db: Session = Depends(get_db)):
    """
    用户注册。
    """
    # 检查用户名是否已存在
    existing_user_by_username = crud_user.get_user_by_username(db, username=user_in.username)
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已被注册",
        )
    # 检查邮箱是否已存在 (如果提供了邮箱)
    if user_in.email:
        existing_user_by_email = crud_user.get_user_by_email(db, email=user_in.email)
        if existing_user_by_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册",
            )
    # 检查手机号是否已存在 (如果提供了手机号)
    if user_in.phone:
        existing_user_by_phone = crud_user.get_user_by_phone(db, phone=user_in.phone)
        if existing_user_by_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="手机号已被注册",
            )

    db_user = crud_user.create_user(db, user=user_in)
    return db_user

@router.post("/token", response_model=auth_schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    用户登录并获取 JWT 访问令牌。
    """
    user = crud_user.get_user_by_username(db, username=form_data.username)
    if not user or not getattr(user, "hashed_password", None) or not verify_password(form_data.password, getattr(user, "hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或密码不正确",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}