lines = open('inputs.txt', 'r').readlines()

lines_set = set(lines)

out = open('output.txt', 'w')

for line in lines_set:
    out.write(line)