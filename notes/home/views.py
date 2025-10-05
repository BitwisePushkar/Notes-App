from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "register.html"
    success_url = reverse_lazy('notes.list')  
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('notes.list')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'Account created successfully! Welcome, {user.username}!')
        return response

class LoginInterfaceView(LoginView):
    template_name = "login.html"
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)

class LogoutInterfaceView(LogoutView):
    template_name = "logout.html"

class HomeView(TemplateView):
    template_name = "welcome.html"