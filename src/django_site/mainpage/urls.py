from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
# from api import views

from . import views

basic = [
    re_path(r'^[/]?$', views.index, name='index'),
    re_path(r'^image-serve[/]?$', views.imageServe, name='imageServe'),
    #path('', include('websockets.urls')),
    #path('admin/', admin.site.urls),
    #path('api/', include('api.urls')),
]

prefix = settings.APP_URL_PREFIX
if(settings.SERVER_HAS_PREFIX_ALIAS):
    prefix = ''

urlpatterns = [
    path('' + prefix, include(basic)),
]