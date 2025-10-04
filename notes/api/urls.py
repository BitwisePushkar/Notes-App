from django.urls import path
from .views import InfoList, InfoDetail, RegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('info/', InfoList.as_view(), name='info-list'),
    path('info/<int:pk>/', InfoDetail.as_view(), name='info-detail'),
]