import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
import requests

URL_EmbeddingAPI = "http://127.0.0.1:8000/RAG"

client = chromadb.PersistentClient(
    path=r"__Recherche\RAG\Skripts\chromadb",
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

def get_saved_embeddings(collectionname:str):
    collection = client.get_collection(collectionname)
    result = collection.get()
    return result["embeddings"], result["documents"]

# Get connection to chromadb
client = chromadb.PersistentClient(
    path=r"__Recherche\RAG\Skripts\chromadb",
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

# List all collections
collections = []
count = 0
print("The following collections are available:\n")
for collection in client.list_collections():
    count += 1
    name = collection.name
    name = name.replace("----", ":")
    print(f'• [{count}] {name}')
    collections.append(collection.name)

# Select a collection
selectedCollection = int(input("\nSelect collection (Number)\n")) - 1

# Transform collectionname if needed to define the used model
model = collections[selectedCollection].split('_')[0].replace("----", ":")
print(f"Your selected model: '{model}'")

# Load the collection from the client
collection = client.get_collection(collections[selectedCollection])

# Get the data of the selected collection
result = collection.get(include=["documents", "embeddings"])

# Get the embeddings of the selected collection
embeddings = result["embeddings"].tolist()

# Define the request
prompt = "Whats the base failure rate of a capacitors, fixed, paper, bi-pass?"

# NOT WORKING: Prompt needs an embedding for RAG

# # API - Send embeddings and request to calculate the results
data = {"embeddings": embeddings, "prompt": prompt}
response = requests.get(URL_EmbeddingAPI, json=data)
# print(response.json())
scores = response.json()
print(scores)

input()
highest_score_index = scores.index(max(scores))
print(f"\nHighscore [index: {highest_score_index}]:")
print(scores[highest_score_index])
print("\nChunk with best score:")
print(result["documents"][highest_score_index])