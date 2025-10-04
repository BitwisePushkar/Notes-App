from django.urls import path, re_path
from .views import InfoList, InfoDetail, RegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Info API Documentation",
        default_version='v1',
        description="""
        Complete API documentation for Info CRUD application with JWT Authentication.
        
        ## Authentication
        This API uses JWT (JSON Web Tokens) for authentication.
        
        ### How to authenticate:
        1. Register a new account using `/api/register/`
        2. Login using `/api/login/` to get access and refresh tokens
        3. Use the access token in the Authorization header: `Bearer <your_access_token>`
        4. When access token expires, use `/api/token/refresh/` with refresh token to get a new access token
        
        ## Password Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character (!@#$%^&*(),.?":{}|<>)
        
        ## Username Requirements:
        - 3-20 characters
        - Must start with a letter
        - Only alphanumeric characters and underscores allowed
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@infoapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('info/', InfoList.as_view(), name='info-list'),
    path('info/<int:pk>/', InfoDetail.as_view(), name='info-detail'),
]