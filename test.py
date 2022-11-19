li = [0,1,2,3]
itli = iter(li)

print('li')
print('yes __iter__' if '__iter__' in li.__dir__() else 'no __iter__')
print('yes __next__' if '__next__' in li.__dir__() else 'no __next__')

print('itli')
print('yes __iter__' if '__iter__' in itli.__dir__() else 'no __iter__')
print('yes __next__' if '__next__' in itli.__dir__() else 'no __next__')

s = 'qwerty'
s = iter(s)
print('s')
print('yes __iter__' if '__iter__' in s.__dir__() else 'no __iter__')
print('yes __next__' if '__next__' in s.__dir__() else 'no __next__')

print(next(s))
print(next(s))
