item = None
data = []
forSubset = None


with open("../items/witnesses_estimateS1ensitivity_MRPC_getSensitivityParts_PMLM_raw_1billion_WithIndep.py", "r") as inFile:
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
 except StopIteration:
     pass

print("---------")
print(data[0])

data = [x for x in data if "sensitivity" in x]

print(len(data))



sensitivities = sorted([(i, x["sensitivity"], len(x["subsets"])) for i, x in enumerate(data)], key=lambda x:x[1])

# 30 items equally spaced
# the top 20 high-sensitivity ones


selected = sorted(set(sensitivities[-30:] + [sensitivities[i] for i in range(0, len(sensitivities), int(len(sensitivities)/30 ))]))
print(selected)

import random
rng = random.Random(5)

def pairs(x):
    print("@", x)
    key = (x[3] + "@ "+ x[4]).replace(" ", "").replace(".", "")
    print("@@@"+key+"@@@")
    return (key , {"0" : "not_entailment", "1" : "entailment"}[x[0]])

with open("../../GLUE/MRPC/dev.tsv", "r") as inFile:
    labels = inFile.read().strip().split("\n")[1:]
    labels = dict([pairs([y.strip() for y in x.split("\t")]) for x in labels])



import json


with open(f"output/{__file__}.txt", "w") as outFile:
  for item_ in selected:
     item = data[item_[0]]
     assert item["sensitivity"] == item_[1]
     subsets = item["subsets"]
     original = item["original"]
     print((item))
     hypothesis, premise = original.replace('"', '\\"').replace("</s>", "").strip().split("@ ")
     originalKey = original.replace("</s>", "").strip().replace(" ", "").replace(".", "")
     print("###"+originalKey+"###")
     print('{"premise" : ' + json.dumps(premise.split(" ")) + ', "hypothesis" : ' +json.dumps(hypothesis.split(" ")) + ', "sentence" : "' + original.replace('"', '\\"').replace("</s>", "").strip() + '", "sensitivity" : ' + str(item["sensitivity"]) + ', "label" : "' + labels[originalKey] + '"},', file=outFile)
#     print()




