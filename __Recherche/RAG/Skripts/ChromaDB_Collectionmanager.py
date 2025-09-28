import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
import PyPDF2
from ollama_embedd import get_embedding, OllamaEmbeddingFunction
import winsound
import requests
# EMBEDDINGS: https://huggingface.co/blog/getting-started-with-embeddings
# https://cookbook.chromadb.dev/core/clients/#http-client

# --------------------------------------------------------------------------------------------------------------------
# ------------------------------------------- CREATE CLIENT ----------------------------------------------------------

client = chromadb.PersistentClient(
    path=r"__Recherche\RAG\Skripts\chromadb",
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE
)

# --------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ CLIENT FUNCTIONS --------------------------------------------------------

def addCollection(collection_name:str, documents:list[str], ids:list[str], embeddings:list[str], model:str):
    collection = client.create_collection(
        name=collection_name,
        embedding_function=OllamaEmbeddingFunction(model)
    )

    collection.add(
        documents= documents,
        ids=ids,
        embeddings=embeddings
    )
    return True

def deleteCollection(collection_name:str):
    client.delete_collection(collection_name)
    return True

def getCollectionStatus():
    amount_collections = client.count_collections()
    collectionnames = client.list_collections()
    print(f"There are {amount_collections} collections.\nNames are {collectionnames}")

def extract_text_from_pdf(pdf_file:str, model:str):
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pdf_text = []
        ids = []
        embeddings = []
        counter = 1

        for page in reader.pages:  
            content = page.extract_text()
            pdf_text.append(content)
            ids.append(str(counter))
            embedding = get_embedding(content, model)
            embeddings.append(embedding)
            counter += 1
            print(f"{round(counter*100/len(reader.pages), 2)}%", end="\r")
        print("Calculating embeddings", end="\r")
        # embeddings = [model.encode(text).tolist() for text in pdf_text]
        print("Finsihed calculating embeddings!", end="\r")
        return {"documents": pdf_text, "ids": ids, "embeddings": embeddings}

# --------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------ RUN ---------------------------------------------------------------
models = ["qwen2.5:7b", "qwen2.5:14b", "qwen2.5:32b", "nomic-embed-text", "granite-embedding:30m", "granite-embedding:278m"]
# documentname = "Umdenken_der_Mobilität_Lück_Scherer"
documentname = "MIL-HDBK-217F"
mode = input("Select your mode for collections.\n• Add\n• Del\n• Repl\n• List\n")

if mode == "Add":
    counter = 0
    print("Available models:")
    for model in models:
        counter += 1
        print(f"• [{counter}] {model}")
    model = models[int(input("\nSelect your model (number)\n")) - 1]
    collectionname = f"{model.replace(":","----")}_{documentname.replace("ä", "ae").replace("ü", "ue").replace("ö", "oe")}"
    collections = []
    for collection in client.list_collections():
        collections.append(collection.name)
    # EXECUTE ADD
    if collectionname in collections:
        print(f'"{collectionname}" already used.')
    else:
        mil217 = extract_text_from_pdf(f"___testdata\\{documentname}.pdf", model)
        addCollection(collectionname, mil217["documents"], mil217["ids"], mil217["embeddings"], model)

elif mode == "Del":
    # Print list of all current names
    collections = []
    counter = 0
    print('List of available collections:\n')
    for collection in client.list_collections():
        counter += 1
        print(f'• [{counter}] {collection.name}')
        collections.append(collection.name)
    selectedCollectionPos = int(input("\nWhich collection should be deleted (number)?\n")) - 1
    selectedCollectionName = collections[selectedCollectionPos]
    # EXECUTE DELETE
    if selectedCollectionName in collections:
        deleteCollection(selectedCollectionName)
    else:
        print(f'"{selectedCollectionName}" not found!')

elif mode == "Repl":
    counter = 0
    for model in models:
        counter += 1
        print(f"• [{counter}]{model}\n")
    model = models[int(input("\nSelect your model (number)")) - 1]
    collections = []
    print('List of available collections:\n')
    for collection in client.list_collections():
        print(f'• {collection.name}')
        collections.append(collection.name)
    collectionname = input("\nWhich collection should be replaced with new embeddings?\n")
    # EXECUTE REPLACEMENT
    deleteCollection(collectionname)
    print("Delete completed.", end="\r")
    print("Recreate collection", end='\r')
    mil217 = extract_text_from_pdf(r"___testdata\MIL-HDBK-217F.pdf", model)
    addCollection(collectionname, mil217["documents"], mil217["ids"], mil217["embeddings"])

elif mode == "List":
    print('\n------------------------------------------------------\nList of all available collections:')
    for collection in client.list_collections():
        name = collection.name.replace("----", ":")
        print(f'• {collection.name}')

elif mode == "remoteAdd":
    url = "http://127.0.0.1:8000/embeddings"

    data = {
        "chunks": ["Hello", "This", "is"]
        }
    response = requests.get(url, json=data)

    print("Status code:", response.status_code)
    print("Response JSON:", response.json())
else:
    print(f"{mode} not a valid mode.")

# NEED FUNCTION TO CHECK IF COLLECTION ALREADY EXISTS BEFORE CALCULATING EMBEDDINGS

print("\nScript end.                            ")
winsound.PlaySound("*", winsound.SND_ALIAS)