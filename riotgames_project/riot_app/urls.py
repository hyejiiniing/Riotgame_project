from django.urls import path
from . import views

urlpatterns = [
    path('summoner/<str:summoner_name>/', views.summoner_view, name='summoner_view'),
]
