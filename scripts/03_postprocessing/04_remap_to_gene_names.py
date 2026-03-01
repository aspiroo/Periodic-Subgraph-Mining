import csv

i = 3
while i <= 9:
    list1 = ['gene1']
    list2 = ['gene2']
    reference = open("../../results/components/gene_numbers/geneNumber1th"+str(i)+".txt").read().strip()
    filetext = open("../../data/processed/gene_mappings/geneNamesWithLineNum.txt").read().strip()

    splitReference = reference.split("\n")
    splitFile = filetext.split("\n")

    for referenceLine in splitReference:
        referenceCells = referenceLine.split()
        for fileLine in splitFile:
            lineCells = fileLine.split()
            if referenceCells[0] == lineCells[0]:
                list1.append(lineCells[1])
            if referenceCells[1] == lineCells[0]:
                list2.append(lineCells[1])

    with open('../../results/components/gene_names/p1s'+str(i)+'.txt','w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(zip(list1,list2))

    from xlsxwriter import Workbook

    workbook = Workbook('../../results/components/gene_names/p1s'+str(i)+'.xlsx')
    Report_Sheet = workbook.add_worksheet()

    for row_ind, row_value in enumerate(zip(list1, list2)):
        for col_ind, col_value in enumerate(row_value):
            Report_Sheet.write(row_ind, col_ind, col_value)

    workbook.close()
    i += 1