from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os, json, traceback
from starlette.formparsers import MultiPartParser

# To run go into folder of this script and execute:
# fastapi run evaluationAPI.py

app = FastAPI()

# Define allowed origins
origins = [
    "http://localhost:3000"
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/ping")
def ping():
    return True

@app.get("/resultList")
def getResultList():
    # Get path of resultfiles
    Resultspathlist = ["..","___myScripts", "2_Promptdevelopment", "Versuch_5", "results_massproduction"]
    Resultspath = ""
    for pathpart in Resultspathlist:
        Resultspath = os.path.join(Resultspath, pathpart)
    # Store list of results in files
    files = []
    for index, filename in enumerate(os.listdir(Resultspath)):
        files.append(filename)
    files.sort()
    return files

@app.get("/getResult")
def getResult(filename):
    # Get path of resultfiles
    Resultspathlist = ["..","___myScripts", "2_Promptdevelopment", "Versuch_5", "results_massproduction"]
    Resultspath = ""
    for pathpart in Resultspathlist:
        Resultspath = os.path.join(Resultspath, pathpart)
    # Store list of results in files
    with open(f"{Resultspath}/{filename}") as jsondata:
        results = json.load(jsondata)
    return results

@app.post("/saveResult")
async def saveResult(request: Request):
    form = await request.form(max_part_size=50 * 1024 * 1024)  # 50 MB

    filename = form["filename"]
    results = json.loads(form["results"])  # Parse stringified JSON array

    print(filename)
    # Build path and ensure dirs exist
    Resultspathlist = ["..", "___myScripts", "2_Promptdevelopment", "Versuch_5", "results_massproduction", filename]
    Resultspath = os.path.join(*Resultspathlist)
    os.makedirs(os.path.dirname(Resultspath), exist_ok=True)

    # Save file
    with open(Resultspath, "w") as outfile:
        json.dump(results, outfile, indent=2)

    return {"message": "Saved", "path": Resultspath}