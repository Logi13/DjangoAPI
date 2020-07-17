from django.shortcuts import render, redirect
from django.template.response import TemplateResponse

# Create your views here.
def index(request):
    context = {}
    return TemplateResponse(request, 'mainpage/home.html', context=context)

def imageServe(request):
    return render(request, 'mainpage/home.html')  