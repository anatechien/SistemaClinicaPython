from telas.tela_relatorio import TelaRelatorio


class ControladorRelatorios:
  def __init__(self, controlador_sistema):
    self.__controlador_sistema = controlador_sistema
    self.__tela_relatorio = TelaRelatorio()

  def _dados_atendimento(self, atendimento):
    return {
      "clinica": atendimento.clinica.nome,
      "paciente": atendimento.paciente.nome,
      "profissional": atendimento.profissional.nome,
      "tipo": str(atendimento.tipo_atendimento),
      "data_horario": (
        f"{atendimento.data.strftime('%d/%m/%Y')} "
        f"{atendimento.horario_inicio.strftime('%H:%M')}-"
        f"{atendimento.horario_fim.strftime('%H:%M')}"
      ),
      "valor": f"R$ {atendimento.valor:.2f}",
    }

  def _todos_atendimentos(self):
    atendimentos = []
    for clinica in self.__controlador_sistema.controlador_clinica.clinicas:
      atendimentos.extend(clinica.atendimentos)
    return atendimentos

  def relatorio_clinicas_mais_atendimentos(self):
    clinicas = self.__controlador_sistema.controlador_clinica.clinicas
    if not clinicas:
      self.__tela_relatorio.mostra_mensagem("ATENCAO: Nenhuma clínica cadastrada.")
      return

    ordenadas = sorted(clinicas, key=lambda clinica: len(clinica.atendimentos), reverse=True)
    self.__tela_relatorio.mostra_mensagem("--- Ranking de clínicas por atendimentos ---")
    for posicao, clinica in enumerate(ordenadas, start=1):
      self.__tela_relatorio.mostra_ranking_clinica({
        "posicao": posicao,
        "nome": clinica.nome,
        "cidade": clinica.cidade,
        "total_atendimentos": len(clinica.atendimentos),
      })

  def relatorio_atendimentos_extremos(self):
    atendimentos = self._todos_atendimentos()
    if not atendimentos:
      self.__tela_relatorio.mostra_mensagem("ATENCAO: Nenhum atendimento cadastrado.")
      return

    valor_maximo = max(atendimento.valor for atendimento in atendimentos)
    valor_minimo = min(atendimento.valor for atendimento in atendimentos)

    self.__tela_relatorio.mostra_mensagem("--- Atendimentos MAIS CAROS ---")
    for atendimento in atendimentos:
      if atendimento.valor == valor_maximo:
        self.__tela_relatorio.mostra_atendimento_relatorio(self._dados_atendimento(atendimento))

    self.__tela_relatorio.mostra_mensagem("--- Atendimentos MAIS BARATOS ---")
    for atendimento in atendimentos:
      if atendimento.valor == valor_minimo:
        self.__tela_relatorio.mostra_atendimento_relatorio(self._dados_atendimento(atendimento))

  def retornar(self):
    self.__controlador_sistema.abre_tela()

  def abre_tela(self):
    lista_opcoes = {
      1: self.relatorio_clinicas_mais_atendimentos,
      2: self.relatorio_atendimentos_extremos,
      3: self.relatorio_procedimentos_populares,
      4: self.relatorio_procedimentos_extremos,
      0: self.retornar,
    }

    while True:
      lista_opcoes[self.__tela_relatorio.tela_opcoes()]()

  def relatorio_procedimentos_populares(self):

    atendimentos = self._todos_atendimentos()

    if not atendimentos:
        self.__tela_relatorio.mostra_mensagem(
            "ATENCAO: Nenhum atendimento cadastrado."
        )
        return

    contagem = {}

    for atendimento in atendimentos:

        for procedimento in atendimento.procedimentos:

            nome = procedimento.nome

            if nome not in contagem:
                contagem[nome] = 0

            contagem[nome] += 1

    ranking = sorted(
        contagem.items(),
        key=lambda item: item[1],
        reverse=True
    )

    self.__tela_relatorio.mostra_mensagem(
        "--- Procedimentos mais realizados ---"
    )

    for nome, quantidade in ranking:

        self.__tela_relatorio.mostra_mensagem(
            f"{nome}: {quantidade} realizações"
        )

  def relatorio_procedimentos_extremos(self):

    procedimentos = self._todos_procedimentos()

    if not procedimentos:

        self.__tela_relatorio.mostra_mensagem(
            "ATENCAO: Nenhum procedimento cadastrado."
        )
        return

    valor_maximo = max(
        procedimento.valor
        for procedimento in procedimentos
    )

    valor_minimo = min(
        procedimento.valor
        for procedimento in procedimentos
    )

    self.__tela_relatorio.mostra_mensagem(
        "--- Procedimentos MAIS CAROS ---"
    )

    for procedimento in procedimentos:

        if procedimento.valor == valor_maximo:

            self.__tela_relatorio.mostra_mensagem(
                f"{procedimento.nome} - R$ {procedimento.valor:.2f}"
            )

    self.__tela_relatorio.mostra_mensagem(
        "--- Procedimentos MAIS BARATOS ---"
    )

    for procedimento in procedimentos:

        if procedimento.valor == valor_minimo:

            self.__tela_relatorio.mostra_mensagem(
                f"{procedimento.nome} - R$ {procedimento.valor:.2f}"
            )