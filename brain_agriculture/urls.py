from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('dashboards/', include('dashboards.urls')),
]

if settings.DEBUG:  # Servir media com Django no DEV
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = [
        # path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
