import pdfplumber  # Extract text from PDF
import requests  # Send API requests to Ollama

def extract_text_from_pdf(pdf_path):
    print("Extracts text from a PDF file using pdfplumber.")
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            print(page)
            extracted = page.extract_text()
            if extracted:  # Avoid NoneType errors
                text += extracted + "\n"
    return text

pdf_path = "Ampelkoalition-Zeit.pdf"  # Change this to your PDF file path
# Extract text from PDF
extracted_text = extract_text_from_pdf(pdf_path)

print(extracted_text)