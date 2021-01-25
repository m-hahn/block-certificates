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


with open(f"output/{__file__}.tsv", "w") as outFile:
  print("\t".join(["original", "sensitivity"]), file=outFile)
  for d in data:
    if "sensitivity" not in d:
        print("ODD?", d)
        continue
    print("\t".join([d["original"], str(d["sensitivity"])]), file=outFile)
