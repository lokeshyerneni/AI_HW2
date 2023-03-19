# Command: python main.py ex1.var1.txt ex1.con.txt
import sys

# Initialized files, dictionary for var file
varFile = open(sys.argv[1], "r")
varLines = varFile.readlines()
varDict = {}
varSize = 0

# Appends numbers into dictionary for each value
for line in varLines:
    vals = line.split(":")
    strListVal = list(line.split(":")[1].strip().replace(" ", ""))
    varDict.update({vals[0]: [int(val) for val in strListVal]})
    varSize += 1

conFile = open(sys.argv[2], "r")
conLines = conFile.readlines()
conDict = []

# Appends numbers into dictionary for each value
for line in conLines:
    conDict.append(line.strip())

forwardChecking = True
if sys.argv[3] == "none":
    forwardChecking = False


def backtrackingSearch(csp, fc):
    return recursiveBacktracking({}, csp, fc)


def selectUnassignedVariable(dict, assignment, csp):
    newKey = [key for key in dict if key not in assignment]
    return newKey[0]


def checkConstraint(key, num, assignment, csp):
    assignment[key] = num
    constBool = True
    for con in csp:
        splitCon = con.split(" ")

        if splitCon[0] in assignment and splitCon[2] in assignment:
            if splitCon[1] == ">":
                constBool = assignment[splitCon[0]] > assignment[splitCon[2]]
                if not constBool:
                    return False
            elif splitCon[1] == "<":
                constBool = assignment[splitCon[0]] < assignment[splitCon[2]]
                if not constBool:
                    return False
            elif splitCon[1] == "=":
                constBool = assignment[splitCon[0]] == assignment[splitCon[2]]
                if not constBool:
                    return False
            elif splitCon[1] == "!":
                constBool = assignment[splitCon[0]] != assignment[splitCon[2]]
                if not constBool:
                    return False
        else:
            continue
    return True


def recursiveBacktracking(assignment, csp, fc):
    if len(assignment) == varSize:
        return assignment

    var = selectUnassignedVariable(varDict, assignment, csp)

    for num in varDict[var]:
        if checkConstraint(var, num, assignment, csp):
            assignment[var] = num
            result = recursiveBacktracking(assignment, csp, fc)
            if result != "Failure":
                return result
        del assignment[var]
    return "Failure"


print(backtrackingSearch(conDict, forwardChecking))
