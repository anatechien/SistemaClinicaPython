from telas.tela_abstrata import TelaAbstrata





class TelaSistema(TelaAbstrata):

  def tela_opcoes(self):

    print("-------- Sistema de Clínicas ---------")

    print("Escolha sua opção")

    print("1 - Clínica")

    print("2 - Pacientes")

    print("3 - Profissionais")

    print("4 - Tipos de Atendimento")

    print("5 - Atendimentos")

    print("6 - Relatórios")

    print("0 - Finalizar sistema")

    return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4, 5, 6])

