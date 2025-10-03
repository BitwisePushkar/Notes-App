from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView,LogoutView

# Create your views here.
class LoginInterfaceView(LoginView):
    template_name="login.html"
    
class LogoutInterfaceView(LogoutView):
    template_name="logout.html"

class HomeView(TemplateView):
    template_name="welcome.html"
