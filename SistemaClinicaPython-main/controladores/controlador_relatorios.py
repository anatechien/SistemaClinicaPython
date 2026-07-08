from collections import Counter

from telas.tela_relatorio import TelaRelatorio


class ControladorRelatorios:
  def __init__(self, controlador_sistema, tela=None):
    self.__controlador_sistema = controlador_sistema
    self.__tela_relatorio = tela or TelaRelatorio()

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

  def _todos_procedimentos(self):
    procedimentos = []
    for atendimento in self._todos_atendimentos():
      procedimentos.extend(atendimento.procedimentos)
    return procedimentos

  def _dados_procedimento(self, procedimento):
    return {
      "descricao": procedimento.descricao,
      "profissional": procedimento.profissional.nome,
      "custo": f"R$ {procedimento.custo:.2f}",
    }

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

  def relatorio_procedimentos_populares(self):
    procedimentos = self._todos_procedimentos()
    if not procedimentos:
      self.__tela_relatorio.mostra_mensagem("ATENCAO: Nenhum procedimento cadastrado.")
      return

    contagem = Counter(procedimento.descricao for procedimento in procedimentos)
    ranking = contagem.most_common()

    self.__tela_relatorio.mostra_mensagem("--- Procedimentos mais realizados ---")
    for posicao, (descricao, quantidade) in enumerate(ranking, start=1):
      self.__tela_relatorio.mostra_ranking_procedimento({
        "posicao": posicao,
        "descricao": descricao,
        "quantidade": quantidade,
      })

  def relatorio_procedimentos_extremos(self):
    procedimentos = self._todos_procedimentos()
    if not procedimentos:
      self.__tela_relatorio.mostra_mensagem("ATENCAO: Nenhum procedimento cadastrado.")
      return

    custo_maximo = max(procedimento.custo for procedimento in procedimentos)
    custo_minimo = min(procedimento.custo for procedimento in procedimentos)

    self.__tela_relatorio.mostra_mensagem("--- Procedimentos MAIS CAROS ---")
    for procedimento in procedimentos:
      if procedimento.custo == custo_maximo:
        self.__tela_relatorio.mostra_procedimento_relatorio(self._dados_procedimento(procedimento))

    self.__tela_relatorio.mostra_mensagem("--- Procedimentos MAIS BARATOS ---")
    for procedimento in procedimentos:
      if procedimento.custo == custo_minimo:
        self.__tela_relatorio.mostra_procedimento_relatorio(self._dados_procedimento(procedimento))

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
