from django.shortcuts import render
from django.http import JsonResponse
from info.models import Info
from .serializers import InfoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET','POST'])
def infoView(request):
    if request.method=='GET':
        info=Info.objects.all()
        serializer=InfoSerializer(info, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method=='POST':
        serializer=InfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def infoDetailView(request,pk):
    try:
        info=Info.objects.get(pk=pk)
    except Info.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method=='GET':
        serializer=InfoSerializer(info)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    elif request.method=='PUT':
        serializer=InfoSerializer(info,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method=='DELETE':
        info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


