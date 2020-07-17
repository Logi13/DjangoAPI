from django.urls import re_path
from . import test_views

urlpatterns = [
    re_path(r'^$', test_views.test_view),
]