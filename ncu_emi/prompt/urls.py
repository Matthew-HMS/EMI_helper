from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.PromptView.as_view()),
]

# from django.contrib import admin
# from django.urls import path
# from .views import PromptView

# urlpatterns = [
#     path('', PromptView.as_view(), name='prompt-list'),  # GET 和 POST
#     path('<int:pk>/', PromptView.as_view(), name='prompt-detail'),  # PATCH 和 DELETE
# ]
