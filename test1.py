import inspect
class A():
    def __init__(self,**kargs):
        pass
    def __call__(self,func):
        print(inspect.getfullargspec(func))
        pass

class B():
    @A()
    def __init__(self,a,b:str):
        pass
