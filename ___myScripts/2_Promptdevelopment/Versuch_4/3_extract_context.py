import os, json

#Read promptlist
PromptlistPathParts = ["___myScripts", "2_Promptdevelopment", "Versuch_4", "promptsWithKeywords"]
PromptlistPath = os.path.join(*PromptlistPathParts)

promptlists = []
for promptlist in os.listdir(PromptlistPath):
    promptlists.append(promptlist)
promptlists.sort()

for i, promptlist in enumerate(promptlists):
    print(f"• [{i+1}] {promptlist}")

# Select promptlist
SelectedFile = promptlists[int(input("\nWhich promptlist should be selected (number)?\n")) - 1]
print(f"Your selected promptlist: \033[1;33m{SelectedFile}\033[0m")

# Open promptlist
with open(os.path.join(PromptlistPath, SelectedFile), "r") as jsonfile:
    prompts = json.load(jsonfile)

# Iterate over all prompts

# What is the goal?
# Find the right page with good content
# save prompt and context