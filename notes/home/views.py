from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'welcome.html')

@login_required(login_url='/admin')
def authorized(request):
    return render(request,'authorized.html')