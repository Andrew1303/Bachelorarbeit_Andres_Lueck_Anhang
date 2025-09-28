import os, json, time, re
from progresbar import progresbar
from Fct_LLM_API import ChattingOne
import datetime

# Get path for prompts with keywords
pathpartlist = ["___myScripts", "2_Promptdevelopment", "Versuch_4", "promptsWithContext"]
promptpath = os.path.join(*pathpartlist)

# List all promptlists
prompts = []
print("\nList of available promptlists:")
for index, list in enumerate(os.listdir(promptpath)):
    prompts.append(list)
prompts.sort()
for j, list in enumerate(prompts):
    list.replace(".json", "")
    print(f"• [{j+1}] {list}")

# Select promptlist
promptlistname = prompts[int(input("\nWhich promptlist should be used (number)?\n")) - 1]
print(f"Your selected promptlistfile: \033[1;33m{promptlistname}\033[0m")

with open(os.path.join(promptpath, promptlistname)) as jsondata:
    promptlist = json.load(jsondata)

# -- Process all prompts with n iterations and save results in a json file. --
iterations = int(input("Define the amount of iterations for each prompt (number)\n"))

# Calculate the amonunt of prompts in promptlist
amount_prompts = len(promptlist)

counter = 0
results = []
for i, prompt in enumerate(promptlist):
    durations = []
    answers = []
    foundbfrs = []
    for n in range(iterations):
        temperature = 0.2
        start = time.time()
        finalresult = ChattingOne(f"{prompt["prompt"]}", prompt["context"], "llama3.3:latest", temperature)
        end = time.time()
        durations.append(end-start)
        answers.append(finalresult)
        filtered_finalresult = re.sub(r'10\^(\d+)', '', finalresult)
        numbers = re.findall(r"\d+(?:[.,]\d+)?", filtered_finalresult)
        numbers = [num.replace(",", ".") for num in numbers]
        foundbfrs.append([float(num) for num in numbers])
        counter += 1
        progresbar(counter, amount_prompts*iterations)
    partial_result = {
        "model": "llama3.3:latest",
        "prompt": prompt["prompt"],
        "itemname": prompt["itemname"],
        "expectedbfr": prompt["expectedbfr"],
        "context": prompt["context"],
        "goodcontext": "neutral",
        "results": {
            "duration": durations,
            "answer": answers,
            "found_bfrs": foundbfrs
        }
    }
    results.append(partial_result)
    progresbar(counter, amount_prompts*iterations)

date = datetime.datetime.now()
name = f"V1_{date.year}{date.month:02d}{date.day:02d}{date.hour:02d}{date.minute:02d}_al-2_ap-{amount_prompts}_it-{iterations}_temp-{temperature}_Prompt_dic_llama3.3:latest"

savepathlist = ["___myScripts", "2_Promptdevelopment", "Versuch_4", "results", f"{name}.json"]
savepath = os.path.join(*savepathlist)

with open(savepath, "w") as outfile:
    json.dump(results, outfile)