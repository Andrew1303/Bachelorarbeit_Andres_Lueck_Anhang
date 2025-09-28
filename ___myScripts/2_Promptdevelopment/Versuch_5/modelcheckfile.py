import os, json

# Path to files
pathresults = ["___myScripts", "2_Promptdevelopment", "Versuch_5", "results"]
resultpath = os.path.join(*pathresults)

# -- Get results --
# Select available file with prompts including embeddings
files = []
print("\nList of available files to calculate embeddings:")
for index, filename in enumerate(os.listdir(resultpath)):
    files.append(filename)
files.sort()
for index, file in enumerate(files):
    print(f"• [{index+1}] {file}")

resultfile = files[int(input("\nWhich results should be used (number)?\n")) - 1]
print(f"Your selected results:\n\033[1;33m{resultfile}\033[0m\n")

# Open selected results
with open(f"{resultpath}/{resultfile}") as jsondata:
    results = json.load(jsondata)

models = []
for r, result in enumerate(results):
    if result["llm"] not in models:
        models.append(result["llm"])

print(models)