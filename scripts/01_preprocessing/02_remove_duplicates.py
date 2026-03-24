lines = open('data/processed/inputs.txt', 'r').readlines()

lines_set = set(lines)

out = open('data/processed/output.txt', 'w')
# # Use dict.fromkeys to preserve first-occurrence order (Python 3.7+)
# seen = {}
# for line in lines:
#     seen[line] = None

for line in lines_set:
    out.write(line)