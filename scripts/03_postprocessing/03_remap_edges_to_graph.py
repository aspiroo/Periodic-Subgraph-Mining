i = 3
while i <= 9:
    reference = open("../../results/listminer_output/union_genes/p1s"+str(i)+".txt").read().strip()
    filetext = open("../../data/processed/outputWithEdgeNum.txt").read().strip()

    splitReference = reference.split(" ")
    convert2int = list(map(int, splitReference))
    filter = list(filter(lambda x: x > 588, convert2int))
    convert2str = list(map(str, filter))

    splitFile = filetext.split("\n")

    for referenceLine in convert2str:
        referenceCells = referenceLine.split()
        for fileLine in splitFile:
            lineCells = fileLine.split()
            if referenceCells[0] == lineCells[0]:
                out = open('../../results/components/remapped/output1th'+str(i)+'.txt', 'a')
                for line in fileLine:
                    out.write(line)
                out.write('\n')
    del convert2int
    del filter
    del convert2str
    i += 1