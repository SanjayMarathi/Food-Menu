# mysite/urls.py

"""
URL configuration for mysite project.
...
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)