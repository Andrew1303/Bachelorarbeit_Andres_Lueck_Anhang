import requests

url = "http://127.0.0.1:8000/embeddings"

data = {
    "chunks": ["Hello", "Test"]
    }
response = requests.get(url, json=data)

print("Status code:", response.status_code)
print("Response JSON:", response.json())