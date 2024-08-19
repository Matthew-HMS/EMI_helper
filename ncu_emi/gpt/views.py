import os
import requests
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Class
from .models import Pptword
from .serializers import PptWordSerializer


class GPTResponseAPIView(GenericAPIView):
    queryset = Pptword.objects.all()
    serializer_class = PptWordSerializer

    def get(self, request):
        pptwords = self.get_queryset()
        serializer = self.serializer_class(pptwords, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        try:  
            if 'class_class' not in data:
                return Response({'error': 'class_class is required.'}, status=status.HTTP_400_BAD_REQUEST)
            
                 
            classes_id = data['class_class']
            
            classes = get_object_or_404(Class, class_id=classes_id)
            
            api_key = os.environ.get('OPENAI_API_KEY')
            client = OpenAI(api_key=api_key)

            assistant_id = classes.class_path

            # 生成GPT回應
            thread = client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": data['message']
                        # "content": "briefly explain 改良QuickSort作業說明_更正.pdf."
                    }
                ]
            )

            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread.id, assistant_id=assistant_id
            )

            messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

            data['pptword_content'] = messages[0].content[0].text.value
        
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()

            return Response({
                "message": messages[0].content[0].text.value
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        
        