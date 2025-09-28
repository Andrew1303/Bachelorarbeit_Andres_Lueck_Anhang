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

version = "V3" #Version 3, 

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
Promptpathlist = ["___myScripts", "2_Promptdevelopment", "Versuch_3", "GeneratedPromptsWithEmbeddings"]
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
    print(f"{language}: {len(prompts[language])}")
print(amount_prompts)
input("Press enter to continue")

# Start prompting
counter = 0
results = []
progresbar(counter, amount_prompts*iterations)
for language in prompts:
    for prompt in prompts[language]:
        durations = []
        answers = []
        foundbfrs = []
        for n in range(iterations):
            # Get the context with cosine similarity
            promptembedding = prompt["embedding"]
            scores = (promptembedding @ np.array(embeddings).T) * 100
            scores = scores.tolist()
            highest_score_index = scores.index(max(scores))
            context = contextlist[highest_score_index]
            # Final prompt
            temperature = 0.2
            start = time.time()
            finalresult = ChattingOne(f"{prompt["prompt"]}", context, "llama3.3:latest", temperature)
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
            progresbar(counter, amount_prompts*iterations)
        # Summarize the results in a dictionary
        partial_result = {
            "model": selectedCollection.split("_")[0],
            "language": language,
            "prompt": prompt["prompt"],
            "itemname": prompt["itemname"],
            "expectedbfr": prompt["expectedbfr"],
            "context": context,
            "goodcontext": "neutral",
            "results": {
                "duration": durations,
                "answer": answers,
                "found_bfrs": foundbfrs
            }
        }
        results.append(partial_result)
progresbar(counter, amount_prompts*iterations)

amount_languages = len(prompts)
date = datetime.datetime.now()
name = f"{version}_{date.year}{date.month:02d}{date.day:02d}{date.hour:02d}{date.minute:02d}_al-{amount_languages}_ap-{amount_prompts}_it-{iterations}_temp-{temperature}_{promptlistname.split(".json")[0]}_{selectedCollection}"

savepathlist = ["___myScripts", "2_Promptdevelopment", "Versuch_3", "results", f"{name}.json"]
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