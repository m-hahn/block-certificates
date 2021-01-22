item = None
data = []
forSubset = None


with open("../items/witnesses_estimateS1ensitivity_SST2_getSensitivityParts_PMLM_raw_1billion.py", "r") as inFile:

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

streams = [open(f"output/{__file__}_{i}.js", "w") for i in range(60)]

for i in range(60):
    print("stimuli = [", file=streams[i])

def prettyPrint(x, sensitivity):
    if x[0] == "ORIG":
        x = x[1].split("@")
        x.append("\"NA\"")
    return ("   { \"text\" : \"" + x[0].replace("  </s>", "").replace('"', '\\"') + "\", \"model_rating\" : " + x[1] + ", \"model_sensitivity\" : " + str(sensitivity) + "},")

for item in data:
     allRelevant = [("ORIG", item["original"])]
     options = item["subsets"]
     print(len(options))
     for i in range(len(options)):
         s = options[i]
         s = sorted(set(s), key=lambda x:float(x[1]))
         print(s)
         if len(s) >= 6:
            select = s[:3] + s[-3:]
         else:
            select = s
         print(select)
         allRelevant += select
     
     while len(allRelevant) < 60:
       allRelevant += allRelevant
     rng.shuffle(allRelevant)
     allRelevant = allRelevant[:60]

     for i in range(60):
        print(prettyPrint(allRelevant[i], item["sensitivity"]), file=streams[i])

for i in range(60):
    print("];", file=streams[i])

for s in streams:
    s.close()



