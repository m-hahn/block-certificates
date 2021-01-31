item = None
data = []
forSubset = None


with open("../items/witnesses_estimateS1ensitivity_QNLI_getSensitivityParts_PMLM_raw_1billion.py", "r") as inFile:

 for line in inFile:
    line = line.strip()
    while line.startswith("######"):
        original = next(inFile).strip()
        print(item)
 #       detokenized = next(inFile).strip()
#        assert detokenized.startswith("DETOKENIZED"), detokenized
  #      detokenized = detokenized.split("\t")[1].strip()
        line = next(inFile).strip()

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
#        item["subsets"].append(forSubset)
        withMask1 = next(inFile)
        withMask1 = withMask1.split("\t")[1].strip()
        item["subsets"].append({"detokenized" : withMask1, "subset_sensitivity" : float(line.split(" ")[-1])})
        withMask2 = next(inFile)
        line = next(inFile).strip()
    while line.startswith("######"):
        original = next(inFile).strip()
#        detokenized = next(inFile).strip()
 #       assert detokenized.startswith("DETOKENIZED"), detokenized
  #      detokenized = detokenized.split("\t")[1].strip()
        line = next(inFile).strip()
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
#        item["subsets"].append(forSubset)
        withMask1 = next(inFile)
        withMask2 = next(inFile)
        item["subsets"].append({"detokenized" : withMask1, "subset_sensitivity" : float(line.split(" ")[-1])})
        line = next(inFile).strip()
    assert not line.startswith("####"), line
    try:
       premise, hypothesis, prediction = line.split("\t")
    except ValueError:
        print("UNEXPECTED", line)
        assert False
        continue

#    forSubset.append((text, prediction.replace("tensor([", "").replace("])", "")))

print("---------")
print(data[0])
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
    return ((x[1] + "@ "+ x[2]) , x[3])

with open("../../GLUE/QNLI/dev.tsv", "r") as inFile:
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
     print('{"premise" : ' + json.dumps(premise.split(" ")) + ', "hypothesis" : ' +json.dumps(hypothesis.split(" ")) + ', "sentence" : "' + original.replace('"', '\\"').replace("</s>", "").strip() + '", "sensitivity" : ' + str(item["sensitivity"]) + ', "label" : "' + labels[original.replace("</s>", "").strip()] + '"},', file=outFile)
#     print()




