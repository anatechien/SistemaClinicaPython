from datetime import date

from models.pessoa import Pessoa

class Paciente(Pessoa):
    def __init__(self, nome: str, celular: str, cpf:  str, data_nascimento: date):
        super().__init__(nome, celular, cpf)
        self.__validar_maior_idade(data_nascimento)
        self.__data_nascimento = data_nascimento

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    def idade(self):
        return self.idade_em(date.today())

    def idade_em(self, data: date):
        idade = data.year - self.__data_nascimento.year
        if (data.month, data.day) < (self.__data_nascimento.month, self.__data_nascimento.day):
            idade -= 1
        return idade

    def __validar_maior_idade(self, data_nascimento: date):
        idade = date.today().year - data_nascimento.year
        if (date.today().month, date.today().day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1
        if idade < 18:
            raise ValueError("Paciente deve ser maior de 18 anos para ser cadastrado.")

    def atualizar(self, nome: str, celular: str, data_nascimento: date):
        self.__validar_maior_idade(data_nascimento)
        self.nome = nome
        self.celular = celular
        self.__data_nascimento = data_nascimento
