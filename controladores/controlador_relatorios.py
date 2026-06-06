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
      0: self.retornar,
    }

    while True:
      lista_opcoes[self.__tela_relatorio.tela_opcoes()]()
