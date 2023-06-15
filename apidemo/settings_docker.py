# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: 花菜
# @File: settings_dev.py.py
# @Time : 2023/6/15 09:57
# @Email: lihuacai168@gmail.com

from os import environ

from .settings import *

DEBUG = False

DB_NAME = environ.get("MYSQL_DATABASE")
DB_PORT = environ.get("MYSQL_PORT", 3306)
DB_HOST = environ.get("MYSQL_HOST", "db")
DB_USER = environ.get("MYSQL_USER", "root")
DB_PASSWORD = environ.get("MYSQL_PASSWORD", "root")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "NAME": DB_NAME,  # 新建数据库名
        "USER": DB_USER,  # 数据库登录名
        "PASSWORD": DB_PASSWORD,  # 数据库登录密码
    }
}
