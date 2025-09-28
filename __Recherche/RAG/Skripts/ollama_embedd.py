import requests
from typing import List
from chromadb import EmbeddingFunction

def get_embedding(text:str, model:str):
    response = requests.post(
        'http://localhost:11434/api/embeddings',
        json={
            "model": model,
            "prompt": text
        }
    )
    embedding = response.json()["embedding"]
    if embedding:
        return response.json()["embedding"]
    else:
        print(f"No embedding; Response:\n{response}\n\nInput:\n{text}")

class OllamaEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model):
        self.model = model
        self.api_url = "http://localhost:11434/api/embeddings"

    def __call__(self, input: List[str]) -> List[List[float]]:
        embeddings = []
        for text in input:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": text
                }
            )
            response.raise_for_status()
            embedding = response.json()["embedding"]
            embeddings.append(embedding)
        return embeddings

# print(get_embedding("This is a test", "granite-embedding"))