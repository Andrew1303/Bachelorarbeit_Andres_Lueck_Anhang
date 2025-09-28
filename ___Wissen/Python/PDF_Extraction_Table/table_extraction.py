import PyPDF2
# How to extract tables from pdf
# Source: https://www.youtube.com/watch?v=yKAuUAPREMw
# 14.04.2025, 18:10
text = ''

with open('___Wissen\Python\PDF_Extraction_Text\Kurzanalyse_flexibleKraftwerke.pdf', 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)

    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        text += page_text + '\n\n'

print(text)