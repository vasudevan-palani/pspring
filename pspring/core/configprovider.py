from abc import abstractmethod

class ConfigurationProvider():
    def __init__(self):
        pass

    @abstractmethod
    def getProperty(self,propertyName):
        return None

    @abstractmethod
    def subscribe(self,callback):
        pass
