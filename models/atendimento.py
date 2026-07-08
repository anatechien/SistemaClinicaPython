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

    possui_responsavel = bool(getattr(paciente, "responsavel", None))
    validar_maior_idade(paciente.data_nascimento, data, possui_responsavel=possui_responsavel)

    self.__clinica = clinica
    self.__paciente_cpf = paciente.cpf
    self.__profissional_cpf = profissional.cpf
    self.__tipo_nome = tipo_atendimento.nome
    self.__resolver = None
    self.__data = data
    self.__horario_inicio = horario_inicio
    self.__horario_fim = horario_fim
    self.__valor_base = valor
    self.__valor = valor
    self.__procedimentos = []
    self.__pagamentos = []
    clinica.adicionar_atendimento(self)

  def __getstate__(self):
    estado = self.__dict__.copy()
    estado["_Atendimento__resolver"] = None
    return estado

  def __setstate__(self, estado):
    self.__dict__.update(estado)
    self.__resolver = None
    self.migrar_se_necessario()

  def migrar_se_necessario(self):
    if hasattr(self, "_Atendimento__paciente"):
      self.__paciente_cpf = self._Atendimento__paciente.cpf
      del self._Atendimento__paciente
    if hasattr(self, "_Atendimento__profissional"):
      self.__profissional_cpf = self._Atendimento__profissional.cpf
      del self._Atendimento__profissional
    if hasattr(self, "_Atendimento__tipo_atendimento"):
      self.__tipo_nome = self._Atendimento__tipo_atendimento.nome
      del self._Atendimento__tipo_atendimento

    for procedimento in self.__procedimentos:
      procedimento.migrar_se_necessario()
    for pagamento in self.__pagamentos:
      pagamento.migrar_se_necessario()

  def vincular_resolver(self, resolver):
    self.__resolver = resolver
    for procedimento in self.__procedimentos:
      procedimento.vincular_resolver(resolver)
    for pagamento in self.__pagamentos:
      pagamento.vincular_resolver(self)

  def _resolver_ou_erro(self):
    if self.__resolver is None:
      raise ValueError("Resolvedor de referências não vinculado ao atendimento.")
    return self.__resolver

  def __validar_horarios(self, clinica, horario_inicio: time, horario_fim: time):
    if horario_inicio >= horario_fim:
      raise ValueError("O horário de início deve ser anterior ao horário de fim.")
    if not clinica.esta_em_funcionamento(horario_inicio, horario_fim):
      raise ValueError("O horário do atendimento está fora do horário de funcionamento da clínica.")

  @property
  def clinica(self):
    return self.__clinica

  @property
  def paciente_cpf(self):
    return self.__paciente_cpf

  @property
  def profissional_cpf(self):
    return self.__profissional_cpf

  @property
  def tipo_nome(self):
    return self.__tipo_nome

  @property
  def paciente(self):
    return self._resolver_ou_erro().paciente(self.__paciente_cpf)

  @property
  def profissional(self):
    return self._resolver_ou_erro().profissional(self.__profissional_cpf)

  @property
  def tipo_atendimento(self):
    return self._resolver_ou_erro().tipo_atendimento(self.__tipo_nome)

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

  def atualizar_chave_paciente(self, cpf_novo: str):
    self.__paciente_cpf = cpf_novo

  def atualizar_chave_profissional(self, cpf_novo: str):
    self.__profissional_cpf = cpf_novo

  def atualizar_chave_tipo(self, nome_novo: str):
    self.__tipo_nome = nome_novo

  def obter_paciente(self, cpf: str = None):
    cpf = cpf or self.__paciente_cpf
    return self._resolver_ou_erro().paciente(cpf)

  def adicionar_procedimento(self, procedimento):
    procedimento.vincular_resolver(self.__resolver)
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
    cpf_profissional_anterior = procedimento.profissional_cpf
    cpf_profissional = profissional.cpf if hasattr(profissional, "cpf") else profissional
    procedimento.atualizar(descricao, custo, cpf_profissional)
    self.__valor += custo - custo_anterior

    if self.total_pago() > self.__valor:
      procedimento.atualizar(descricao_anterior, custo_anterior, cpf_profissional_anterior)
      self.__valor -= custo - custo_anterior
      raise ValueError(
        "Alteração inviável: o valor total ficaria menor que o total já pago."
      )

  def registrar_pagamento(self, pagamento):
    if pagamento.valor > self.valor_restante():
      raise ValueError("Valor do pagamento excede o valor restante do atendimento.")
    pagamento.vincular_resolver(self)
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

    paciente = self.paciente
    possui_responsavel = bool(getattr(paciente, "responsavel", None))
    validar_maior_idade(paciente.data_nascimento, data, possui_responsavel=possui_responsavel)

    custo_procedimentos = sum(procedimento.custo for procedimento in self.__procedimentos)
    self.__data = data
    self.__horario_inicio = horario_inicio
    self.__horario_fim = horario_fim
    self.__tipo_nome = tipo_atendimento.nome
    self.__valor_base = valor_base
    self.__valor = valor_base + custo_procedimentos

    if self.total_pago() > self.__valor:
      raise ValueError(
        "Valor total após alteração ficou menor que o total já pago. "
        "Exclua pagamentos antes de reduzir o valor."
      )
