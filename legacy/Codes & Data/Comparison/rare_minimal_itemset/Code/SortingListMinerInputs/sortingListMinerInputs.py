reference = open("listMinerInputs.txt").read().strip()
splitReference = reference.split("\n")
for referenceLine in splitReference:
    # split that line into a list of strings, splitting each time you encouter a stretch of whitespace
    referenceCells = referenceLine.split()
    referenceCells = list(map(int,referenceCells))
    referenceCells.sort()
    print(referenceCells)
    out = open('sortedlistMinerInputs.txt', 'a')
    for item in referenceCells:
        out.write('%s' % item)
        out.write(" ")
    out.write('\n')
