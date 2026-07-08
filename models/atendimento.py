from datetime import date, time
from models.paciente import Paciente, validar_maior_idade
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
    self.__validar_horarios(clinica, horario_inicio, horario_fim)
    if valor < 0:
      raise ValueError("O valor do atendimento não pode ser negativo.")
    
    possui_responsavel = bool(getattr(paciente, 'responsavel', None))
    validar_maior_idade(paciente.data_nascimento, data, possui_responsavel=possui_responsavel)

    self.__clinica = clinica
    self.__paciente = paciente
    self.__profissional = profissional
    self.__data = data
    self.__horario_inicio = horario_inicio
    self.__horario_fim = horario_fim
    self.__tipo_atendimento = tipo_atendimento
    self.__valor_base = valor
    self.__valor = valor
    self.__procedimentos = []
    self.__pagamentos = []
    clinica.adicionar_atendimento(self)

  def __validar_horarios(self, clinica, horario_inicio: time, horario_fim: time):
    if horario_inicio >= horario_fim:
      raise ValueError("O horário de início deve ser anterior ao horário de fim.")
    if not clinica.esta_em_funcionamento(horario_inicio, horario_fim):
      raise ValueError("O horário do atendimento está fora do horário de funcionamento da clínica.")

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
  def valor_base(self):
    return self.__valor_base

  @property
  def valor(self):
    return self.__valor

  @property
  def procedimentos(self):
    return self.__procedimentos

  @property
  def pagamentos(self):
    return self.__pagamentos

  def adicionar_procedimento(self, procedimento):
    self.__procedimentos.append(procedimento)
    self.__valor += procedimento.custo

  def remover_procedimento(self, procedimento):
    if self.valor_restante() - procedimento.custo < 0:
      raise ValueError(
        "Remoção inviável: o valor total ficaria menor que o total já pago."
      )
    self.__procedimentos.remove(procedimento)
    self.__valor -= procedimento.custo

  def atualizar_procedimento(self, procedimento, descricao: str, custo: float, profissional):
    if procedimento not in self.__procedimentos:
      raise ValueError("Procedimento não pertence a este atendimento.")

    descricao_anterior = procedimento.descricao
    custo_anterior = procedimento.custo
    profissional_anterior = procedimento.profissional
    procedimento.atualizar(descricao, custo, profissional)
    self.__valor += custo - custo_anterior

    if self.total_pago() > self.__valor:
      procedimento.atualizar(descricao_anterior, custo_anterior, profissional_anterior)
      self.__valor -= custo - custo_anterior
      raise ValueError(
        "Alteração inviável: o valor total ficaria menor que o total já pago."
      )

  def registrar_pagamento(self, pagamento):
    if pagamento.valor > self.valor_restante():
      raise ValueError("Valor do pagamento excede o valor restante do atendimento.")
    self.__pagamentos.append(pagamento)

  def remover_pagamento(self, pagamento):
    self.__pagamentos.remove(pagamento)

  def total_pago(self):
    return sum(pagamento.valor for pagamento in self.__pagamentos)

  def valor_restante(self):
    return self.__valor - self.total_pago()

  def atualizar(
    self,
    data: date,
    horario_inicio: time,
    horario_fim: time,
    tipo_atendimento: TipoAtendimento,
    valor_base: float,
  ):
    self.__validar_horarios(self.__clinica, horario_inicio, horario_fim)
    if valor_base < 0:
      raise ValueError("O valor do atendimento não pode ser negativo.")
    
    possui_responsavel = bool(getattr(self.__paciente, 'responsavel', None))
    validar_maior_idade(self.__paciente.data_nascimento, data, possui_responsavel=possui_responsavel)

    custo_procedimentos = sum(procedimento.custo for procedimento in self.__procedimentos)
    self.__data = data
    self.__horario_inicio = horario_inicio
    self.__horario_fim = horario_fim
    self.__tipo_atendimento = tipo_atendimento
    self.__valor_base = valor_base
    self.__valor = valor_base + custo_procedimentos

    if self.total_pago() > self.__valor:
      raise ValueError(
        "Valor total após alteração ficou menor que o total já pago. "
        "Exclua pagamentos antes de reduzir o valor."
      )
