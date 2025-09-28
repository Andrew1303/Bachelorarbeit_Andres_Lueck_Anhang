import requests

# modelname = "llama3.2-vision"
# modelname = "DeepSeek-R1"
modelname = 'llama3.2-vision'

url = "http://localhost:11434/api/generate"
data = {
    "model": modelname,
    "prompt": "Hello, how are you?",
    "stream": False
}

response = requests.post(url, json=data)
print(response.json()['response'])