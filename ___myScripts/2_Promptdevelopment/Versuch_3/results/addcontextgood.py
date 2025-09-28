import os, json

pathresults = ["___myScripts", "2_Promptdevelopment", "Versuch_4", "results"]
resultpath = ""
for pathpart in pathresults:
    resultpath = os.path.join(resultpath, pathpart)

resultfiles = os.listdir(resultpath)

# Define path for new solutions
savepathparts = ["___myScripts", "2_Promptdevelopment", "Versuch_4", "results_V2"]
savepath = os.path.join(*savepathparts)

for index, file in enumerate(resultfiles):
    if file != "addcontextgood.py":
        filepath = os.path.join(resultpath, file)
        with open(filepath) as jsondata:
            resultfile = json.load(jsondata)
        
        for result in resultfile:
            result["goodcontext"] = "neutral"
        savepathindividual = os.path.join(savepath, file)
        with open(savepathindividual, "w") as outfile:
            json.dump(resultfile, outfile)
