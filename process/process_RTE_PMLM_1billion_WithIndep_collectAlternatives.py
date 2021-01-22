item = None
data = []
forSubset = None


with open("../items/witnesses_estimateS1ensitivity_RTE_getSensitivityParts_PMLM_raw_1billion_WithIndep.py", "r") as inFile:

 for line in inFile:
    line = line.strip()
    while line.startswith("######"):
        original = next(inFile).strip()
        line = next(inFile).strip()
        print(item)
        item = {"subsets" : [], "original" : original}
        data.append(item)
    if line.startswith("OVERALL SENSITIVITY ON THIS DATAPOI"):
        overall = line
        line = next(inFile).strip()
    while line.startswith("&&&&&&&&&&& SUBSET SEN"):
        if forSubset is not None:
           print(len(forSubset))
        forSubset = []
        assert item is not None
        item["subsets"].append(forSubset)
        withMask1 = next(inFile)
        withMask2 = next(inFile)
        line = next(inFile).strip()
    while line.startswith("######"):
        original = next(inFile).strip()
        line = next(inFile).strip()
        item = {"subsets" : [], "original" : original}
        data.append(item)
    assert not line.startswith("####"), line
    try:
       premise, hypothesis, prediction = line.split("\t")
    except ValueError:
        print("UNEXPECTED", line)
        continue
    forSubset.append((premise, hypothesis, prediction))


print(data)

import random
rng = random.Random(5)


#def prettyPrint(x):
#    if x[0] == "ORIG":
#        x = x[1].split("@")
#        x.append("\"NA\"")
#    return ("   { \"premise\" : \"" + x[0].replace('"', '\\"') + "\", \"hypothesis\" : \"" + x[1].replace('"', '\\"') + "\", \"model_rating\" : " + x[2] + "},")

with open(f"output/{__file__}.tsv", "w") as outFile:
 for itemID, item in enumerate(data):
     allRelevant = [("ORIG", item["original"])]
     options = item["subsets"]
     for i in range(len(options)):
         for x in options[i]:
             print("\t".join([str(itemID), str(i), x[0].strip(), x[1].strip(), str(float(x[2]))]), file=outFile)
     if itemID > 100:
         break
