from django.shortcuts import render
from django.http import JsonResponse
import PyPDF2

# Create your views here.
def read_pdf_file(request):
    try:
        with open("file.pdf", "rb") as f:
            reader = PyPDF2.PdfFileReader(f)
            content = ""
            for page in range(reader.getNumPages()):
                content += reader.getPage(page).extractText()
        return JsonResponse({'file_content': content})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)