import pdfplumber  # Extract text from PDF
import requests  # Send API requests to Ollama
import json
import sys
import os
import re


def extract_text_from_pdf(pdf_path):
    print("Extracts text from a PDF file using pdfplumber.")
    text = "MIL-HDBK-217F I 6.1 DIODES, LOW FREQUENCY — SPECIFICATION DESCRIPTION MlL-S-l 9500 @ Frecpxmqr D-s: General Putpse Analog, Switch~ Fast Rewvery, f%wer RecWer, Tmsient S~r, Current Regulator, Vol@e Regulator, Voltage Reference Lp = &##czQzE Failures/l OG Hours Base Failure Rate - & Diode Type/Appiicatbn “ ~ General PuqxM Analog .0038 switching .0010 Power Redfiir, Fast Recovery .069 Power Rectifier/Schottky .0030 Power Diode Power Rectifier with .0050/ HigiI Voltage Stacks Junction Transient Suppressor/Vanstor .0013 Current Reguiator .0034 Voltage Regulator and Voltage .0020 Reference (Avaianche and Zener) I i Terrperature Factor - XT (General Purpose Analog, Switching, Fast Recovery, Poul TJ (’C) 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100 r Rectifier, TI XT 1.0 1.2 1.4 1.6 1.9 2.2 2.6 3.0 3.4 3.9 4.4 5.0 5.7 6.4 7.2 8.0 dent Su-pgm TJ ~C) 105 110 115 120 125 130 135 140 145 150 155 160 165 170 175 isor) XT 9.0 10 11 12 14 15 16 18 20 21 23 25 28 30 32 ((-3091 1 1 XT = exp TJ + 273 )) -Z& TJ - JunctionTemperature (“C) Temperature Factor - q (VOitag. Regulator, Voitqo Rdormce, h cun’UWRncddYW)—.- ---- . ... . -~---. # TJ (“C) %T ‘J (’=) v 25 1.0 105 3.9 30 1.1 110 4.2 35 1.2 115 4.5 40 1.4 120 4.8 45 1.5 125 5.1 50 1.6 130 5.4 55 1.8 135 5.7 60 2.0 140 6.0 65 2.1 145 6.4 70 2.3 150 6.7 75 2.5 155 7.1 80 2.7 160 7.5 85 3.0 165 7.9 90 3.2 170 8.3 95 3.4 175 8.7 100 3.7 (( 1 1 %T = exp -1925 TJ +273-= )) TJ . Junctio"
    # text = ""
    return text

# def query_llm(prompt, text, model="DeepSeek-R1"):
#     """Sends a prompt and extracted text to the local Ollama API."""
#     url = "http://localhost:11434/api/generate"
#     data = {
#         "model": model,
#         "prompt": f"{prompt}\n\n{text[:4000]}",  # Limit input to avoid truncation
#         "stream": True
#     }


#     response = requests.post(url, json=data, stream=True)
#     response_json = response.json()

#     return response_json.get("response", "No response received from LLM.")

def query_llm(prompt, text, model="DeepSeek-R1"):
    """Sends a prompt and extracted text to the local Ollama API and handles streaming."""
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": f"{prompt}\n\n{text[:4000]}",  # Limit input to avoid truncation
        "stream": True
    }

    # Send POST request with stream=True to handle the response as a stream
    response = requests.post(url, json=data, stream=True)

    if response.status_code == 200:
        # Initialize an empty string to store the result
        result = ""
        
        # Iterating over the stream content
        try:
            for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
                if chunk:
                    # Append the chunk to the result string
                    result += json.loads(chunk.decode('utf-8')).get("response", "No response found")
                    cleaned_result = re.sub(r'<think.*?>', '', result)
                    cleaned_result = re.sub(r'</think.*?>', '', cleaned_result)
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"{cleaned_result}", end='', flush=True)
        except Exception as e:
            return f"Error while reading stream: {str(e)}"
        
        return result
    else:
        return f"Error: {response.status_code}"

if __name__ == "__main__":
    # ------------------------------ PDF PATH ---------------------------------------------------

    pdf_path = "_Testphase\\diodes_low_frequency.pdf"

    # ------------- MODEL SELECTION (MAKE SURE IT RUNS IN LLAMA OR ANYWHERE ACCESSABLE) ---------

    model = "llama3.2-vision"
    # model = "DeepSeek-R1"
    # model = "phi4-mini"


    
    # Extract text from PDF
    extracted_text = extract_text_from_pdf(pdf_path)
    # extracted_text = ''

    # ------------------------------- PROMPT ----------------------------------------------------

    # user_prompt = input("Enter your analysis prompt: ")
    user_prompt = "Base Failure Rate (BFR) diode low frequency\nRespond a specific number, no arguing"
    # user_prompt = "Base Failure Rate (BFR) diode low frequency\nRespond a specific number and naming"

    # Query LLM using Ollama API
    query_llm(user_prompt, extracted_text, model)

    # print("\nAnalysis Result:\n", analysis_result)
