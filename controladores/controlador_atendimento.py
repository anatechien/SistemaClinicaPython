from exceptions.pagamento_dados_invalidos_exception import PagamentoDadosInvalidosException
from exceptions.pagamento_fora_do_prazo_exception import PagamentoForaDoPrazoException
from exceptions.paciente_menor_idade_exception import PacienteMenorDeIdadeException
from telas.tela_atendimento import TelaAtendimento
from models.atendimento import Atendimento
from models.pagamento import (
  Pagamento,
  PagamentoCartaoCredito,
  PagamentoDinheiro,
  PagamentoPix,
)
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

  def _selecionar_atendimento(self):
    atendimentos = self._todos_atendimentos()
    if not atendimentos:
      self.__tela_atendimento.mostra_mensagem("ATENCAO: Nenhum atendimento cadastrado.")
      return None, None
    self.lista_atendimentos()
    codigo = self.__tela_atendimento.seleciona_atendimento(len(atendimentos))
    return codigo, self.pega_atendimento_por_codigo(codigo)

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

  def _dados_procedimento(self, codigo: int, procedimento):
    return {
      "codigo": codigo,
      "descricao": procedimento.descricao,
      "profissional": procedimento.profissional.nome,
      "custo": f"R$ {procedimento.custo:.2f}",
    }

  def _dados_pagamento(self, codigo: int, pagamento):
    return {
      "codigo": codigo,
      "data": pagamento.data.strftime("%d/%m/%Y"),
      "valor": f"R$ {pagamento.valor:.2f}",
      "detalhes": str(pagamento),
    }

  def _selecionar_procedimento(self, atendimento):
    if not atendimento.procedimentos:
      self.__tela_atendimento.mostra_mensagem("ATENCAO: Nenhum procedimento neste atendimento.")
      return None
    self.lista_procedimentos_do_atendimento(atendimento)
    indice = self.__tela_atendimento.seleciona_procedimento(len(atendimento.procedimentos))
    return atendimento.procedimentos[indice - 1]

  def _selecionar_pagamento(self, atendimento):
    if not atendimento.pagamentos:
      self.__tela_atendimento.mostra_mensagem("ATENCAO: Nenhum pagamento neste atendimento.")
      return None
    self.lista_pagamentos_do_atendimento(atendimento)
    indice = self.__tela_atendimento.seleciona_pagamento(len(atendimento.pagamentos))
    return atendimento.pagamentos[indice - 1]

  def _modalidade_pagamento(self, pagamento: Pagamento):
    if isinstance(pagamento, PagamentoPix):
      return "2"
    if isinstance(pagamento, PagamentoCartaoCredito):
      return "3"
    return "1"

  def _atualizar_pagamento(self, pagamento: Pagamento, dados):
    if isinstance(pagamento, PagamentoPix):
      pagamento.atualizar(dados["data"], dados["valor"], dados["cpf_pagador"])
    elif isinstance(pagamento, PagamentoCartaoCredito):
      pagamento.atualizar(
        dados["data"],
        dados["valor"],
        dados["numero_cartao"],
        dados["bandeira"],
      )
    else:
      pagamento.atualizar(dados["data"], dados["valor"])

  def _criar_pagamento(self, dados, atendimento):
    if dados["modalidade"] == "1":
      return PagamentoDinheiro(
        dados["data"], atendimento, atendimento.paciente, dados["valor"]
      )
    if dados["modalidade"] == "2":
      return PagamentoPix(
        dados["data"],
        atendimento,
        atendimento.paciente,
        dados["valor"],
        dados["cpf_pagador"],
      )
    if dados["modalidade"] == "3":
      return PagamentoCartaoCredito(
        dados["data"],
        atendimento,
        atendimento.paciente,
        dados["valor"],
        dados["numero_cartao"],
        dados["bandeira"],
      )
    raise PagamentoDadosInvalidosException("Modalidade de pagamento inválida.")

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

    while True:
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
      try:
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
        break
      except (ValueError, PacienteMenorDeIdadeException) as erro:
        self.__tela_atendimento.mostra_mensagem(f"ATENCAO: {erro}")

  def lista_atendimentos(self):
    atendimentos = self._todos_atendimentos()
    if not atendimentos:
      self.__tela_atendimento.mostra_mensagem("ATENCAO: Nenhum atendimento cadastrado.")
      return
    for codigo, atendimento in enumerate(atendimentos, start=1):
      self.__tela_atendimento.mostra_atendimento(self._dados_atendimento(codigo, atendimento))

  def alterar_atendimento(self):
    codigo, atendimento = self._selecionar_atendimento()
    if atendimento is None:
      return

    clinica = atendimento.clinica
    while True:
      dados = self.__tela_atendimento.pega_dados_alteracao_atendimento(
        tipo_existe=lambda nome: (
          self.__controlador_sistema.controlador_tipos_atendimento.pega_tipo_por_nome(nome) is not None
        ),
        validar_horario_clinica=lambda inicio, fim: clinica.esta_em_funcionamento(inicio, fim),
      )
      try:
        tipo = self.__controlador_sistema.controlador_tipos_atendimento.pega_tipo_por_nome(
          dados["nome_tipo"]
        )
        atendimento.atualizar(
          dados["data"],
          dados["horario_inicio"],
          dados["horario_fim"],
          tipo,
          dados["valor"],
        )
        self.__tela_atendimento.mostra_mensagem("Atendimento alterado com sucesso!")
        self.lista_atendimentos()
        break
      except (ValueError, PacienteMenorDeIdadeException) as erro:
        self.__tela_atendimento.mostra_mensagem(f"ATENCAO: {erro}")

  def excluir_atendimento(self):
    codigo, atendimento = self._selecionar_atendimento()
    if atendimento is None:
      return
    atendimento.clinica.remover_atendimento(atendimento)
    self.lista_atendimentos()

  def adicionar_procedimento(self):
    codigo, atendimento = self._selecionar_atendimento()
    if atendimento is None:
      return

    self.__controlador_sistema.controlador_profissionais.lista_profissionais()
    try:
      dados = self.__tela_atendimento.pega_dados_procedimento(
        profissional_existe=lambda cpf: (
          self.__controlador_sistema.controlador_profissionais.pega_profissional_por_cpf(cpf) is not None
        )
      )
      profissional = self.__controlador_sistema.controlador_profissionais.pega_profissional_por_cpf(
        dados["cpf_profissional"]
      )
      procedimento = Procedimento(dados["descricao"], dados["custo"], profissional)
      atendimento.adicionar_procedimento(procedimento)
      self.__tela_atendimento.mostra_mensagem(
        f"Procedimento adicionado. Valor total: R$ {atendimento.valor:.2f}"
      )
    except ValueError as erro:
      self.__tela_atendimento.mostra_mensagem(f"ATENCAO: {erro}")

  def lista_procedimentos(self):
    codigo, atendimento = self._selecionar_atendimento()
    if atendimento is None:
      return
    if not atendimento.procedimentos:
      self.__tela_atendimento.mostra_mensagem("ATENCAO: Nenhum procedimento neste atendimento.")
      return
    for indice, procedimento in enumerate(atendimento.procedimentos, start=1):
      self.__tela_atendimento.mostra_procedimento(
        self._dados_procedimento(indice, procedimento)
      )

  def alterar_procedimento(self):
    codigo, atendimento = self._selecionar_atendimento()
    if atendimento is None:
      return

    procedimento = self._selecionar_procedimento(atendimento)
    if procedimento is None:
      return

    self.__controlador_sistema.controlador_profissionais.lista_profissionais()
    while True:
      try:
        dados = self.__tela_atendimento.pega_dados_procedimento(
          profissional_existe=lambda cpf: (
            self.__controlador_sistema.controlador_profissionais.pega_profissional_por_cpf(cpf) is not None
          )
        )
        profissional = self.__controlador_sistema.controlador_profissionais.pega_profissional_por_cpf(
          dados["cpf_profissional"]
        )
        atendimento.atualizar_procedimento(
          procedimento,
          dados["descricao"],
          dados["custo"],
          profissional,
        )
        self.__tela_atendimento.mostra_mensagem(
          f"Procedimento alterado. Valor total: R$ {atendimento.valor:.2f}"
        )
        break
      except ValueError as erro:
        self.__tela_atendimento.mostra_mensagem(f"ATENCAO: {erro}")

  def excluir_procedimento(self):
    codigo, atendimento = self._selecionar_atendimento()
    if atendimento is None:
      return

    procedimento = self._selecionar_procedimento(atendimento)
    if procedimento is None:
      return

    if atendimento.total_pago() > atendimento.valor - procedimento.custo:
      self.__tela_atendimento.mostra_mensagem(
        "ATENCAO: Não é possível excluir. O valor pago excederia o total após remoção."
      )
      return

    atendimento.remover_procedimento(procedimento)
    self.__tela_atendimento.mostra_mensagem("Procedimento excluído com sucesso!")

  def lista_procedimentos_do_atendimento(self, atendimento):
    for indice, procedimento in enumerate(atendimento.procedimentos, start=1):
      self.__tela_atendimento.mostra_procedimento(
        self._dados_procedimento(indice, procedimento)
      )

  def registrar_pagamento(self):
    codigo, atendimento = self._selecionar_atendimento()
    if atendimento is None:
      return

    while True:
      dados = self.__tela_atendimento.pega_dados_pagamento(
        atendimento.valor_restante(),
        atendimento.data,
      )
      try:
        pagamento = self._criar_pagamento(dados, atendimento)
        self.__tela_atendimento.mostra_mensagem(f"Pagamento registrado: {pagamento}")
        self.__tela_atendimento.mostra_mensagem(
          f"Total pago: R$ {atendimento.total_pago():.2f} | "
          f"Restante: R$ {atendimento.valor_restante():.2f}"
        )
        break
      except (
        ValueError,
        PagamentoForaDoPrazoException,
        PagamentoDadosInvalidosException,
      ) as erro:
        self.__tela_atendimento.mostra_mensagem(f"ATENCAO: {erro}")

  def lista_pagamentos(self):
    codigo, atendimento = self._selecionar_atendimento()
    if atendimento is None:
      return
    if not atendimento.pagamentos:
      self.__tela_atendimento.mostra_mensagem("ATENCAO: Nenhum pagamento neste atendimento.")
      return
    for indice, pagamento in enumerate(atendimento.pagamentos, start=1):
      self.__tela_atendimento.mostra_pagamento(self._dados_pagamento(indice, pagamento))

  def alterar_pagamento(self):
    codigo, atendimento = self._selecionar_atendimento()
    if atendimento is None:
      return

    pagamento = self._selecionar_pagamento(atendimento)
    if pagamento is None:
      return

    modalidade = self._modalidade_pagamento(pagamento)
    valor_maximo = atendimento.valor_restante() + pagamento.valor

    while True:
      dados = self.__tela_atendimento.pega_dados_alteracao_pagamento(
        modalidade,
        valor_maximo,
        atendimento.data,
      )
      try:
        self._atualizar_pagamento(pagamento, dados)
        self.__tela_atendimento.mostra_mensagem(f"Pagamento alterado: {pagamento}")
        self.__tela_atendimento.mostra_mensagem(
          f"Total pago: R$ {atendimento.total_pago():.2f} | "
          f"Restante: R$ {atendimento.valor_restante():.2f}"
        )
        break
      except (
        ValueError,
        PagamentoForaDoPrazoException,
        PagamentoDadosInvalidosException,
      ) as erro:
        self.__tela_atendimento.mostra_mensagem(f"ATENCAO: {erro}")

  def excluir_pagamento(self):
    codigo, atendimento = self._selecionar_atendimento()
    if atendimento is None:
      return

    pagamento = self._selecionar_pagamento(atendimento)
    if pagamento is None:
      return

    atendimento.remover_pagamento(pagamento)
    self.__tela_atendimento.mostra_mensagem("Pagamento excluído com sucesso!")

  def lista_pagamentos_do_atendimento(self, atendimento):
    for indice, pagamento in enumerate(atendimento.pagamentos, start=1):
      self.__tela_atendimento.mostra_pagamento(self._dados_pagamento(indice, pagamento))

  def retornar(self):
    self.__controlador_sistema.abre_tela()

  def abre_tela(self):
    lista_opcoes = {
      1: self.incluir_atendimento,
      2: self.lista_atendimentos,
      3: self.alterar_atendimento,
      4: self.excluir_atendimento,
      5: self.adicionar_procedimento,
      6: self.lista_procedimentos,
      7: self.alterar_procedimento,
      8: self.excluir_procedimento,
      9: self.registrar_pagamento,
      10: self.lista_pagamentos,
      11: self.alterar_pagamento,
      12: self.excluir_pagamento,
      0: self.retornar,
    }

    while True:
      lista_opcoes[self.__tela_atendimento.tela_opcoes()]()
