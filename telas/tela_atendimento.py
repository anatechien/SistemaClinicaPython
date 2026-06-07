from telas.tela_abstrata import TelaAbstrata


class TelaAtendimento(TelaAbstrata):
  def tela_opcoes(self):
    print("-------- ATENDIMENTOS ----------")
    print("Escolha a opção")
    print("1 - Incluir Atendimento")
    print("2 - Listar Atendimentos")
    print("3 - Alterar Atendimento")
    print("4 - Excluir Atendimento")
    print("5 - Adicionar Procedimento")
    print("6 - Listar Procedimentos")
    print("7 - Alterar Procedimento")
    print("8 - Excluir Procedimento")
    print("9 - Registrar Pagamento")
    print("10 - Listar Pagamentos")
    print("11 - Alterar Pagamento")
    print("12 - Excluir Pagamento")
    print("0 - Retornar")
    return self.le_num_inteiro("Escolha a opção: ", list(range(0, 13)))

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

  def pega_dados_alteracao_atendimento(self, tipo_existe=None, validar_horario_clinica=None):
    print("-------- ALTERAR ATENDIMENTO ----------")

    if tipo_existe is None:
      nome_tipo = self.le_texto("Nome do tipo de atendimento: ")
    else:
      nome_tipo = self.le_texto_validado(
        "Nome do tipo de atendimento: ",
        tipo_existe,
        "Tipo de atendimento não encontrado. Tente novamente.",
      )

    data = self.le_data("Nova data do atendimento (DD/MM/AAAA): ")
    horario_inicio, horario_fim = self.le_horarios_atendimento(validar_horario_clinica)
    valor = self.le_float("Novo valor base (R$): ", minimo=0)
    return {
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

  def pega_dados_alteracao_pagamento(self, modalidade: str, valor_maximo=None, data_atendimento=None):
    print("-------- ALTERAR PAGAMENTO ----------")
    nomes = {"1": "Dinheiro", "2": "PIX", "3": "Cartão de crédito"}
    print(f"Modalidade: {nomes[modalidade]} (não pode ser alterada)")
    return self._pega_dados_pagamento_interno(modalidade, valor_maximo, data_atendimento)

  def pega_dados_pagamento(self, valor_maximo=None, data_atendimento=None):
    print("-------- DADOS PAGAMENTO ----------")
    print("Modalidade: 1-Dinheiro  2-PIX  3-Cartão de crédito")
    modalidade = str(self.le_num_inteiro("Modalidade: ", [1, 2, 3]))
    return self._pega_dados_pagamento_interno(modalidade, valor_maximo, data_atendimento)

  def _pega_dados_pagamento_interno(self, modalidade, valor_maximo=None, data_atendimento=None):
    while True:
      data = self.le_data(
        f"Data do pagamento (DD/MM/AAAA, até {data_atendimento.strftime('%d/%m/%Y')}): "
        if data_atendimento
        else "Data do pagamento (DD/MM/AAAA): "
      )
      if data_atendimento and data > data_atendimento:
        print(
          f"Pagamento deve ser realizado até a data do atendimento "
          f"({data_atendimento.strftime('%d/%m/%Y')}). Tente novamente."
        )
        continue
      break

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

    if modalidade == "2":
      cpf_pagador = self.le_texto("CPF do pagador: ")
      numero_cartao = ""
      bandeira = ""
    elif modalidade == "3":
      cpf_pagador = ""
      numero_cartao = self.le_texto("Número do cartão: ")
      bandeira = self.le_texto("Bandeira: ")
    else:
      cpf_pagador = ""
      numero_cartao = ""
      bandeira = ""

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

  def mostra_procedimento(self, dados):
    print(f"CÓDIGO: {dados['codigo']}")
    print(f"DESCRIÇÃO: {dados['descricao']}")
    print(f"PROFISSIONAL: {dados['profissional']}")
    print(f"CUSTO: {dados['custo']}")
    print()

  def mostra_pagamento(self, dados):
    print(f"CÓDIGO: {dados['codigo']}")
    print(f"DATA: {dados['data']}")
    print(f"VALOR: {dados['valor']}")
    print(f"DETALHES: {dados['detalhes']}")
    print()

  def seleciona_atendimento(self, total_atendimentos):
    return self.le_num_inteiro(
      "Código do atendimento que deseja selecionar: ",
      list(range(1, total_atendimentos + 1)),
    )

  def seleciona_procedimento(self, total_procedimentos):
    return self.le_num_inteiro(
      "Código do procedimento que deseja selecionar: ",
      list(range(1, total_procedimentos + 1)),
    )

  def seleciona_pagamento(self, total_pagamentos):
    return self.le_num_inteiro(
      "Código do pagamento que deseja selecionar: ",
      list(range(1, total_pagamentos + 1)),
    )

  def seleciona_clinica(self, total_clinicas):
    return self.le_num_inteiro(
      "Código da clínica que deseja selecionar: ",
      list(range(1, total_clinicas + 1)),
    )
