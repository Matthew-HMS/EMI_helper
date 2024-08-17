from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework import status
import os
from openai import OpenAI
import requests
from django.shortcuts import get_object_or_404

from .serializers import PptSerializer
from .models import Ppt
from .models import Class
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
            classes_id = data['class_class']
            
            try:
                classes = get_object_or_404(Class, class_id=classes_id)

                vector_store = classes.vector_store_id
                assistant_id = classes.class_path
                
                api_key = os.environ.get('OPENAI_API_KEY')
                client = OpenAI(api_key=api_key)
                
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "OpenAI-Beta": "assistants=v2"
                }
                
             
                directory = r"C:\中央大學第六學期\專題\EMI\EMI_helper\ncu_emi\gpt\Eclipse安裝與輸出說明.pdf"
                print(f"File path: {directory}")  

                if not os.path.exists(directory):
                    return JsonResponse({'error': 'File not found at the specified path.'}, status=status.HTTP_400_BAD_REQUEST)
                
                
                files = client.files.create(
                    file=open(directory, "rb"),
                    purpose="assistants",
                )
                
                data['ppt_path'] = files.id
                
                batch_add = client.beta.vector_stores.file_batches.create(
                    vector_store_id=vector_store,
                    file_ids=[files.id]
                )
                
                assistant = client.beta.assistants.update(
                    assistant_id=assistant_id,
                    tool_resources={"file_search": {"vector_store_ids": [vector_store]}},
                )
                
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                
                with transaction.atomic():
                    serializer.save()               
                
                return JsonResponse(data, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                data = {'error': str(e)}
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
  
  
        def delete (self, request, *args, **krgs):
            data = request.data
            try:
                api_key = os.environ.get('OPENAI_API_KEY')
                client = OpenAI(api_key=api_key)
                
                ppts = Ppt.objects.get(ppt_id=data['ppt_id'])
                ppts.delete()
                
                client.files.delete(file_id=ppts.ppt_path)
                
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