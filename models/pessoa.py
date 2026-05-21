from abc import ABC

class Pessoa(ABC):
    def __init__(self, nome: str, celular: str, cpf: str):
        self.__nome = nome
        self.__celular = celular
        self.__cpf = cpf

    @property
    def nome(self):
        return self.__nome
    
    @property
    def celular(self):
        return self.__celular 
      
    @property
    def cpf(self):
        return self.__cpf
    
    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @celular.setter
    def celular(self, celular: str):
        self.__celular = celular

    @cpf.setter
    def cpf(self, cpf: str):
        self.__cpf = cpf

        