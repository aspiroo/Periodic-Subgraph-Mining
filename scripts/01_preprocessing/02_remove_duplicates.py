lines = open('data/processed/total_edges/inputs.txt', 'r').readlines()

lines_set = set(lines)

out = open('data/processed/edges_after_removing_duplicates/output.txt', 'w')

for line in lines_set:
    out.write(line)