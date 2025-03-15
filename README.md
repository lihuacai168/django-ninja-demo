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
python manage.py migrate
```

### Start Development Server
```shell
python manage.py runserver localhost:8000
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
python -m celery -A apidemo.celery_config worker -l INFO
```

## Run Celery Beat
```shell
# Start celery beat
python -m celery -A apidemo.celery_config beat -l DEBUG
```

## IDE Configuration
### PyCharm Celery Worker Configuration
![pycharm_run_celery_worker_configuration](assets/celery_worker.png)

### PyCharm Celery Beat Configuration
![pycharm_run_celery_beat_configuration](assets/celery_beat.png)

# Development Notes

## Dependency Management
- Dependencies are managed through `pyproject.toml`
- Use `uv sync` to install dependencies
- Use `uv sync --upgrade` to upgrade dependencies
- Use `uv sync --no-dev` for production environments

## Testing
```shell
# Run tests with coverage
coverage run --source='.' manage.py test

# Generate coverage report
coverage xml
```