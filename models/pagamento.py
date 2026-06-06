from datetime import date

from models.atendimento import Atendimento
from models.paciente import Paciente


class Pagamento:
  def __init__(self, data: date, atendimento: Atendimento, paciente: Paciente, valor: float):
    if valor <= 0:
      raise ValueError("O valor do pagamento deve ser maior que zero.")

    self.__data = data
    self.__atendimento = atendimento
    self.__paciente = paciente
    self.__valor = valor
    atendimento.registrar_pagamento(self)

  @property
  def data(self):
    return self.__data

  @property
  def atendimento(self):
    return self.__atendimento

  @property
  def paciente(self):
    return self.__paciente

  @property
  def valor(self):
    return self.__valor


class PagamentoDinheiro(Pagamento):
  def __str__(self):
    return f"Pagamento em dinheiro de R$ {self.valor:.2f} em {self.data.strftime('%d/%m/%Y')}"


class PagamentoPix(Pagamento):
  def __init__(
    self,
    data: date,
    atendimento: Atendimento,
    paciente: Paciente,
    valor: float,
    cpf_pagador: str,
  ):
    super().__init__(data, atendimento, paciente, valor)
    self.__cpf_pagador = cpf_pagador

  @property
  def cpf_pagador(self):
    return self.__cpf_pagador

  def __str__(self):
    return (
      f"Pagamento via Pix de R$ {self.valor:.2f} "
      f"(CPF pagador: {self.cpf_pagador}) em {self.data.strftime('%d/%m/%Y')}"
    )


class PagamentoCartaoCredito(Pagamento):
  def __init__(
    self,
    data: date,
    atendimento: Atendimento,
    paciente: Paciente,
    valor: float,
    numero_cartao: str,
    bandeira: str,
  ):
    super().__init__(data, atendimento, paciente, valor)
    self.__numero_cartao = numero_cartao
    self.__bandeira = bandeira

  @property
  def numero_cartao(self):
    return self.__numero_cartao

  @property
  def bandeira(self):
    return self.__bandeira

  def __str__(self):
    return (
      f"Pagamento com cartão {self.bandeira} "
      f"(****{self.numero_cartao[-4:]}) de R$ {self.valor:.2f} "
      f"em {self.data.strftime('%d/%m/%Y')}"
    )
