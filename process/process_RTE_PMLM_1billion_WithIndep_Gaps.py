item = None
data_insens = []
forSubset_insens = None


with open("../items/insensitive_witnesses_estimateS1ensitivity_RTE_getSensitivityParts_PMLM_raw_1billion_WithIndep_GetInsensitiveSamples.py", "r") as inFile:
 try:
  for line in inFile:
    line = line.strip()
    while line.startswith("######"):
        original = next(inFile).strip()
        line = next(inFile).strip()
        print(item)
        item = {"subsets" : [], "original" : original}
        data_insens.append(item)
    assert not line.startswith("####"), line
    assert line.startswith("&&&&&&&&&@ SUBSETS"), line
    try:
       _, premise, hypothesis = line.split("\t")
    except ValueError:
        print("UNEXPECTED", line)
        continue
    item["subsets"].append((premise, hypothesis, 0))
 except StopIteration:
   pass
print(data_insens)



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
        item["overall_sens"] = overall.split(" ")[-1]
        line = next(inFile).strip()
    while line.startswith("&&&&&&&&&&& SUBSET SEN"):
        if forSubset is not None:
           print(len(forSubset))
        #forSubset = []
        assert item is not None
        #item["subsets"].append(forSubset)
        withMask1 = next(inFile)
        withMask2 = next(inFile)
        _, _, subsetSensitivity = line.strip().split("\t")
        print(withMask1)
        _, premise, hypothesis = withMask1.strip().split("\t")
        item["subsets"].append((premise, hypothesis, subsetSensitivity))
        line = next(inFile).strip()
    while line.startswith("######"):
        original = next(inFile).strip()
        line = next(inFile).strip()
        item = {"subsets" : [], "original" : original}
        data.append(item)
    if line.startswith("OVERALL SENSITIVITY ON THIS DATAPOI"):
        overall = line
        item["overall_sens"] = overall.split(" ")[-1]
        line = next(inFile).strip()
    assert not line.startswith("####"), line
    try:
       premise, hypothesis, prediction = line.split("\t")
    except ValueError:
        print("UNEXPECTED", line)
        continue
    #forSubset.append((premise, hypothesis, prediction))

ssum = 0
isum = 0
for i in range(len(data_insens)):
    ins = data_insens[i]
    sens = data[i]
  #  print(i)
 #   print(ins["original"])
#    print(sens["original"])
    assert ins["original"] == sens["original"]
    if len(data[i]["subsets"]) == 0:
        continue
    #try:
    print(len(data[i]["subsets"]), len(ins["subsets"]), [x[2] for x in data[i]["subsets"]], data[i]["overall_sens"])
    ssum += len(data[i]["subsets"])
    isum += len(ins["subsets"])
  #  except IndexError:
   #   print(data[i]["subsets"])
    data[i]["subsets"] += ins["subsets"]
#    print(len(data[i]["subsets"]))
print(ssum, isum)
#quit()
print(data)

import random
rng = random.Random(5)

streams = [open(f"output/{__file__}_{i}.js", "w") for i in range(14)]

for i in range(14):
    print("stimuli = [", file=streams[i])

def prettyPrint(x):
    return ("   { \"premise\" : \"" + x[0].replace('"', '\\"').replace("###########", "########### ")+ "\", \"hypothesis\" : \"" + x[1].replace('"', '\\"').replace("###########", "########### ") + "\", \"model_sens\" : " + str(float(x[2])) + "},")




for item in data:
     if len(item["subsets"]) == 0:
         continue
     allRelevant = [("ORIG", item["original"])]
     options = item["subsets"]
    
     options_sens = [x for x in options if float(x[2]) > 1e-5]
     options_insens = [x for x in options if float(x[2]) <= 1e-5]
     if len(options_sens) == 0:
         continue
     if len(options_insens) == 0:
         continue
     while len(options_insens) < 7:
       options_insens += options_insens
     while len(options_sens) < 7:
       options_sens += options_sens
     rng.shuffle(options_sens)
     rng.shuffle(options_insens)
     options = options_insens[:7] + options_sens[:7]
     rng.shuffle(options)

     for i in range(14):
        print(prettyPrint(options[i]), file=streams[i])

for i in range(14):
    print("];", file=streams[i])

for s in streams:
    s.close()



