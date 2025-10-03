from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,CreateView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

class SignupView(CreateView):
    form_class=UserCreationForm
    template_name="register.html"
    success_url="smart/notes"

    def get(self,request,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('notes.list')
        return super().get(request,*args,**kwargs)


class LoginInterfaceView(LoginView):
    template_name="login.html"
    
class LogoutInterfaceView(LogoutView):
    template_name="logout.html"

class HomeView(TemplateView):
    template_name="welcome.html"
