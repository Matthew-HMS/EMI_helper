from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework import status

from .serializers import fileSerializer
from .models import File
# Create your views here.

class FileView(GenericAPIView):
        queryset = File.objects.all()
        serializer_class = fileSerializer
        
        def get(self, request, *args, **kwargs):
            files = self.get_queryset()
            serializer = self.serializer_class(files, many=True)
            data = serializer.data
            return JsonResponse(data, safe=False)

        
        def post(self, request, *args, **kwargs):
            data = request.data
            
            try:
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                
                with transaction.atomic():
                    serializer.save()
                
                data = serializer.data
                return JsonResponse(data, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                data = {'error': str(e)}
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
  
  
        def delete (self, request, *args, **krgs):
            data = request.data
            try:
                files = File.objects.get(file_id=data['file_id'])
                files.delete()
                data = {'file_id': data['file_id']}
            except Exception as e:
                data = {'error': str(e)}
            return JsonResponse(data)
