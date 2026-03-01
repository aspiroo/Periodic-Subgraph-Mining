f = open("D:/p5s4.txt","r")
line = f.readlines()

i=0
while i < 189:
    out = open("D:\Research\Periodic Subgraph Mining\Postprocessing\Largest Connected components\\test3rd"+str(i+1)+".txt", "w")
    out.write(line[i])
    print("file " + str(i+1) + " complete")
    i += 1