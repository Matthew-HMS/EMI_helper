from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework import status
import os
import shutil
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
        destination_folder = '../../Flutter_project/flutter_application_ncu_emi/assets/'  # =cd..,cd..,cd flutter_project,...
        
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
            print(f"Data: {data}")
            class_id = data['class_class']
            class_name = data['class_name']
            
            try:
                # copy the file to the destination folder
                ppt_local_path=data['ppt_local_path']
                print(f"Ppt local path: {ppt_local_path}")
                destination_path = os.path.join(self.destination_folder, class_name)
                shutil.copy(ppt_local_path, destination_path)

                data['ppt_local_path'] = os.path.join(destination_path, data['ppt_name'])
                print(f"copy ppt to destination path: {destination_path}")

                # upload the file to the openai
                classes = get_object_or_404(Class, class_id=class_id)

                vector_store = classes.vector_store_id
                assistant_id = classes.class_path
                
                api_key = os.environ.get('OPENAI_API_KEY')
                client = OpenAI(api_key=api_key)
                
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "OpenAI-Beta": "assistants=v2"
                }              
                
                if not os.path.exists(ppt_local_path):
                    return JsonResponse({'error': 'File not found at the specified path.'}, status=status.HTTP_400_BAD_REQUEST)
                
                files = client.files.create(
                    file=open(ppt_local_path, "rb"),
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
            ppt_id = data['ppt_id']

            try:
                ppt_instance = get_object_or_404(Ppt, ppt_id=ppt_id)
                ppt_local_path = ppt_instance.ppt_local_path
                os.remove(ppt_local_path)

                # delete the file from the openai
                api_key = os.environ.get('OPENAI_API_KEY')
                client = OpenAI(api_key=api_key)
                
                ppts = Ppt.objects.get(ppt_id=data['ppt_id'])
                ppts.delete()
                
                client.files.delete(file_id=ppts.ppt_path)                
                data = {'ppt_id': data['ppt_id']}
                return JsonResponse(data, status=status.HTTP_204_NO_CONTENT)
            except FileNotFoundError:
                print(f'File not found at the specified path: {ppt_local_path}')
                data = {'error': 'File not found at the specified path.'}
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            except Ppt.DoesNotExist:
                data = {'error': 'Ppt with the given ID does not exist'}
                return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                data = {'error': str(e)}
                return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # should be discussed
        def patch (self, request, *args, **krgs):
            # data = request.data
            # try:
            #     ppt = Ppt.objects.get(ppt_id=data['ppt_id'])
            #     serializer = self.serializer_class(ppt, data=data, partial=True)
            #     serializer.is_valid(raise_exception=True)
            #     with transaction.atomic():
            #         serializer.save()
            #     data = serializer.data
            #     return JsonResponse(data, status=status.HTTP_200_OK)
            # except Ppt.DoesNotExist:
            #     data = {'error': 'ppt with the given ID does not exist'}
            #     return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            # except Exception as e:
            #     data = {'error': str(e)}
            #     return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return JsonResponse({'error': 'PATCH method is not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        def get_extra_actions():
            return []