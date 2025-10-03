from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('authorized/', views.AuthorizedView.as_view()),
]