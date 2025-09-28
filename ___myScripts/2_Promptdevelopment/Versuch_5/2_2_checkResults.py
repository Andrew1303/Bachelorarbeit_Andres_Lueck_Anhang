import os
import json
import numpy as np
import math
import matplotlib.pyplot as plt

# Path to files
pathresults = ["___myScripts", "2_Promptdevelopment", "Versuch_4", "results_V2"]
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
print(results[0]["results"])

print(f"Contextjudgement: {results[0]["goodcontext"]}")

sumhit = 0
summiss = 0

Prompts = [
        # "How high is the base failure rate (BFR) of [itemname]?",
        #"How high is the base failure rate (BFR) of [itemname]?\n\nOnly return numbers",
        # "How high is the base failure rate (BFR) of [itemname]?\n\nOnly return numbers without unit",
        # "How high is the base failure rate (BFR) of [itemname]?\n\nRefer on the given context",
        #"How high is the base failure rate (BFR) of [itemname]?\n\nOnly return numbers and refer on the given context",
        "How high is the base failure rate (BFR) of [itemname]?\n\nOnly return numbers without unit and refer on the given context"
    ]

# Prompts = [
#         "How high is the base failure rate (BFR) of [itemname]?\n\nReturn one number without measurement",
#         "How high is the base failure rate (BFR) of [itemname]? \n Return one number without measurement. Keep it short. No other information needed.",
#         "Extract the most general base failure rate of [itemname]. Return one number without measurement. Keep it short. No other information needed.\n\n",
#         "How high is the base failure rate (BFR) of [itemname]? Analyze the following context and return the most general number without measurement. Keep it short. No other information needed."
#     ]

plotdata = []
print(len(results))
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
            

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return f"{pct:.0f}% ({val})"
        return my_autopct

    if Success["tp"] + Success["tn"] + Success["fp"] + Success["fn"] > 0:
        sizes = [Success["tp"], Success["fn"], Success["f_null"], Success["fp"], Success["tn"], Success["t_null"]]
    else:
        sizes = [0, 55-Success["t_null"], Success["t_null"]]

    # --- PLOT 1 ---
    # labels = 'Korrekt', 'Falsch'
    
    # colors = ["#53FF53", "#FF4A4A"]
    # fig, ax = plt.subplots()
    # ax.pie(
    #     sizes,
    #     radius=1,
    #     explode=(0, 0.2),
    #     labels=labels,
    #     autopct=make_autopct(sizes),
    #     shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9}, startangle=120,
    #     colors=colors
    # )
    # ax.axis('equal')
    # ax.set_title(prompt)
    # plt.tight_layout()
    # # plt.savefig(f"/aidata/users/andresl/Bachelorarbeit_Andres_Lueck/___myScripts/2_Promptdevelopment/Versuch_3/checkresultsplots/V1_{p+1}_{i}.png")
    # plt.savefig(f"./___myScripts/2_Promptdevelopment/Versuch_3/checkresultsplots/V1_{p+1}_{i}.png")

    # --- PLOT 2 ---
    fig, ax = plt.subplots()
    innercolors = ["#B1B1B1", "#424242"] #["#009688", "#FF5722"]
    # outercolors = ["#53FF53", "#FF4A4A"]
    outercolors = ["#56B4E9", "#E69F00", "#0072B2", "#CC79A7", "#F0E442", "#009E73"]
    size = 0.3

    #OUTER
    outer_wedges, _ = ax.pie(
        sizes, 
        radius=1,
        wedgeprops=dict(width=size, edgecolor='w'),
        startangle=90,
        colors=outercolors)
    sizesum = sum(sizes)
    outer_labels = []
    for sizeparameter in sizes:
        if sizeparameter > 0:
            outer_labels.append(f"{round(sizeparameter/sizesum*100, 1)}%")
        else:
            outer_labels.append("")
    # outer_labels = [f"{round(sizes[0]/sizesum*100, 1)}%", f"{round(sizes[1]/sizesum*100, 1)}%", f"{round(sizes[2]/sizesum*100, 1)}%", f"{round(sizes[3]/sizesum*100, 1)}%", f"{round(sizes[4]/sizesum*100, 1)}%", f"{round(sizes[5]/sizesum*100, 1)}%"]
    for k, wedge in enumerate(outer_wedges):
        ang = (wedge.theta2 + wedge.theta1) / 2
        x = np.cos(np.deg2rad(ang))
        y = np.sin(np.deg2rad(ang))

        x_start, y_start = x * (1 * 0.5), y * (1* 0.5)
        x_end_text, y_end_text = x * .85, y * .85

        # ax.plot([x_start, x_end_line], [y_start, y_end_line], color='black', lw=0.8)
        ax.text(x_end_text, y_end_text, outer_labels[k], ha='center', va='center')

    # ax.plot([.3, 1], [-0.45, -1], color='black', lw=0.8)
    # ax.text(1.05, -1, "Context", ha='left', va='center')

    # INNER
    inner_wedges, _ = ax.pie(
        [contextsuccess["good"], 
        contextsuccess["bad"]], 
        radius=1-size,
        startangle=90,
        wedgeprops=dict(width=size, edgecolor='w'),
        colors=innercolors
        )
    
    inner_labels = [f"{round(contextsuccess["good"]/(contextsuccess['good']+contextsuccess['bad'])*100, 1)}%", f"{round(contextsuccess["bad"]/(contextsuccess['good']+contextsuccess['bad'])*100, 1)}%"]
    # inner_labels = ["", ""]
    for j, wedge in enumerate(inner_wedges):
        ang = (wedge.theta2 + wedge.theta1) / 2
        x = np.cos(np.deg2rad(ang))
        y = np.sin(np.deg2rad(ang))

        # Starting point (on wedge), and label location
        x_start, y_start = x * (1 * 0.5), y * (1 * 0.5)
        x_end_line, y_end_line = x * 1.3, y * 1.3
        x_end_text, y_end_text = x * .55, y * .55

        # ax.plot([x_start, x_end_line], [y_start, y_end_line], color='black', lw=0.8)
        ax.text(x_end_text, y_end_text, inner_labels[j], ha='center', va='center')

    ax.plot([-.5, -1], [0.7, 1], color='black', lw=0.8)
    ax.text(-1.05, 1, "Basefailurerate", ha='right', va='center')
    ax.legend(['True Positive', 'False Negative', 'False Null', 'False Positive', 'True Negative', 'True Null', 'Good Context', 'Bad Context'], loc="upper right", bbox_to_anchor=(1.25, 1))
# sizes = [Success["tp"], Success["fn"], Success["f_null"], Success["fp"], Success["tn"], Success["t_null"]]
    ax.set(aspect="equal", title=prompt)
    plt.tight_layout()

    savepathparts = ["___myScripts", "2_Promptdevelopment", "Versuch_5", "checkresultsplots", f"V1_{p+1}_{i}.png"]
    savepath = os.path.join(*savepathparts)
    plt.savefig(savepath)
    print("Plot saved")

    #Multiplotdata
    Dataset = [sizes, contextsuccess]
    plotdata.append(Dataset)
    


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