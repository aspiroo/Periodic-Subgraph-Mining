fo = open("D:\Research\Periodic Subgraph Mining\Comparison\\randomize\output_ara2_sir_v2.txt").read().strip()
i = 3
while i <= 9:
    lines = fo.split("\n")
    for splitLine in lines:
        lineCells = splitLine.split(" ")
        if (int(lineCells[1]) <= (90-(i-1)*2) and lineCells[3] == str(i) and lineCells[5] == str(2)):
            out = open('D:\Research\Periodic Subgraph Mining\Comparison\\randomize\p2s'+str(i)+'_ara2_sir_v2.txt', 'a')
            for item in lineCells:
                out.write('%s' % item)
                out.write(" ")
            out.write('\n')
    i += 1