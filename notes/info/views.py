from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def info(request):
    return HttpResponse("<h1>hello started working for api</h1>")