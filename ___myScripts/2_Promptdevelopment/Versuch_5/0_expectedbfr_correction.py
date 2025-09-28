import os
import json
import numpy as np
import math
import matplotlib.pyplot as plt
from progresbar import progresbar

# Path to files
pathresults = ["___myScripts", "2_Promptdevelopment", "Versuch_5", "results"]
resultpath = os.path.join(*pathresults)

# -- Get results --
# Extract all available files in path
files = []
print("\nList of available files to calculate embeddings:")
for i, filename in enumerate(os.listdir(resultpath)):
    files.append(filename)

# Sort and show all options for the user
files.sort()
for i, file in enumerate(files):
    print(f"• [{i+1}] {file}")

# Select available file with prompts including embeddings
resultfile = files[int(input("\nWhich results should be used (number)?\n")) - 1]
print(f"Your selected results:\n\033[1;33m{resultfile}\033[0m\n")

# Open selected results
with open(f"{resultpath}/{resultfile}") as resultdata:
    results = json.load(resultdata)

# Path to objects
pathobjects = ["___myScripts", "2_Promptdevelopment", "Versuch_5", "Objects.json"]
objectspath = os.path.join(*pathobjects)

# Open objects file
with open(objectspath) as objectdata:
    objects = json.load(objectdata)

print(objects[0])
print(results[0].keys())

promptlen = len(results)
# progresbar(0, promptlen)
for p, prompt in enumerate(results):
    itemname = prompt["itemname"]
    for object in objects:
        if object[0] == itemname:
            if results[p]["expectedbfr"] != object[1]:
                differences = [bfr for bfr in object[1] if bfr not in results[p]["expectedbfr"]]
                results[p]["expectedbfr"] = object[1]
                print(f"Some values were missing in {object[0]}:\n{differences}\n")
    # progresbar(p+1, promptlen)

with open(f"{resultpath}/{resultfile}", "w") as outfile:
    json.dump(results, outfile)