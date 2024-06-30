from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from openai import OpenAI
import os
import pytesseract

client = OpenAI(
    api_key = os.environ.get('OPENAI_API_KEY')
)









def gpt_read_pdf():
    page_numbers = range(1, 6)  
    pdf_content = read_pdf_pages("D:\\中央大學\\第6學期\\專題\\project\\EMI_helper\\ncu_emi\\gpt\\[中央大學]20240417創造社群與自媒體影響力的經營策略(列印版).pdf", page_numbers)

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "read pdf's content and give me an English script for class:"},
            {"role": "user", "content": pdf_content}
        ]
    )    

    reply =  completion.choices[0].message.content
    print(reply)

        

def read_pdf_pages(file_path, pages):
    content = ""   
    reader = PdfReader(file_path)
    number_of_pages = len(reader.pages)
    print(number_of_pages)

    for page in pages:
        if page <= number_of_pages:
            content += reader.pages[page - 1].extract_text()
        else:
            content += f"Page {page} does not exist in the PDF\n"

    return content
    




def read_pdf_pages_with_ocr(file_path, pages):
    # Convert PDF pages to images
    images = convert_from_path(file_path, first_page=min(pages), last_page=max(pages))
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\chenp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    
    text = ""
    for i, page in enumerate(pages):
        image_text = pytesseract.image_to_string(images[i])
        text += f"Page {page}:\n{image_text}\n\n"

    return text


# gpt_read_pdf()
# read_pdf_pages("D:\\中央大學\\第6學期\\專題\\project\\EMI_helper\\ncu_emi\\gpt\\[中央大學]20240417創造社群與自媒體影響力的經營策略(列印版).pdf", range(1,6))
# read_pdf_pages_with_ocr("D:\\中央大學\\第6學期\\專題\\project\\EMI_helper\\ncu_emi\\gpt\\417冰雪娜娜演講心得_110403523_陳品睿.pdf", range(1, 6))
