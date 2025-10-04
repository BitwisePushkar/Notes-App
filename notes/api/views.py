from django.shortcuts import render
from django.http import JsonResponse,Http404
from info.models import Info
from .serializers import InfoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

class InfoList(APIView):

    def get(self,request):
        info=Info.objects.all()
        serializer=InfoSerializer(info, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=InfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class InfoDetail(APIView):

    def get_object(self,pk):
        try:
            return Info.objects.get(pk=pk)
        except Info.DoesNotExist:
            raise Http404
        
    def get(self,request,pk):
        info=self.get_object(pk)
        serializer=InfoSerializer(info)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        info=self.get_object(pk)
        serializer=InfoSerializer(info,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        info=self.get_object(pk)
        info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)