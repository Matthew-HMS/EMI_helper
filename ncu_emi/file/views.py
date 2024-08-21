from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework import status
from openai import OpenAI
from django.shortcuts import get_object_or_404

from .serializers import fileSerializer
from .models import File
from .models import Class

import shutil
import os
# Create your views here.

class FileView(GenericAPIView):
        queryset = File.objects.all()
        serializer_class = fileSerializer
        destination_folder = '../../Flutter_project/flutter_application_ncu_emi/assets/user_data/'  # =cd..,cd..,cd flutter_project,...
        
        def get(self, request, *args, **kwargs):
            class_class = request.GET.get('class_class')    
            if class_class:
                files = self.get_queryset().filter(class_class=class_class)
            else:
                files = self.get_queryset()
            # files = self.get_queryset()
            serializer = self.serializer_class(files, many=True)
            data = serializer.data
            return JsonResponse(data, safe=False)

        
        def post(self, request, *args, **kwargs):
            print("file post")
            data = request.data
            classes_id = data['class_class']
            file_path=data['file_path']

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
                
                print(f"File path: {file_path}")  
                if not os.path.exists(file_path):
                    return JsonResponse({'error': 'File not found at the specified path.'}, status=status.HTTP_400_BAD_REQUEST)
                
                files = client.files.create(
                    file=open(file_path, "rb"),
                    purpose="assistants",
                )
                
                data['file_path'] = files.id
                
                batch_add = client.beta.vector_stores.file_batches.create(
                    vector_store_id=vector_store,
                    file_ids=[files.id]
                )
                
                assistant = client.beta.assistants.update(
                    assistant_id=assistant_id,
                    tool_resources={"file_search": {"vector_store_ids": [vector_store]}},
                )
                
                # post to the database
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
                
                files = File.objects.get(file_id=data['file_id'])
                files.delete()
                
                client.files.delete(file_id=files.file_path)
                data = {'file_id': data['file_id']}
                return JsonResponse(data, status=status.HTTP_204_NO_CONTENT)
            except File.DoesNotExist:
                data = {'error': 'File with the given ID does not exist'}
                return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                data = {'error': str(e)}
                return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # should be usless
        def patch (self, request, *args, **krgs):
            # data = request.data
            # try:
            #     file = File.objects.get(file_id=data['file_id'])
            #     serializer = self.serializer_class(file, data=data, partial=True)
            #     serializer.is_valid(raise_exception=True)
            #     with transaction.atomic():
            #         serializer.save()
            #     data = serializer.data
            #     return JsonResponse(data, status=status.HTTP_200_OK)
            # except File.DoesNotExist:
            #     data = {'error': 'Class with the given ID does not exist'}
            #     return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            # except Exception as e:
            #     data = {'error': str(e)}
            #     return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return JsonResponse({'error': 'PATCH method is not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        def get_extra_actions():
            return []