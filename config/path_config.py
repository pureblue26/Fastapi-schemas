"""路径与文件常量。"""
from pathlib import Path

# 项目根目录（用 __file__ 定位，和"当前工作目录"无关）
BASE_DIR = Path(__file__).resolve().parent.parent


def env_file(environment: str) -> Path:
    """返回指定环境对应的 .env 文件路径，如 .env.dev / .env.prod。"""
    return BASE_DIR / f".env.{environment}"
