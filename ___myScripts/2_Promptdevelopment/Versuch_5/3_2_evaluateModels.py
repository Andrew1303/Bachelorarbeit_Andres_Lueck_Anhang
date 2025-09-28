import os
import json
import numpy as np
import math
import matplotlib.pyplot as plt

Versuch = "11"

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

# print(f"Amount: {len(results)}")
# # print(f"Example: {results[0]}")
# print(f"Cleaned example:\n")
# print(f"Prompt: {results[0]["prompt"]}")
# print(f"Item: {results[0]["itemname"]}")
# print(f"expected bfrs: {results[0]["expectedbfr"]}")
# print(f"found bfrs: {results[0]["results"]["found_bfrs"]}")
# print(f"Duration: {results[0]["results"]["duration"]}")
# print(f"Mean duration: {np.mean(results[0]["results"]["duration"])}")

# ------ CREATE TABLEDATA -------

# Generate list of all models in dataset
llmlist = []
llm2list = []
for p, prompt in enumerate(results):
    if "llm" in prompt:
        if prompt["llm"] not in llmlist:
            llmlist.append(prompt["llm"])
    if "llm2" in prompt:
        if prompt["llm2"] not in llm2list:
            llm2list.append(prompt["llm2"])

print(llmlist)
print(llm2list)

sumhit = 0
summiss = 0
Tabledata = {}
for l, llm in enumerate(llmlist):
    llmperformance = {}
    for index in range(len(results)):
        name = results[index]["itemname"]
        hit = 0
        miss = 0
        # Check for llm
        if llm == results[index]["llm"]:
            # Check every single found bfrs and set hit or miss for the current llm
            for list in results[index]["results"]["found_bfrs"]:
                for bfr in list:
                    if bfr in results[index]["expectedbfr"]:
                        hit +=1
                    else:
                        miss +=1
            if name not in Tabledata:
                Tabledata[name] = {}
            # Create Tabledata with llm as key and itemname as subkey
            if hit == 0 and miss == 0:
                Tabledata[name][llm] = {"Contextquality": results[index]["goodcontext"], "hitrate": "NaN"}
            else:
                hitrate = hit/(miss+hit)
                Tabledata[name][llm] = {"Contextquality": results[index]["goodcontext"], "hitrate": hitrate}
            sumhit += hit
            summiss += miss
            llmperformance[llm] = {"hit": hit, "miss": miss}
            # print(f"{results[index]["llm"]} - {results[index]["itemname"]}\nHitrate: {hit/(miss+hit)}")
        # print(f"LLM: {llm} - Hitrate: {hit/}")

print("Overall:")
print(f"Hit: {sumhit}\nMiss: {summiss}")

# Laufzeitermittlung
Gesamtlaufzeit = 0
for index in range(len(results)):
    for runtime in results[index]["results"]["duration"]:
        Gesamtlaufzeit += runtime

Laufzeitstunden = math.floor(Gesamtlaufzeit/3600)
Laufzeitminuten = math.floor((Gesamtlaufzeit%3600)/60)
Laufzeitsekunden = round((Gesamtlaufzeit%60), 2)

print(f'{Laufzeitstunden}:{Laufzeitminuten}:{Laufzeitsekunden}')

def LaTeX_Tabledata_creation(data):
    formatted_Data = []
    for item in data:
        row = {
            "Teilename": item
        }
        for llm in data[item]:
            row[llm] = data[item][llm]
        formatted_Data.append(row)
    savepathlist = ["______PDF", "Data", "Versuch"+ Versuch + "Table.json"]
    savepath = ""
    for part in savepathlist:
        savepath = os.path.join(savepath, part)
    with open(savepath, "w") as outfile:
        json.dump(formatted_Data, outfile)

LaTeX_Tabledata_creation(Tabledata)