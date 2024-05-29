from django.shortcuts import render
import requests
from django.http import JsonResponse, HttpRequest
from openai import OpenAI
import os
# Create your views here.

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def translate_to_chinese(request):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Translate the following English text to Chinese:"},
                {"role": "user", "content": "Hello world!"}
            ]
        )
        return JsonResponse({'translated_text': completion.choices[0].message.content})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)






