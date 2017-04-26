from django.conf.urls import url
import django
from . import views
import webserver.settings
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)