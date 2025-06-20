from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[str] = Field(None, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9]{7,15}$")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6) # 密码至少6位

class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_active: bool = True
    is_admin: bool = False

    class Config:
        # Pydantic V2+ 使用 from_attributes 代替 orm_mode
        from_attributes = True

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True # 确保能够从 SQLAlchemy 模型创建