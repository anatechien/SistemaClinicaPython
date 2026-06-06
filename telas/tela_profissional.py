from telas.tela_abstrata import TelaAbstrata


class TelaProfissional(TelaAbstrata):
  def tela_opcoes(self):
    print("-------- PROFISSIONAIS ----------")
    print("Escolha a opção")
    print("1 - Incluir Profissional")
    print("2 - Alterar Profissional")
    print("3 - Listar Profissionais")
    print("4 - Excluir Profissional")
    print("0 - Retornar")
    return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

  def pega_dados_profissional(self, cpf_disponivel=None):
    print("-------- DADOS PROFISSIONAL ----------")
    nome = self.le_texto("Nome: ")
    celular = self.le_texto("Celular: ")

    if cpf_disponivel is None:
      cpf = self.le_texto("CPF: ")
    else:
      cpf = self.le_texto_validado(
        "CPF: ",
        cpf_disponivel,
        "CPF já cadastrado. Tente novamente.",
      )

    especialidade = self.le_texto("Especialidade: ")
    registro_profissional = self.le_texto("Registro profissional: ")
    return {
      "nome": nome,
      "celular": celular,
      "cpf": cpf,
      "especialidade": especialidade,
      "registro_profissional": registro_profissional,
    }

  def mostra_profissional(self, dados_profissional):
    print("NOME: ", dados_profissional["nome"])
    print("CELULAR: ", dados_profissional["celular"])
    print("CPF: ", dados_profissional["cpf"])
    print("ESPECIALIDADE: ", dados_profissional["especialidade"])
    print("REGISTRO: ", dados_profissional["registro_profissional"])
    print("\n")

  def seleciona_profissional(self):
    return self.le_texto("CPF do profissional que deseja selecionar: ")
