def parse_response(response, nameStr):
    parsedData = [x.split("\t") for x in str(response).split("\n")][1:]
    return [
        x[1]
        for x in parsedData
        if len(x) == 2
        and any(nameStr.lower() in z for z in [y.lower() for y in x[0].split("_")])
    ]

# If urlopen.read() returns bytes:
response = b'Entry name\tEntry\nEGFR_HUMAN\tP00533\n'
print("Byte response:", parse_response(response, "EGFR"))

# If it returns string?
response = 'Entry name\tEntry\nEGFR_HUMAN\tP00533\n'
print("String response:", parse_response(response, "EGFR"))
