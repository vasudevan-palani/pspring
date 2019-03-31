from .context import context
import inspect
class Bean():
    def __init__(self,**kargs):
        self.name = kargs.get("name","")

    def __call__(self,classObj):
        name = self.name if self.name != "" else classObj.__name__
        classObj.__bean_name__ = name
        context.addBeanDefinition(classObj)
        return classObj