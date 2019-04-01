import inspect


class Context():
    context = None
    def __init__(self):
        if Context.context == None:
            Context.context = {"byQualifier":{},"byType":{},"definitions":{}}

    def addBeanDefinition(self,beanObj):
        Context.context.get("definitions").update({
            beanObj.__bean_name__ : beanObj
        })

    def getClassByName(self,name):
        return Context.context.get("byQualifier").get(name,None)

    def getClassByType(self,type):
        return Context.context.get("byType").get(type,None)

    def resolve(self,name,type):
        inst = self.getClassByName(name)
        if inst != None:
            return inst
        else:
            inst = self.getClassByType(type)
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
            Context.context.get("byType").update({
                typeName : inst
            })

    def createBean(self,beanName,beanObj):
        argspec = inspect.getfullargspec(beanObj.__init__)[0]
        args = [];
        for i in range(len(argspec)-1):
            args.append(None)
        inst = beanObj(*args)

        self.registerByName(beanName,inst)
        self.registerByType(inst)


    def initialize(self):
        definitions = Context.context.get("definitions")
        for beanName in definitions:
            self.createBean(beanName,definitions[beanName])

context = Context()
