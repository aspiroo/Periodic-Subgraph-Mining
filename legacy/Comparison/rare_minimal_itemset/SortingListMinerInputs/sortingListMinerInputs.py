reference = open("D:\Research\Periodic Subgraph Mining\Comparison\\rare_minimal_itemset\listMinerInputs.txt").read().strip()
splitReference = reference.split("\n")
for referenceLine in splitReference:
    # split that line into a list of strings, splitting each time you encouter a stretch of whitespace
    referenceCells = referenceLine.split()
    referenceCells = list(map(int,referenceCells))
    referenceCells.sort()
    print(referenceCells)
    out = open('D:\Research\Periodic Subgraph Mining\Comparison\\rare_minimal_itemset\sortedlistMinerInputs.txt', 'a')
    for item in referenceCells:
        out.write('%s' % item)
        out.write(" ")
    out.write('\n')
