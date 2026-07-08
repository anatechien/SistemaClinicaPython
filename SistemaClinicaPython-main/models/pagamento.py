from datetime import date

from exceptions.pagamento_dados_invalidos_exception import PagamentoDadosInvalidosException
from exceptions.pagamento_fora_do_prazo_exception import PagamentoForaDoPrazoException
from models.atendimento import Atendimento
from models.paciente import Paciente


def validar_data_pagamento(data_pagamento: date, atendimento: Atendimento):
  if data_pagamento > atendimento.data:
    raise PagamentoForaDoPrazoException(
      data_pagamento.strftime("%d/%m/%Y"),
      atendimento.data.strftime("%d/%m/%Y"),
    )


class Pagamento:
  def __init__(self, data: date, atendimento: Atendimento, paciente: Paciente, valor: float):
    if valor <= 0:
      raise ValueError("O valor do pagamento deve ser maior que zero.")
    validar_data_pagamento(data, atendimento)

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

  def _validar_atualizacao(self, data: date, valor: float):
    if valor <= 0:
      raise ValueError("O valor do pagamento deve ser maior que zero.")
    validar_data_pagamento(data, self.__atendimento)
    total_sem_este = self.__atendimento.total_pago() - self.__valor
    if total_sem_este + valor > self.__atendimento.valor:
      raise ValueError("Valor do pagamento excede o valor restante do atendimento.")

  def atualizar(self, data: date, valor: float):
    self._validar_atualizacao(data, valor)
    self.__data = data
    self.__valor = valor


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
    if not cpf_pagador.strip():
      raise PagamentoDadosInvalidosException("CPF do pagador é obrigatório para pagamento via PIX.")
    super().__init__(data, atendimento, paciente, valor)
    self.__cpf_pagador = cpf_pagador.strip()

  @property
  def cpf_pagador(self):
    return self.__cpf_pagador

  def atualizar(self, data: date, valor: float, cpf_pagador: str):
    if not cpf_pagador.strip():
      raise PagamentoDadosInvalidosException("CPF do pagador é obrigatório para pagamento via PIX.")
    super().atualizar(data, valor)
    self.__cpf_pagador = cpf_pagador.strip()

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
    if not numero_cartao.strip():
      raise PagamentoDadosInvalidosException(
        "Número do cartão é obrigatório para pagamento com cartão de crédito."
      )
    if not bandeira.strip():
      raise PagamentoDadosInvalidosException(
        "Bandeira é obrigatória para pagamento com cartão de crédito."
      )
    super().__init__(data, atendimento, paciente, valor)
    self.__numero_cartao = numero_cartao.strip()
    self.__bandeira = bandeira.strip()

  @property
  def numero_cartao(self):
    return self.__numero_cartao

  @property
  def bandeira(self):
    return self.__bandeira

  def atualizar(self, data: date, valor: float, numero_cartao: str, bandeira: str):
    if not numero_cartao.strip():
      raise PagamentoDadosInvalidosException(
        "Número do cartão é obrigatório para pagamento com cartão de crédito."
      )
    if not bandeira.strip():
      raise PagamentoDadosInvalidosException(
        "Bandeira é obrigatória para pagamento com cartão de crédito."
      )
    super().atualizar(data, valor)
    self.__numero_cartao = numero_cartao.strip()
    self.__bandeira = bandeira.strip()

  def __str__(self):
    return (
      f"Pagamento com cartão {self.bandeira} "
      f"(****{self.numero_cartao[-4:]}) de R$ {self.valor:.2f} "
      f"em {self.data.strftime('%d/%m/%Y')}"
    )
