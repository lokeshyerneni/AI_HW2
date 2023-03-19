def initializeVariables(fileName):
    varFile = open(fileName, "r")
    varLines = varFile.readlines()
    varDict = {}
    varSize = 0
    # Appends numbers into dictionary for each value
    for line in varLines:
        vals = line.split(":")
        strListVal = list(line.split(":")[1].strip().replace(" ", ""))
        varDict.update({vals[0]: [int(val) for val in strListVal]})
        varSize += 1

    return varDict


def initializeConstraints(fileName):
    conFile = open(fileName, "r")
    conLines = conFile.readlines()
    conArr = []

    # Appends numbers into dictionary for each value
    for line in conLines:
        conArr.append(line.strip())
    return conArr
