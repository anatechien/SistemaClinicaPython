import os
import pickle
from abc import ABC

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


class DAO(ABC):
    def __init__(self, datasource=""):
        os.makedirs(_DATA_DIR, exist_ok=True)
        self.__datasource = os.path.join(_DATA_DIR, datasource)
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
