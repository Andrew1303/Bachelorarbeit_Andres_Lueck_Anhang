import json, os
import requests
from progresbar import progresbar
import time, datetime

# Get path for objectlist
pathpartlist = ["___myScripts", "2_Promptdevelopment", "Versuch_3", "Objects.json"]
itemlistpath = os.path.join(*pathpartlist)

with open(itemlistpath) as jsondata:
    items = json.load(jsondata)


# ---------------------------------------- GET PROMPTS -----------------------------------------------------------
# Generate path to promptlists
pathpromptlist = ["___myScripts", "2_Promptdevelopment", "Prompts"]
promptlistpath = os.path.join(*pathpromptlist)

# List all promptlists
promptlists = []
print("\nList of available promptlists:")
for index, promptlist in enumerate(os.listdir(promptlistpath)):
    promptlists.append(promptlist)
promptlists.sort()
for i, promptlist in enumerate(promptlists):
    promptlist.replace(".json", "")
    print(f"• [{i+1}] {promptlist}")

# Select promptlist
promptlistname = promptlists[int(input("\nWhich promptlist should be used (number)?\n")) - 1]
print(f"Your selected promptlistfile: \033[1;33m{promptlistname}\033[0m")

# Open promptlist by adding the selected file
with open(os.path.join(promptlistpath, promptlistname)) as jsondata:
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
keyword_promptlist = []
counter = 0
progresbar(counter, amount_prompts)
for language in prompts:
    for index, prompt in enumerate(prompts[language]):
        for item in items:
            if item[3] != "":
                continue
            # -- Replace each [itemname] with searched itemname and calculate embeddings
            # newprompt = prompt.replace("[itemname]", item[0])
            # data = {"chunk": newprompt}
            # embedding = requests.get("http://127.0.0.1:8000/embeddings", params=data)
            # embedded_prompts[language].append({
            #     "prompt": newprompt,
            #     "itemname": item[0],
            #     "embedding": embedding.json(),
            #     "expectedbfr": item[1]
            #     }
            # )
            keyword_promptlist.append(
                {
                "prompt": prompt.replace("[itemname]", item[0]),
                "itemname": item[0],
                "expectedbfr": item[1],
                # "keywords": [item[0], "base", "failure", "rate", "table"]
                "keywords": item[0].split()
            })
            counter += 1
            progresbar(counter, amount_prompts)
# Create name for savefile
date = datetime.datetime.now()
name = f"{date.year}{date.month:02d}{date.day:02d}{date.hour:02d}{date.minute:02d}_{promptlistname}_keywordversion"

# Get path for savefile
savepathlist = ["___myScripts", "2_Promptdevelopment", "Versuch_4", "promptsWithKeywords", f"{name}.json"]
savepath = os.path.join(*savepathlist)

# Save the file
with open(savepath, "w") as outfile:
    json.dump(keyword_promptlist, outfile)