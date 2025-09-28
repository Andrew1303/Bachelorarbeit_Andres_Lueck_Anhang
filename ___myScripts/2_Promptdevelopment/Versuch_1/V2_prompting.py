import json
import time
from Fct_LLM_API import Chatting, ChattingOne
import datetime
import re
import requests
import sys
# json.loads(open("___Scripts-relevant\\Promptdevelopment\\Prompts.json", "r"))

# --------------------------------------- CHECK LLM AVAILABITLITY ------------------------------------------------
# https://stackoverflow.com/questions/65009692/how-to-quickly-check-if-domain-exists
url = "http://localhost:11434"
model = "DeepSeek-R1"
try:
    check = requests.get(url, timeout=10)
    if check.status_code != 200:
        sys.exit(f"\033[31m'{url}' is not available! Please check your API.\033[0m")
except:
    sys.exit(f"\033[31m'{url}' is not available! Please check your API.\033[0m")

# ---------------------------------------- GET PROMPTS -----------------------------------------------------------
with open("___Scripts-relevant\\Promptdevelopment\\Prompts_Dic.json") as jsondata:
    prompts = json.load(jsondata)

amount_languages = len(prompts)
amount_promptsperlanguage = []
for language in prompts:
    amount_promptsperlanguage.append(len(prompts[language]))

amount_prompts = sum(amount_promptsperlanguage)

# --------------------------------------- DEFINE PARTNAME --------------------------------------------------------
partname = input("Whats the name of the part you are searching a base failure rate for?\n")

# ------------------------------------------- RAG ----------------------------------------------------------------
# Replace context with RAG vector database and it's created context
context = "MIL-HDBK-217F I 6.1 DIODES, LOW FREQUENCY — SPECIFICATION DESCRIPTION MlL-S-l 9500 @ Frecpxmqr D-s: General Putpse Analog, Switch~ Fast Rewvery, f%wer RecWer, Tmsient S~r, Current Regulator, Vol@e Regulator, Voltage Reference Lp = &##czQzE Failures/l OG Hours Base Failure Rate - & Diode Type/Appiicatbn “ ~ General PuqxM Analog .0038 switching .0010 Power Redfiir, Fast Recovery .069 Power Rectifier/Schottky .0030 Power Diode Power Rectifier with .0050/ HigiI Voltage Stacks Junction Transient Suppressor/Vanstor .0013 Current Reguiator .0034 Voltage Regulator and Voltage .0020 Reference (Avaianche and Zener) I i Terrperature Factor - XT (General Purpose Analog, Switching, Fast Recovery, Poul TJ (’C) 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100 r Rectifier, TI XT 1.0 1.2 1.4 1.6 1.9 2.2 2.6 3.0 3.4 3.9 4.4 5.0 5.7 6.4 7.2 8.0 dent Su-pgm TJ ~C) 105 110 115 120 125 130 135 140 145 150 155 160 165 170 175 isor) XT 9.0 10 11 12 14 15 16 18 20 21 23 25 28 30 32 ((-3091 1 1 XT = exp TJ + 273 )) -Z& TJ - JunctionTemperature (“C) Temperature Factor - q (VOitag. Regulator, Voitqo Rdormce, h cun’UWRncddYW)—.- ---- . ... . -~---. # TJ (“C) %T ‘J (’=) v 25 1.0 105 3.9 30 1.1 110 4.2 35 1.2 115 4.5 40 1.4 120 4.8 45 1.5 125 5.1 50 1.6 130 5.4 55 1.8 135 5.7 60 2.0 140 6.0 65 2.1 145 6.4 70 2.3 150 6.7 75 2.5 155 7.1 80 2.7 160 7.5 85 3.0 165 7.9 90 3.2 170 8.3 95 3.4 175 8.7 100 3.7 (( 1 1 %T = exp -1925 TJ +273-= )) TJ . Junctio"

# ------------------------------- REPLACE [itemname] with searched itemname --------------------------------------


results = []
promptcounter = 0
# For each language
for laindex, language in enumerate(prompts):
    # Language status
    print(f'{laindex+1}/{amount_languages} languages')
    # For each prompt in selected language
    for index, prompt in enumerate(prompts[language]):
        print(f'{laindex+1}/{amount_promptsperlanguage[laindex]} in type {language}')
        print(f'{promptcounter}/{amount_prompts} of all prompts done')
        prompt = prompt.replace("[itemname]", partname)
        small_result = {
            "language": language,
            "model": model,
            "index": index,
            "prompt": prompt,
            "results": {
                "duration": [],
                "answer": [],
                "found_bfrs":[]
            }
        }
        # Each prompt gets x iterations with probably different results
        iterations = 5
        for i in range(iterations):
            print(f'{i}/{iterations} repeats done', end="\r")
            start = time.time()
            result = ChattingOne(prompt, context, model)
            end = time.time()
            duration = end - start
            small_result["results"]["answer"].append(result)
            small_result["results"]["duration"].append(duration)
            # Quelle: https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string
            # numbers = re.findall(r"(?:\d*\.*\d+)", result)
            numbers = re.findall(r"\d+(?:[.,]\d+)?", result)
            numbers = [num.replace(",", ".") for num in numbers]
            small_result["results"]["found_bfrs"].append([float(num) for num in numbers])
        # Count finished prompts 
        promptcounter += 1
        # Add partial results for the prompt to results
        results.append(small_result)

date = datetime.datetime.now()
name = f"V2_{date.year}{date.month:02d}{date.day:02d}{date.hour:02d}{date.minute:02d}{date.second:02d}_al-{amount_languages}_ap-{amount_prompts}_{partname.replace(" ", "-")}"

with open(f"___Scripts-relevant\\Promptdevelopment\\Versuch 1\\results\\{name}.json", "w") as outfile:
    json.dump(results, outfile)

# # -------------------------------------- GENERATE ANSWERS --------------------------------------------------------

# with open("___Scripts-relevant\\Promptdevelopment\\Versuch 1\\results.txt", "a") as results:
#     for prompt in itemprompts:
#         start = time.time()
#         result = ChattingOne(prompt=prompt, context=context)
#         end = time.time()
#         duration = end - start

#         results.write(f"P:{prompt}\nT:{duration}\nA:{result}\r\n")