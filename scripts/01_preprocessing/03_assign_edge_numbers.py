with open('data/processed/edges_after_removing_duplicates/output.txt', 'r') as program:
    data = program.readlines()

with open('data/processed/edges_with_given_number/outputWithEdgeNum.txt', 'w') as program:
    for (number, line) in enumerate(data):
        program.write('%d\t%s' % (number + 589, line))