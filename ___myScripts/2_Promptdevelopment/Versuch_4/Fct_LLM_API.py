import json
import re
import os
import requests

def Chatting(prompt: str, context: str, model: str, url: str):
    """Sends a prompt and extracted text to the local Ollama API and handles streaming."""
    model = model
    url = url
    data = {
        "model": model,
        "prompt": f"{prompt}\n\n{context[:4000]}",  # Limit input to avoid truncation
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

def ChattingOne(prompt: str, context: str, model: str, temperature: float):
    """Sends prompt and context to local Ollama API and returns result"""
    model = model
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": f"{prompt}\n\n{context}",  # Limit input to avoid truncation
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }

    response = requests.post(url, json=data)
    answer = response.json()['response']
    return answer