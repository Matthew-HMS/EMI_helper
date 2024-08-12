from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Max
from rest_framework.generics import GenericAPIView
from rest_framework import status

from .serializers import ClassSerializer
from .models import Class
# Create your views here.

class ClassView(GenericAPIView):        
        queryset = Class.objects.all()
        serializer_class = ClassSerializer
        
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
                return JsonResponse(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                data = {'error': str(e)}
                return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  
        def delete (self, request, *args, **krgs):
            data = request.data
            try:
                classes = Class.objects.get(class_id=data['class_id'])
                classes.delete()
                data = {'class_id': data['class_id']}
                return JsonResponse(data, status=status.HTTP_204_NO_CONTENT)
            except Class.DoesNotExist:
                data = {'error': 'Class with the given ID does not exist'}
                return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                data = {'error': str(e)}
                return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        def patch (self, request, *args, **krgs):
            data = request.data
            try:
                classes = Class.objects.get(class_id=data['class_id'])
                serializer = self.serializer_class(classes, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                with transaction.atomic():
                    serializer.save()
                data = serializer.data
                return JsonResponse(data, status=status.HTTP_200_OK)
            except Class.DoesNotExist:
                data = {'error': 'Class with the given ID does not exist'}
                return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                data = {'error': str(e)}
                return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        def get_extra_actions():
            return []