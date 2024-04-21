"""apidemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ninja import File, NinjaAPI
from ninja.errors import AuthenticationError
from ninja_extra import exceptions as extra_exceptions
from ninja_jwt.routers.obtain import obtain_pair_router

from employee.views import router as employee_router

api_v1 = NinjaAPI(version="1.0.0")

api_v1.add_router("/employee/", employee_router)
api_v1.add_router("/token", tags=["Auth"], router=obtain_pair_router)


def obtain_token_exception_handler(request, exc):

    if isinstance(exc, extra_exceptions.APIException):
        data = {
            "message": exc.detail.get("detail", str(exc)),
            "success": False,
            "data": None,
        }
    else:  # pragma: no cover
        data = {"message": exc.detail, "success": False, "data": None}

    response = api_v1.create_response(request, data, status=exc.status_code)

    return response


def auth_error_exception_handler(request, exc): # pragma: no cover
    data = {
        "message": "AuthenticationError",
        "success": False,
        "data": None,
    }
    response = api_v1.create_response(request, data, status=401)
    return response


api_v1.exception_handler(extra_exceptions.APIException)(obtain_token_exception_handler)
api_v1.exception_handler(AuthenticationError)(auth_error_exception_handler)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api_v1.urls),
]
