"""
URL configuration for ncu_emi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls.conf import include, path
# edit by chou
from rest_framework.routers import DefaultRouter

# Import views from each application
from prompt import views as prompt_views
from login import views as login_views
from gpt import views as gpt_views
from index import views as index_views
from classes import views as class_views
from file import views as file_views
from ppt import views as ppt_views

# 創建一個默認的Router
router = DefaultRouter()
# 註冊 prompt 應用程式中的視圖集(views)
router.register(r'prompt', prompt_views.PromptView)
# router.register(r'login', login_views.LoginView)
# router.register(r'gpt', gpt_views.GptView)
# router.register(r'index', index_views.IndexView)
router.register(r'classes', class_views.ClassView)
router.register(r'file', file_views.FileView)
router.register(r'ppt', ppt_views.PptView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", include("login.urls")),
    path("gpt/", include("gpt.urls")),
    path("index/" , include("index.urls")),
    path("prompt/", include("prompt.urls")),
    path("classes/", include("classes.urls")),
    path("file/", include("file.urls")),
    path("ppt/", include("ppt.urls")),
    # edit by chou
    path('api/', include(router.urls)),  # 包含 API 路由
]
