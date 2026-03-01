

s3 = []
s3_count = []

i = 4
j = 3
while (i > 2):
    input = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\subgraph_count\individual\p9s"+str(i)+".txt").read().strip()
    out = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\subgraph_count\p9s" + str(i) + ".txt", "a")

    ln = input.split('\n')
    for line in ln:
        cell = line.split()
        if (int(cell [1]) <= j and cell[3]==str(i) and cell[5]== "9"):
            s3.append("1")
            out.write(line + "\n")
        else:
            s3.append("0")

    s3_count.append(s3.count("1"))
    print (s3_count[4-i])
    s3 = []
    j = j + 9
    i = i-1