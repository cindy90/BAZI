from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from typing import Generator

# DATABASE_URL 从 settings 中获取，例如 "postgresql://user:password@host:port/dbname"
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# SessionLocal 是一个数据库会话的生成器
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI 依赖注入，用于获取数据库会话。
    确保会话在请求结束后关闭。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()