
input1 = open('data/raw/Just_development.txt', 'r')
data = input1.readlines()

out1 = open('data/processed/gene_mappings/justDevelopmentwithLineNum.txt', 'w')
for (number, line) in enumerate(data):
    out1.write('%d\t%s' % (number+1, line))

input2 = open('data/raw/genenames.txt', 'r')
data = input2.readlines()

out2 = open('data/processed/gene_mappings/geneNamesWithLineNum.txt', 'w')
for (number, line) in enumerate(data):
    out2.write('%d\t%s' % (number+1, line))

