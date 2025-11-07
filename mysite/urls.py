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
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('users/', include('users.urls')),
    path("how-to-use/", TemplateView.as_view(template_name="myapp/how_to_use.html"), name="how_to_use"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)