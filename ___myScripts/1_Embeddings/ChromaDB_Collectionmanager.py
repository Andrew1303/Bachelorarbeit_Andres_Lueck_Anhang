import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
import PyPDF2
from ollama_embedd import get_embedding, OllamaEmbeddingFunction
from progresbar import progresbar
import requests
import os
# EMBEDDINGS: https://huggingface.co/blog/getting-started-with-embeddings
# https://cookbook.chromadb.dev/core/clients/#http-client

# --------------------------------------------------------------------------------------------------------------------
# ------------------------------------------- CREATE CLIENT ----------------------------------------------------------

# -- Generate relativ clientpath --

clientpathlist = ["database", "chromadb"]
clientpath = ""
for pathpart in clientpathlist:
    clientpath = os.path.join(clientpath, pathpart)

# -- Connect to client
client = chromadb.PersistentClient(
    path = clientpath,
    settings = Settings(),
    tenant = DEFAULT_TENANT,
    database = DEFAULT_DATABASE
)

print(clientpath)

URL_EmbeddingAPI = "http://127.0.0.1:8000/embeddings"

# --------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ CLIENT FUNCTIONS --------------------------------------------------------

def addCollection(collection_name:str, documents:list[str], ids:list[str], embeddings:list[list[float]], model:str):
    collection = client.create_collection(
        name=collection_name
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

def extract_text_from_pdf(pdf_file:str):
    print("Extract whole text of selected pdf file.")
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)
        completeText = ""
        amountPages = len(reader.pages)
        counter = 1
        for page in reader.pages: 
            progresbar(counter, amountPages)
            completeText = completeText + page.extract_text()
            counter += 1
        return completeText

def extract_text_from_pdf_pagewise(path_to_pdf:str):
    with open(path_to_pdf, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)
        amountPages = len(reader.pages)
        chunks = []
        ids = []  
        for index, page in enumerate(reader.pages):
            progresbar(index+1, amountPages)   
            content = page.extract_text()
            chunks.append(content)
            ids.append(str(index))
        return {"documents": chunks, "ids": ids}
    
def extract_text_from_pdf_chunky(pdf_file:str, model:str, chunkLength:int):
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)
        pdf_text = []
        ids = []
        embeddings = []
        counter = 1
        completeText = ""
        amountPages = len(reader.pages)
        counter = 0
        print("Generate Text from PDF")
        for page in reader.pages:
            progresbar(counter, amountPages)   
            counter += 1
            completeText = completeText + page.extract_text()
        progresbar(counter, amountPages) 
        print("Generate chunks")
        counter = 0
        while completeText != "":
            cuttedText = completeText[:chunkLength]
            completeText = completeText[chunkLength:]
            pdf_text.append(cuttedText)
            ids.append(str(counter))
            counter += 1
        print("Generate embeddings for each chunk")
        counter = 0
        amountTexts = len(pdf_text)
        for text in pdf_text:
            progresbar(counter, amountTexts)
            counter += 1
            embedding = get_embedding(text, model)
            embeddings.append(embedding)
        progresbar(counter, amountTexts)   
        return {"documents": pdf_text, "ids": ids, "embeddings": embeddings}
    
def chunking(Text:str, chunkLength:int, overlapping:float) -> list[str]:
    """Text: Text is the string that should be chunked
    chunkLength: chunkLength is the amount of characters per chunk
    overlapping: overlappings defines how much percentage of the previous chunk should stay for the following chunk"""
    assert overlapping < 1, "Overlapping must be under 1 (100%)"
    assert overlapping >= 0, "Overlapping must be bigger than or equal 0 (0%)"
    chunktext = Text
    chunks = []
    ids = []
    counter = 0
    print(f"Create chunks from text.")
    amountCutting = int((1-overlapping)*chunkLength)
    while chunktext != "":
        # progresbar((maxlength - chunkLength*counter), maxlength)
        chunk = chunktext[:chunkLength]
        chunktext = chunktext[amountCutting:]
        chunks.append(chunk)
        ids.append(str(counter))
        counter += 1
    print("Chunked.")
    # print(len(chunks))
    return {"documents": chunks, "ids": ids}

# FUNCTION TO SELECT DOCUMENT TO MAKE EMBEDDINGS FOR
def selectPDF():
    files = []
    for filename in os.listdir("Dokumente"):
        files.append(filename)
    return files

# --------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------ RUN ---------------------------------------------------------------
models = ["qwen2.5:7b", "qwen2.5:14b", "qwen2.5:32b", "nomic-embed-text", "granite-embedding:30m", "granite-embedding:278m"]
# documentname = "Umdenken_der_Mobilität_Lück_Scherer"
documentname = "MIL-HDBK-217F"
mode = input("Select your mode for collections.\n• Add\n• Del\n• Repl\n• List\n")

if mode == "Add2":
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
        Chunklength = int(input('What is the Chunklength you wanna use? [Int]\n'))
        # mil217 = extract_text_from_pdf_pagewise(f"Dokumente\\{documentname}.pdf", model)
        mil217 = extract_text_from_pdf_chunky(f"Dokumente\\{documentname}.pdf", model, Chunklength)
        addCollection(collectionname + f"_Chunk-{Chunklength}", mil217["documents"], mil217["ids"], mil217["embeddings"], model)

elif mode == "Del":
    # Print list of all current names
    collections = []
    print('List of available collections:\n')
    for index, collection in enumerate(client.list_collections()):
        print(f'• [{index + 1}] {collection.name}')
        collections.append(collection.name)
    selectedCollectionPos = int(input("\nWhich collection should be deleted (number)?\n")) - 1
    selectedCollectionName = collections[selectedCollectionPos]
    # EXECUTE DELETE
    if selectedCollectionName in collections:
        deleteCollection(selectedCollectionName)
    else:
        print(f'"{selectedCollectionName}" not found!')

elif mode == "Repl":
    for index, model in enumerate(models):
        print(f"• [{index + 1}]{model}\n")
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
    mil217 = extract_text_from_pdf_pagewise(f"Dokumente\\{documentname}.pdf", model)
    addCollection(collectionname, mil217["documents"], mil217["ids"], mil217["embeddings"])

elif mode == "List":
    print('\n------------------------------------------------------\nList of all available collections:')
    for collection in client.list_collections():
        name = collection.name.replace("----", ":")
        print(f'• {collection.name}')

elif mode == "Add":

    # Define the name of the used llm of the API
    # model = "gte-Qwen2-1.5B-instruct"
    model = "Qwen3-Embedding-8B"

    # Select the pdf document for the embedding calculation
    files = selectPDF()
    print("List of available files to calculate embeddings:")
    counter = 0
    for index, file in enumerate(files):
        print(f"• [{index+1}] {file}")
    documentindex = int(input("\nWhich file should be used to calculate embeddings (number)?\n")) - 1
    documentname = files[documentindex].replace(".pdf", "")
    print(documentname)
    
    # Get all names of available collections in client
    collections = []
    for collection in client.list_collections():
        collections.append(collection.name)

    # Select mode for chunking
    chunkmode = int(input(f"\nSelect chunkmode:\n• [1] Chunks by length\n• [2] Chunks by page\n"))

    # MODE: By length
    if chunkmode == 1:
        # Define the amount of characters for each chunk
        Chunklength = int(input('What is the Chunklength you wanna use? [Int]\n'))
        # Define the percentage of overlapping of each chunk
        overlapping = float(input('How much overlapping [%] do you want for each chunk? [Float]\n'))

        # Generate the name of the new collection (by length)
        version = 1
        collectionname = f"{model.replace(":","----")}_{documentname.replace("ä", "ae").replace("ü", "ue").replace("ö", "oe")}_lenchunk-{Chunklength}_ol-{overlapping}_V{version}"
        while collectionname in collections:
            version += 1
            collectionname = f"{model.replace(":","----")}_{documentname.replace("ä", "ae").replace("ü", "ue").replace("ö", "oe")}_lenchunk-{Chunklength}_ol-{overlapping}_V{version}"
        # Extract the string of the pdf
        

        pathlist = ["Dokumente", f"{documentname}.pdf"]
        pdfPath = ""
        for folder in pathlist:
            pdfPath = os.path.join(pdfPath, folder)
        pdfText = extract_text_from_pdf(pdfPath)
        # Split the extracted string in different chunks by predefined parameters
        chunks = chunking(pdfText, Chunklength, overlapping)

    # MODE: Pagewise
    elif chunkmode == 2:
        # Generate the name of the new collection (pagewise)
        version = 1
        collectionname = f"{model.replace(":","----")}_{documentname.replace("ä", "ae").replace("ü", "ue").replace("ö", "oe")}_pagechunk_V{version}"
        while collectionname in collections:
            version += 1
            collectionname = f"{model.replace(":","----")}_{documentname.replace("ä", "ae").replace("ü", "ue").replace("ö", "oe")}_pagechunk_V{version}"
        # Split pages of pdf and create chunks
        pathlist = ["Dokumente", f"{documentname}.pdf"]
        pdfPath = ""
        for folder in pathlist:
            pdfPath = os.path.join(pdfPath, folder)
        chunks = extract_text_from_pdf_pagewise(pdfPath)

    # -- Stepwise api request code: --
    embeddings = []
    amountChunks = len(chunks["documents"])
    
    for index, chunk in enumerate(chunks["documents"]):
        progresbar(index, amountChunks)
        data = {"chunk": chunk}
        hellourl = "http://127.0.0.1:8000/hello"
        # response = requests.get(URL_EmbeddingAPI, params=data)
        response = requests.get(URL_EmbeddingAPI, params=data)
        # Checkprints for debugging
        # print("Status code:", response.status_code)
        # if index == 0:
        #     print(response.json())
        embeddings.append(response.json())
    # # -- Onestep api request code: --
    # data = {"chunks": chunks["documents"]}
    # embeddings = requests.get(URL_EmbeddingAPI, json=data)

    # Add embedding results to collection with defined collectionname
    addCollection(collectionname, chunks["documents"], chunks["ids"], embeddings, "gte-qwen2-1.5B")
    print(f"Collection named '{collectionname}' added")
elif mode == "Test":
    params = {"name": "Andres"}
    hellourl = "http://127.0.0.1:8000/hello"
    response = requests.get(hellourl, params=params)
    print(response.json())
else:
    print(f"{mode} not a valid mode.")

# NEED FUNCTION TO CHECK IF COLLECTION ALREADY EXISTS BEFORE CALCULATING EMBEDDINGS

print("\nScript end.                            Ay! What about using langchain?")