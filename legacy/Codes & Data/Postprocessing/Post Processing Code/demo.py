i = 3
while (i < 4):
    import csv
    delete_list = ["start", "psup", "p", "m", "[", "]", "\n"]
    fin = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\subgraph_count\p9s"+str(i)+".txt")
    fout = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\subgraph_count\junk\junk9"+str(i)+".txt", "w+")
    for line in fin:
        for word in delete_list:
            line = line.replace(word, "")
        fout.write(line)
    fin.close()
    fout.close()

    reference = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\subgraph_count\junk\junk9"+str(i)+".txt").read().strip()

    splitReference = reference.split(" ")
    str_list = list(filter(None, splitReference))
    convert2int = list(map(int, str_list))
    filt = list(filter(lambda x: x > 588, convert2int))
    convert2str = list(map(str, filt))


    def remove_duplicates(values):
        output = []
        seen = set()
        for value in values:
            # If value has not been encountered yet,
            # ... add it to both list and set.
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output


    # Remove duplicates from this list.
    result = remove_duplicates(convert2str)

    with open('D:\Studies & Researches\Researches\Periodic Subgraph Mining\listMinerOutputs (with Edges)\\union_genes_count_new\\test9'+str(i)+'.txt', 'w') as f:
        for item in result:
            f.write("%s " % item)

    reference = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\listMinerOutputs (with Edges)\\union_genes_count_new\\test9"+str(i)+".txt").read().strip()
    filetext = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\Preprocessing\Python\outputWithEdgeNum.txt").read().strip()

    splitReference = reference.split(" ")
    convert2int = list(map(int, splitReference))
    filter = list(filter(lambda x: x > 588, convert2int))
    convert2str = list(map(str, filter))

    splitFile = filetext.split("\n")

    for referenceLine in convert2str:
        referenceCells = referenceLine.split()
        for fileLine in splitFile:
            lineCells = fileLine.split()
            if referenceCells[0] == lineCells[0]:
                out = open('D:\Studies & Researches\Researches\Periodic Subgraph Mining\Postprocessing\\union_genes_count_new\p9s'+str(i)+'.txt', 'a')
                for line in fileLine:
                    out.write(line)
                out.write('\n')
    del convert2int
    del filter
    del convert2str

    reference = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\Postprocessing\\union_genes_count_new\p9s"+str(i)+".txt").read().strip()
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
                out = open('D:\Studies & Researches\Researches\Periodic Subgraph Mining\Postprocessing\\union_genes_count_new\gene_Number_p9s'+str(i)+'.txt', 'a')
                out.write(value2 +"\t"+ value1 +"\n")

    list1 = ['gene1']
    list2 = ['gene2']
    reference = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\Postprocessing\\union_genes_count_new\gene_Number_p9s"+str(i)+".txt").read().strip()
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
                #value1 = lineCells[1]
                #out = open('gene1.txt', 'a')
                #out.write(value1 + "\n")
            if referenceCells[1] == lineCells[0]:
                list2.append(lineCells[1])
                #value2 = lineCells[1]
                #out = open('gene2.txt', 'a')
                #out.write(value2 + "\n")

    with open('D:\Studies & Researches\Researches\Periodic Subgraph Mining\Postprocessing\\union_genes_count_new\\results\p9s'+str(i)+'.txt','w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(zip(list1,list2))

    from xlsxwriter import Workbook


    workbook = Workbook('D:\Studies & Researches\Researches\Periodic Subgraph Mining\Postprocessing\\union_genes_count_new\\results\p9s'+str(i)+'.xlsx')
    Report_Sheet = workbook.add_worksheet()

    for row_ind, row_value in enumerate(zip(list1, list2)):
        for col_ind, col_value in enumerate(row_value):
            Report_Sheet.write(row_ind, col_ind, col_value)

    workbook.close()
    i = i + 1