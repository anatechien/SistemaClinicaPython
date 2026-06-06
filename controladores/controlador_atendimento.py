from telas.tela_atendimento import TelaAtendimento
from models.atendimento import Atendimento
from models.pagamento import PagamentoCartaoCredito, PagamentoDinheiro, PagamentoPix
from models.procedimento import Procedimento


class ControladorAtendimentos:
  def __init__(self, controlador_sistema):
    self.__controlador_sistema = controlador_sistema
    self.__tela_atendimento = TelaAtendimento()

  def _todos_atendimentos(self):
    atendimentos = []
    for clinica in self.__controlador_sistema.controlador_clinica.clinicas:
      atendimentos.extend(clinica.atendimentos)
    return atendimentos

  def pega_atendimento_por_codigo(self, codigo: int):
    atendimentos = self._todos_atendimentos()
    if 1 <= codigo <= len(atendimentos):
      return atendimentos[codigo - 1]
    return None

  def _dados_atendimento(self, codigo: int, atendimento: Atendimento):
    return {
      "codigo": codigo,
      "clinica": atendimento.clinica.nome,
      "paciente": atendimento.paciente.nome,
      "profissional": atendimento.profissional.nome,
      "tipo": str(atendimento.tipo_atendimento),
      "data_horario": (
        f"{atendimento.data.strftime('%d/%m/%Y')} "
        f"{atendimento.horario_inicio.strftime('%H:%M')}-"
        f"{atendimento.horario_fim.strftime('%H:%M')}"
      ),
      "valor_total": f"R$ {atendimento.valor:.2f}",
      "total_pago": f"R$ {atendimento.total_pago():.2f}",
      "valor_restante": f"R$ {atendimento.valor_restante():.2f}",
    }

  def incluir_atendimento(self):
    clinicas = self.__controlador_sistema.controlador_clinica.clinicas
    if not clinicas:
      self.__tela_atendimento.mostra_mensagem("ATENCAO: Cadastre uma clínica antes de agendar.")
      return

    if not self.__controlador_sistema.controlador_pacientes.pacientes:
      self.__tela_atendimento.mostra_mensagem("ATENCAO: Cadastre pacientes antes de agendar.")
      return

    if not self.__controlador_sistema.controlador_profissionais.profissionais:
      self.__tela_atendimento.mostra_mensagem("ATENCAO: Cadastre profissionais antes de agendar.")
      return

    if not self.__controlador_sistema.controlador_tipos_atendimento.tipos:
      self.__tela_atendimento.mostra_mensagem("ATENCAO: Cadastre tipos de atendimento antes de agendar.")
      return

    self.__controlador_sistema.controlador_clinica.lista_clinicas()
    codigo_clinica = self.__tela_atendimento.seleciona_clinica(len(clinicas))
    clinica = self.__controlador_sistema.controlador_clinica.pega_clinica_por_codigo(codigo_clinica)

    self.__controlador_sistema.controlador_pacientes.lista_pacientes()
    self.__controlador_sistema.controlador_profissionais.lista_profissionais()
    self.__controlador_sistema.controlador_tipos_atendimento.lista_tipos()

    dados = self.__tela_atendimento.pega_dados_atendimento(
      paciente_existe=lambda cpf: (
        self.__controlador_sistema.controlador_pacientes.pega_paciente_por_cpf(cpf) is not None
      ),
      profissional_existe=lambda cpf: (
        self.__controlador_sistema.controlador_profissionais.pega_profissional_por_cpf(cpf) is not None
      ),
      tipo_existe=lambda nome: (
        self.__controlador_sistema.controlador_tipos_atendimento.pega_tipo_por_nome(nome) is not None
      ),
      validar_horario_clinica=lambda inicio, fim: clinica.esta_em_funcionamento(inicio, fim),
    )

    paciente = self.__controlador_sistema.controlador_pacientes.pega_paciente_por_cpf(
      dados["cpf_paciente"]
    )
    profissional = self.__controlador_sistema.controlador_profissionais.pega_profissional_por_cpf(
      dados["cpf_profissional"]
    )
    tipo = self.__controlador_sistema.controlador_tipos_atendimento.pega_tipo_por_nome(
      dados["nome_tipo"]
    )

    Atendimento(
      clinica,
      paciente,
      profissional,
      dados["data"],
      dados["horario_inicio"],
      dados["horario_fim"],
      tipo,
      dados["valor"],
    )
    self.__tela_atendimento.mostra_mensagem("Atendimento agendado com sucesso!")
    self.lista_atendimentos()

  def lista_atendimentos(self):
    atendimentos = self._todos_atendimentos()
    if not atendimentos:
      self.__tela_atendimento.mostra_mensagem("ATENCAO: Nenhum atendimento cadastrado.")
      return
    for codigo, atendimento in enumerate(atendimentos, start=1):
      self.__tela_atendimento.mostra_atendimento(self._dados_atendimento(codigo, atendimento))

  def excluir_atendimento(self):
    atendimentos = self._todos_atendimentos()
    if not atendimentos:
      self.__tela_atendimento.mostra_mensagem("ATENCAO: Nenhum atendimento cadastrado.")
      return

    self.lista_atendimentos()
    codigo = self.__tela_atendimento.seleciona_atendimento(len(atendimentos))
    atendimento = self.pega_atendimento_por_codigo(codigo)
    atendimento.clinica.remover_atendimento(atendimento)
    self.lista_atendimentos()

  def adicionar_procedimento(self):
    atendimentos = self._todos_atendimentos()
    if not atendimentos:
      self.__tela_atendimento.mostra_mensagem("ATENCAO: Nenhum atendimento cadastrado.")
      return

    self.lista_atendimentos()
    codigo = self.__tela_atendimento.seleciona_atendimento(len(atendimentos))
    atendimento = self.pega_atendimento_por_codigo(codigo)

    self.__controlador_sistema.controlador_profissionais.lista_profissionais()
    dados = self.__tela_atendimento.pega_dados_procedimento(
      profissional_existe=lambda cpf: (
        self.__controlador_sistema.controlador_profissionais.pega_profissional_por_cpf(cpf) is not None
      )
    )
    profissional = self.__controlador_sistema.controlador_profissionais.pega_profissional_por_cpf(
      dados["cpf_profissional"]
    )

    procedimento = Procedimento(
      dados["descricao"],
      dados["custo"],
      profissional,
    )
    atendimento.adicionar_procedimento(procedimento)
    self.__tela_atendimento.mostra_mensagem(
      f"Procedimento adicionado. Valor total: R$ {atendimento.valor:.2f}"
    )

  def registrar_pagamento(self):
    atendimentos = self._todos_atendimentos()
    if not atendimentos:
      self.__tela_atendimento.mostra_mensagem("ATENCAO: Nenhum atendimento cadastrado.")
      return

    self.lista_atendimentos()
    codigo = self.__tela_atendimento.seleciona_atendimento(len(atendimentos))
    atendimento = self.pega_atendimento_por_codigo(codigo)

    while True:
      dados = self.__tela_atendimento.pega_dados_pagamento(atendimento.valor_restante())
      try:
        if dados["modalidade"] == "1":
          pagamento = PagamentoDinheiro(
            dados["data"], atendimento, atendimento.paciente, dados["valor"]
          )
        elif dados["modalidade"] == "2":
          pagamento = PagamentoPix(
            dados["data"],
            atendimento,
            atendimento.paciente,
            dados["valor"],
            dados["cpf_pagador"],
          )
        elif dados["modalidade"] == "3":
          pagamento = PagamentoCartaoCredito(
            dados["data"],
            atendimento,
            atendimento.paciente,
            dados["valor"],
            dados["numero_cartao"],
            dados["bandeira"],
          )
        else:
          self.__tela_atendimento.mostra_mensagem("ATENCAO: Modalidade inválida.")
          continue

        self.__tela_atendimento.mostra_mensagem(f"Pagamento registrado: {pagamento}")
        self.__tela_atendimento.mostra_mensagem(
          f"Total pago: R$ {atendimento.total_pago():.2f} | "
          f"Restante: R$ {atendimento.valor_restante():.2f}"
        )
        break
      except ValueError as erro:
        self.__tela_atendimento.mostra_mensagem(str(erro))

  def retornar(self):
    self.__controlador_sistema.abre_tela()

  def abre_tela(self):
    lista_opcoes = {
      1: self.incluir_atendimento,
      2: self.lista_atendimentos,
      3: self.excluir_atendimento,
      4: self.adicionar_procedimento,
      5: self.registrar_pagamento,
      0: self.retornar,
    }

    while True:
      lista_opcoes[self.__tela_atendimento.tela_opcoes()]()
