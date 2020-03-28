import inspect
import os
from datetime import datetime
from .configprovider import ConfigurationProvider

class _ConfigInstance():
    def __init__(self,name,config,timeout):
        self.name = name
        self.config = config
        config.subscribe(self.callback)
        self.subscriptions = []
        self.timeout = timeout
        self.lastUpdated = int(datetime.now().timestamp())

    def getProperty(self,propertyName,defaultValue=None):
        lastUpdatedSeconds = int(datetime.now().timestamp()) - self.lastUpdated
        if(self.timeout != None and lastUpdatedSeconds > self.timeout):
            self.config.refresh()
            self.lastUpdated = int(datetime.now().timestamp())
        propertyValue = self.config.getProperty(self.name+"."+propertyName)
        if propertyValue == None:
            propertyValue = defaultValue

        return propertyValue

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
    def getConfig(moduleName,timeout=os.environ.get("PSPRING_CONFIG_TIMEOUT",None)):
        return _ConfigInstance(moduleName,Configuration,timeout)

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
    def refresh():
        for bean in Configuration._configProviders:
            bean.refresh()

    @staticmethod
    def initialize(_configProviders):
        Configuration._configProviders = _configProviders
        #_configProviders = ApplicationContext.getClassByType(ConfigurationProvider)
        for bean in _configProviders:
            bean.subscribe(Configuration.callback)
