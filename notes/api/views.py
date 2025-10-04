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


class RegisterView(APIView):
    permission_classes = [AllowAny]

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

    def get(self, request):
        info = Info.objects.all()
        serializer = InfoSerializer(info, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
        
    def get(self, request, pk):
        info = self.get_object(pk)
        if not info:
            return Response({
                'error': 'Info not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = InfoSerializer(info)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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