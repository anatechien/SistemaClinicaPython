from datetime import date

from pessoa import Pessoa

class Paciente(Pessoa):
    def __init__(self, nome: str, celular: str, cpf:  str, data_nascimento: date):
        super().__init__(nome, celular, cpf)
        self.__data_nascimento = data_nascimento

    @property
    def data_nascimento(self):
        return self.__data_nascimento   
    
    def idade(self):
        data_atual = date.today()
        idade = data_atual.year - self.data_nascimento.year
        if (data_atual.month, data_atual.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1
        return idade
    
    def pode_ser_atendido(self):
        return self.idade() >= 18