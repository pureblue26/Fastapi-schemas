from pydantic_settings import BaseSettings, SettingsConfigDict
from config.path_config import ENV_FILE
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict( env_file=f".env.{os.getenv('ENVIRONMENT', 'dev')}",
        extra="ignore",
        env_file_encoding="utf-8",
    )
    """"环境配置"""
    DEBUG:bool
    VERSION:str
    """"服务器配置"""
    SERVER_HOST:str
    SERVER_PORT:int 
    SECRET_KEY: str
    """"数据库配置"""
    DATABASE_URL: str


def get_settings()->Settings:
    return Settings()