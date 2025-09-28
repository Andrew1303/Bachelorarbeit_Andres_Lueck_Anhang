import json, os

# -- Get prompts with precalculated embedding --
# Select available file with prompts including embeddings
files = []
print("\nList of available files to calculate embeddings:")

# Generate path for promptlist with embeddings
Embeddingpathlist = ["___myScripts", "2_Promptdevelopment", "Versuch_5", "GeneratedPromptsWithEmbeddings"]

Embeddingpath = ""
for part in Embeddingpathlist:
    Embeddingpath = os.path.join(Embeddingpath, part)

# List all available promptlists with embeddings
for index, filename in enumerate(os.listdir(Embeddingpath)):
    files.append(filename)
files.sort()
for index, file in enumerate(files):
    print(f"• [{index+1}] {file}")

# Select promptlist
promptlistname = files[int(input("\nWhich promptlist should be used (number)?\n")) - 1]
print(f"Your selected promptlistfile: \033[1;33m{promptlistname}\033[0m")

# Add selected promptlistname to path and open file
Embeddingpath = os.path.join(Embeddingpath, promptlistname)
with open(Embeddingpath) as jsondata:
    prompts = json.load(jsondata)

# Extract all items from prompts
items = []
for language in prompts:
    for prompt in prompts[language]:
        if prompt["itemname"] not in items:
            items.append(prompt["itemname"])

# Return amount of items and name of each item
print("Amount of items:", len(items))
for item in items:
    print(item)