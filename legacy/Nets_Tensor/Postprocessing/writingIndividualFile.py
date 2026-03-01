f = open("C:/Users/Legion Y530/Downloads/NetsTensor_dist/bin/results/minGene3minNet8minD0.6.PATTERN","r")
line = f.readlines()

i=1
while i < 3488:
    out = open("D:/Research/Periodic Subgraph Mining/Nets_Tensor/Postprocessing/net8/file"+str(i)+".txt", "w")
    out.write(line[i-1])
    print("file " + str(i) + " complete")
    i += 1