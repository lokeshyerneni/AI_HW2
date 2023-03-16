import sys

# Initialized files, dictionary for var file
varFile = open(sys.argv[1], 'r')
varLines = varFile.readlines()
varDict = {}

# Appends numbers into dictionary for each value
for line in varLines:
    vals = line.split(":")
    strListVal = list(line.split(":")[1].strip().replace(" ", ""))
    varDict.update({vals[0]: [int(val) for val in strListVal]})

conFile = open(sys.argv[2], 'r')
conLines = conFile.readlines()
conDict = []

# Appends numbers into dictionary for each value
for line in conLines:
    conDict.append(line.strip())

print(conDict)