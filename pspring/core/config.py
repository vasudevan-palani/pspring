import inspect

from .context import ApplicationContext
from .configprovider import ConfigurationProvider

class Configuration():
    def __init__(self):
        raise Exception("This is a singleton")

    @staticmethod
    def getProperty(propertyName):
        envProperty = Configuration.getEnvProperty(propertyName)
        if envProperty != None:
            return envProperty

        return Configuration.getFromProvider(propertyName)

    @staticmethod
    def getPropertyFromProvider(propertyName):
        beans = ApplicationContext.getClassByType(ConfigurationProvider)
        for bean in beans:
            if hasattr(bean,"getProperty"):
                propertyValue = bean.getProperty(propertyName)
                if propertyValue != None:
                    return propertyValue
        return None
