from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def infoView(request):
    info={
        'id':23,
        'name':'king'
    }
    return JsonResponse(info)
