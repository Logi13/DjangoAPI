from django.urls import re_path, include

from modernizr import test_views

urlpatterns = [
    re_path(r'^$', test_views.test_view),
    re_path(r'^content-length/$', test_views.test_view_with_content_length),
    re_path(r'^charset/$', test_views.test_view_with_charset),
    re_path(r'^404/$', test_views.test_view_404),
    re_path(r'^css/$', test_views.test_css),
    re_path(r'^tag/$', test_views.test_tag),
    re_path(r'^no-tag/$', test_views.test_no_tag),
]