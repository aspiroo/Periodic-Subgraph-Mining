i = 3
while i <= 9:
    delete_list = ["start", "psup", "p", "m", "[", "]", "\n"]
    fin = open("D:\Research\Periodic Subgraph Mining\Paper\\filteringNetwork\p1s"+str(i)+".txt")
    fout = open("newfile1th"+str(i)+".txt", "w+")
    for line in fin:
        for word in delete_list:
            line = line.replace(word, "")
        fout.write(line)
    fin.close()
    fout.close()

    reference = open("D:\Research\Periodic Subgraph Mining\Postprocessing\\newfile1th"+str(i)+".txt").read().strip()

    splitReference = reference.split(" ")
    str_list = list(filter(None, splitReference))
    convert2int = list(map(int, str_list))
    filt = list(filter(lambda x: x > 588, convert2int))
    convert2str = list(map(str, filt))


    def remove_duplicates(values):
        output = []
        seen = set()
        for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output


# Remove duplicates from this list.
    result = remove_duplicates(convert2str)

    with open('D:\Research\Periodic Subgraph Mining\listMinerOutputs (with Edges)\\new\p1s'+str(i)+'.txt', 'w') as f:
        for item in result:
            f.write("%s " % item)
    i += 1