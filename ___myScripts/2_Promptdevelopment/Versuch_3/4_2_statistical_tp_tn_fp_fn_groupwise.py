import os, json
import math

def fillgap(input):
    inputstr = f"{input}"
    if len(inputstr) == 33:
        return inputstr
    else:
        margin = 33 - len(inputstr)
        if margin%2 == 1:
            left = int(margin/2) * " "
            right = left + " "
            return left + inputstr + right
        else:
            pad = int(margin/2) * " "
            return pad + inputstr + pad

# Path to files
pathresults = ["___myScripts", "2_Promptdevelopment", "Versuch_4", "results_V2"]
resultpath = os.path.join(*pathresults)

# Read files
resultfiles = os.listdir(resultpath)
resultfiles.sort()

for index, file in enumerate(resultfiles):
    print(f"• [{index+1}] {file}")

# Select promptlist
filename = resultfiles[int(input("\nWhich resultlist should be used (number)?\n")) - 1]
print(f"Your selected promptlistfile: \033[1;33m{filename}\033[0m")

# Read selected resultlistname to path and open file
resultpath = os.path.join(resultpath, filename)
with open(resultpath) as jsondata:
    results = json.load(jsondata)

# evaluate data
good = 0
bad = 0
neutral = 0

tp = 0
tn = 0
fp = 0
fn = 0

# --- ANOTHER TRY ----

Prompts = [
        "How high is the base failure rate (BFR) of [itemname]?",
        "How high is the base failure rate (BFR) of [itemname]?\n\nJust one number, find type representative",
        "How high is the base failure rate (BFR) of [itemname]?\n\nJust one number, find type representative, choose the most general number",
        "How high is the base failure rate (BFR) of [itemname]?\n\nReturn one number without measurement",
        "Wie hoch ist die Base Failure Rate (BFR) von [itemname]?",
        "Wie hoch ist die Base Failure Rate (BFR) von [itemname]?\n\nNur eine Zahl, finde Typenvertreter",
        "Wie hoch ist die Base Failure Rate (BFR) von [itemname]?\n\nNur eine Zahl, finde Typenvertreter, wähle die allgemeinste geltende Zahl",
        "Wie hoch ist die Base Failure Rate (BFR) von [itemname]?\n\nGib eine Zahl ohne größe zurück"
        # "Wie hoch ist die Base Failure Rate (BFR) von [itemname]?\n\nNur eine Zahl, finde Typenvertreter, wÃ¤hle die allgemeinste geltende Zahl",
        # "Wie hoch ist die Base Failure Rate (BFR) von [itemname]?\n\nGib eine Zahl ohne grÃ¶ÃŸe zurÃ¼ck"
    ]

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
            # REMOVED FALSE NULL AND TRUE NULL FOR BINARY CLASSIFICATION
            # # No Success
            # else:
            #     # Expected Result
            #     if Success[item]["hit"] == 0:
            #         if Success[item]["context"] == "good":
            #             Success["f_null"] += 1
            #         else:
            #             Success["t_null"] += 1
            else:
                # True numbers are okay
                if Success[item]["context"] == "good":
                    Success["fn"] += 1
                # True numbers are random hits
                else:
                    Success["tn"] += 1
        # Context evaluation
        if results[i]["goodcontext"] == "good":
            good += 1
        elif results[i]["goodcontext"] == "bad":
            bad += 1
        else:
            neutral += 1
    tp = Success["tp"]
    fn = Success["fn"]
    fp = Success["fp"]
    tn = Success["tn"]
    # Ausgabe pro Promptart
    # if (p+1)%55 == 0:
        # print(f"Prompt {int(index/55)+1} done.")
    accuracy = round((tp)/(tp+fn+fp+tn), 2)
    if tp+fp != 0:
        precision = round(tp/(tp+fp), 2)
    else:
        precision = "NA"
    if tp+fn != 0:
        sensitivity = round(tp/(tp+fn),2)
    else:
        sensitivity = "NA"
    if tn+fp != 0:
        specificity = round(tn/(tn+fp), 2)
    else:
        specificity = "NA"
    recall = round(tp/(tp+fp))
    f1_score = 2*((precision*recall)/(precision+recall))
    # print(f"TP:{tp} - TN: {tn} - FP: {fp} - FN: {fn}")
    # print(f"   Accuracy = {accuracy}\n  Precision = {precision}\nSensitivity = {sensitivity}\nSpecificity = {specificity}\n recall = {recall}\nF1 Score = {f1_score}")
    # print(f"Context was {round(good/(good+bad)*100, 2)}% correct. Undefined was {neutral} times.\n")
    
    if tp+fp != 0:
        fnr = round(fn/(tp+fn), 2) # True positive rate (miss rate)
    else: 
        fnr = 0.0
    if tp+fp != 0:
        tpr = round(tp/(tp+fn), 2) # True positive rate (recall, sensitivity) - Probability of detection, hit rate
    else:
        tpr = 0.0

    if fp+tn != 0:
        fpr = round(fp/(fp+tn), 2) # False positive rate (Probability of false alarm, fall out) rate of all false positive to all negative vlaues either false or true
    else:
        fpr = 0.0
    if tn+fn != 0:
        tnr = round(tn/(fp+tn), 2) # True negative rate (specificity, selectivity)
    else:
        tnr = 0.0

    informedness = round(tpr + tnr - 1, 2)
    prevalence_threshold = round((math.sqrt(tpr*fpr)-fpr)/(tpr-fpr), 2)
    prevalence = round((tp+fp)/(fp+tp+fn+tn), 2)

    positive_predictive_value = round(tp/(tp+fp), 2) # Precision
    negative_predictive_value = round(tn/(tn+fn), 2)
    markedness = round(positive_predictive_value + negative_predictive_value - 1, 2) # Delta P
    f1_score = round((2*positive_predictive_value*tpr)/(positive_predictive_value+tpr), 2)

    if fpr != 0:
        positive_likelihood_ratio = round(tpr/fpr, 2)
    else:
        positive_likelihood_ratio = "∞"
    if tnr != 0:
        negative_likelihood_ratio = round(fnr/tnr, 2)
    else:
        negative_likelihood_ratio = "∞"
    if negative_likelihood_ratio != "∞" and positive_likelihood_ratio != "∞":
        diagnostic_odds_ratio = round(positive_likelihood_ratio/negative_likelihood_ratio, 2)
    else:
        diagnostic_odds_ratio = "∞"

    accuracy = round((tp+tn)/(tp+tn+fp+fn), 2)

    false_discovery_rate = round(fp/(tp+fp), 2)
    false_omission_rate = round(fn/(tn+fn), 2)
    
    
    balanced_accuracy = round((tpr+tnr)/2, 2)
    Fowlkes_mallows_index = round(math.sqrt(positive_predictive_value*tpr), 2)
    mcc = round(math.sqrt(tpr*tnr*positive_predictive_value*negative_predictive_value)-math.sqrt(fnr*fpr*false_omission_rate*false_discovery_rate), 2) # Matthews correlation coefficient or phi
    Threat_score = round(tp/(tp+fn+fp), 2) # Critical success index, jaccard index


    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    clear = "\033[0m"
    print(f"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(f"|{fillgap(f"Prompt {p+1}")}|{fillgap("Predicted condition")}{fillgap("")} |{fillgap("")} {fillgap("")}|")
    print(f"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(f"|{fillgap("Total population")}|{green}{fillgap("Predicted positive")}{clear}|{green}{fillgap("Predicted negative")}{clear}|{red}{fillgap("Informedness (1.0)[0.0]")}{clear}|{red}{fillgap("Prevalence Threshold (0.0)")}{clear}|")
    print(f"|{fillgap(tp+fp+tn+fn)}|{green}{fillgap(tp+fp)}{clear}|{green}{fillgap(tn+fn)}{clear}|{red}{fillgap(informedness)}{clear}|{red}{fillgap(prevalence_threshold)}{clear}|")
    print(f"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(f"|{fillgap("Positive (P)")}|{green}{fillgap("True Positive (Good)")}{clear}|{yellow}{fillgap("False Negative (bad)")}{clear}|{yellow}{fillgap("TPR (1.0)")}{clear}|{yellow}{fillgap("FNR (0.0)")}{clear}|")
    print(f"|{fillgap(fn+tp)}|{green}{fillgap(tp)}{clear}|{yellow}{fillgap(fn)}{clear}|{yellow}{fillgap(tpr)}{clear}|{yellow}{fillgap(fnr)}{clear}|")
    print(f"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(f"|{fillgap("Negative (N)")}|{green}{fillgap("False Positive (bad)")}{clear}|{yellow}{fillgap("True Negative (good)[bad]")}{clear}|{yellow}{fillgap("FPR (0.0)")}{clear}|{red}{fillgap("TNR (1.0)[0.0]")}{clear}|")
    print(f"|{fillgap(tn+fp)}|{green}{fillgap(fp)}{clear}|{yellow}{fillgap(tn)}{clear}|{yellow}{fillgap(fpr)}{clear}|{red}{fillgap(tnr)}{clear}|")
    print(f"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(f"|{green}{fillgap("Prevalence (1.0)")}{clear}|{green}{fillgap("Positive Predictive Value (1.0)")}{clear}|{yellow}{fillgap("Negative Predictive Value (1.0)")}{clear}|{red}{fillgap("Positive Likelihood Ratio (hi)")}{clear}|{red}{fillgap("Negative Likelihood Ratio (lo)")}{clear}|")
    print(f"|{green}{fillgap(prevalence)}{clear}|{green}{fillgap(positive_predictive_value)}{clear}|{yellow}{fillgap(negative_predictive_value)}{clear}|{red}{fillgap(positive_likelihood_ratio)}{clear}|{red}{fillgap(negative_likelihood_ratio)}{clear}|")
    print(f"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(f"|{yellow}{fillgap("Accuracy (1.0)")}{clear}|{green}{fillgap("False Discovery Rate (0.0)")}{clear}|{yellow}{fillgap("False Omission Rate (0.0)")}{clear}|{red}{fillgap("Markedness (0.0)")}{clear}|{red}{fillgap("Diagnostic Odds Ratio (hi)")}{clear}|")
    print(f"|{yellow}{fillgap(accuracy)}{clear}|{green}{fillgap(false_discovery_rate)}{clear}|{yellow}{fillgap(false_omission_rate)}{clear}|{red}{fillgap(markedness)}{clear}|{red}{fillgap(diagnostic_odds_ratio)}{clear}|")
    print(f"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(f"|{red}{fillgap("Balanced Accuracy (1.0)[0.5]")}{clear}|{yellow}{fillgap("F1 Score (1.0)")}{clear}|{yellow}{fillgap("FM (1.0)")}{clear}|{red}{fillgap("MCC (1.0)")}{clear}|{green}{fillgap("Threat Score (1.0)")}{clear}|")
    print(f"|{red}{fillgap(balanced_accuracy)}{clear}|{yellow}{fillgap(f1_score)}{clear}|{yellow}{fillgap(Fowlkes_mallows_index)}{clear}|{red}{fillgap(mcc)}{clear}|{green}{fillgap(Threat_score)}{clear}|")
    print(f"---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print()

    tp = 0
    tn = 0
    fn = 0
    fp = 0
    good = 0
    bad = 0
    neutral = 0

# Save file
pathresults = ["___myScripts", "2_Promptdevelopment", "Versuch_3", "results_V3", filename]
savepath = os.path.join(*pathresults)
with open(savepath, "w") as outfile:
    json.dump(results, outfile, indent=2)
        



# Context evaluation
