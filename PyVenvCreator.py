import os
import json
import sys

# SETTINGS:
RED = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0m"

# -------------------------------------------- SCRIPT PATH DECLARATION (WITHOUT PRESET PATHS) ------------------------------------------------------------

# STEP 1: Path to your python.exe you want to use
pyPath = "C:\\Users\\andres.lueck\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
# STEP 2: Path to your venvfolder
venvPath = "C:\\Users\\andres.lueck\\Documents\\PyVenvs"

# ------------------------------------------------------------ PATHCODE () --------------------------------------------------------------------------

# Select mode:
mode = 0
print(f'{BOLD}Select pathmode:{RESET}\n\n1 - Skriptpath\n2 - Saved Paths\n________________\n')
while mode not in [1, 2]:
    mode = int(input('Mode: '))
    if mode in [1, 2]:
        break
    # Move cursor up and clear the line
    sys.stdout.write("\033[F")  # Move cursor up
    sys.stdout.write("\033[K")  # Clear the line

selectedSystem = ''
def getSystemName():
    print(f'\nOptions:\n')
    for name in systems:
        print(name)
    selectedSystem = input(f'{RESET}\nYour Systemname: ')
    return selectedSystem

if mode == 2:
    # With JSON:
    with open('PyVenvPaths.json') as file:
        Paths = json.load(file)
        systems = [entry['name'] for entry in Paths]
    
    print(f'\n{BOLD}Type your current system name')
    
    while selectedSystem not in systems:
        selectedSystem = getSystemName()
        if selectedSystem not in systems:
            print(f'\n{BOLD}{RED}System not found, try again{RESET}')
        else:
            pyPath = next((item['pypath'] for item in Paths if item['name'] == selectedSystem), None)
            venvPath = next((item['venvpath'] for item in Paths if item['name'] == selectedSystem), None)
            break

# ----------------------------------------------------------- VENV CREATION ----------------------------------------------------------
# Checks for the folders to exist.
check1 = os.access(pyPath, os.F_OK)
check2 = os.access(venvPath, os.F_OK)

if check1 & check2:
    # Input for name declaration for the new venv
    venvname = input("What's the name of the new venv?\n")
    print("Creating a new virtual environment")

    # os command execution to create new environment
    executed_command = os.system(f'cd "{venvPath}" && "{pyPath}" -m venv {venvname}')

    print(f"New virtual environment {BOLD}{venvname}{RESET} created!")
elif not check1 and check2:
    print(f'{RED}ERROR: python.exe not found in your defined path.{RESET}')
elif not check1 and not check2:
    print(f'{RED}ERROR: python.exe not found in your defined path.\n       {pyPath}\n       Venvs path not found.\n       {venvPath}{RESET}')
else:
    print(f'{RED}ERROR: Venvs path not found.\n       {venvPath}{RESET}')