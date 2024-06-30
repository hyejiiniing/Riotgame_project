from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('riot/', include('riot_app.urls')),
    path('', include('riot_app.urls')),  # 빈 경로를 riot_app.urls로 포함시킴
]
