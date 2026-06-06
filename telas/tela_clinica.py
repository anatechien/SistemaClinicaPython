from telas.tela_abstrata import TelaAbstrata


class TelaClinica(TelaAbstrata):
  def tela_opcoes(self):
    print("-------- CLÍNICA ----------")
    print("Escolha a opção")
    print("1 - Incluir Clínica")
    print("2 - Alterar Clínica")
    print("3 - Listar Clínicas")
    print("0 - Retornar")
    return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3])

  def pega_dados_clinica(self, nome_disponivel=None):
    print("-------- DADOS CLÍNICA ----------")

    if nome_disponivel is None:
      nome = self.le_texto("Nome: ")
    else:
      nome = self.le_texto_validado(
        "Nome: ",
        nome_disponivel,
        "Já existe uma clínica com esse nome. Tente novamente.",
      )

    cidade = self.le_texto("Cidade: ")
    descricao = self.le_texto("Descrição: ")
    horario_abertura = self.le_horario("Horário de abertura (HH:MM): ")
    horario_fechamento = self.le_horario_fechamento(horario_abertura)
    return {
      "nome": nome,
      "cidade": cidade,
      "descricao": descricao,
      "horario_abertura": horario_abertura,
      "horario_fechamento": horario_fechamento,
    }

  def mostra_clinica(self, dados_clinica):
    print("CÓDIGO: ", dados_clinica["codigo"])
    print("NOME: ", dados_clinica["nome"])
    print("CIDADE: ", dados_clinica["cidade"])
    print("DESCRIÇÃO: ", dados_clinica["descricao"])
    print("HORÁRIO: ", dados_clinica["horario"])
    print("ATENDIMENTOS: ", dados_clinica["total_atendimentos"])
    print("\n")

  def seleciona_clinica(self, total_clinicas=None):
    if total_clinicas:
      return self.le_num_inteiro(
        "Código da clínica que deseja selecionar: ",
        list(range(1, total_clinicas + 1)),
      )
    return self.le_num_inteiro("Código da clínica que deseja selecionar: ")
