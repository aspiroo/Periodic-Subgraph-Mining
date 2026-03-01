i = 1
while i < 7:
    f = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\\Nets_Tensor\Journal_comparison_v2\\file"+str(i)+".txt").read().strip()
    s1 = f.split(']')[0]
    s2 = s1.split('[')[1]
    delete_list = ","
    o = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\\Nets_Tensor\Journal_comparison_v2\out\\file"+str(i)+".txt","w")
    line = s2.replace(delete_list, "")
    list = line.split(" ")
    for word in list:
        o.write(word+"\n")
    print("file " + str(i) + " complete")
    i = i+1