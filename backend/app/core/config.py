# backend/app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict # <-- 确保这里导入了 SettingsConfigDict
import secrets # <-- 确保导入了 secrets，用于生成默认 SECRET_KEY

class Settings(BaseSettings):
    DATABASE_URL: str = ""
    # 你的 SECRET_KEY 已经有了，不需要再生成默认值，但如果你想用代码生成新的，可以这样
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24    # DeepSeek API 配置
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_TIMEOUT: int = 60  # 增加超时时间
    DEEPSEEK_TEMPERATURE: float = 0.7
    DEEPSEEK_MAX_TOKENS: int = 3000  # 增加最大令牌数

    # 使用 Pydantic v2 的 model_config 语法
    # 确保 env_file 和 extra="allow" (为了解决 PYTHONPATH 问题)
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="allow")

settings = Settings()