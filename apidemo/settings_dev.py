# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: settings_dev.py.py
# @Time : 2023/6/15 09:57
# @Email: lihuacai168@gmail.com

from .settings import *


DEBUG = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "ninja_demo",
        "HOST": "localhost",
        "PORT": 3306,
        "USER": "root",
        "PASSWORD": "123456",
        "OPTIONS": {"charset": "utf8mb4"},
    }
}
