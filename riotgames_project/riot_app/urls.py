from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # 빈 경로를 home_view와 연결
]
