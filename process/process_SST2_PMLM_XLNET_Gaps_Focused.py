item = None
data = []
forSubset = None


with open("../items/witnesses_estimateS1ensitivity_SST2_getSensitivityParts_finetuned_New.py", "r") as inFile:

 for line in inFile:
    line = line.strip()
    while line.startswith("######"):
        original = next(inFile).strip()
        print(item)
        detokenized = next(inFile).strip()
        assert detokenized.startswith("DETOKENIZED"), detokenized
        detokenized = detokenized.split("\t")[1].strip()
        line = next(inFile).strip()

        item = {"subsets" : [], "original" : original, "original_detokenized" : detokenized}
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
        detokenized = next(inFile).strip()
        assert detokenized.startswith("DETOKENIZED"), detokenized
        detokenized = detokenized.split("\t")[1].strip()
        line = next(inFile).strip()
        item = {"subsets" : [], "original" : original, "original_detokenized" : detokenized}
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
       text, prediction = line.split("\t")
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


selected = sorted(set(sensitivities[-30:]))
print(selected)

import random
rng = random.Random(5)

with open("../../GLUE/SST-2/dev.tsv", "r") as inFile:
    labels = inFile.read().strip().split("\n")[1:]
    labels = dict([[y.strip() for y in x.split("\t")] for x in labels])


streams = [open(f"output/{__file__}_{i}.js", "w") for i in range(10)]

for i in range(10):
    print("stimuli = [", file=streams[i])



with open(f"output/{__file__}.txt", "w") as outFile:
  for item_ in selected:
     item = data[item_[0]]
     assert item["sensitivity"] == item_[1]
     subsets = item["subsets"]
     original = item["original"]
     print('{"sentence" : "' + item["original_detokenized"].replace("</s>", "").strip().replace('"', '\\"') + '", "original" : "' + original.replace('"', '\\"') + '", "sensitivity" : ' + str(item["sensitivity"]) + ', "label" : ' + labels[original.replace("</s>", "").strip()] + '},', file=outFile)
#     print()
     if len(subsets) > 0:
        while len(subsets) < 10:
            subsets = subsets + subsets
        rng.shuffle(subsets)
        subsets = subsets[:10]
   
        for i in range(10):
           masked = subsets[i]["detokenized"]
           subset_sensitivity = subsets[i]["subset_sensitivity"]
           sensitivity = item["sensitivity"]
           masked_ = masked.replace("</s>", "").strip().replace('"', '\\"')
           print(masked_)
           r = [""]
           while "#" in masked_:
               q = masked_.index("#")
               r[-1] += masked_[:q]
               masked_ = masked_[q:]
               k = ([i for i in range(len(masked_)) if masked_[i] != "#"]+[len(masked_)])[0]
               r.append(masked_[:k])
               r.append("")
               masked_ = masked_[k:]
           if len(masked_) > 0:
               r[-1] += (masked_)
           r = [x for x in r if len(x) > 0]
           print('{"sentence" : ' + str(r) + ', "original" : "' + original.replace('"', '\\"') + '", "subset_sensitivity" : '+str(subset_sensitivity) + ', "sensitivity" : ' + str(sensitivity) + '},', file=streams[i])

for i in range(10):
    print("];", file=streams[i])

for s in streams:
    s.close()



