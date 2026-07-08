from telas.tela_abstrata import TelaAbstrata


class TelaTipoAtendimento(TelaAbstrata):
  def tela_opcoes(self):
    print("-------- TIPOS DE ATENDIMENTO ----------")
    print("Escolha a opção")
    print("1 - Incluir Tipo")
    print("2 - Alterar Tipo")
    print("3 - Listar Tipos")
    print("4 - Excluir Tipo")
    print("0 - Retornar")
    return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

  def pega_dados_tipo(self, nome_disponivel=None):
    print("-------- DADOS TIPO DE ATENDIMENTO ----------")

    if nome_disponivel is None:
      nome = self.le_texto("Nome: ")
    else:
      nome = self.le_texto_validado(
        "Nome: ",
        nome_disponivel,
        "Já existe um tipo com esse nome. Tente novamente.",
      )

    descricao = self.le_texto("Descrição: ")
    return {"nome": nome, "descricao": descricao}

  def mostra_tipo(self, dados_tipo):
    print("NOME: ", dados_tipo["nome"])
    print("DESCRIÇÃO: ", dados_tipo["descricao"])
    print("\n")

  def seleciona_tipo(self):
    return self.le_texto("Nome do tipo de atendimento que deseja selecionar: ")
