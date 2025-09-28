import os
import json
import numpy as np
import math
import matplotlib.pyplot as plt

def multipieplot(context_data_list:list, bfr_data_list:list, title_list:list, name:str):
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))

    # outercolors = ["#56B4E9", "#E69F00", "#0072B2", "#CC79A7", "#F0E442", "#009E73"]
    outercolors = ["#56B4E9", "#B1B1B1", "#636363"]
    innercolors = ["#B1B1B1", "#636363"]
    size = 0.6
    for ax, bfr_data, context_data, title in zip(axs.flat, bfr_data_list, context_data_list, title_list):
        # General numbers
        bfr_sum = sum(bfr_data)

        # Outer ring
        outer_wedges, _ = ax.pie(
            bfr_data,
            radius=1,
            wedgeprops=dict(width=size, edgecolor='w'),
            colors=outercolors,
            startangle=90
        )
        outer_labels = []
        for sizeparameter in bfr_data:
            if sizeparameter > 0:
                outer_labels.append(f"{round(sizeparameter/bfr_sum*100, 1)}%")
            else:
                outer_labels.append("")
        # 
        for k, wedge in enumerate(outer_wedges):
            ang = (wedge.theta2 + wedge.theta1) / 2
            x = np.cos(np.deg2rad(ang))
            y = np.sin(np.deg2rad(ang))

            x_start, y_start = x * (1 * 0.5), y * (1* 0.5)
            x_end_text, y_end_text = x * .7, y * .7

            # ax.plot([x_start, x_end_line], [y_start, y_end_line], color='black', lw=0.8)
            ax.text(x_end_text, y_end_text, outer_labels[k], ha='center', va='center')

        # # Inner ring
        # inner_wedges, _ = ax.pie(
        #     context_data,
        #     radius = 1-size,
        #     wedgeprops = dict(width=size, edgecolor='w'),
        #     colors=innercolors,
        #     startangle=90
        # )
        # inner_labels = [f"{round(context_data[0]/(context_data[0]+context_data[1])*100, 1)}%", f"{round(context_data[1]/(context_data[0]+context_data[1])*100, 1)}%"]
        # for j, wedge in enumerate(inner_wedges):
        #     ang = (wedge.theta2 + wedge.theta1) / 2 # angle of wedge
        #     x = np.cos(np.deg2rad(ang)) # x coord of center
        #     y = np.sin(np.deg2rad(ang)) # y coord of center

        #     # Starting point (on wedge), and label location
        #     # x_start, y_start = x * (1 * 0.5), y * (1 * 0.5)
        #     # x_end_line, y_end_line = x * 1.3, y * 1.3
        #     x_end_text, y_end_text = x * .55, y * .55

        #     ax.text(x_end_text, y_end_text, inner_labels[j], ha='center', va='center')

        ax.set_title(title[1], y=0.87, fontsize=16)
        ax.axis('equal')

        # ax.text(-0.16, 0, "Context", ha='left', va='center', fontsize=12)
        # ax.plot([.2, .4], [0, 0], color='black', lw=0.8)
        
        ax.text(-0.7, 1, "Basefailurerate", ha='right', va='center', fontsize=12)
        # ax.plot([-.5, -1], [0.7, -1], color='black', lw=0.8)

        ax.text(
            0.5, 0.07, title[0], 
            transform=ax.transAxes,
            ha="center", va="top",
            fontsize=10, color="gray"
        )

    # fig.legend(['True Positive', 'False Negative', 'False Null', 'False Positive', 'True Negative', 'True Null', 'Good Context', 'Bad Context'], loc="upper right", title="Categories", bbox_to_anchor=(0.97, 0.97))
    fig.legend(['IQ ≥ 50%', '0 < IQ < 0.5', 'IQ = 0'], loc="upper right", title="Categories", bbox_to_anchor=(0.97, 0.97))
    plt.tight_layout(rect=[0, 0, 0.85, 1], pad=2)
    # plt.show()

    savepathparts = ["___myScripts", "2_Promptdevelopment", "Versuch_3", "checkresultmultiplots", name + ".png"]
    savepath = os.path.join(*savepathparts)
    fig.savefig(savepath, bbox_inches='tight', dpi=300)
    

# Path to files
pathresults = ["___myScripts", "2_Promptdevelopment", "Versuch_3", "results_V2"]
resultpath = os.path.join(*pathresults)

# -- Get results --
# Select available file with prompts including embeddings
files = []
print("\nList of available files to calculate embeddings:")
for i, filename in enumerate(os.listdir(resultpath)):
    files.append(filename)


print(files)
files.sort()
for i, file in enumerate(files):
    print(f"• [{i+1}] {file}")

resultfile = files[int(input("\nWhich results should be used (number)?\n")) - 1]
print(f"Your selected results:\n\033[1;33m{resultfile}\033[0m\n")

# Open selected results
with open(f"{resultpath}/{resultfile}") as jsondata:
    results = json.load(jsondata)

print(f"Amount: {len(results)}")
# print(f"Example: {results[0]}")
print(f"Cleaned example:\n")
print(f"Prompt: {results[0]["prompt"]}")
print(f"Item: {results[0]["itemname"]}")
print(f"expected bfrs: {results[0]["expectedbfr"]}")
print(f"found bfrs: {results[0]["results"]["found_bfrs"]}")
print(f"Duration: {results[0]["results"]["duration"]}")
print(f"Mean duration: {np.mean(results[0]["results"]["duration"])}")

print(f"Contextjudgement: {results[0]["goodcontext"]}")

sumhit = 0
summiss = 0

Prompts = [
        "How high is the base failure rate (BFR) of [itemname]?",
        "How high is the base failure rate (BFR) of [itemname]?\n\nJust one number, find type representative",
        "How high is the base failure rate (BFR) of [itemname]?\n\nJust one number, find type representative, choose the most general number",
        "How high is the base failure rate (BFR) of [itemname]?\n\nReturn one number without measurement",
        "Wie hoch ist die Base Failure Rate (BFR) von [itemname]?",
        "Wie hoch ist die Base Failure Rate (BFR) von [itemname]?\n\nNur eine Zahl, finde Typenvertreter",
        # "Wie hoch ist die Base Failure Rate (BFR) von [itemname]?\n\nNur eine Zahl, finde Typenvertreter, wähle die allgemeinste geltende Zahl",
        # "Wie hoch ist die Base Failure Rate (BFR) von [itemname]?\n\nGib eine Zahl ohne größe zurück"
        "Wie hoch ist die Base Failure Rate (BFR) von [itemname]?\n\nNur eine Zahl, finde Typenvertreter, wÃ¤hle die allgemeinste geltende Zahl",
        "Wie hoch ist die Base Failure Rate (BFR) von [itemname]?\n\nGib eine Zahl ohne grÃ¶ÃŸe zurÃ¼ck"
    ]

# Prompts = [
#         "How high is the base failure rate (BFR) of [itemname]?\n\nReturn one number without measurement",
#         "How high is the base failure rate (BFR) of [itemname]? \n Return one number without measurement. Keep it short. No other information needed.",
#         "Extract the most general base failure rate of [itemname]. Return one number without measurement. Keep it short. No other information needed.\n\n",
#         "How high is the base failure rate (BFR) of [itemname]? Analyze the following context and return the most general number without measurement. Keep it short. No other information needed."
#     ]


print(len(results))
context_data_list = []
bfr_data_list = []
title_list = []
for p, prompt in enumerate(Prompts):
    Success = {"tp": 0, "fp": 0, "tn": 0, "fn": 0, "t_null":0, "f_null": 0}
    contextsuccess = {"good": 0, "bad": 0}
    
    for i in range(len(results)):
        name = results[i]["itemname"]
        hit = 0
        miss = 0
        # Abgleich mit erwarteten Werten und gefundenen Werten (hit und miss)
        # print(f"Found: {results[index]["results"]["found_bfrs"]}\nExpect: {results[index]["expectedbfr"]}")
        # input("Press Enter to continue")
        if prompt.replace("[itemname]", name) ==  results[i]["prompt"]:
            # print(results[index]["prompt"])
            for list in results[i]["results"]["found_bfrs"]:
                for bfr in list:
                    # print(f"Found: {list}\nExpect: {results[index]["expectedbfr"]}\n")
                    if bfr in results[i]["expectedbfr"]:
                        hit +=1
                    else:
                        miss +=1
            # Auswertung der Ergebnisse
            if name not in Success:
                Success[name] = {"hit": hit, "miss": miss, "context": results[i]["goodcontext"]}
            else:
                Success[name]["hit"] += hit
                Success[name]["miss"] += miss
            # if hit > miss:
            #     Success[name]["success"] = True
            # else:
            #     Success[name]["success"] = False
            sumhit += hit
            summiss += miss
            # Contextjudgemenet
            if results[i]["goodcontext"] == "good":
                contextsuccess["good"] += 1
            else:
                contextsuccess["bad"] += 1
        # else:
            # print("|" + results[i]["prompt"] + "|")

    # Zählen der erfolgreichen Ermittlung der Base Failure Rate:
    
    for item in Success:
        # Ignoring the trueamount and falseamount
        if item not in ["tp", "tn", "fp", "fn", "t_null", "f_null"]:
            # Success:
            if Success[item]["hit"] > Success[item]["miss"]:
                if Success[item]["context"] == "good":
                    Success["tp"] += 1
                else:
                    Success["fp"] += 1
            # No Success
            else:
                # Expected Result
                if Success[item]["hit"] == 0:
                    if Success[item]["context"] == "good":
                        Success["f_null"] += 1
                    else:
                        Success["t_null"] += 1
                else:
                    # True numbers are okay
                    if Success[item]["context"] == "good":
                        Success["fn"] += 1
                    # True numbers are random hits
                    else:
                        Success["tn"] += 1
    
    print(f"\nPrompt {p+1}")
    print(f"tp: {Success["tp"]} [IR>=50%]\nfp: {Success["fp"]} [IR>=50%]\ntn: {Success["tn"]} [0%<IR<50%]\nfn: {Success["fn"]} [0%<IR<50%]\nNullamount: {Success["t_null"]}\n")
    print("True Positive (tp):  IR>=50% correct and context was good")
    print("False Positive (fp): IR>=50% correct but context was bad")
    print("True Negative (tn):  0%<IR<50% correct and context was bad")
    print("False Negative (fn): 0%<IR<50% correct but context was good")

    if Success["tp"] + Success["tn"] + Success["fp"] + Success["fn"] > 0:
        sizes = [Success["tp"], Success["fn"], Success["f_null"], Success["fp"], Success["tn"], Success["t_null"]]
    else:
        sizes = [0, 0, 0, 0, 55-Success["t_null"], Success["t_null"]]

    context_data_list.append([contextsuccess["good"], contextsuccess["bad"]])
    bfr_data_list.append(sizes)
    title_list.append([prompt, f"Prompt {p+1}"])

    if (p+1)%4 == 0:
        multipieplot(context_data_list, bfr_data_list, title_list, f"multigraph-{p}")
        context_data_list = []
        bfr_data_list = []
        title_list = []



# BIS HIER PRO PROMPT

print("Overall:")
print(f"Hit: {sumhit}\nMiss: {summiss}")

# Laufzeitermittlung
Gesamtlaufzeit = 0
for i in range(len(results)):
    for runtime in results[i]["results"]["duration"]:
        Gesamtlaufzeit += runtime

Laufzeitstunden = math.floor(Gesamtlaufzeit/3600)
Laufzeitminuten = math.floor((Gesamtlaufzeit%3600)/60)
Laufzeitsekunden = round((Gesamtlaufzeit%60), 2)

print(f'{Laufzeitstunden}:{Laufzeitminuten}:{Laufzeitsekunden}')