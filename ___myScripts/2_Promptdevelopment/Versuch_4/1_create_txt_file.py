import os, json
import PyPDF2
from progresbar import progresbar

DocumentPathParts = ["Dokumente"]
DocumentPath = os.path.join(*DocumentPathParts)

# List all promptlists
files = []
print("\nList of available files:")
for index, filename in enumerate(os.listdir(DocumentPath)):
    files.append(filename)
files.sort()

for i, file in enumerate(files):
    print(f"• [{i+1}] {file}")

# Select promptlist
SelectedFile = files[int(input("\nWhich file should be converted (number)?\n")) - 1]
print(f"Your selected file: \033[1;33m{SelectedFile}\033[0m")

DocumentPath = os.path.join(DocumentPath, SelectedFile)
print(DocumentPath)
with open(DocumentPath, 'rb') as pdf:
    pdfFile = PyPDF2.PdfReader(pdf, strict=False)
    amountPages = len(pdfFile.pages)
    counter = 1
    pages = []
    for page in pdfFile.pages:
        progresbar(counter, amountPages)
        pages.append(page.extract_text())
        counter += 1

savepathParts = ["___myScripts", "2_Promptdevelopment", "Versuch_4", "txt_Files", SelectedFile.replace(".pdf", ".json")]
savepath = os.path.join(*savepathParts)

with open(savepath, "w",) as file:
    json.dump(pages, file)