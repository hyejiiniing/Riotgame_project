from django.contrib import admin
from django.urls import path, include
from riot_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('riot/', include('riot_app.urls')),  # riot_app의 URL 설정을 포함
    path('', views.home_view, name='home'),  # 루트 URL을 home_view로 매칭
]
