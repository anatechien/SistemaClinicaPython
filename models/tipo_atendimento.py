class TipoAtendimento:
    def __init__(self, nome: str,  descricao:str = ""):
        self.__nome = nome
        self.__descricao = descricao    

    @property
    def nome(self):
        return self.__nome
    
    @property
    def descricao(self):
        return self.__descricao
    
    @nome.setter
    def nome(self, nome: str):  
        self.__nome = nome

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao
