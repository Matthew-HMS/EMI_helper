from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("api", views.ClassView.as_view(), name="class_view"),
]
