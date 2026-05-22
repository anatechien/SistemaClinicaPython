class Procedimento:
    def __init__(self, nome:str, valor:float, descricao: str):
        self.__nome = nome
        self.__valor = valor
        self.__descricao = descricao


    @property
    def nome(self):
        return self.__nome
    
    @property
    def valor(self):
        return self.__valor
    
    @property
    def descricao(self):
        return self.__descricao
    
    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @valor.setter
    def valor(self, valor: float):
        self.__valor = valor

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao