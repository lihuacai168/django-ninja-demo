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


from employee.views import router as employee_router


from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, File


api_v1 = NinjaAPI(version='1.0.0')

api_v1.add_router('/employee/', employee_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api_v1.urls),
]
