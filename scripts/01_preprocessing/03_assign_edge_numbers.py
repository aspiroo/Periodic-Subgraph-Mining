with open('data/processed/output.txt', 'r') as program:
    data = program.readlines()

with open('data/processed/outputWithEdgeNum.txt', 'w') as program:
    for (number, line) in enumerate(data):
        program.write('%d\t%s' % (number + 589, line))