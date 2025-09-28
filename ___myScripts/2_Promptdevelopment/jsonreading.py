import json
import time
import re

with open("___Scripts-relevant\\Promptdevelopment\\Prompts_Dic.json") as jsondata:
    prompts = json.load(jsondata)

# Read dictionarys
print(prompts["en"][0])

for key in prompts:
    print(key)

print(len(prompts))

for index, language in enumerate(prompts):
    print(f'{index+1}/{len(prompts)}')
    print(language)

for i in range(10):
    print(f'\r{i+1}/10', end="\r")
    time.sleep(.1)

name = str(1) + "Hello"
print(name)

print(re.findall("(?:\d*\.*\d+)", "Current Level: -13.2db or 14.2 or 3"))
