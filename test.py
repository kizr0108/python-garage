import os
import vobject
import pprint
import inspect
import re
class TestFunc:
    def __init__(self):
        a = 1

    def deco(self,func):
        def wrap(*args, **kwargs):
            print('Hi')
            return func(*args, **kwargs)
        return wrap

test = TestFunc()
@test.deco
def a():
    print('world!')

a()

a = {'b':1,'c':2}
print(str(a))
print(str(type(1)))
print(type(1))

path = os.path.join(os.path.dirname(__file__),'for_offline\\data\\')
with open(path+'iCloud vCards.vcf', 'r', encoding='UTF-8') as f:
    v = vobject.readOne(f)
    print(v.serialize())
    text = ''
    i = 1
    for x in inspect.getmembers(v, inspect.ismethod):
        if re.match('__',x[0]) != None:
            continue
        text += x[0]
        if i % 4 == 0:
            text += '()\n'
        else:
            text += '(), '
        i += 1
    print(text)
    print(vars(v))
with open(path+'test.vcf', 'w' ,encoding='UTF-8') as f:
    f.write(v.serialize())
