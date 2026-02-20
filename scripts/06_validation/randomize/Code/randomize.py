import numpy as np
import wilcoxon as w
in1 = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
#in2 = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
p = np.array([])
i = 0
while (i<2):
    np.random.shuffle(in1)
    in2 = in1
    print(in2)
    p = np.append(p, w.wilcoxon(in1, in2, 'pratt'))
    i += 1
print(p)
index_min = np.argmin(p)
print(index_min)
"""
print(in1)
np.random.shuffle(in1)
in2 = in1
print(in2)
p = np.append(p,w.wilcoxon(in1,in2,'pratt'))
print(p)
"""

