import PyPDF2
# How to extract text from pdf
# Source: https://www.youtube.com/watch?v=RULkvM7AdzY
# 14.04.2025, 17:14

def extract_text_from_pdf(pdf_file: str) -> [str]:
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pdf_text = []
        ids = []

        for index, page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)
            ids.append(index)
        return pdf_text, ids
    

    
# if __name__ == '__main__':
#     extracted_text = extract_text_from_pdf('___testdata\MIL-HDBK-217F.pdf')
#     for text in extracted_text:
#         print(text)