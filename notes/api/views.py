from django.shortcuts import render
from django.http import JsonResponse, Http404
from info.models import Info
from .serializers import InfoSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user account",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Username (3-20 characters, alphanumeric and underscore, must start with letter)',
                    example='john_doe'
                ),
                'email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format='email',
                    description='Valid email address',
                    example='john@example.com'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format='password',
                    description='Password (min 8 chars, must include uppercase, lowercase, digit, special char)',
                    example='SecurePass@123'
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Account created successfully",
                examples={
                    "application/json": {
                        "message": "Account created successfully",
                        "user": {
                            "id": 1,
                            "username": "john_doe",
                            "email": "john@example.com"
                        },
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request - Validation errors",
                examples={
                    "application/json": {
                        "username": ["Username must be between 3 and 20 characters."],
                        "password": ["Password must contain at least one uppercase letter."],
                        "email": ["Enter a valid email address."]
                    }
                }
            ),
        },
        tags=['Authentication']
    )
    def post(self, request):
        user_data = UserSerializer(data=request.data)
        if user_data.is_valid():
            new_user = user_data.save()
            user_token = RefreshToken.for_user(new_user)
            return Response({
                'message': 'Account created successfully',
                'user': user_data.data,
                'refresh': str(user_token),
                'access': str(user_token.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(user_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login with username and password to get JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Username',
                    example='john_doe'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format='password',
                    description='Password',
                    example='SecurePass@123'
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "message": "Login successful",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request - Missing credentials",
                examples={
                    "application/json": {
                        "error": "Please provide both username and password"
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized - Invalid credentials",
                examples={
                    "application/json": {
                        "error": "Invalid credentials"
                    }
                }
            ),
        },
        tags=['Authentication']
    )
    def post(self, request):
        user_name = request.data.get('username')
        user_password = request.data.get('password')
        
        if not user_name or not user_password:
            return Response({
                'error': 'Please provide both username and password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        current_user = authenticate(username=user_name, password=user_password)
        
        if current_user:
            user_token = RefreshToken.for_user(current_user)
            return Response({
                'message': 'Login successful',
                'refresh': str(user_token),
                'access': str(user_token.access_token),
            }, status=status.HTTP_200_OK)
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


class InfoList(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get list of all Info objects. Requires JWT authentication.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <JWT Token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="List of Info objects",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "title": "Sample Title",
                            "text": "Sample text content"
                        }
                    ]
                }
            ),
            401: openapi.Response(
                description="Unauthorized - Invalid or missing token",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
        },
        tags=['Info CRUD']
    )
    def get(self, request):
        info = Info.objects.all()
        serializer = InfoSerializer(info, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new Info object. Requires JWT authentication.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <JWT Token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'text'],
            properties={
                'title': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Title of the info (max 200 characters)',
                    example='My First Info'
                ),
                'text': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Text content of the info',
                    example='This is the detailed text content.'
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Info created successfully",
                examples={
                    "application/json": {
                        "message": "Info created successfully",
                        "data": {
                            "id": 1,
                            "title": "My First Info",
                            "text": "This is the detailed text content."
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request - Validation errors",
                examples={
                    "application/json": {
                        "title": ["Title cannot be empty."],
                        "text": ["Text cannot be empty."]
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized - Invalid or missing token",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
        },
        tags=['Info CRUD']
    )
    def post(self, request):
        serializer = InfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Info created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class InfoDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Info.objects.get(pk=pk)
        except Info.DoesNotExist:
            return None
    
    @swagger_auto_schema(
        operation_description="Retrieve a specific Info object by ID. Requires JWT authentication.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <JWT Token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Info object retrieved successfully",
                examples={
                    "application/json": {
                        "id": 1,
                        "title": "Sample Title",
                        "text": "Sample text content"
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found - Info object does not exist",
                examples={
                    "application/json": {
                        "error": "Info not found"
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized - Invalid or missing token",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
        },
        tags=['Info CRUD']
    )
    def get(self, request, pk):
        info = self.get_object(pk)
        if not info:
            return Response({
                'error': 'Info not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = InfoSerializer(info)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Update an Info object (partial update supported). Requires JWT authentication.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <JWT Token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Title of the info (max 200 characters)',
                    example='Updated Title'
                ),
                'text': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Text content of the info',
                    example='Updated text content.'
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Info updated successfully",
                examples={
                    "application/json": {
                        "message": "Info updated successfully",
                        "data": {
                            "id": 1,
                            "title": "Updated Title",
                            "text": "Updated text content."
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request - Validation errors",
                examples={
                    "application/json": {
                        "title": ["Title cannot be empty."]
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found - Info object does not exist",
                examples={
                    "application/json": {
                        "error": "Info not found"
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized - Invalid or missing token",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
        },
        tags=['Info CRUD']
    )
    def put(self, request, pk):
        info = self.get_object(pk)
        if not info:
            return Response({
                'error': 'Info not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = InfoSerializer(info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Info updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete an Info object. Requires JWT authentication.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <JWT Token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            204: openapi.Response(
                description="Info deleted successfully",
                examples={
                    "application/json": {
                        "message": "Info deleted successfully"
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found - Info object does not exist",
                examples={
                    "application/json": {
                        "error": "Info not found"
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized - Invalid or missing token",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
        },
        tags=['Info CRUD']
    )
    def delete(self, request, pk):
        info = self.get_object(pk)
        if not info:
            return Response({
                'error': 'Info not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        info.delete()
        return Response({
            'message': 'Info deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)