[![Github Actions](https://github.com/lihuacai168/django-ninja-demo/actions/workflows/django-test.yml/badge.svg)](https://github.com/lihuacai168/django-ninja-demo/actions)
[![codecov](https://codecov.io/gh/lihuacai168/django-ninja-demo/branch/main/graph/badge.svg)](https://app.codecov.io/gh/lihuacai168/django-ninja-demo)
![Dynamic YAML Badge](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Flihuacai168%2Fdjango-ninja-demo%2Fmain%2F.github%2Fworkflows%2Fdjango-test.yml&query=%24.jobs.build.strategy.matrix%5B'python-version'%5D&style=flat-square&logo=python&logoColor=blue&label=Python&color=yellow)

# Key Features
- 🛡️ **High Coverage: Rigorous unit tests for robust codebase assurance.**
- 😊 **Fast CRUD Router: Quick and easy create, read, update, and delete operations.**
- ✅ **Uniform API: Consistent responses throughout the service.**
- 🔍 **Trace IDs:  Simplified issue tracking with trace IDs in logs**
- 🚀 **Modern Dependency Management: Using uv for fast and reliable Python package management**
![fast_curd](assets/fast_curd.png)
![stand_response](assets/stand_response.png)
![response_trace_id](assets/response_trace_id.png)
![log_trace_id](assets/log_trace_id.png)


# Quick start
## Clone code
```shell
git clone https://github.com/lihuacai168/django-ninja-demo.git
cd django-ninja-demo
```

## Local Development

### Install uv
```shell
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Setup Development Environment
```shell
# Create virtual environment and activate it
uv venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Install all dependencies (including dev dependencies)
uv sync

# Or install without dev dependencies for production
uv sync --no-dev
```

### Database Setup
```shell
uv run python manage.py migrate
```

### Start Development Server
```shell
# 开发环境启动
uv run python manage.py runserver localhost:8000

# 或使用 gunicorn 启动（生产环境推荐）
# 使用 4 个 worker
uv run gunicorn apidemo.wsgi:application --workers=4 --bind=0.0.0.0:8000

# 使用 gevent worker
uv run gunicorn apidemo.wsgi:application --worker-class=gevent --workers=4 --bind=0.0.0.0:8000

# 后台运行
uv run gunicorn apidemo.wsgi:application --daemon --workers=4 --bind=0.0.0.0:8000 --pid=/tmp/gunicorn.pid --access-logfile=/var/log/gunicorn/access.log --error-logfile=/var/log/gunicorn/error.log

# 停止后台运行的 gunicorn
kill -9 $(cat /tmp/gunicorn.pid)
```

## Docker Deployment

### Environment Setup
```shell
# Copy environment configuration
cp .env.example .env
```

### Build and Run
```shell
# Build and start the application
docker-compose -f docker-compose-without-db.yml --env-file=${PWD}/.env up --build
```

## API Documentation
Visit [http://localhost:8000/api/docs](http://localhost:8000/api/docs) in your browser to view the API documentation.

## Authentication

### Obtain Access Token
![img.png](assets/obtain_token_request.png)
![img_1.png](assets/obtain_token_response.png)

### Authorize and Request API
![img.png](assets/authorize.png)
![img_1.png](assets/request_api.png)

# Celery Integration

## Configure Celery Broker
```python
# setting.py
broker_url = "redis://127.0.0.1:6379/0"
```

## Run Celery Worker
```shell
# Start celery worker
uv run celery -A apidemo.celery_config worker -l INFO
```

## Run Celery Beat
```shell
# Start celery beat
uv run celery -A apidemo.celery_config beat -l DEBUG
```

## IDE Configuration
### PyCharm Celery Worker Configuration
![pycharm_run_celery_worker_configuration](assets/celery_worker.png)

### PyCharm Celery Beat Configuration
![pycharm_run_celery_beat_configuration](assets/celery_beat.png)

# Development Notes

## Dependency Management
- Dependencies are managed through `pyproject.toml`
- Dependencies are locked in `uv.lock` for reproducible builds
- Use `uv sync` to install dependencies
- Use `uv sync --locked` to install dependencies with exact versions
- Use `uv lock` to regenerate the lock file
- Use `uv sync --upgrade` to upgrade dependencies
- Use `uv sync --no-dev` for production environments

### Using Mirror Sources
```shell
# 使用豆瓣源
export UV_INDEX_URL=https://pypi.doubanio.com/simple/
# 或使用清华源
export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
# 或使用阿里云源
export UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/

# 然后运行 uv 命令
uv sync  # 安装依赖
uv pip install package-name  # 安装单个包
```

对于 Windows PowerShell：
```powershell
# 使用豆瓣源
$env:UV_INDEX_URL = "https://pypi.doubanio.com/simple/"
# 或使用清华源
$env:UV_INDEX_URL = "https://pypi.tuna.tsinghua.edu.cn/simple/"
# 或使用阿里云源
$env:UV_INDEX_URL = "https://mirrors.aliyun.com/pypi/simple/"

# 然后运行 uv 命令
uv sync
```

对于 Windows CMD：
```cmd
# 使用豆瓣源
set UV_INDEX_URL=https://pypi.doubanio.com/simple/
# 或使用清华源
set UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
# 或使用阿里云源
set UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/

# 然后运行 uv 命令
uv sync
```

永久设置（推荐）：
```shell
# macOS/Linux: 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/' >> ~/.zshrc
source ~/.zshrc

# Windows: 在系统环境变量中添加 UV_INDEX_URL
```

## Testing
```shell
# Run tests with coverage
uv run coverage run --source='.' manage.py test

# Generate coverage report
uv run coverage xml
```