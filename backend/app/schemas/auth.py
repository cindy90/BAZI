from pydantic import BaseModel
from app.schemas.user import UserCreate # 导入我们刚刚定义的 UserCreate

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(UserCreate):
    # 继承 UserCreate 的所有字段，例如 username, email, phone, password
    pass