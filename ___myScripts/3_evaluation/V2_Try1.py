import matplotlib.pyplot as plt
import numpy as np
import json
import os 
# -- Get results --
# Select available file with prompts including embeddings
files = []
print("\nList of available files to calculate embeddings:")
for index, filename in enumerate(os.listdir(r"___myScripts\2_Promptdevelopment\Versuch_2\results")):
    files.append(filename)
    print(f"• [{index+1}] {filename}")

resultfile = files[int(input("\nWhich results should be used (number)?\n")) - 1]
print(f"Your selected results: \033[1;33m{resultfile}\033[0m")

# Open selected results
with open(f"___myScripts\\2_Promptdevelopment\\Versuch_2\\results\\{resultfile}") as jsondata:
    data = json.load(jsondata)

# Sort data for plot
plotdata = []
for index, prompt in enumerate(data):
    print(f'{index}: {data[index]["prompt"]}')
    print(data[index]["results"]["duration"])
    tempfoundbfrs = []
    for foundbfrs in data[index]["results"]["found_bfrs"]:
        tempfoundbfrs = tempfoundbfrs + foundbfrs
    results_plot = {
        "prompt": data[index]["prompt"],
        "duration": data[index]["results"]["duration"],
        "foundbfrs": tempfoundbfrs
        }
    plotdata.append(results_plot)

# Prepare data for bar chart by counting amount of results


titles = []
durations = []
foundbfrs=[]
for set in plotdata:
    titles.append(set["prompt"])
    durations.append(set["duration"])
    foundbfrs.append(set["foundbfrs"])
    # Count each found bfr for another plot
    countbfrs = {}
    for bfr in set["foundbfrs"]:
        if bfr in countbfrs:
            countbfrs[bfr] += 1
        else:
            countbfrs[bfr] = 1
    sorted_countbfrs = dict(sorted(countbfrs.items()))
    x = list(sorted_countbfrs.keys())
    y = list(sorted_countbfrs.values())
    
    fig, ax = plt.subplots()
    ax.bar(range(len(x)), y, width=.5, edgecolor="white", linewidth=0.7)
    plt.xticks(ticks=range(len(x)), labels=x)
    plt.title(set["prompt"])

    plt.show()

# plt.xlabel('index')
# plt.ylabel('duration [s]')
# for index, dat in enumerate(titles):
#     plt.title(titles[index])
#     plt.plot(foundbfrs[index])
#     plt.show()



# fig = plt.figure(figsize=(amount_prompts, 3))

# plt.subplot(131)
# plt.plot()