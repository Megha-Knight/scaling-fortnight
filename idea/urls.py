
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lab.urls')),
  # Include app URLs
]

if settings.DEBUG:  # Serve media files only during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
