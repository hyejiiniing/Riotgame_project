from django.urls import path
from . import views

urlpatterns = [
    path('champion-rotation/', views.champion_rotation_view, name='champion_rotation_view'),
    path('', views.home_view, name='home'),  # 빈 경로를 home_view와 연결
]
