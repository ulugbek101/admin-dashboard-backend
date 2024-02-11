from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('main.urls')),
    path('api/v1/profiles/', include('users.urls')),
]
