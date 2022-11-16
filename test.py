import numpy as np


rnd = np.random.default_rng()

inpt = np.array([1,1,1,1]).reshape(4,1)
a = rnd.random(size=(2,4))
b = rnd.random(size=(36,2))
c = rnd.integers(low=0, high=1, size=(5,1), endpoint=True)

res = np.dot(a, inpt)
print(res.shape)
res = np.tanh(np.dot(b, res))
print(res.shape)

slic = slice(10, 15)
print(res[slic])

res = res[slic]
print(res.shape)
print('c\n', c, c.shape)
#res1 = np.dot(res.reshape(5,1), c.reshape(1,5))
#print(res1, res1.shape)

res2 = res.reshape(5,1) * c.reshape(5,1)
print(res2, res2.shape)
print(res2.argmax())

