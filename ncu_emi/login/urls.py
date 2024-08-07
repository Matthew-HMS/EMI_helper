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
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path("", views.login_view, name="login_view"),
    path("index/", views.index_view, name="index_view"),
    path("api/", views.LoginView.as_view()),
    path("register/", views.RegisterView.as_view()),
    path("api/logout/", views.LogoutView.as_view()),
    path('api/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
