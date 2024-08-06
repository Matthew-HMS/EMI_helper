from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from rest_framework.generics import GenericAPIView

from .serializers import PromptSerializer 
from .models import Prompt

#edit
from rest_framework import status


# Create your views here.

class PromptView(GenericAPIView):
    
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    
    def get(self, request, *args, **krgs):
        prompts = self.get_queryset()
        serializer = self.serializer_class(prompts, many=True)
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
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        data = request.data
        try:
            prompt = Prompt.objects.get(prompt_id=data['prompt_id'])
            prompt.delete()
            data = {'prompt_id': data['prompt_id']}
            return JsonResponse(data, status=status.HTTP_204_NO_CONTENT)
        except Prompt.DoesNotExist:
            data = {'error': 'Prompt with the given ID does not exist'}
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = {'error': str(e)}
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        
    
    def patch(self, request, *args, **kwargs):
        data = request.data
        try:
            prompt_id = data.get('prompt_id')
            prompt = Prompt.objects.get(prompt_id=prompt_id)
            serializer = self.serializer_class(prompt, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            data = serializer.data
        except Prompt.DoesNotExist:
            data = {'error': 'Prompt with the given ID does not exist'}
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data)
    
    def get_extra_actions():
        return []
    

    