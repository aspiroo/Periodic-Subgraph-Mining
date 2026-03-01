fo = open("D:\Research\\filtered\output.txt").read().strip()
lines = fo.split("\n")
for splitLine in lines:
    lineCells = splitLine.split(" ")
    if (int(lineCells[1]) <= (24-(8-1)*2) and lineCells[3] == '3' and lineCells[5] == '2'):
        out = open('D:\Research\\filtered\p2s3.txt', 'a')
        for item in lineCells:
            out.write('%s' % item)
            out.write(" ")
        out.write('\n')
