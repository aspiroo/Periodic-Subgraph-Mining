i = 1
while (i <=66):
    reference = open("C:/Users/Legion Y530/Downloads/NetsTensor_dist/bin/datasets/net"+str(i)+".network").read().strip()


    # split the reference file into a list of strings, splitting each time you encounter a new line
    splitReference = reference.split("\n")

    # then, for each line in the reference,
    for referenceLine in splitReference:

        # split that line into a list of strings, splitting each time you encouter a stretch of whitespace
        referenceCells = referenceLine.split()
        referenceCells.insert(2, '1')
        filetext = open("net" + str(i) + ".network", "a")
        filetext.write(referenceCells[0] + "\t" + referenceCells[1] + "\t" + referenceCells[2] +"\n")
    i = i+1