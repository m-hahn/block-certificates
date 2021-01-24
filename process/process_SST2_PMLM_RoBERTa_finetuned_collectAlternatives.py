item = None
data = []
forSubset = None


with open("../items/witnesses_estimateS1ensitivity_SST2_getSensitivityParts_finetuned_RoBERTa_New.py", "r") as inFile:

 for line in inFile:
    line = line.strip()
    while line.startswith("######"):
        original = next(inFile).strip()
        line = next(inFile).strip()
        print(item)
        item = {"subsets" : [], "original" : original}
        data.append(item)
    if line.startswith("OVERALL SENSITIVITY ON THIS DATAPOI"):
        overall = float(line.split(" ")[-1])
        item["sensitivity"] = overall
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
       text, prediction = line.split("\t")
    except ValueError:
        print("UNEXPECTED", line)
        assert False
        continue

    forSubset.append((text, prediction.replace("tensor([", "").replace("])", "")))

print(data)

import random
rng = random.Random(5)



with open(f"output/{__file__}.tsv", "w") as outFile:
 for itemID, item in enumerate(data):
     allRelevant = [("ORIG", item["original"])]
     options = item["subsets"]
     print(len(options))
     for i in range(len(options)):
         for x in options[i]:
             print("\t".join([str(itemID), str(i), x[0].strip(), str(float(x[1]))]), file=outFile)
     if itemID > 100:
         break

