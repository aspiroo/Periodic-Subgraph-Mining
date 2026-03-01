i = 1
while (i <= 66):
    with open("D:/Research/Periodic Subgraph Mining/Preprocessing/Inputs/drosophila_subset_t"+str(i)+".txt") as f:
        with open("C:/Users/Legion Y530/Downloads/NetsTensor_dist/bin/datasets/net"+str(i)+".network", "w") as f1:
            for line in f:
                 f1.write(line)
    print (str(i))
    i = i+1