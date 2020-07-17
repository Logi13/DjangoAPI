from django.shortcuts import render
from django.template.response import TemplateResponse

# Create your views here.


def test_view(request):
    context = {}
    return TemplateResponse(request, "initialHeaderMiddleware/index.html", context=context)