from pathlib import Path

# Clear output file first
out_file = Path('data/processed/listMinerInputs.txt')
if out_file.exists():
    out_file.unlink()
print("Cleared listMinerInputs.txt")

import re
import os

i = 1
while i <= 30:
    string1 = open('data/processed/timesteps_with_edge_number/t'+str(i)+'.txt').read().strip()
    out = open('data/processed/listMinerInputs.txt', 'a')
    words = set()
    result = []
    for word in string1.split():
        if word not in words:
            result.append(word)
            words.add(word)
    out.write('*'+str(i)+'s ' + ' '.join(result))
    out.write('\n')
    print("file " + str(i) + " complete")
    i += 1