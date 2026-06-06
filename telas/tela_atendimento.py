from telas.tela_abstrata import TelaAbstrata


class TelaAtendimento(TelaAbstrata):
  def tela_opcoes(self):
    print("-------- ATENDIMENTOS ----------")
    print("Escolha a opção")
    print("1 - Incluir Atendimento")
    print("2 - Listar Atendimentos")
    print("3 - Excluir Atendimento")
    print("4 - Adicionar Procedimento")
    print("5 - Registrar Pagamento")
    print("0 - Retornar")
    return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4, 5])

  def pega_dados_atendimento(
    self,
    paciente_existe=None,
    profissional_existe=None,
    tipo_existe=None,
    validar_horario_clinica=None,
  ):
    print("-------- DADOS ATENDIMENTO ----------")

    if paciente_existe is None:
      cpf_paciente = self.le_texto("CPF do paciente: ")
    else:
      cpf_paciente = self.le_texto_validado(
        "CPF do paciente: ",
        paciente_existe,
        "Paciente não encontrado. Tente novamente.",
      )

    if profissional_existe is None:
      cpf_profissional = self.le_texto("CPF do profissional: ")
    else:
      cpf_profissional = self.le_texto_validado(
        "CPF do profissional: ",
        profissional_existe,
        "Profissional não encontrado. Tente novamente.",
      )

    if tipo_existe is None:
      nome_tipo = self.le_texto("Nome do tipo de atendimento: ")
    else:
      nome_tipo = self.le_texto_validado(
        "Nome do tipo de atendimento: ",
        tipo_existe,
        "Tipo de atendimento não encontrado. Tente novamente.",
      )

    data = self.le_data("Data do atendimento (DD/MM/AAAA): ")
    horario_inicio, horario_fim = self.le_horarios_atendimento(validar_horario_clinica)
    valor = self.le_float("Valor base (R$): ", minimo=0)
    return {
      "cpf_paciente": cpf_paciente,
      "cpf_profissional": cpf_profissional,
      "nome_tipo": nome_tipo,
      "data": data,
      "horario_inicio": horario_inicio,
      "horario_fim": horario_fim,
      "valor": valor,
    }

  def pega_dados_procedimento(self, profissional_existe=None):
    print("-------- DADOS PROCEDIMENTO ----------")

    if profissional_existe is None:
      cpf_profissional = self.le_texto("CPF do profissional responsável: ")
    else:
      cpf_profissional = self.le_texto_validado(
        "CPF do profissional responsável: ",
        profissional_existe,
        "Profissional não encontrado. Tente novamente.",
      )

    descricao = self.le_texto("Descrição: ")
    custo = self.le_float("Custo (R$): ", minimo=0.01)
    return {
      "cpf_profissional": cpf_profissional,
      "descricao": descricao,
      "custo": custo,
    }

  def pega_dados_pagamento(self, valor_maximo=None):
    print("-------- DADOS PAGAMENTO ----------")
    data = self.le_data("Data do pagamento (DD/MM/AAAA): ")

    if valor_maximo is None:
      valor = self.le_float("Valor pago (R$): ", minimo=0.01)
    else:
      while True:
        valor = self.le_float("Valor pago (R$): ", minimo=0.01)
        if valor <= valor_maximo:
          break
        print(
          f"Valor não pode exceder R$ {valor_maximo:.2f} restantes. Tente novamente."
        )
    print("Modalidade: 1-Dinheiro  2-PIX  3-Cartão de crédito")
    modalidade = str(self.le_num_inteiro("Modalidade: ", [1, 2, 3]))
    cpf_pagador = input("CPF do pagador (PIX, ou vazio): ")
    numero_cartao = input("Número do cartão (cartão, ou vazio): ")
    bandeira = input("Bandeira (cartão, ou vazio): ")
    return {
      "data": data,
      "valor": valor,
      "modalidade": modalidade,
      "cpf_pagador": cpf_pagador,
      "numero_cartao": numero_cartao,
      "bandeira": bandeira,
    }

  def mostra_atendimento(self, dados_atendimento):
    print("CÓDIGO: ", dados_atendimento["codigo"])
    print("CLÍNICA: ", dados_atendimento["clinica"])
    print("PACIENTE: ", dados_atendimento["paciente"])
    print("PROFISSIONAL: ", dados_atendimento["profissional"])
    print("TIPO: ", dados_atendimento["tipo"])
    print("DATA/HORÁRIO: ", dados_atendimento["data_horario"])
    print("VALOR TOTAL: ", dados_atendimento["valor_total"])
    print("TOTAL PAGO: ", dados_atendimento["total_pago"])
    print("VALOR RESTANTE: ", dados_atendimento["valor_restante"])
    print("\n")

  def seleciona_atendimento(self, total_atendimentos):
    return self.le_num_inteiro(
      "Código do atendimento que deseja selecionar: ",
      list(range(1, total_atendimentos + 1)),
    )

  def seleciona_clinica(self, total_clinicas):
    return self.le_num_inteiro(
      "Código da clínica que deseja selecionar: ",
      list(range(1, total_clinicas + 1)),
    )
