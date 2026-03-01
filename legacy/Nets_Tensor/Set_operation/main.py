import csv

i = 1
while (1 < 4069):
    reference = open("D:\Research\Periodic Subgraph Mining\\Nets_Tensor\Postprocessing\\net3\out\out2\out3\out"+str(i)+".csv").read().strip()
    filetext = open("D:\Research\Periodic Subgraph Mining\\Nets_Tensor\Set_operation\CAF-1.txt").read().strip()
    splitReference = reference.split("\n")
    splitFile = filetext.split("\n")

    reference_set = set(splitReference)
    chromosome_set = set(splitFile)

    intersect = reference_set.intersection(chromosome_set)
    intersect_len = len(intersect)

    difference_RC = reference_set - chromosome_set
    difference_RC_len = len(difference_RC)

    difference_CR = chromosome_set - reference_set
    difference_CR_len = len(difference_CR)

    list1 = ['out'+str(i), difference_RC_len, intersect_len, difference_CR_len]
    with open('D:\Research\Periodic Subgraph Mining\\Nets_Tensor\Set_operation\\caf-1_p7s3.csv', 'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(list1)
    print("file " + str(i) + " complete")
    i = i+1