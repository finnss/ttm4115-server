from django.conf.urls import url
import django

from . import views
import webserver.settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^assets/(?P<path>.*)$', django.views.static.serve, {'document_root': webserver.settings.MEDIA_ROOT})
]