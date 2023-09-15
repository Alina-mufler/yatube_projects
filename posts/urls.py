from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.index),
    # Страница с постами, отфильтрованными по группам
    path('group/<slug:pk>/', views.group_posts),
]