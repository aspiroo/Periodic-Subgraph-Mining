reference1 = open("listMinerInputs.txt").read().strip()
reference2 = open("p8s3.txt")
reference3 = open("p8s4.txt")
reference4 = open("p9s3.txt")
reference5 = open("p9s4.txt")

fout1 = open("p8s3_new.txt", "w+")
fout2 = open("p8s4_new.txt", "w+")
fout3 = open("p9s3_new.txt", "w+")
fout4 = open("p9s4_new.txt", "w+")

delete_list = ["start", "psup", "p", "m", "[", "]", "\n"]

for line in reference2:
    for word in delete_list:
        line = line.replace(word, "")
    fout1.write(line)
    fout1.write("\n")
reference2.close()
fout1.close()

for line in reference3:
    for word in delete_list:
        line = line.replace(word, "")
    fout2.write(line)
    fout2.write("\n")
reference3.close()
fout2.close()

for line in reference4:
    for word in delete_list:
        line = line.replace(word, "")
    fout3.write(line)
    fout3.write("\n")
reference4.close()
fout3.close()

for line in reference5:
    for word in delete_list:
        line = line.replace(word, "")
    fout4.write(line)
    fout4.write("\n")
reference5.close()
fout4.close()

splitReference1 = reference1.split("\n")

p2s8 = open("p8s3_new.txt").read().strip()
splitReference2 = p2s8.split("\n")

p7s3 = open("p8s4_new.txt").read().strip()
splitReference3 = p7s3.split("\n")

p4s5 = open("p9s3_new.txt").read().strip()
splitReference4 = p4s5.split("\n")

p9s4 = open("p9s4_new.txt").read().strip()
splitReference5 = p9s4.split("\n")

count1 = 0
count2 = 0
count3 = 0
count4 = 0

p2s8_period = 8
p7s3_period = 8
p4s5_period = 9
p9s4_period = 9

p2s8_support = 3
p7s3_support = 4
p4s5_support = 3
p9s4_support = 4

p2s8_start = []
p7s3_start = []
p4s5_start = []
p9s4_start = []

for fileLine in splitReference2:
    splitReference2_new = fileLine.split(" ")
    str_list = list(filter(None, splitReference2_new))
    convert2int = list(map(int, str_list))
    p2s8_start.append(convert2int[0])
    filt = list(filter(lambda x: x > 588, convert2int))
    convert2str = list(map(str, filt))
    p2s8_end = (p2s8_period * p2s8_support) + p2s8_start[-1]

    for referenceLine in splitReference1[p2s8_start[-1]-1:p2s8_end]:
        referenceCells = referenceLine.split()
        if (set(convert2str).issubset(set(referenceCells))):
            count1 = count1 + 1
        else:
            count1 = count1 + 0

    out = open('p8s3_purity.txt', 'a')
    try:
        out.write(str(p2s8_support/count1) + "\n")
    except ZeroDivisionError:
        out.write("Cant divide by Zero" + "\n")
    count1 = 0

for fileLine in splitReference3:
    splitReference3_new = fileLine.split(" ")
    str_list = list(filter(None, splitReference3_new))
    convert2int = list(map(int, str_list))
    p7s3_start.append(convert2int[0])
    filt = list(filter(lambda x: x > 588, convert2int))
    convert2str = list(map(str, filt))
    p7s3_end = (p7s3_period * p7s3_support) + p7s3_start[-1]

    for referenceLine in splitReference1[p7s3_start[-1]-1:p7s3_end]:
        referenceCells = referenceLine.split()
        if (set(convert2str).issubset(set(referenceCells))):
            count2 = count2 + 1
        else:
            count2 = count2 + 0

    out = open('p8s4_purity.txt', 'a')
    try:
        out.write(str(p7s3_support/count2) + "\n")
    except ZeroDivisionError:
        out.write("Cant divide by Zero" + "\n")
    count2 = 0

for fileLine in splitReference4:
    splitReference4_new = fileLine.split(" ")
    str_list = list(filter(None, splitReference4_new))
    convert2int = list(map(int, str_list))
    p4s5_start.append(convert2int[0])
    filt = list(filter(lambda x: x > 588, convert2int))
    convert2str = list(map(str, filt))
    p4s5_end = (p4s5_period * p4s5_support) + p4s5_start[-1]

    for referenceLine in splitReference1[p4s5_start[-1]-1:p4s5_end]:
        referenceCells = referenceLine.split()
        if (set(convert2str).issubset(set(referenceCells))):
            count3 = count3 + 1
        else:
            count3 = count3 + 0

    out = open('p9s3_purity.txt', 'a')
    try:
        out.write(str(p4s5_support/count3) + "\n")
    except ZeroDivisionError:
        out.write("Cant divide by Zero" + "\n")
    count3 = 0

for fileLine in splitReference5:
    splitReference5_new = fileLine.split(" ")
    str_list = list(filter(None, splitReference5_new))
    convert2int = list(map(int, str_list))
    p9s4_start.append(convert2int[0])
    filt = list(filter(lambda x: x > 588, convert2int))
    convert2str = list(map(str, filt))
    p9s4_end = (p9s4_period * p9s4_support) + p9s4_start[-1]

    for referenceLine in splitReference1[p9s4_start[-1]-1:p9s4_end]:
        referenceCells = referenceLine.split()
        if (set(convert2str).issubset(set(referenceCells))):
            count4 = count4 + 1
        else:
            count4 = count4 + 0

    out = open('p9s4_purity.txt', 'a')
    try:
        out.write(str(p9s4_support/count4) + "\n")
    except ZeroDivisionError:
        out.write("Cant divide by Zero" + "\n")
    count4 = 0