i = 3
while i <= 9:
    reference = open("../../results/components/remapped/output1th"+str(i)+".txt").read().strip()
    filetext = open("../../data/processed/gene_mappings/justDevelopmentwithLineNum.txt").read().strip()

    splitReference = reference.split("\n")
    splitFile = filetext.split("\n")

    for referenceLine in splitReference:
        referenceCells = referenceLine.split()
        for fileLine in splitFile:
            lineCells = fileLine.split()
            if referenceCells[2] == lineCells[0]:
                value1 = lineCells[1]
            if referenceCells[1] == lineCells[0]:
                value2 = lineCells[1]
                out = open('../../results/components/gene_numbers/geneNumber1th'+str(i)+'.txt', 'a')
                out.write(value2 +"\t"+ value1 +"\n")
    i += 1