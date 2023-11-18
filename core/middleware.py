# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: middleware.py
# @Time : 2023/8/19 11:46
# @Email: lihuacai168@gmail.com


import json
from typing import Callable

from django.http import HttpResponse, JsonResponse


class ResponseDataRequestIDMiddleware:
    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.headers._store.get("trace_id") and isinstance(
            response, (HttpResponse, JsonResponse)
        ):
            try:
                data: dict = json.loads(response.content)
                _, data["trace_id"] = response.headers._store.get("trace_id")
                _response = JsonResponse(data)
                _response.status_code = response.status_code
                response = _response

            except Exception:
                ...

        return response
