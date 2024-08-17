from openai import OpenAI
import os
import requests

client = OpenAI(
    api_key = os.environ.get('OPENAI_API_KEY')
)


def upload_file():
    api_endpoint = "https://api.openai.com/v1/vector_stores"
    api_key = os.environ.get('OPENAI_API_KEY')

    # 定義請求標頭
    headers = {
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Beta": "assistants=v2"
    }

    # 發送GET請求以獲取所有的vector stores
    response = requests.get(api_endpoint, headers=headers)

    # 檢查請求是否成功
    if response.status_code == 200:
        vector_stores = response.json()
        # 列出所有的vector stores
        for store in vector_stores['data']:
            print(f"ID: {store['id']}, Name: {store['name']}")
    else:
        print(f"Failed to retrieve vector stores: {response.status_code} {response.text}")

    api_endpoint2 = "https://api.openai.com/v1/files"

    response2 = requests.get(api_endpoint2, headers=headers)

    if response2.status_code == 200:
        vector_stores = response2.json()
        # 列出所有的vector stores
        for store in vector_stores['data']:
            print(f"ID: {store['id']}, Name: {store['filename']}")
    else:
        print(f"Failed to retrieve vector stores: {response2.status_code} {response2.text}")

        vector_store = client.beta.vector_stores.create(name="Algorithm")

    # file_paths = ["改良QuickSort作業說明_更正.pdf","Eclipse安裝與輸出說明.pdf","chapter5.pdf"]
    directory = "../../Flutter_project/flutter_application_ncu_emi/assets/user_data/"
    file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    file_streams = [open(file_path, "rb") for file_path in file_paths]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
    )

    print(file_batch.status)
    print(file_batch.file_counts)

    assistant = client.beta.assistants.create(
    name="Algorithm",
    instructions="1. You are now an assistant for the professor in algorithm class, you need to teach the class in English 2. Read pdf's content and give me an English script for class 3. Use the knowledge only in the pdf, else don't answer and say you don't know",
    model="gpt-4o",
    # tools=[{"type": "file_search"}, {"type": "vision"}],
    tools=[{"type": "file_search"}],
    )

    assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

def gpt_response():  


    thread = client.beta.threads.create(
    messages=[
        {
        "role": "user",
        "content": "briefly explain test2.pdf."
        }
    ]
    )

    print(thread.tool_resources.file_search)

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    # print(messages)
    print(messages[0].content[0].text.value)