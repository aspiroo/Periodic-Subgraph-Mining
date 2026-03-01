input = open("D:\Studies & Researches\Researches\Periodic Subgraph Mining\\Nets_Tensor\Journal_comparison_v2\minGene9minNet24minD0.8.SUMMERIZED",'r')

i = 1
for line in input:
    print(line)
    out = open('D:\Studies & Researches\Researches\Periodic Subgraph Mining\\Nets_Tensor\Journal_comparison_v2\\file' +str(i)+ '.txt','w')
    out.write(line)
    i = i + 1