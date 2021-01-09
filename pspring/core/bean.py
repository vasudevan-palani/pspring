from .context import ApplicationContext
import inspect
class Bean():
    def __init__(self,**kargs):
        self.name = kargs.get("name","")
        self.initargs = kargs.get("args",None)

    def __call__(self,classObj):
        name = self.name if self.name != "" else classObj.__name__
        classObj.__bean_name__ = name
        ApplicationContext.addBeanDefinition(classObj,self.initargs)
        return classObj

    @classmethod
    def register(cls,class_obj,**kargs):
        initargs = kargs.get("args",None)
        name = kargs.get("name","")
        name = name if name != None else class_obj.__name__
        def get_instance():
            return class_obj

        get_instance.__bean_name__ = name

        ApplicationContext.addBeanDefinition(get_instance,initargs)
