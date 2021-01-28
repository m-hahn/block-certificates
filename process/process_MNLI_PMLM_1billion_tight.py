item = None
data = []
forSubset = None


with open("../items/witnesses_estimateS1ensitivity_MNLI_getSensitivityParts_PMLM_raw_1billion.py", "r") as inFile:
 try:
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
    assert not line.startswith("####"), line
    try:
       premise, hypothesis, prediction = line.split("\t")
    except ValueError:
        print("UNEXPECTED", line)
        assert False
        continue
    forSubset.append((premise, hypothesis, prediction))
 except StopIteration:
     pass

print(data)
print(len(data))

import random
rng = random.Random(5)

rng.shuffle(data)

data = data[:30]

allItems = []
for item in data:
     allItems.append((item["original"], '"NA"'))
     options = item["subsets"]
     for y in options:
        allItems += y
allItems = list(set(allItems))
rng.shuffle(allItems)
print(allItems)
print(len(allItems))

numberOfLists = int(len(allItems)/40)
lengthOfList = int(len(allItems)/numberOfLists)

streams = [open(f"output/{__file__}_{i}.js", "w") for i in range(numberOfLists)]

for i in range(numberOfLists):
    print("stimuli = [", file=streams[i])

def prettyPrint(x):
  #  if x[0] == "ORIG":
 #       x = x[1].split("@")
#        x.append("\"NA\"")
    if len(x) == 2:
        x = x[0].split("@")
        x.append("'NA'")
    print(x)
    x = list(x)
    x[0] = x[0].replace("Flam?­boy?­ant", "Flamboyant").replace("Flam? <unk> boy? <unk> ant", "Flamboyant").replace("R?? publique", "Republique").replace("R?? man", "Roman").replace("?.", "?").replace("Pe??", "Pe")
    return ("   { \"premise\" : \"" + x[0].replace('"', '\\"') + "\", \"hypothesis\" : \"" + x[1].replace('"', '\\"') + "\", \"model_rating\" : " + x[2] + "},")

for i in range(numberOfLists):
     relevant = allItems[i*lengthOfList : (i+1) * lengthOfList]
     for x in relevant:
        print("@@@", x)
        print(prettyPrint(x), file=streams[i])

for i in range(numberOfLists):
    print("];", file=streams[i])

for s in streams:
    s.close()



