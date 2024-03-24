import json

file_path = "tests.json"

with open(file_path, 'r') as file:
    probData = json.load(file)
    probData["programs"]["haha"] = "boi"

#WRite the changes up
with open(file_path, 'w') as file:
    json.dump(probData, file, indent=4)