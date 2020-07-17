"""
Django Modernizr middleware

Some parts borrowed from:
Django Debug Toolbar
Copyright (c) Rob Hudson and individual contributors.
https://github.com/robhudson/django-debug-toolbar
"""
from django.conf import settings
from django.http import HttpResponse, QueryDict
from django.template.loader import render_to_string
from django.utils.encoding import smart_text
from django.utils.http import http_date

from django.contrib.staticfiles.storage import staticfiles_storage

from modernizr.settings import contribute_to_settings

# Default settings needed by ModernizrMiddleware
contribute_to_settings({
    'MODERNIZR_STORAGE': 'cookie',
    'MODERNIZR_COOKIE_NAME': 'modernizr',
    'MODERNIZR_COOKIE_AGE': 60 * 60 * 24 * 7 * 2, # 2 weeks
    'MODERNIZR_COOKIE_DOMAIN': None,
    'MODERNIZR_COOKIE_SECURE': False,
    'MODERNIZR_COOKIE_PATH': '/',
    'MODERNIZR_SESSION_KEY': 'modernizr',
    'MODERNIZR_JS_URL': staticfiles_storage.url('js/modernizr-custom.js'),
    'MODERNIZR_SENTINEL_IMAGE_URL': staticfiles_storage.url('images/1.js'),
    'MODERNIZR_INCLUDE_TAG': 'body',
})

_HTML_TYPES = ('text/html', 'application/xhtml+xml')

def replace_insensitive(string, target, replacement):
    """
    Similar to string.replace() but is case insensitive
    Code borrowed from: http://forums.devshed.com/python-programming-11/case-insensitive-string-replace-490921.html
    """
    no_case = string.lower()
    index = no_case.rfind(target.lower())
    print("index:", index)
    if index >= 0:
        print("-----", string[:index] + replacement + string[index + len(target):])
        return string[:index] + replacement + string[index + len(target):]
    else: # no results so return the original string
        return string

class ModernizrMiddleware(object):
    def __init__(self, get_response):
        print("Init modernizr middleware...")
        self.get_response = get_response
        #self.add_modernizr()

    def __call__(self, request):
        print("Call modernizr middleware...")
        #self.add_modernizr()
        return self.get_response(request)

    def persist_modernizr(self, request):
        print("persist_modernizr...")
        data = request.GET
        if settings.MODERNIZR_STORAGE == 'cookie':
            self.get_response.set_cookie(settings.MODERNIZR_COOKIE_NAME,
                data.urlencode(),
                max_age=settings.MODERNIZR_COOKIE_AGE,
                expires=http_date(settings.MODERNIZR_COOKIE_AGE),
                domain=settings.MODERNIZR_COOKIE_DOMAIN,
                path=settings.MODERNIZR_COOKIE_PATH,
                secure=settings.MODERNIZR_COOKIE_DOMAIN or None)
        elif settings.MODERNIZR_STORAGE == 'session':
            request.session[settings.MODERNIZR_SESSION_KEY] = data
        else:
            raise ValueError("Invalid value for settings.MODERNIZR_STORAGE")
        print(data)
        return self.get_response

    def load_modernizr_from_storage(self, request):
        print("load_modernizr_from_storage...")
        data = None
        if settings.MODERNIZR_STORAGE == 'cookie':
            if settings.MODERNIZR_COOKIE_NAME in request.COOKIES:
                data = QueryDict(request.COOKIES[settings.MODERNIZR_COOKIE_NAME])
        elif settings.MODERNIZR_STORAGE == 'session':
            data = request.session.get(settings.MODERNIZR_SESSION_KEY)

        if data is not None:
            request.modernizr = dict([(k, bool(int(v))) for k,v in data.items()])
        else:
            request.modernizr = None
        print(data)

    def add_modernizr(self):
        print("add_modernizr...")
        modernizr_content = render_to_string('add_modernizr.html', {
            'modernizr_js_url': settings.MODERNIZR_JS_URL,
            'modernizr_sentinel_img_url': settings.MODERNIZR_SENTINEL_IMAGE_URL,
        })
        tag = u'</' + settings.MODERNIZR_INCLUDE_TAG + u'>'
        self.get_response.content = replace_insensitive(
            smart_text(self.get_response.content), 
            tag,
            smart_text(modernizr_content + tag))
        if self.get_response.get('Content-Length', None):
            self.get_response['Content-Length'] = len(self.get_response.content)
        return self.get_response

    def process_request(self, request):
        print("process_request...")
        self.load_modernizr_from_storage(request)
        if request.path == settings.MODERNIZR_SENTINEL_IMAGE_URL:
            response = HttpResponse('')
            response = self.persist_modernizr(request)
            return response
        else:
            return None

    def process_response(self, request):
        print("process_response...")
        if request.modernizr is None and self.get_response.status_code == 200 and \
            self.get_response['Content-Type'].split(';')[0] in _HTML_TYPES:

            self.get_response = self.add_modernizr()

        return self.get_response

    def process_exception(self, request, exception):
        if settings.DEBUG:
            print(exception.__class__.__name__)
            print(exception.message)
        return None