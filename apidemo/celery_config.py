# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
from datetime import timedelta
from logging.handlers import RotatingFileHandler

from celery import Celery, platforms, shared_task
from celery.schedules import crontab
from celery.signals import after_setup_logger

logger = logging.getLogger(__name__)

platforms.C_FORCE_ROOT = True
# https://www.celerycn.io/fu-lu/django
# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rhea.settings')
app = Celery("proj")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
settings_module_obj = os.getenv("DJANGO_SETTINGS_MODULE")
app.config_from_object(settings_module_obj, namespace="CELERY")

app.autodiscover_tasks()

app.conf.update(
    CELERY_BEAT_SCHEDULER="django_celery_beat.schedulers:DatabaseScheduler",
    task_reject_on_worker_lost=True,
    task_acks_late=True,
    # celery worker的并发数 根据并发量是适当配置，不易太大
    CELERYD_CONCURRENCY=20,
    # 每个worker执行了多少次任务后就会死掉，建议数量大一些
    CELERYD_MAX_TASKS_PER_CHILD=300,
    # 每个worker一次性拿的任务数
    CELERYD_PREFETCH_MULTIPLIER=1,
)


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    # fh = logging.FileHandler("logs/celery.log", "a", encoding="utf-8")  # 这个是python3的
    # 使用RotatingFileHandler替代FileHandler
    # maxBytes设置为50MB，backupCount设置为5，意思是日志文件会轮转5个，每个日志文件最大50MB
    fh = RotatingFileHandler(
        "logs/celery.log",
        "a",
        maxBytes=50 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    fh.setLevel(logging.INFO)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # 定义handler的输出格式
    formatter = logging.Formatter(
        "%(asctime)s  %(levelname)s  [pid:%(process)d] [%(name)s %(filename)s->%(funcName)s:%(lineno)s] %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)


@shared_task(name="apidemo.celery_config.test.ping124")
def ping123():
    print("pong.......")


@app.task(bind=True)
def test(self):
    print("test task......")


app.conf.beat_schedule = {
    "ping123": {
        "task": "apidemo.celery_config.test.ping124",
        "schedule": timedelta(seconds=3),
    },
    "test": {
        "task": "apidemo.celery_config.test",
        "schedule": timedelta(seconds=3),
    },
}
