from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from rest_framework.generics import GenericAPIView

from .serializers import classSerializer
from .models import Class
# Create your views here.

class ClassView(GenericAPIView):
        
        queryset = Class.objects.all()
        serializer_class = classSerializer
        
        def get(self, request, *args, **kwargs):
            classes = self.get_queryset()
            serializer = self.serializer_class(classes, many=True)
            data = serializer.data
            return JsonResponse(data, safe=False)

        
        def post(self, request, *args, **krgs):
            data = request.data
            user = request.user
            try:
                data['user'] = user.id
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                with transaction.atomic():
                    serializer.save()
                data = serializer.data
            except Exception as e:
                data = {'error': str(e)}
            return JsonResponse(data)
  
  
        def delete (self, request, *args, **krgs):
            data = request.data
            try:
                classes = Class.objects.get(id=data['id'])
                classes.delete()
                data = {'id': data['id']}
            except Exception as e:
                data = {'error': str(e)}
            return JsonResponse(data)
