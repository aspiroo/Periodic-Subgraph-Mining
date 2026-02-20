reference1 = open("p7s3_6.txt")

fout1 = open("p7s3_6_new.txt", "w+")

delete_list = ["start", "psup", "p", "m", "[", "]", "\n"]

for line in reference1:
    for word in delete_list:
        line = line.replace(word, "")
    fout1.write(line)
    fout1.write("\n")
reference1.close()
fout1.close()

ps = open("p7s3_6_new.txt").read().strip()
splitReference1 = ps.split("\n")

list_ps = []
list_ps_u= []
list_ps_i = []
list_ps_j = []
ji = []

for fileLine in splitReference1:
    splitReference1_new = fileLine.split(" ")
    str_list = list(filter(None, splitReference1_new))
    convert2int = list(map(int, str_list))
    filt = list(filter(lambda x: x > 588, convert2int))
    convert2str = list(map(str, filt))
    list_ps_u = list(set(list_ps_u) | set(convert2str))

for fileLine in splitReference1:
    splitReference1_new = fileLine.split(" ")
    str_list = list(filter(None, splitReference1_new))
    convert2int = list(map(int, str_list))
    filt = list(filter(lambda x: x > 588, convert2int))
    convert2str = list(map(str, filt))
    list_ps.append(convert2str)

from functools import reduce
list_ps_i = list(reduce(set.intersection, [set(item) for item in list_ps]))

list_ps_j = str(len(list_ps_i)/len(list_ps_u))
ji.append(list_ps_j)

out1 = open("p7s3_ji.txt", "a")
out2 = open("p7s3_6_u.txt", "a")

for item in ji:
    out1.write(item + "\n")
for item in list_ps_u:
    out2.write(item + " ")
