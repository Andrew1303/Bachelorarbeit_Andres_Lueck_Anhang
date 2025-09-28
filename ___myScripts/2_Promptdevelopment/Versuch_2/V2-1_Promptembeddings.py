import json
import requests

# DESCRIPTION
# This file is the first attempt to reach out for an API (Application Programming Interface) that converts texts into embeddings and returns the results.
# It it used to preprocess prompts and save the embeddings to use different llm's on a single low performance computer by splitting the processes into several steps.

# ---------------------------------------- GET PROMPTS -----------------------------------------------------------
with open(r"___myScripts\Promptdevelopment\Prompts_Dic.json") as jsondata:
    prompts = json.load(jsondata)

embedded_prompts = {}

# --------------------------------------- DEFINE PARTNAME --------------------------------------------------------
partname = input("Whats the name of the part you are searching a base failure rate for?\n")

# Read each language in prompts
for language in prompts:
    # Create an empty list of prompts for key language
    embedded_prompts[language] = {}
    for index, prompt in enumerate(prompts[language]):
        # -- Replace each [itemname] with searched itemname
        prompt = prompt.replace("[itemname]", partname)
        data = {"chunks": [prompt]}
        # Calculate embedding 
        embedding = requests.get("http://127.0.0.1:8000/embeddings", json=data)
        # append
        embedded_prompts[language][index] = {
            "prompt": prompt,
            "embedding": embedding.json()[0]
        }


# print(embedded_prompts)

name = "TEST"

with open(f"___myScripts\\2_Promptdevelopment\\Versuch_2\\GeneratedPromptsWithEmbeedings\\{name}.json", "w") as outfile:
    json.dump(embedded_prompts, outfile)