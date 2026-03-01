i = 1
while (i < 7):
    reference = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\\Nets_Tensor\Journal_comparison_v2\\out\\file"+str(i)+".txt").read().strip()
    filetext = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\Postprocessing\justDevelopmentWithLineNum.txt").read().strip()

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
            if referenceCells[0] == lineCells[0]:
                value1 = lineCells[1]
                out = open('D:\Studies & Researches\Researches\Periodic Subgraph Mining\\Nets_Tensor\Journal_comparison_v2\out\out2\out'+str(i)+'.txt','a')
                out.write(value1 + "\n")
    i = i + 1