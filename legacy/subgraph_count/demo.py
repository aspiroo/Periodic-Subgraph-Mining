input = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\subgraph_count\\new_subgraphs.txt").read().strip()

ln = input.split('\n')

s3 = []
s3_count = []

i = 3

while (i < 10):
    for line in ln:
        cell = line.split()
        if (cell[3]==str(i) and cell[5]== "9"):
            out = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\subgraph_count\p9s"+str(i)+".txt","a")
            out.write(line + "\n")
            s3.append("1")
        else:
            s3.append("0")

    s3_count.append(s3.count("1"))
    print (s3_count[i-3])
    s3 = []
    i = i+1