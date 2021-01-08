from .configprovider import ConfigurationProvider
import logging,json
import yaml
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class JsonConfigProvider(ConfigurationProvider):
    def __init__(self,json):
        self.value = json.copy()
        self.subscriptions = []
        self.config={}
        self.refresh()
        self.lastUpdated = int(datetime.now().timestamp())

    def getProperty(self,propertyName):
        # Check for json based keys
        config = self.value
        propertyNames = propertyName.split(".")
        for propertyNameItem in propertyNames:
            if config != None:
                config = config.get(propertyNameItem)

        if config != None:
            return config

        # return default way of property access
        return self.value.get(propertyName)

    def refresh(self):
        pass

    def subscribe(self,callback):
        self.subscriptions.append(callback)

    def publish(self):
        for subscription in self.subscriptions:
            subscription()