item = None
data = []
forSubset = None


with open("../items/witnesses_estimateS1ensitivity_WSC_getSensitivityParts_PMLM_raw_1billion.py", "r") as inFile:

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
    try:
       text, prediction = line.replace("\t \t", "\t").replace(" \t", "\t").replace("\t ", "\t").split("\t")
    except ValueError:
        print("UNEXPECTED", line.split("\t"))
        assert False
        continue

    forSubset.append((text, prediction.replace("tensor([", "").replace("])", "")))

print(data)

import random
rng = random.Random(5)


#def prettyPrint(x):
#    if x[0] == "ORIG":
#        x = x[1].split("@")
#        x.append("\"NA\"")
#    return ("   { \"premise\" : \"" + x[0].replace('"', '\\"') + "\", \"hypothesis\" : \"" + x[1].replace('"', '\\"') + "\", \"model_rating\" : " + x[2] + "},")


def prettyPrint(x):
    pretty = x.replace("  </s>", "").replace('"', '\\"')
    pretty = pretty[:pretty.index("_")] + "<i><u>" + pretty[pretty.index("_")+1:]
    pretty = pretty[:pretty.index("_")] + "</u></i>" + pretty[pretty.index("_")+1:]
    pretty = pretty[:pretty.index("[")] + "<b>" + pretty[pretty.index("[")+1:]
    pretty = pretty[:pretty.index("]")] + "</b>" + pretty[pretty.index("]")+1:]
    return pretty


with open(f"output/{__file__}.tsv", "w") as outFile:
 for itemID, item in enumerate(data):
     allRelevant = [("ORIG", item["original"])]
     options = item["subsets"]
     for i in range(len(options)):
         for x in options[i]:
             print("\t".join([str(itemID), str(i), prettyPrint(x[0]).strip(), str(float(x[1]))]), file=outFile)
     if itemID > 100:
         break

