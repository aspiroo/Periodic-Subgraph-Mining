import csv
term = []
go = []
with open('GO_Biological_Process_2018_table.tsv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    for row in reader:
        term.append(row['Term'])


i = 0
while i < len(term):
    y = term[i].split('(')[1].split(')')[0]
    go.append(y)
    i = i+1

with open('GO_Biological_Process_2018_table.txt', 'w') as f:
    for item in go:
        f.write("%s\n" % item)
