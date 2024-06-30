from django.shortcuts import render
import requests
from django.http import JsonResponse, HttpRequest
from openai import OpenAI
import os
from PyPDF2 import PdfReader

# Create your views here.

client = OpenAI(
    api_key = os.environ.get('OPENAI_API_KEY')
)



def gpt_read_pdf(request):
    try:
        page_numbers = range(1, 6)  
        pdf_content = read_pdf_pages("D:\\中央大學\\第6學期\\專題\\project\\EMI_helper\\ncu_emi\\gpt\\[中央大學]20240417創造社群與自媒體影響力的經營策略(列印版).pdf", page_numbers)

        completion = client.chat_completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "read pdf's content and give me an English script for class:"},
                {"role": "user", "content": pdf_content}
            ]
        )
        
        reply = completion['choices'][0]['message']['content']
        return JsonResponse({'reply': reply})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def read_pdf_pages(file_path, pages):

    reader = PdfReader(file_path)
    number_of_pages = len(reader.pages)
    content = ""

    for page in pages:
        if page <= number_of_pages:
            content += reader.pages[page - 1].extract_text()
        else:
            content += f"Page {page} does not exist in the PDF"
    
    return content
            

    










