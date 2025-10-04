from django.urls import path
from . import views

urlpatterns = [
    path('info/',views.InfoList.as_view()),
    path('info/<int:pk>/',views.InfoDetail.as_view()),
]
