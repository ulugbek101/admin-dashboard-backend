from django.contrib import admin
from django.urls import path, include, re_path

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/profiles/', include('app_users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(prefix=settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(prefix=settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
