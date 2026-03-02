lines = open('data/processed/inputs.txt', 'r').readlines()

lines_set = set(lines)

out = open('data/processed/output.txt', 'w')

for line in lines_set:
    out.write(line)