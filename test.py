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


try:
    a = 1 / 0
except Exception as e:
    print('wow')
    raise e
