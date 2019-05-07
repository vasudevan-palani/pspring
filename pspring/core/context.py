import inspect, types

from .config import Configuration

class Context():
    context = None
    def __init__(self):
        if Context.context == None:
            Context.context = {"byQualifier":{},"byType":{},"definitions":{}}

    def clear(self):
        Context.context.clear()
        Context.context = {"byQualifier":{},"byType":{},"definitions":{}}

    def addBeanDefinition(self,beanObj,args=None):
        Context.context.get("definitions").update({
            beanObj.__bean_name__ : (beanObj,args)
        })

    def getClassByName(self,name):
        return Context.context.get("byQualifier").get(name,None)

    def getClassByType(self,type):
        return Context.context.get("byType").get(type,None)

    def getClassThatDefinedMethod(self,meth):
        if inspect.ismethod(meth):
            for cls in inspect.getmro(meth.__self__.__class__):
               if cls.__dict__.get(meth.__name__) is meth:
                    return cls
            meth = meth.__func__  # fallback to __qualname__ parsing
        if inspect.isfunction(meth):
            cls = getattr(inspect.getmodule(meth),
                          meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
            if isinstance(cls, type):
                return cls
        return getattr(meth, '__objclass__', None) 

    def resolve(self,name,type):
        inst = self.getClassByName(name)
        if inst != None:
            return inst
        else:
            instArray = self.getClassByType(type)
            if instArray!=None and len(instArray) > 1:
                raise Exception("More than one instance found for type " +str(type))
            else:
                inst = instArray[0]
            if inst == None and Context.context.get("definitions").get(name,None) != None:
                return self.createBean(name,Context.context.get("definitions").get(name))
            else:
                return inst

    def registerByName(self,name,inst):
        Context.context.get("byQualifier").update({
            name : inst
        })

    def registerByType(self,inst):
        typeList = inspect.getmro(type(inst))
        for typeName in typeList:
            if typeName == type(object()):
                continue

            if Context.context.get("byType").get(typeName,None) == None:
                Context.context.get("byType")[typeName]=[]

            Context.context.get("byType")[typeName].append(inst)

    def createBeanFromMethod(self,beanClass,beanArgs):
        argspec = inspect.getfullargspec(beanClass)[0]
        args = [];
        for i in range(len(argspec)):
            #Skip the self args for methods bound to class
            #
            if(argspec[i]=="self"):
                args.append(self.getClassThatDefinedMethod(beanClass)())

            #Check if the args is provided
            #
            elif beanArgs!=None and beanArgs.get(argspec[i]) != None:
                args.append(beanArgs.get(argspec[i]))

            #Default args
            else:
                args.append(None)

        #Create the instance of the bean
        #
        inst = beanClass(*args)

        return inst

    def createBeanFromClass(self,beanClass,beanArgs):
        argspec = inspect.getfullargspec(beanClass.__init__)[0]
        args = [];
        for i in range(len(argspec)):
            #Skip the self args for methods bound to class
            #
            if(argspec[i]=="self"):
                continue

            #Check if the args is provided
            #
            if beanArgs.get(argspec[i]) != None:
                args.append(beanArgs.get(argspec[i]))

            #Default args
            else:
                args.append(None)

        #Create the instance of the bean
        #
        inst = beanClass(*args)

        return inst

    def createBean(self,beanName,beanObj):
        beanClass = beanObj[0]
        beanArgs = beanObj[1]
        inst = None
        if type(beanClass) == types.FunctionType:
            inst = self.createBeanFromMethod(beanClass,beanArgs)
        else:
            inst = self.createBeanFromClass(beanClass,beanArgs)
        
        if (inst != None):
            self.registerByName(beanName,inst)
            self.registerByType(inst)


    def initialize(self):
        definitions = Context.context.get("definitions")
        for beanName in definitions:
            self.createBean(beanName,definitions[beanName])

ApplicationContext = Context()
