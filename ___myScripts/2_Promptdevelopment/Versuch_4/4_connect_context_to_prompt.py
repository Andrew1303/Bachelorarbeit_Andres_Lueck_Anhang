import os, json
from progresbar import progresbar
import datetime
# Get path for documentpages
pathpartlist = ["___myScripts", "2_Promptdevelopment", "Versuch_4", "documentpages"]
documentpagespath = os.path.join(*pathpartlist)

# List all promptlists
documentlists = []
print("\nList of available promptlists:")
for index, list in enumerate(os.listdir(documentpagespath)):
    documentlists.append(list)
documentlists.sort()
for j, list in enumerate(documentlists):
    list.replace(".json", "")
    print(f"• [{j+1}] {list}")

# Select promptlist
documentlistname = documentlists[int(input("\nWhich promptlist should be used (number)?\n")) - 1]
print(f"Your selected promptlistfile: \033[1;33m{documentlistname}\033[0m")

with open(os.path.join(documentpagespath, documentlistname)) as jsondata:
    documentpages = json.load(jsondata)

# Get path for prompts with keywords
pathpartlist = ["___myScripts", "2_Promptdevelopment", "Versuch_4", "promptsWithKeywords"]
promptkeywordlist = os.path.join(*pathpartlist)

# List all promptlists
promptkeylists = []
print("\nList of available promptlists:")
for index, list in enumerate(os.listdir(promptkeywordlist)):
    promptkeylists.append(list)
promptkeylists.sort()
for j, list in enumerate(promptkeylists):
    list.replace(".json", "")
    print(f"• [{j+1}] {list}")

# Select promptlist
promptkeylistname = promptkeylists[int(input("\nWhich promptlist should be used (number)?\n")) - 1]
print(f"Your selected promptlistfile: \033[1;33m{promptkeylistname}\033[0m")

with open(os.path.join(promptkeywordlist, promptkeylistname)) as jsondata:
    promptkeywordlist = json.load(jsondata)

print(promptkeywordlist[0])
print(documentpages[0])
# FIND CONTEXT
contextscore = []
# For each prompt
counter = 1
for i, keywordprompt in enumerate(promptkeywordlist):
    # progresbar(i, len(promptkeywordlist))
    # Iterate over each page
    pagescores = []
    for j, page in enumerate(documentpages):
        if j < 8:
            continue
        else:
        # Check each key for the page and define a score
            keyhitrate = 0
            for key in keywordprompt["keywords"]:
                if key in page:
                    keyhitrate += 1
            pagescores.append({"pageindex": j, "keyhitrate": keyhitrate/len(keywordprompt["keywords"])})
    highestscore = sorted(pagescores, key=lambda x: x["keyhitrate"], reverse=True)
    highestscore = highestscore[0]
    print(f"{keywordprompt["prompt"]}\n{highestscore}\n\n")
    keywordprompt["context"] = documentpages[highestscore["pageindex"]]
    # contextfind = {"prompt": keywordprompt["prompt"], "pagescores": pagescores}    #

# SAVE CONTEXT PROMPT FILE
date = datetime.datetime.now()
name = f"{date.year}{date.month:02d}{date.day:02d}{date.hour:02d}{date.minute:02d}_Prompts_Dic_with_context"
# Get path for savefile
savepathlist = ["___myScripts", "2_Promptdevelopment", "Versuch_4", "promptsWithContext", f"{name}.json"]
savepath = os.path.join(*savepathlist)

# Save the file
with open(savepath, "w") as outfile:
    json.dump(promptkeywordlist, outfile)