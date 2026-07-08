import pickle
from abc import ABC

class DAO(ABC):
    def __init__(self, datasource=""):
        self.__datasource = datasource
        self.__cache = {}
        self.load()

    def load(self):
        try:
            with open(self.__datasource, 'rb') as f:
                self.__cache = pickle.load(f)
        except (FileNotFoundError, EOFError):
            self.__cache = {}
            self.dump()

    def dump(self):
        with open(self.__datasource, 'wb') as f:
            pickle.dump(self.__cache, f)

    def add(self, key, obj):
        self.__cache[key] = obj
        self.dump()

    def get(self, key):
        return self.__cache.get(key)

    def remove(self, key):
        if key in self.__cache:
            self.__cache.pop(key)
            self.dump()

    def get_all(self):
        return list(self.__cache.values())

    def update(self):
        self.dump()