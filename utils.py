def initializeVariables(fileName):
    varFile = open(fileName, "r")
    varLines = varFile.readlines()
    varDict = {}
    varSize = 0
    # Appends numbers into dictionary for each value
    for line in varLines:
        var, raw_vals = line.split(":")
        vals = raw_vals.strip().split(" ")

        # strListVal = list(line.split(":")[1].strip().replace(" ", ""))
        varDict.update({var: [int(val) for val in vals]})
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


def formatOutput(
    assignment: dict,
    step: int,
    isSuccess: bool,
):
    output = str(step) + "."
    for value in assignment:
        output += " " + str(value) + "=" + str(assignment[value]) + ","

    output = output[:-1]

    output += "  solution" if isSuccess else "  failure"

    return output
