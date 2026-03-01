i = 1
while i <= 66:
    string1 = open('D:\Research\Periodic Subgraph Mining\Preprocessing\Python\Timesteps with Edge Number\\t'+str(i)+'.txt').read().strip()
    out = open('listMinerInputs.txt', 'a')
    words = set()
    result = ''
    for word in string1.split():
        if word not in words:
            result = result + word + ' '
            words.add(word)
    out.write('*'+str(i)+'s ' + result)
    out.write('\n')
    print("file " + str(i) + " complete")
    i += 1
