import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI

class UploadFileAPIView(APIView):
    def post(self, request):
        api_key = os.environ.get('OPENAI_API_KEY')
        client = OpenAI(api_key=api_key)

        # 获取 vector stores
        api_endpoint = "https://api.openai.com/v1/vector_stores"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "OpenAI-Beta": "assistants=v2"
        }

        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 200:
            vector_stores = response.json()
            # 在這裡創建一個新的 vector store
            vector_store = client.beta.vector_stores.create(name="Algorithm")
        else:
            return Response(
                {"error": f"Failed to retrieve vector stores: {response.status_code} {response.text}"},
                status=response.status_code,
            )

        # 上傳文件
        directory = "../../Flutter_project/flutter_application_ncu_emi/assets/user_data/"
        file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
        file_streams = [open(file_path, "rb") for file_path in file_paths]

        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
        )

        return Response({
            "status": file_batch.status,
            "file_counts": file_batch.file_counts
        }, status=status.HTTP_200_OK)

class GPTResponseAPIView(APIView):
    def post(self, request):
        api_key = os.environ.get('OPENAI_API_KEY')
        client = OpenAI(api_key=api_key)

        # 先前已在 UploadFileAPIView 中創建了 vector_store
        vector_store = client.beta.vector_stores.create(name="Algorithm")

        # 創建Assistant
        assistant = client.beta.assistants.create(
            name="Algorithm",
            instructions="1. You are now an assistant for the professor in algorithm class, you need to teach the class in English 2. Read pdf's content and give me an English script for class 3. Use the knowledge only in the pdf, else don't answer and say you don't know",
            model="gpt-4o",
            tools=[{"type": "file_search"}],
        )

        # 更新Assistant
        assistant = client.beta.assistants.update(
            assistant_id=assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        )

        # 生成GPT回應
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": "briefly explain test2.pdf."
                }
            ]
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=assistant.id
        )

        messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

        return Response({
            "message": messages[0].content[0].text.value
        }, status=status.HTTP_200_OK)
