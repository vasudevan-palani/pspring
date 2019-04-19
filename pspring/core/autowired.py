from .context import ApplicationContext
import inspect

class Autowired():

    def __init__(self,**kargs):
        self.config = kargs

    def __call__(self,beanMethod):
        def constructor(*args, **kargs):
            spec = inspect.getfullargspec(beanMethod)
            argsList = spec[0]
            annotations = spec[6]
            realargs=[args[0]]
            for arg in argsList:
                if arg == 'self' :
                    continue
                if self.config.get(arg) != None:
                    bean = ApplicationContext.resolve(self.config.get(arg),annotations.get(arg))
                else:
                    bean = ApplicationContext.resolve(arg,annotations.get(arg))
                realargs.append(bean)
            return beanMethod(*realargs,**kargs)
        return constructor
