from telas.tela_abstrata import TelaAbstrata


class TelaPaciente(TelaAbstrata):
  def tela_opcoes(self):
    print("-------- PACIENTES ----------")
    print("Escolha a opção")
    print("1 - Incluir Paciente")
    print("2 - Alterar Paciente")
    print("3 - Listar Pacientes")
    print("4 - Excluir Paciente")
    print("0 - Retornar")
    return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

  def pega_dados_paciente(self, cpf_disponivel=None):
    print("-------- DADOS PACIENTE ----------")
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

    data_nascimento = self.le_data_nascimento_paciente()
    return {
      "nome": nome,
      "celular": celular,
      "cpf": cpf,
      "data_nascimento": data_nascimento,
    }

  def mostra_paciente(self, dados_paciente):
    print("NOME: ", dados_paciente["nome"])
    print("CELULAR: ", dados_paciente["celular"])
    print("CPF: ", dados_paciente["cpf"])
    print("DATA DE NASCIMENTO: ", dados_paciente["data_nascimento"])
    print("\n")

  def seleciona_paciente(self):
    return self.le_texto("CPF do paciente que deseja selecionar: ")
