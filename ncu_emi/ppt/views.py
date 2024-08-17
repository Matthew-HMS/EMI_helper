from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework import status

from .serializers import PptSerializer
from .models import Ppt
# Create your views here.

class PptView(GenericAPIView):
        queryset = Ppt.objects.all()
        serializer_class = PptSerializer
        
        def get(self, request, *args, **kwargs):
            class_class = request.GET.get('class_class')
            if class_class:
                ppts = self.get_queryset().filter(class_class=class_class)
            else:
                ppts = self.get_queryset()
            # ppt = self.get_queryset()
            serializer = self.serializer_class(ppts, many=True)
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
                ppts = Ppt.objects.get(ppt_id=data['ppt_id'])
                ppts.delete()
                data = {'ppt_id': data['ppt_id']}
            except Exception as e:
                data = {'error': str(e)}
            return JsonResponse(data)
        
        def patch (self, request, *args, **krgs):
            data = request.data
            try:
                ppt = Ppt.objects.get(ppt_id=data['ppt_id'])
                serializer = self.serializer_class(ppt, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                with transaction.atomic():
                    serializer.save()
                data = serializer.data
            except Ppt.DoesNotExist:
                data = {'error': 'ppt with the given ID does not exist'}
            except Exception as e:
                data = {'error': str(e)}
            return JsonResponse(data)
        
        def get_extra_actions():
            return []