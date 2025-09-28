import json, os
import requests
from progresbar import progresbar
import datetime

# Get path for objectlist
pathpartlist = ["___myScripts", "2_Promptdevelopment", "Versuch_5", "Objects.json"]
promptlistpath = os.path.join(*pathpartlist)

with open(promptlistpath) as jsondata:
    items = json.load(jsondata)

# PREPARE EMBEDDINGS

# DESCRIPTION
# This file is the first attempt to reach out for an API (Application Programming Interface) that converts texts into embeddings and returns the results.
# It it used to preprocess prompts and save the embeddings to use different llm's on a single low performance computer by splitting the processes into several steps.

# ---------------------------------------- GET PROMPTS -----------------------------------------------------------
# Generate path to promptlists
pathpromptlist = ["___myScripts", "2_Promptdevelopment", "Prompts"]
promptlistpath = os.path.join(*pathpromptlist)

# List all promptlists
files = []
print("\nList of available files to calculate embeddings:")
for index, filename in enumerate(os.listdir(promptlistpath)):
    files.append(filename)
    filename = filename.replace(".json", "")
    print(f"• [{index+1}] {filename}")

# Select promptlist
promptlistname = files[int(input("\nWhich promptlist should be used (number)?\n")) - 1]
print(f"Your selected promptlistfile: \033[1;33m{promptlistname}\033[0m")

# Generate path for promptlist
promptlistpathlist = ["___myScripts", "2_Promptdevelopment", "Prompts", promptlistname]
promptlistpath = os.path.join(*promptlistpathlist)

# Open promptlist
with open(promptlistpath) as jsondata:
    prompts = json.load(jsondata)

# Get amounts of prompts for progresbar
amount_prompts = 0
for language in prompts:
    for prompt in prompts[language]:
        amount_prompts += 1
print(f"Amount prompts: {amount_prompts}")

amount_items = 0
for item in items:
    if item[3] == "":
        amount_items += 1
print(f"Amount items: {amount_items}")

amount_prompts = amount_items*amount_prompts

# Read each language in prompts
embedded_prompts = {}
counter = 0
progresbar(counter, amount_prompts)
for language in prompts:
    # Create an empty list of prompts for key language
    embedded_prompts[language] = []
    for index, prompt in enumerate(prompts[language]):
        for item in items:
            if item[3] != "":
                continue
            # -- Replace each [itemname] with searched itemname and calculate embeddings
            newprompt = prompt.replace("[itemname]", item[0])
            data = {"chunk": newprompt}
            embedding = requests.get("http://127.0.0.1:8000/embeddings", params=data)
            embedded_prompts[language].append({
                "prompt": newprompt,
                "itemname": item[0],
                "embedding": embedding.json(),
                "expectedbfr": item[1]
                }
            )
            counter += 1
            progresbar(counter, amount_prompts)

# Create name for savefile
date = datetime.datetime.now()
name = f"{date.year}{date.month:02d}{date.day:02d}{date.hour:02d}{date.minute:02d}_{promptlistname}"

# Get path for savefile
savepathlist = ["___myScripts", "2_Promptdevelopment", "Versuch_5", "GeneratedPromptsWithEmbeddings", f"{name}"]
savepath = os.path.join(*savepathlist)

# Save the file   
with open(savepath, "w") as outfile:
    json.dump(embedded_prompts, outfile)