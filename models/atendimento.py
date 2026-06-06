from datetime import date, time

from models.paciente import Paciente
from models.profissional import ProfissionalSaude
from models.tipo_atendimento import TipoAtendimento


class Atendimento:
  def __init__(
    self,
    clinica,
    paciente: Paciente,
    profissional: ProfissionalSaude,
    data: date,
    horario_inicio: time,
    horario_fim: time,
    tipo_atendimento: TipoAtendimento,
    valor: float,
  ):
    if horario_inicio >= horario_fim:
      raise ValueError("O horário de início deve ser anterior ao horário de fim.")
    if not clinica.esta_em_funcionamento(horario_inicio, horario_fim):
      raise ValueError("Atendimento fora do horário de funcionamento da clínica.")
    if valor < 0:
      raise ValueError("O valor do atendimento não pode ser negativo.")

    self.__clinica = clinica
    self.__paciente = paciente
    self.__profissional = profissional
    self.__data = data
    self.__horario_inicio = horario_inicio
    self.__horario_fim = horario_fim
    self.__tipo_atendimento = tipo_atendimento
    self.__valor = valor
    self.__procedimentos = []
    self.__pagamentos = []
    clinica.adicionar_atendimento(self)

  @property
  def clinica(self):
    return self.__clinica

  @property
  def paciente(self):
    return self.__paciente

  @property
  def profissional(self):
    return self.__profissional

  @property
  def data(self):
    return self.__data

  @property
  def horario_inicio(self):
    return self.__horario_inicio

  @property
  def horario_fim(self):
    return self.__horario_fim

  @property
  def tipo_atendimento(self):
    return self.__tipo_atendimento

  @property
  def valor(self):
    return self.__valor

  @valor.setter
  def valor(self, valor: float):
    self.__valor = valor

  def adicionar_procedimento(self, procedimento):
    self.__procedimentos.append(procedimento)
    self.__valor += procedimento.custo

  def registrar_pagamento(self, pagamento):
    if pagamento.valor > self.valor_restante():
      raise ValueError("Valor do pagamento excede o valor restante do atendimento.")
    self.__pagamentos.append(pagamento)

  def total_pago(self):
    return sum(pagamento.valor for pagamento in self.__pagamentos)

  def valor_restante(self):
    return self.__valor - self.total_pago()
