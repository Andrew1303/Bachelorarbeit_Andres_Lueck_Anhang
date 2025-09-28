import requests

def ollama_embedding(texts, model):  # Or llama3 if it supports embedding
    embeddings = []
    for text in texts:
        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={
                "model": model,
                "prompt": text
            }
        )
        response.raise_for_status()
        embedding = response.json()["embedding"]
        embeddings.append(embedding)
    return embeddings

print(ollama_embedding(["Testtext"], "qwen2.5:7b"))