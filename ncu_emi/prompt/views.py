from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction
from rest_framework.generics import GenericAPIView

from .serializers import PromptSerializer 
from .models import Prompt


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
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data)

    def delete (self, request, *args, **krgs):
        data = request.data
        try:
            prompt = Prompt.objects.get(id=data['id'])
            prompt.delete()
            data = {'id': data['id']}
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data)
