from abc import abstractmethod

class CacheProvider():
    def __init__(self):
        raise NotImplementedError()

    @abstractmethod
    def set(self,key,data):
        pass

    @abstractmethod
    def get(self,key):
        pass
