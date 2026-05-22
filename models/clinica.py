from datetime import time

class Clinica:
    def __init__(self, nome: str, cidade: str,  descricao: str, horario_abertura: time, horario_fechamento: time):
        self.__nome = nome
        self.__cidade = cidade
        self.__descricao = descricao
        self.__horario_abertura = horario_abertura
        self.__horario_fechamento = horario_fechamento

    @property
    def nome(self):
        return self.__nome

    @property
    def cidade(self):
        return self.__cidade

    @property
    def descricao(self):
        return self.__descricao

    @property
    def horario_abertura(self):
        return self.__horario_abertura

    @property
    def horario_fechamento(self):
        return self.__horario_fechamento
    
    @nome.setter
    def nome(self, nome: str):  
        self.__nome = nome          

    @cidade.setter
    def cidade(self, cidade: str):
        self.__cidade = cidade

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @horario_abertura.setter
    def horario_abertura(self, horario_abertura: time): 
        self.__horario_abertura = horario_abertura

    @horario_fechamento.setter
    def horario_fechamento(self, horario_fechamento: time):
        self.__horario_fechamento = horario_fechamento

    def esta_em_funcionamento(self, horario: time):
        return (self.__horario_abertura <= horario <= self.__horario_fechamento)

    #def esta_em_funcionamento(self, horario_inicio: time, horario_fim: time):
    #    return (self.__horario_abertura <= horario_inicio and horario_fim <= self.__horario_fechamento and horario_inicio < horario_fim)   