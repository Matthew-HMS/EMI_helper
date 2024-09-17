import os
import requests
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import json
from django.http import JsonResponse
from rest_framework import status
from openai import OpenAI
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Class
from .models import Pptword
from .models import Ppt
from .serializers import PptWordSerializer


class GPTResponseAPIView(GenericAPIView):
    queryset = Pptword.objects.all()
    serializer_class = PptWordSerializer

    def get(self, request):
        # print(request.GET)
        pptword_page = request.GET.get('pptword_page')
        ppt_ppt = request.GET.get('ppt_ppt')
        
        if pptword_page and ppt_ppt:
            print("gpt get by page and ppt")
            pptwords = self.get_queryset().filter(pptword_page=pptword_page, ppt_ppt=ppt_ppt)
        else:
            print("gpt get all")
            pptwords = self.get_queryset()
        serializer = self.serializer_class(pptwords, many=True)
        data = serializer.data
        return JsonResponse(
            json.loads(json.dumps(data, ensure_ascii=False)),
            status=status.HTTP_200_OK,
            safe=False
        )
        

    def post(self, request):
        data = request.data
        print("gpt post")

        try:  
            if 'ppt_ppt' not in data:
                return Response({'error': 'ppt_ppt is required.'}, status=status.HTTP_400_BAD_REQUEST)            
                 
            ppt_id = data['ppt_ppt']

            ppt_instance = get_object_or_404(Ppt, ppt_id=ppt_id)
            class_instance = ppt_instance.class_class
                       
            api_key = os.environ.get('OPENAI_API_KEY')
            client = OpenAI(api_key=api_key)

            assistant_id = class_instance.class_path
            print(assistant_id)

            # 生成GPT回應
            thread = client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": data['message']+ " in " + ppt_instance.ppt_name
                        # "content": "briefly explain 改良QuickSort作業說明_更正.pdf."
                    }
                ]
            )

            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread.id, assistant_id=assistant_id
            )

            messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

            data['pptword_content'] = messages[0].content[0].text.value
            data['pptword_question'] = data['message']
        
            print(data['pptword_content'])

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()

            # return Response(
            #     {"message": messages[0].content[0].text.value}, 
            #     status=status.HTTP_200_OK
            #     )
            return JsonResponse(
                json.loads(json.dumps({
                    "message": messages[0].content[0].text.value
                }, ensure_ascii=False)),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print({'error': str(e)})
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
    # def delete(self, request):
    #     data = request.data
    #     try:
    #         pptword_id = data.get('pptword_id')
    #         pttword_instance = Pptword.objects.get(pptword_id=pptword_id)
    #         pttword_instance.delete()
    #         return JsonResponse({'message': 'chat deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    #     except Pptword.DoesNotExist:
    #         print(f'Chat with the given ID does not exist: {pptword_id}')
    #         return JsonResponse({'error': 'Ppt with the given ID does not exist'}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         print(f'Failed to delete pptword: {e}')
    #         return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # def deleteByPage(self, request):
    #     data = request.data
    #     try:
    #         pptword_page = data.get('pptword_page')
    #         ppt_id = data.get('ppt_id')
    #         pttword_instance = Pptword.objects.get(pptword_page=pptword_page, ppt_ppt=ppt_id)
    #         pttword_instance.delete()
    #         return JsonResponse({'message': 'chat deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    #     except Pptword.DoesNotExist:
    #         print(f'Chat with the given page or ppt does not exist: p.{pptword_page} in ppt{ppt_id}')
    #         return JsonResponse({'error': 'Chat with the given page or ppt does not exist'}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         print(f'Failed to delete pptword: {e}')
    #         return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request):
        data = request.data
        try:
            pptword_id = data.get('pptword_id')
            pptword_page = data.get('pptword_page')
            ppt_id = data.get('ppt_id')
        
            # 如果有提供 pptword_id，則進行單個刪除
            if pptword_id:
                pttword_instance = Pptword.objects.get(pptword_id=pptword_id)
                pttword_instance.delete()
                return JsonResponse({'message': 'Chat deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

            # 否則，根據頁面和 ppt_id 進行刪除
            elif pptword_page and ppt_id:
                pptword_instance = Pptword.objects.filter(pptword_page=pptword_page, ppt_ppt=ppt_id)
                if not pptword_instance.exists():
                    return JsonResponse({'error': 'Chat with the given page or ppt does not exist'}, status=status.HTTP_404_NOT_FOUND)
                pptword_instance.delete()
                return JsonResponse({'message': 'Chat deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

            # 若資料不完整
            else:
                print('pptword_id or both pptword_page and ppt_id are required.')
                return JsonResponse({'error': 'pptword_id or both pptword_page and ppt_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

        except Pptword.DoesNotExist:
            print('Pptword with the given ID or page does not exist')
            return JsonResponse({'error': 'Pptword with the given ID or page does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print({'error': str(e)})
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
