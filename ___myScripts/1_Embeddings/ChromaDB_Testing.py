import chromadb 
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from ollama_embedd import OllamaEmbeddingFunction
# QUELLE:
# https://docs.trychroma.com/docs/overview/getting-started

client = chromadb.PersistentClient(
    path=r"__Recherche\RAG\Skripts\chromadb",
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

collections = []
count = 0
print("The following collections are available:\n")
for collection in client.list_collections():
    count += 1
    name = collection.name
    name = name.replace("----", ":")
    print(f'• [{count}] {name}')
    collections.append(collection.name)
selectedCollection = int(input("\nSelect collection (Number)\n")) - 1

model = collections[selectedCollection].split('_')[0].replace("----", ":")
print(f"Your selected model: '{model}'")

collection = client.get_collection(
    collections[selectedCollection],
    embedding_function=OllamaEmbeddingFunction(model)
    )

results = collection.query(
    # query_texts=["What is the base failure rate of diodes low frequency in general?"], # Chroma will embed this for you
    query_texts=["Instruct: Given the pdf document MIL-HDBK-217F get the information for the query\nQuery: What is a base failure rate?"],
    n_results=5, # how many results to return
)

print(results['ids'][0])
print(results['distances'][0])
print(results['documents'][0][0])
# if str(48) in results['ids'][0]:
#     print('Correct page found')
# else:
#     print('Embedding not successfull.')
# print(results['documents'][0][0])