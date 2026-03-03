list1 = list(range(1,589))
list2 = []
reference = open("justDevelopmentwithLineNum.txt").read().strip()
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
        if referenceCells[1] == lineCells[0]:
            list2.append(lineCells[1])

#print(list1)
#print(list2)
"""
with open('justDevelopmentWithGeneNameAndNumber.txt','w') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(zip(list1,list2))"""

with open('justDevelopmentWithGeneName.txt', 'w') as f:
    for item in list2:
        f.write("%s\n" % item)