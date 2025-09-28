import os
import json
from plot3d import create3d_plot

Versuch = "6"

# Path to files
pathresults = ["___myScripts", "2_Promptdevelopment", "Versuch_5", "results_massproduction"]
# pathresults = ["___myScripts", "2_Promptdevelopment", "Versuch_5", "results"]
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

# Clean data with new keynames
if "llm2" in results[0]:
    for r, result in enumerate(results):
        results[r]["evallm"] = results[r].pop("llm2")

# Create list of all evallm in results
List_evallm = []
List_llm = []
for r, result in enumerate(results):
    if results[r]["evallm"]["name"] not in List_evallm:
        List_evallm.append(results[r]["evallm"]["name"])
    if results[r]["llm"] not in List_llm:
        List_llm.append(results[r]["llm"])

print(List_evallm)
print(List_llm)

Plot3d_Z_Data = []
for e, evallm in enumerate(List_evallm):
    partial_result = []
    for l, llm in enumerate(List_llm):
        calculation_data = []
        for index in range(len(results)):
            name = results[index]["itemname"]
            hit = 0
            miss = 0
            # Check for llm
            if evallm == results[index]["evallm"]["name"] and llm == results[index]["llm"]:
                # Check every single found bfrs and set hit or miss for the current llm
                for list in results[index]["results"]["found_bfrs"]:
                    for bfr in list:
                        if bfr in results[index]["expectedbfr"]:
                            hit +=1
                        else:
                            miss +=1
                # print("hit", hit, "miss", miss)
                if hit+miss > 0:
                    calculation_data.append((hit/(hit+miss))*100)
                else:
                    calculation_data.append(0)
        print(llm)
        partial_result.append(sum(calculation_data)/len(calculation_data))
    print(partial_result, evallm)
    Plot3d_Z_Data.append(partial_result)

print(Plot3d_Z_Data)
# Create Barchart
create3d_plot(List_evallm, List_llm, Plot3d_Z_Data)