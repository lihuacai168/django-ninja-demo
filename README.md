# Features
- Easy and fast CURD
- Stand format response
- Log and response trace_id
![easy_and_fast_crud](assets/easy_and_fast_crud.png)
![stand_response](assets/stand_response.png)
![response_trace_id](assets/response_trace_id.png)
![log_trace_id](assets/log_trace_id.png)


# Quick start
## Clone code
`git clone https://github.com/lihuacai168/django-ninja-demo.git`


## Docker-compose

```shell
# set env
cp .env.example .env
```

## Make sure db have migrated
    
```shell
# start app
docker-compose -f docker-compose-without-db.yml --env-file=${PWD}/.env up --build
```


## Local Dev

## Create virtualenv
```
python3 -m venv venv
```

## Activate virtualenv
```
source venv/bin/activate
```

## Install dependencies
```
cd django-ninja-demo && pip install -r requirements.txt
```

## Migrate db
```
python manage.py migrate
```

## Start app
```
python manage.py runserver localhost:8000
```

## Open api docs [open in browser](http://localhost:8000/api/docs)


## Obtain access token
![img.png](assets/obtain_token_request.png)
![img_1.png](assets/obtain_token_response.png)


## Authorize and request API
![img.png](assets/authorize.png)
![img_1.png](assets/request_api.png)

# Celery
## Config celery broker
```python
# setting.py
broker_url = "redis://127.0.0.1:6379/0"
```
## Run celery worker
```shell
# start celery worker, using command line
python -m celery -A apidemo.celery_config worker -l INFO 
```

## PyCharm run_celery_worker_configuration
![pycharm_run_celery_worker_configuration](assets/celery_worker.png)


## Run celery beat
```shell
# start celery beat, using command line
python -m celery -A apidemo.celery_config beat -l DEBUG 
```

## PyCharm run_celery_beat_configuration
![pycharm_run_celery_beat_configuration](assets/celery_beat.png)