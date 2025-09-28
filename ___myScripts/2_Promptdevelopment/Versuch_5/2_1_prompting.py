import json, os
import time, datetime
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
import numpy as np
from Fct_LLM_API import ChattingOne
import re #Regex
from progresbar import progresbar

# DESCRIPTION
# ! This script requires precalculated embeddings for prompts and knowledge base. !
# This script is made to generate base failure rates with RAG (Retrieval Augmented Generation) and a LLM (Large Language Model)
# The result is saved in a file which can be used to verify the correctness of it.

version = "V7" #Version 3, 
models = [
    {"name": "qwen3:32b", "size": 18},
    {"name": "deepseek-r1:14b", "size": 9},
    {"name": "gpt-oss:20b", "size": 14}
]

gemmamodels = [
    {"name": "gemma3:270m", "size": 0.29},
    {"name": "gemma3:1b", "size": 0.81},
    {"name": "gemma3:4b", "size": 3.3},
    {"name": "gemma3:12b", "size": 8.1},
    {"name": "gemma3:27b", "size": 17},
]

llamamodels = [
    {"name": "llama3.2:1b", "size": 1.3},
    {"name": "llama3.2:3b", "size": 2},
    {"name": "llama3:8b", "size": 4.7},
    {"name": "llama3.3:latest", "size": 43},
]

deepseekmodels = [
    {"name": "deepseek-r1:1.5b", "size": 1.1},
    {"name": "deepseek-r1:8b", "size": 5.2},
    {"name": "deepseek-r1:14b", "size": 9},
    {"name": "deepseek-r1:32b", "size": 20},
    {"name": "deepseek-r1:70b", "size": 43}
]

qwen3models = [
    {"name": "qwen3:0.6b", "size": 0.5},
    {"name": "qwen3:1.7b", "size": 1.4},
    {"name": "qwen3:4b", "size": 2.5},
    {"name": "qwen3:8b", "size": 5.2},
    {"name": "qwen3:14b", "size": 9.3},
    {"name": "qwen3:30b", "size": 18},
    {"name": "qwen3:32b", "size": 20}
]

falcon3models = [
    {"name": "falcon3:1b", "size": 1.8},
    {"name": "falcon3:3b", "size": 2},
    {"name": "falcon3:7b", "size": 4.6},
    {"name": "falcon3:10b", "size": 6.3},
]

singlemodel = [
    {"name": "deepseek-r1:1.5b", "size": 1.1}
]

modellist = falcon3models
evamodellist = falcon3models

# model = models[4]["name"]

# - Get embeddings precalculated -

# -- Generate relativ clientpath --

clientpathlist = ["database", "chromadb"]
clientpath = ""
for pathpart in clientpathlist:
    clientpath = os.path.join(clientpath, pathpart)

# -- Open client --
client = chromadb.PersistentClient(
    path = clientpath,
    settings = Settings(),
    tenant = DEFAULT_TENANT,
    database = DEFAULT_DATABASE
)

# -- Choose the collection for the process --
# Get all collection names
collections = []
for index, collection in enumerate(client.list_collections()):
    collections.append(collection.name)
collections.sort()
# Show all available collections
print("\n\033[1;33mList of available collections:\033[0m")
for index, name in enumerate(collections):
    name = name.replace("----", ":")
    print(f'• [{index + 1}] {name}')
selectedCollection = collections[int(input("\nSelect collection for RAG (number)\n")) - 1]
print(f"\nYour selected collection: \033[1;33m{selectedCollection}\033[0m")

# Load the collection from the client
collection = client.get_collection(selectedCollection)
# Get the data of the selected collection
collectionData = collection.get(include=["documents", "embeddings"])
embeddings = collectionData["embeddings"]
contextlist = collectionData["documents"]

# Get prompts with precalculated embedding
# Select available file with prompts including embeddings
Promptpathlist = ["___myScripts", "2_Promptdevelopment", "Versuch_5", "GeneratedPromptsWithEmbeddings"]
Promptpath = ""
for pathpart in Promptpathlist:
    Promptpath = os.path.join(Promptpath, pathpart)

files = []
print("\nList of available files to calculate embeddings:")
for index, filename in enumerate(os.listdir(Promptpath)):
    files.append(filename)
    print(f"• [{index+1}] {filename}")

promptlistname = files[int(input("\nWhich promptlist should be used (number)?\n")) - 1]
print(f"Your selected promptlistfile: \033[1;33m{promptlistname}\033[0m")

# Open selected file including prompts with embeddings
SelectedPromptpath = os.path.join(Promptpath, promptlistname)
with open(SelectedPromptpath) as jsondata:
    prompts = json.load(jsondata)

# -- Process all prompts with n iterations and save results in a json file. --
iterations = int(input("Define the amount of iterations for each prompt (number)\n"))

# Calculate the amount of prompts in promptlist
amount_prompts = 0
for language in prompts:
    amount_prompts += len(prompts[language])
    # print(f"{language}: {len(prompts[language])}")
maxlength = amount_prompts*iterations*len(modellist)*len(evamodellist)
print(f"Prompts: {amount_prompts}\nModels: {len(modellist)}\nIterations: {iterations}\nSum: {maxlength}")
input("Press enter to continue")

# Start prompting
counter = 0
results = []

progresbar(counter, maxlength)

# For each evaluation model 
for em, evamodel in enumerate(evamodellist):
    # For each model (5)
    for m, model in enumerate(modellist):
        model = model["name"]
        # For each language (1)
        for language in prompts:
            # for each prompt (55)
            for p, prompt in enumerate(prompts[language]):
                durations = []
                firstanswers = []
                answers = []
                foundbfrs = []
                # For each iteration
                for _ in range(iterations):
                    # Get the context with cosine similarity
                    promptembedding = prompt["embedding"]
                    scores = (promptembedding @ np.array(embeddings).T) * 100
                    scores = scores.tolist()
                    highest_score_index = scores.index(max(scores))
                    context = contextlist[highest_score_index]
                    # Final prompt
                    temperature = 0.2
                    start = time.time()
                    firstresult = ChattingOne(f"{prompt["prompt"]}", context, model, temperature)
                    firstanswers.append(firstresult)
                    finalresult = ChattingOne("Return all available base failure rates from the following answer.\n\nReturn only the numbers of the base failure rates without unit in a list. Use hyphens (-) for bullet points, without numbering.\n", firstresult, evamodel["name"], temperature)
                    end = time.time()
                    durations.append(end-start)
                    answers.append(finalresult)
                    # Quelle: https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string
                    # numbers = re.findall(r"(?:\d*\.*\d+)", result)
                    filtered_finalresult = re.sub(r'10\^(\d+)', '', finalresult)
                    numbers = re.findall(r"\d+(?:[.,]\d+)?", filtered_finalresult)
                    numbers = [num.replace(",", ".") for num in numbers]
                    foundbfrs.append([float(num) for num in numbers])
                    counter += 1
                    progresbar(counter, maxlength)
                # Summarize the results in a dictionary
                partial_result = {
                    "model": selectedCollection.split("_")[0],
                    "llm": model,
                    "evallm": evamodel,
                    "language": language,
                    "prompt": prompt["prompt"],
                    "itemname": prompt["itemname"],
                    "expectedbfr": prompt["expectedbfr"],
                    "context": context,
                    "goodcontext": "neutral",
                    "results": {
                        "duration": durations,
                        "firstanswers": firstanswers,
                        "answer": answers,
                        "found_bfrs": foundbfrs
                    }
                }
                results.append(partial_result)
                # print(counter)
                # TESTING:
        #         print(p)
        #         if p == 0:
        #             break
        # print(m)
        # if m == 0:
        #     break
progresbar(counter, maxlength)


amount_languages = len(prompts)
date = datetime.datetime.now()
name = f"{version}_{date.year}{date.month:02d}{date.day:02d}{date.hour:02d}{date.minute:02d}{date.second:02d}_al-{amount_languages}_ap-{amount_prompts}_it-{iterations}_temp-{temperature}_{promptlistname.split(".json")[0]}_{selectedCollection}_{model}"
name = name.replace(".", "_")
name = name.replace(":", "_")
savepathlist = ["___myScripts", "2_Promptdevelopment", "Versuch_5", "results", f"{name}.json"]
savepath = ""
for part in savepathlist:
    savepath = os.path.join(savepath, part)

with open(savepath, "w") as outfile:
    json.dump(results, outfile)

# # Request llm for each prompt and embedding
# for language in prompts:
#     for id in prompts[f"{language}"]:
#         # Available info: prompt, embedding

#         promptembedding = prompts[language][id]["embedding"]
#         scores = (promptembedding @ np.array(embeddings).T) * 100
#         scores = scores.tolist()
#         highest_score_index = scores.index(max(scores))
#         context = result["documents"][highest_score_index]
#         print(f"\033[1;34m{prompts[language][id]["prompt"]}\033[0m")
#         showcontext = input('Send "y" to show context? (Enter to skip)')
#         if showcontext == "y":
#             print(context)

#         # Request with prompt and context
#         start = time.time()
#         finalresult = ChattingOne(f"{prompts[f"{language}"][f"{id}"]["prompt"]}", context, "llama3.2-vision:latest", temperature=0.2)
#         end = time.time()
#         duration = end - start
#         print(finalresult)
#         print(f'Duration: {duration}')
#         input("Continue: Press Enter")