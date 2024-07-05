from django.urls import path, include
from . import views
from .views import match_list, match_list_api
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),  # 빈 경로를 home_view와 
    path('matches/', match_list, name='match_list'),
    path('api/matches/<str:month>/', match_list_api, name='match_list_api'),
    path('champions/', views.champion_list, name='champion_list'),
    path('champions/<str:champion_id>/', views.champion_detail, name='champion_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)