import os
import json
import numpy as np
import math
import matplotlib.pyplot as plt

Versuch = "6"

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

Prompts = [
        # "How high is the base failure rate (BFR) of [itemname]?",
        #"How high is the base failure rate (BFR) of [itemname]?\n\nOnly return numbers",
        # "How high is the base failure rate (BFR) of [itemname]?\n\nOnly return numbers without unit",
        # "How high is the base failure rate (BFR) of [itemname]?\n\nRefer on the given context",
        #"How high is the base failure rate (BFR) of [itemname]?\n\nOnly return numbers and refer on the given context",
        "How high is the base failure rate (BFR) of [itemname]?\n\nOnly return numbers without unit and refer on the given context"
    ]

print(len(results))
sumhit = 0
summiss = 0
Tabledata = {}
for i, prompt in enumerate(Prompts):
    # print(i+1)
    Success = {"trueamount": 0, "falseamount": 0}
    for index in range(len(results)):
        name = results[index]["itemname"]
        hit = 0
        miss = 0
        # Abgleich mit erwarteten Werten und gefundenen Werten (hit und miss)
        # print(f"Found: {results[index]["results"]["found_bfrs"]}\nExpect: {results[index]["expectedbfr"]}")
        if prompt.replace("[itemname]", name) ==  results[index]["prompt"]:
            # print(results[index]["prompt"])
            for list in results[index]["results"]["found_bfrs"]:
                for bfr in list:
                    # print(f"Found: {list}\nExpect: {results[index]["expectedbfr"]}\n")
                    if bfr in results[index]["expectedbfr"]:
                        hit +=1
                    else:
                        miss +=1
            # Auswertung der Ergebnisse
            if name not in Success:
                Success[name] = {"hit": hit, "miss": miss}
            else:
                Success[name]["hit"] += hit
                Success[name]["miss"] += miss
            sumhit += hit
            summiss += miss
            print(f"{results[index]["prompt"]}\nmiss: {miss}\nsummiss: {summiss}")
            # print(Success[name], i, name)
            if name not in Tabledata:
                Tabledata[name] = {1: {"Contextquality": "neutral", "hitrate": 0}, 2: {"Contextquality": "neutral", "hitrate": 0}, 3: {"Contextquality": "neutral", "hitrate": 0}, 4: {"Contextquality": "neutral", "hitrate": 0}}

            if Success[name]["hit"] == 0 and Success[name]["miss"] == 0:
                Tabledata[name][i+1] = {"Contextquality": results[index]["goodcontext"], "hitrate": "NaN"}
            else:
                hitrate = int(Success[name]["hit"]) / (int(Success[name]["miss"]) + int(Success[name]["hit"]))
                Tabledata[name][i+1] = {"Contextquality": results[index]["goodcontext"], "hitrate": hitrate}
                # print(hitrate)
                
    # Zählen der erfolgreichen Ermittlung der Base Failure Rate:
    # print("Success is:", Success)
    for item in Success:
        # print(f"{item}\nHit: {Success[item]["hit"], Miss: {Success[item]["miss"]}}")
        if item != "trueamount" and item != "falseamount":
            if Success[item]["hit"] > Success[item]["miss"]:
                Success["trueamount"] += 1
            else:
                Success["falseamount"] += 1
        # print(f"{Success[item]} Success: {Success["trueamount"]} Failed: {Success["falseamount"]}\n")
    # print(f"Successful items: {Success["trueamount"]}")
    # print(f"Bad items: {Success["falseamount"]}")
    # print(prompt)

# print("This is tabledata:", Tabledata)

# BIS HIER PRO PROMPT

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
            "Teilename": item,
            "1": data[item][1],
        }
        formatted_Data.append(row)
    savepathlist = ["______PDF", "Data", "Versuch"+ Versuch + "Table.json"]
    savepath = ""
    for part in savepathlist:
        savepath = os.path.join(savepath, part)
    with open(savepath, "w") as outfile:
        json.dump(formatted_Data, outfile)

LaTeX_Tabledata_creation(Tabledata)