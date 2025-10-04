from django.urls import path
from . import views

urlpatterns = [
    path('info/',views.infoView),
    path('info/<int:pk>/',views.infoDetailView),
]
