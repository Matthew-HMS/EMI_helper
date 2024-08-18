import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from django.shortcuts import get_object_or_404

from .models import Class


class GPTResponseAPIView(APIView):
    def post(self, request):
        data = request.data
        try:           
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

            return Response({
                "message": messages[0].content[0].text.value
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        
        