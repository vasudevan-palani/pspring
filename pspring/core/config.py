import inspect
import os
from .configprovider import ConfigurationProvider

class _ConfigInstance():
    def __init__(self,name,config):
        self.name = name
        self.config = config
        config.subscribe(self.callback)
        self.subscriptions = []

    def getProperty(self,propertyName):
        return self.config.getProperty(self.name+"."+propertyName)

    def callback(self):
        for subscription in self.subscriptions:
            subscription()

    def subscribe(self,callback):
        self.subscriptions.append(callback)

class Configuration():
    _defaults = {}
    _config = {}
    _configProviders = []
    _subscriptions = []

    def __init__(self):
        raise Exception("This is a singleton")

    @staticmethod
    def getConfig(moduleName):
        return _ConfigInstance(moduleName,Configuration)

    @staticmethod
    def subscribe(callback):
        Configuration._subscriptions.append(callback)

    @staticmethod
    def callback():
        for subscription in Configuration._subscriptions:
            subscription()

    @staticmethod
    def defaults(propertyMap):
        Configuration._defaults.update(propertyMap)

    @staticmethod
    def getProperty(propertyName):
        propertyScopeArray = propertyName.split(".")
        propertyScopes = []

        configProperty = propertyScopeArray.pop()
        propertyScopes.append(configProperty)
        fullPropertyScope=""

        for propertyScope in propertyScopeArray:
            fullPropertyScope = fullPropertyScope+propertyScope + "."
            propertyScopes.append(fullPropertyScope+configProperty)

        for derivedPropertyName in propertyScopes:
            if os.environ.get(derivedPropertyName) != None:
                return os.environ.get(derivedPropertyName)
            else:
                for bean in Configuration._configProviders:
                    propertyValue = bean.getProperty(derivedPropertyName)
                    if propertyValue != None:
                        return propertyValue

            if Configuration._defaults.get(derivedPropertyName) != None:
                return Configuration._defaults.get(derivedPropertyName)

        return None

    @staticmethod
    def clear():
        return Configuration._config.clear()


    @staticmethod
    def initialize(_configProviders):
        Configuration._configProviders = _configProviders
        #_configProviders = ApplicationContext.getClassByType(ConfigurationProvider)
        for bean in _configProviders:
            bean.subscribe(Configuration.callback)
