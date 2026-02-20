i = 1
while i <= 101:
    import csv

    list1 = ['gene1']
    list2 = ['gene2']
    reference = open('Connected Components\Gene Number 3\geneNumber'+str(i)+'.txt').read().strip()
    filetext = open("geneNamesWithLineNum.txt").read().strip()

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
                list1.append(lineCells[1])
                # value1 = lineCells[1]
                # out = open('gene1.txt', 'a')
                # out.write(value1 + "\n")
            if referenceCells[1] == lineCells[0]:
                list2.append(lineCells[1])
                # value2 = lineCells[1]
                # out = open('gene2.txt', 'a')
                # out.write(value2 + "\n")

    from xlsxwriter import Workbook

    workbook = Workbook('Connected Components\Gene Name 3\connection'+str(i)+'.xlsx')
    Report_Sheet = workbook.add_worksheet()

    for row_ind, row_value in enumerate(zip(list1, list2)):
        for col_ind, col_value in enumerate(row_value):
            Report_Sheet.write(row_ind, col_ind, col_value)

    workbook.close()
    i+=1