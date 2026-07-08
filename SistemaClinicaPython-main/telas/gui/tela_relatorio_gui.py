from telas.gui.tela_abstrata_gui import TelaAbstrataGUI


class TelaRelatorioGUI(TelaAbstrataGUI):
  def tela_opcoes(self):
    return self._menu_botoes(
      "Relatórios",
      [
        (1, "Clínicas com maior número de atendimentos"),
        (2, "Atendimentos mais caros e mais baratos"),
        (3, "Procedimentos mais realizados"),
        (4, "Procedimentos mais caros e mais baratos"),
        (0, "Retornar"),
      ],
      "Relatórios",
      "Relatórios",
    )

  def mostra_mensagem(self, msg):
    if msg.startswith("---"):
      self._init_listagem()
      self._listagem_buffer.append(msg)
      return
    self._exibir_listagem("Relatórios")
    super().mostra_mensagem(msg)

  def mostra_ranking_clinica(self, dados):
    self._init_listagem()
    self._listagem_buffer.append(
      f"{dados['posicao']}º - {dados['nome']} ({dados['cidade']})\n"
      f"   Total de atendimentos: {dados['total_atendimentos']}"
    )

  def mostra_atendimento_relatorio(self, dados):
    self._init_listagem()
    self._listagem_buffer.append(
      f"CLÍNICA: {dados['clinica']}\n"
      f"PACIENTE: {dados['paciente']}\n"
      f"PROFISSIONAL: {dados['profissional']}\n"
      f"TIPO: {dados['tipo']}\n"
      f"DATA/HORÁRIO: {dados['data_horario']}\n"
      f"VALOR: {dados['valor']}"
    )

  def mostra_ranking_procedimento(self, dados):
    self._init_listagem()
    self._listagem_buffer.append(
      f"{dados['posicao']}º - {dados['descricao']}\n"
      f"   Realizações: {dados['quantidade']}"
    )

  def mostra_procedimento_relatorio(self, dados):
    self._init_listagem()
    self._listagem_buffer.append(
      f"DESCRIÇÃO: {dados['descricao']}\n"
      f"PROFISSIONAL: {dados['profissional']}\n"
      f"CUSTO: {dados['custo']}"
    )
