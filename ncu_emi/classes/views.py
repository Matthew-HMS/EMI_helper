from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Max
from rest_framework.generics import GenericAPIView
from rest_framework import status
import os
from openai import OpenAI

from .serializers import ClassSerializer
from .models import Class
from .models import Ppt
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
                            
                api_key = os.environ.get('OPENAI_API_KEY')
                client = OpenAI(api_key=api_key)

                # check if class exists
                existing_vector_stores = client.beta.vector_stores.list()
                if any(vs.name == data['class_name'] for vs in existing_vector_stores):
                    return JsonResponse({'error': 'Class exists'}, status=status.HTTP_409_CONFLICT)

                vector_store = client.beta.vector_stores.create(name=data['class_name'])

                # 創建Assistant
                assistant = client.beta.assistants.create(
                    name=data['class_name'],
                    instructions='''1. You are now an assistant for the professor, you need to teach the class in English 
                    2. Read pdf's content and give me an English script for class  
                    3. You can only answer the question related to pdf 
                    4. The default limit of your response is 200 words unless user tell you the specific limit''',
                    model="gpt-4o-mini",
                    tools=[{"type": "file_search"}],
                )

                data['vector_store_id'] = vector_store.id
                data['class_path'] = assistant.id
                
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                with transaction.atomic():
                    print(serializer.validated_data)
                    serializer.save()
            
                return JsonResponse(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                data = {'error': str(e)}
                return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
  
        def delete (self, request, *args, **krgs):
            data = request.data
            try:
                api_key = os.environ.get('OPENAI_API_KEY')
                client = OpenAI(api_key=api_key)
                
                classes = Class.objects.get(class_id=data['class_id'])
                classes.delete()
                
                client.beta.vector_stores.delete(vector_store_id=classes.vector_store_id)
                client.beta.assistants.delete(assistant_id=classes.class_path)
                
                data = {'class_id': data['class_id']}
                return JsonResponse(data, status=status.HTTP_204_NO_CONTENT)
            except Class.DoesNotExist:
                data = {'error': 'Class with the given ID does not exist'}
                print("error: ",data)
                return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                data = {'error': str(e)}
                print("error: ",data)
                return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        def patch (self, request, *args, **krgs):
            data = request.data
            try:
                classes = Class.objects.get(class_id=data['class_id'])
                old_class_name = classes.class_name
                new_class_name = data.get('class_name')
                
        
                # update vector_store name                
                if new_class_name:
                    api_key = os.environ.get('OPENAI_API_KEY')
                    client = OpenAI(api_key=api_key)
                    
                    client.beta.vector_stores.update(vector_store_id=classes.vector_store_id, name=new_class_name)
                    client.beta.assistants.update(assistant_id=classes.class_path, name=new_class_name)

                # revise ppt local path
                ppt_instances = Ppt.objects.filter(class_class=classes.class_id)
                for ppt_instance in ppt_instances:
                    old_path = ppt_instance.ppt_local_path
                    new_path = old_path.replace(old_class_name,new_class_name)
                    ppt_instance.ppt_local_path = new_path
                    ppt_instance.save()

                serializer = self.serializer_class(classes, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                with transaction.atomic():
                    serializer.save()
                data = serializer.data
                return JsonResponse(data, status=status.HTTP_200_OK)
            except Class.DoesNotExist:
                data = {'error': 'Class with the given ID does not exist'}
                print("error: ",data)
                return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                data = {'error': str(e)}
                print("error: ",data)
                return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        def get_extra_actions():
            return []