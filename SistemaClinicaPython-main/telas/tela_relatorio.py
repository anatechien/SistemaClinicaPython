from telas.tela_abstrata import TelaAbstrata


class TelaRelatorio(TelaAbstrata):
  def tela_opcoes(self):
    print("-------- RELATÓRIOS ----------")
    print("Escolha a opção")
    print("1 - Clínicas com maior número de atendimentos")
    print("2 - Atendimentos mais caros e mais baratos")
    print("3 - Procedimentos mais realizados")
    print("4 - Procedimentos mais caros e mais baratos")
    print("0 - Retornar")
    return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

  def mostra_ranking_clinica(self, dados):
    print(f"{dados['posicao']}º - {dados['nome']} ({dados['cidade']})")
    print(f"   Total de atendimentos: {dados['total_atendimentos']}")
    print()

  def mostra_atendimento_relatorio(self, dados):
    print(f"CLÍNICA: {dados['clinica']}")
    print(f"PACIENTE: {dados['paciente']}")
    print(f"PROFISSIONAL: {dados['profissional']}")
    print(f"TIPO: {dados['tipo']}")
    print(f"DATA/HORÁRIO: {dados['data_horario']}")
    print(f"VALOR: {dados['valor']}")
    print()

  def mostra_ranking_procedimento(self, dados):
    print(f"{dados['posicao']}º - {dados['descricao']}")
    print(f"   Realizações: {dados['quantidade']}")
    print()

  def mostra_procedimento_relatorio(self, dados):
    print(f"DESCRIÇÃO: {dados['descricao']}")
    print(f"PROFISSIONAL: {dados['profissional']}")
    print(f"CUSTO: {dados['custo']}")
    print()
