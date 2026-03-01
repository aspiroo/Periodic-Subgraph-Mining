
input1 = open('D:\Research\Periodic Subgraph Mining\Keller\data\Just_development.txt', 'r')
data = input1.readlines()

out1 = open('justDevelopmentwithLineNum.txt', 'w')
for (number, line) in enumerate(data):
    out1.write('%d\t%s' % (number+1, line))

input2 = open('D:\Research\Periodic Subgraph Mining\Keller\data\genenames.txt', 'r')
data = input2.readlines()

out2 = open('geneNamesWithLineNum.txt', 'w')
for (number, line) in enumerate(data):
    out2.write('%d\t%s' % (number+1, line))

