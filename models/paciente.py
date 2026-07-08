from datetime import date
from exceptions.paciente_menor_idade_exception import PacienteMenorDeIdadeException
from models.pessoa import Pessoa

def calcular_idade(data_nascimento: date, data_referencia: date = None) -> int:
  if data_referencia is None:
    data_referencia = date.today()
  idade = data_referencia.year - data_nascimento.year
  if (data_referencia.month, data_referencia.day) < (data_nascimento.month, data_nascimento.day):
    idade -= 1
  return idade

def validar_maior_idade(data_nascimento: date, data_referencia: date = None, idade_minima: int = 18, possui_responsavel: bool = False):
  if possui_responsavel:
    return
  idade = calcular_idade(data_nascimento, data_referencia)
  if idade < idade_minima:
    raise PacienteMenorDeIdadeException(idade, idade_minima)

class Paciente(Pessoa):
  def __init__(self, nome: str, celular: str, cpf: str, data_nascimento: date, responsavel: str = None):
    super().__init__(nome, celular, cpf)
    self.__data_nascimento = data_nascimento
    self.__responsavel = responsavel
    validar_maior_idade(data_nascimento, possui_responsavel=bool(responsavel))

  @property
  def data_nascimento(self):
    return self.__data_nascimento

  @property
  def responsavel(self):
    return self.__responsavel

  @responsavel.setter
  def responsavel(self, responsavel: str):
    self.__responsavel = responsavel

  def idade(self):
    return self.idade_em(date.today())

  def idade_em(self, data: date):
    return calcular_idade(self.__data_nascimento, data)

  def atualizar(self, nome: str, celular: str, data_nascimento: date, responsavel: str = None):
    self.nome = nome
    self.celular = celular
    self.__data_nascimento = data_nascimento
    self.__responsavel = responsavel
    validar_maior_idade(data_nascimento, possui_responsavel=bool(responsavel))