i = 3
while i <= 9:
    reference = open("D:\Research\Periodic Subgraph Mining\Postprocessing\\new\output1th"+str(i)+".txt").read().strip()
    filetext = open("justDevelopmentWithLineNum.txt").read().strip()

# split the reference file into a list of strings, splitting each time you encounter a new line
    splitReference = reference.split("\n")

# do the same for the file
    splitFile = filetext.split("\n")

# then, for each line in the reference,
    for referenceLine in splitReference:

    # split that line into a list of strings, splitting each time you encouter a stretch of whitespace
        referenceCells = referenceLine.split()

    # then, for each line in your 'file',
        for fileLine in splitFile:

        # split that line into a list of strings, splitting each time you encouter a stretch of whitespace
            lineCells = fileLine.split()

        # now, for each line in 'reference' check to see if the first value is equal to the first value of the current line in 'file'
            if referenceCells[2] == lineCells[0]:
                value1 = lineCells[1]
            if referenceCells[1] == lineCells[0]:
                value2 = lineCells[1]
                out = open('D:\Research\Periodic Subgraph Mining\Postprocessing\\new\geneNumber1th'+str(i)+'.txt', 'a')
                out.write(value2 +"\t"+ value1 +"\n")
    i += 1