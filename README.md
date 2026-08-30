# ecommerce

FastAPI + MySQL 电商项目骨架（环境配置练习）。

## 技术栈

- Python 3.12 + [uv](https://docs.astral.sh/uv/)（包管理与虚拟环境）
- FastAPI + SQLAlchemy(async) + asyncmy
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)（类型化环境配置）
- MySQL 8（docker-compose）

## 快速开始

```bash
# 1. 安装依赖（创建 .venv 并同步 uv.lock）
uv sync

# 2. 启动数据库
docker compose up -d

# 3. 准备本地环境变量
cp .env.example .env.dev   # 按需修改，如数据库密码

# 4. 运行
uv run python -m app.main
```

## 环境配置机制

配置读取优先级：**环境变量 > .env.<ENVIRONMENT> 文件 > 代码默认值**。

- `ENVIRONMENT`（默认 `dev`）决定读取哪个 `.env.<环境>` 文件；
- 所有 `.env.*` 已被 gitignore 排除，`.env.example` 是唯一提交的模板；
- 测试/生产环境不要携带 `.env` 文件，直接由 CI/CD 或密钥管理注入真实环境变量；
- 配置在代码里以 `Settings` 模型声明，类型错误启动即报错，不会运行时才炸。
- 生产环境（`ENVIRONMENT=prod`）启动即 fail-fast：SECRET_KEY 必须 32 位以上随机串、数据库密码不能是默认值、`DEBUG` 必须为 False，否则拒绝启动。

```python
from config.settings import get_settings

settings = get_settings()   # 进程内缓存，重复调用开销可忽略
print(settings.DATABASE_URL)
```

## 切换运行环境

```bash
# Windows PowerShell
$env:ENVIRONMENT='test'; uv run python -m app.main

# bash / CI
ENVIRONMENT=test uv run python -m app.main
```

启动日志会打印当前环境；环境变量（如 `SERVER_PORT`）始终优先于 .env 文件。

## 开发常用命令

```bash
uv add <包名>              # 添加依赖（自动更新 lock）
uv add --group dev <包名>  # 添加开发依赖
uv run pytest              # 跑测试
uv run ruff check .        # 代码检查
```

> 入口：`app/main.py` 是 FastAPI 应用，启动时打印当前环境与数据库连接串；`/health/db` 可实测数据库连通。
