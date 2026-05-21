def name2uniprot(nameStr, organism):
    response = "Entry name\tEntry\nEGFR_HUMAN\tP00533\n"
    parsedData = [x.split("\t") for x in str(response).split("\n")][1:]
    print("ParsedData", parsedData)
    return [
        x[1]
        for x in parsedData
        if len(x) == 2
        and any(nameStr.lower() in z for z in [y.lower() for y in x[0].split("_")])
    ]

print(name2uniprot("EGFR", ["tax/9606"]))
