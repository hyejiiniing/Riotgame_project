from django.urls import path
from . import views
from .views import match_list, match_list_api

urlpatterns = [
    path('', views.home_view, name='home'),  # 빈 경로를 home_view와 
    path('matches/', match_list, name='match_list'),
    path('api/matches/<str:month>/', match_list_api, name='match_list_api'),
]
