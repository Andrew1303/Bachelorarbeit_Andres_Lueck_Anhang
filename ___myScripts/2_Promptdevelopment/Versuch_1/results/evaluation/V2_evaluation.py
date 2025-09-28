import json
import numpy as np

path = r'___Scripts-relevant\Promptdevelopment\Versuch 1\results\V2_20250507175905_al-2_ap-8_diode-low-frequency.json'

with open(path) as jsondata:
    results = json.load(jsondata)
print(len(results))

# For each prompt
for j in range(len(results)):
    print(f"- {j} -------------------------------------------------------------------------------------\n")
    prompt = results[j]["prompt"]
    duration = results[j]["results"]["duration"]
    answer = results[j]["results"]["answer"]
    found_bfrs = results[j]["results"]["found_bfrs"]

    amount_results = len(duration)

    bfrs = []
    all_bfrs = []
    # For each answer per prompt
    for i in range(amount_results):
        
        # print(f'Prompt: {prompt}\n\nDuration: {duration[i]}\n\nAnswer:\n{answer[i]}\n\nFound BFR: {found_bfrs[i]}\n\n')
        for number in found_bfrs[i]:
            all_bfrs.append(number)
            if number < 1 and number != 0.0:
                bfrs.append(number)
    if len(bfrs) > 1:
        mean_bfr = np.mean(bfrs)
        print(f"{prompt}\n\nAnswer: {mean_bfr}\nBFR's: {bfrs}\nAll_BFRS: {all_bfrs[i]}")
    else:
        mean_bfr = None
        print(f"{prompt}\n\nAnswer: {mean_bfr}\nBFR's: {bfrs}\nAll_BFRS: {all_bfrs[i]}")
        print(f'Previous llm-answer was:\n{answer}')