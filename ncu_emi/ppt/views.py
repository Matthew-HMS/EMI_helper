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
from pypdf import PdfReader, PdfWriter

from .serializers import PptSerializer
from .serializers import Ppt_pageSerializer
from .models import Ppt
from .models import Class
from .models import Ppt_page
from .models import Pptword
# Create your views here.

class PptView(GenericAPIView):
        queryset = Ppt.objects.all()
        serializer_class = PptSerializer
        serializer_class_page = Ppt_pageSerializer
        destination_folder = '../../Flutter_project/ncu_emi/assets/'  # =cd..,cd..,cd flutter_project,...
        
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
            # ppt_id = data['ppt_id']
            
            try:
                try:
                # 複製文件到目標資料夾
                    ppt_local_path = data['ppt_local_path']
                    # ppt_local_path = r"C:\中央大學第六學期\專題\EMI\EMI_helper\ncu_emi\gpt\Eclipse安裝與輸出說明.pdf"
                    print(f"Ppt local path: {ppt_local_path}")
                    destination_path = os.path.join(self.destination_folder, class_name)
                    os.makedirs(destination_path, exist_ok=True)  # 確保目標資料夾存在
                    shutil.copy(ppt_local_path, destination_path)

                    # 更新檔案路徑
                    data['ppt_local_path'] = os.path.join(destination_path, data['ppt_name'])
                    print(f"Copied ppt to destination path: {destination_path}")                

                    # 切割 PDF 文件
                    pdf_path = data['ppt_local_path']
                    pdf_reader = PdfReader(pdf_path)
                    pdf_files = []

                    for i in range(len(pdf_reader.pages)):
                        pdf_writer = PdfWriter()
                        pdf_writer.add_page(pdf_reader.pages[i])
                        
                        split_pdf_path = os.path.join(destination_path, f"{data['ppt_name'].split('.')[0]}_page_{i + 1}.pdf")
                        with open(split_pdf_path, "wb") as split_pdf_file:
                            pdf_writer.write(split_pdf_file)
                            pdf_files.append(split_pdf_path)

                    # 保存ppt到資料庫
                    serializer = self.serializer_class(data=data)
                    serializer.is_valid(raise_exception=True)              
                    with transaction.atomic():
                        ppt_temp = serializer.save() 
                    print(f"ppt_temp_id: {ppt_temp.ppt_id}")   
                    

                except Exception as e:
                    print(f"Failed to copy ppt file or split ppt: {e}")
                    data = {'fail to copy ppt file or split ppt': str(e)}
                    return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # 上傳每個分割的 PDF 文件到 OpenAI
                classes = get_object_or_404(Class, class_id=class_id)
                vector_store = classes.vector_store_id
                assistant_id = classes.class_path
                
                api_key = os.environ.get('OPENAI_API_KEY')
                client = OpenAI(api_key=api_key)
                
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "OpenAI-Beta": "assistants=v2"
                }

                uploaded_file_ids = []
                
                for pdf_file_path in pdf_files:
                    if not os.path.exists(pdf_file_path):
                        return JsonResponse({'error': f'File not found: {pdf_file_path}'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    with open(pdf_file_path, "rb") as pdf_file:
                        files = client.files.create(
                            file=pdf_file,
                            purpose="assistants",
                        )
                        uploaded_file_ids.append(files.id)
                    
                    serializer = self.serializer_class_page(data={'uploaded_id': files.id, 'ppt_ppt': ppt_temp.ppt_id})                    
                    serializer.is_valid(raise_exception=True)
                    
                    with transaction.atomic():
                        serializer.save()
                    
                
                # 更新向量儲存和助理資料
                batch_add = client.beta.vector_stores.file_batches.create(
                    vector_store_id=vector_store,
                    file_ids=uploaded_file_ids
                )
                
                assistant = client.beta.assistants.update(
                    assistant_id=assistant_id,
                    tool_resources={"file_search": {"vector_store_ids": [vector_store]}},
                )
                                
                return JsonResponse(data, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                print(f"Failed to upload ppt file to OpenAI: {e}")
                data = {'error': str(e)}
                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
  
  
        def delete(self, request, *args, **kwargs):
            data = request.data
            ppt_id = data.get('ppt_id')

            try:
                # 取得 ppt 實例
                ppt_instance = get_object_or_404(Ppt, ppt_id=ppt_id)
                ppt_local_path = ppt_instance.ppt_local_path

                ppt_page_instances = Ppt_page.objects.filter(ppt_ppt=ppt_instance.ppt_id)

                # 刪除本地文件
                if os.path.exists(ppt_local_path):
                    os.remove(ppt_local_path)
                else:
                    print(f'File not found at the specified path: {ppt_local_path}')
                    return JsonResponse({'error': 'File not found at the specified path.'}, status=status.HTTP_400_BAD_REQUEST)

                # 初始化 OpenAI 客户端
                api_key = os.environ.get('OPENAI_API_KEY')
                if not api_key:
                    return JsonResponse({'error': 'OpenAI API key not found in environment variables.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                client = OpenAI(api_key=api_key) 
                
                # 刪除 OpenAI 文件
                for page_instance in ppt_page_instances:
                    try:
                        page_instance.delete()
                        client.files.delete(file_id=page_instance.uploaded_id)                        
                    except Exception as openai_error:
                        print(f"Failed to delete file from OpenAI: {openai_error}")
                        continue 
                        # return JsonResponse({'error': f'Failed to delete file from OpenAI: {openai_error}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
                # 刪除 pptword 再刪除 ppt
                Pptword.objects.filter(ppt_ppt=ppt_instance.ppt_id).delete()
                ppt_instance.delete()

                return JsonResponse({'message': f'Ppt with ID {ppt_id} and all associated pages deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

            except Ppt.DoesNotExist:
                print(f'Ppt with the given ID does not exist: {ppt_id}')
                return JsonResponse({'error': 'Ppt with the given ID does not exist'}, status=status.HTTP_404_NOT_FOUND)
            except FileNotFoundError:
                print(f'File not found at the specified path: {ppt_local_path}')
                return JsonResponse({'error': 'File not found at the specified path.'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(f'Failed to delete ppt: {e}')
                return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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