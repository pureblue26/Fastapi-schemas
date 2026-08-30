"""FastAPI 应用入口：演示环境配置如何驱动服务启动。

启动方式：
    uv run python -m app.main            # 开发环境（读 .env.dev）
    $env:ENVIRONMENT='test'; uv run python -m app.main   # 测试环境
"""
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from config.settings import get_settings

# 让日志能打印到控制台（uvicorn 自带的日志配置不会给 root logger 挂 handler）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("ecommerce")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动/关闭钩子：进程一启动就读配置、打印环境信息。"""
    settings = get_settings()
    logger.info("应用启动 | 环境=%s | DEBUG=%s", settings.ENVIRONMENT.value, settings.DEBUG)
    logger.info("数据库连接串: %s", settings.DATABASE_URL)
    yield
    logger.info("应用关闭")


settings = get_settings()  # 模块级单例（lru_cache 保证整个进程只解析一次）

app = FastAPI(
    title="Ecommerce API",
    version=settings.VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """根路径：返回环境信息（不含任何密钥）。"""
    return {
        "app": "ecommerce",
        "environment": settings.ENVIRONMENT.value,
        "version": settings.VERSION,
        "debug": settings.DEBUG,
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """轻量健康检查：不碰数据库。"""
    return {"status": "ok", "environment": settings.ENVIRONMENT.value}


@app.get("/health/db")
async def health_db():
    """数据库连通性检查：用 settings.DATABASE_URL 实际连一次。

    MySQL 没启动时也会返回明确的错误信息，而不是应用静默挂掉。
    """
    engine = create_async_engine(settings.DATABASE_URL)
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        return {"status": "error", "database": str(exc)[:200]}
    finally:
        await engine.dispose()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",          # import 字符串形式：以后开 reload 热重载也支持
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
    )
