from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from typing import Optional

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    根据用户名从数据库获取用户。
    """
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    根据邮箱从数据库获取用户。
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_phone(db: Session, phone: str) -> Optional[User]:
    """
    根据手机号从数据库获取用户。
    """
    return db.query(User).filter(User.phone == phone).first()

def create_user(db: Session, user: UserCreate) -> User:
    """
    创建新用户并将其保存到数据库。
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        phone=user.phone,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # 刷新 db_user 以获取数据库生成的数据（如 id）
    return db_user