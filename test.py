import numpy as np



a = np.array([0,1,2,3,4,5])
b = np.array([5,4,3,2,1,0])

ss = []
ss.append (a)
ss.append (b)

b[-1] = 111

ss.pop(-1)
ss.append (b)

print('a', a)
print('b', b)
print('ss', ss)