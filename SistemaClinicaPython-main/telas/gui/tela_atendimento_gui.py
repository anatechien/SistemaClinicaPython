from datetime import datetime

import FreeSimpleGUI as sg

from telas.gui.tela_abstrata_gui import TelaAbstrataGUI


class TelaAtendimentoGUI(TelaAbstrataGUI):
  def tela_opcoes(self):
    return self._menu_botoes(
      "Atendimentos",
      [
        (1, "Cadastro de Atendimento"),
        (2, "Procedimentos"),
        (3, "Pagamentos"),
        (0, "Retornar"),
      ],
      "Atendimentos",
      "Atendimentos",
    )

  def tela_opcoes_cadastro_atendimento(self):
    return self._menu_botoes(
      "Cadastro de Atendimento",
      [
        (1, "Incluir Atendimento"),
        (2, "Listar Atendimentos"),
        (3, "Alterar Atendimento"),
        (4, "Excluir Atendimento"),
        (0, "Retornar"),
      ],
      "Cadastro de Atendimento",
      "Atendimentos",
    )

  def tela_opcoes_procedimento(self):
    return self._menu_botoes(
      "Procedimentos",
      [
        (1, "Adicionar Procedimento"),
        (2, "Listar Procedimentos"),
        (3, "Alterar Procedimento"),
        (4, "Excluir Procedimento"),
        (0, "Retornar"),
      ],
      "Procedimentos",
      "Procedimentos",
    )

  def tela_opcoes_pagamento(self):
    return self._menu_botoes(
      "Pagamentos",
      [
        (1, "Registrar Pagamento"),
        (2, "Listar Pagamentos"),
        (3, "Alterar Pagamento"),
        (4, "Excluir Pagamento"),
        (0, "Retornar"),
      ],
      "Pagamentos",
      "Pagamentos",
    )

  def _validar_horarios(self, inicio_texto, fim_texto, validador=None):
    try:
      horario_inicio = datetime.strptime(inicio_texto, "%H:%M").time()
    except ValueError:
      self._mostra_erro("Horário de início inválido! Use o formato HH:MM.")
      return None

    try:
      horario_fim = datetime.strptime(fim_texto, "%H:%M").time()
    except ValueError:
      self._mostra_erro("Horário de término inválido! Use o formato HH:MM.")
      return None

    if horario_inicio >= horario_fim:
      self._mostra_erro(
        "Horário de término deve ser posterior ao de início. Tente novamente."
      )
      return None

    if validador is not None and not validador(horario_inicio, horario_fim):
      self._mostra_erro(
        "Atendimento fora do horário de funcionamento da clínica. Tente novamente."
      )
      return None

    return horario_inicio, horario_fim

  def pega_dados_atendimento(
    self,
    paciente_existe=None,
    profissional_existe=None,
    tipo_existe=None,
    validar_horario_clinica=None,
  ):
    self._exibir_listagem("Atendimentos")

    layout = [
      [sg.Text("Dados do Atendimento", font=("Helvetica", 14))],
      [sg.Text("CPF do paciente:", size=(24, 1)), sg.Input(key="cpf_paciente", size=(28, 1))],
      [sg.Text("CPF do profissional:", size=(24, 1)), sg.Input(key="cpf_profissional", size=(28, 1))],
      [sg.Text("Tipo de atendimento:", size=(24, 1)), sg.Input(key="nome_tipo", size=(28, 1))],
      [sg.Text("Data (DD/MM/AAAA):", size=(24, 1)), sg.Input(key="data", size=(28, 1))],
      [sg.Text("Início (HH:MM):", size=(24, 1)), sg.Input(key="horario_inicio", size=(28, 1))],
      [sg.Text("Término (HH:MM):", size=(24, 1)), sg.Input(key="horario_fim", size=(28, 1))],
      [sg.Text("Valor base (R$):", size=(24, 1)), sg.Input(key="valor", size=(28, 1))],
      [sg.Button("Salvar", key="Salvar"), sg.Button("Cancelar", key="Cancelar")],
    ]
    window = sg.Window("Cadastro de Atendimento", layout, modal=True)

    while True:
      event, values = window.read()
      if event in self.EVENTOS_FECHAMENTO or event == "Cancelar":
        window.close()
        return None
      if event != "Salvar":
        continue

      cpf_paciente = values["cpf_paciente"].strip()
      cpf_profissional = values["cpf_profissional"].strip()
      nome_tipo = values["nome_tipo"].strip()
      data_texto = values["data"].strip()
      inicio = values["horario_inicio"].strip()
      fim = values["horario_fim"].strip()
      valor_texto = values["valor"].strip().replace(",", ".")

      if not all([cpf_paciente, cpf_profissional, nome_tipo, data_texto, inicio, fim, valor_texto]):
        self._mostra_erro("Todos os campos são obrigatórios.")
        continue

      if paciente_existe is not None and not paciente_existe(cpf_paciente):
        self._mostra_erro("Paciente não encontrado. Tente novamente.")
        continue

      if profissional_existe is not None and not profissional_existe(cpf_profissional):
        self._mostra_erro("Profissional não encontrado. Tente novamente.")
        continue

      if tipo_existe is not None and not tipo_existe(nome_tipo):
        self._mostra_erro("Tipo de atendimento não encontrado. Tente novamente.")
        continue

      try:
        data = datetime.strptime(data_texto, "%d/%m/%Y").date()
      except ValueError:
        self._mostra_erro("Data inválida! Use o formato DD/MM/AAAA.")
        continue

      horarios = self._validar_horarios(inicio, fim, validar_horario_clinica)
      if horarios is None:
        continue
      horario_inicio, horario_fim = horarios

      try:
        valor = float(valor_texto)
        if valor < 0:
          raise ValueError
      except ValueError:
        self._mostra_erro("Valor incorreto! Informe um número válido maior ou igual a 0.")
        continue

      window.close()
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
    self._exibir_listagem("Atendimentos")

    layout = [
      [sg.Text("Alterar Atendimento", font=("Helvetica", 14))],
      [sg.Text("Tipo de atendimento:", size=(24, 1)), sg.Input(key="nome_tipo", size=(28, 1))],
      [sg.Text("Nova data (DD/MM/AAAA):", size=(24, 1)), sg.Input(key="data", size=(28, 1))],
      [sg.Text("Início (HH:MM):", size=(24, 1)), sg.Input(key="horario_inicio", size=(28, 1))],
      [sg.Text("Término (HH:MM):", size=(24, 1)), sg.Input(key="horario_fim", size=(28, 1))],
      [sg.Text("Novo valor base (R$):", size=(24, 1)), sg.Input(key="valor", size=(28, 1))],
      [sg.Button("Salvar", key="Salvar"), sg.Button("Cancelar", key="Cancelar")],
    ]
    window = sg.Window("Alterar Atendimento", layout, modal=True)

    while True:
      event, values = window.read()
      if event in self.EVENTOS_FECHAMENTO or event == "Cancelar":
        window.close()
        return None
      if event != "Salvar":
        continue

      nome_tipo = values["nome_tipo"].strip()
      data_texto = values["data"].strip()
      inicio = values["horario_inicio"].strip()
      fim = values["horario_fim"].strip()
      valor_texto = values["valor"].strip().replace(",", ".")

      if not all([nome_tipo, data_texto, inicio, fim, valor_texto]):
        self._mostra_erro("Todos os campos são obrigatórios.")
        continue

      if tipo_existe is not None and not tipo_existe(nome_tipo):
        self._mostra_erro("Tipo de atendimento não encontrado. Tente novamente.")
        continue

      try:
        data = datetime.strptime(data_texto, "%d/%m/%Y").date()
      except ValueError:
        self._mostra_erro("Data inválida! Use o formato DD/MM/AAAA.")
        continue

      horarios = self._validar_horarios(inicio, fim, validar_horario_clinica)
      if horarios is None:
        continue
      horario_inicio, horario_fim = horarios

      try:
        valor = float(valor_texto)
        if valor < 0:
          raise ValueError
      except ValueError:
        self._mostra_erro("Valor incorreto! Informe um número válido maior ou igual a 0.")
        continue

      window.close()
      return {
        "nome_tipo": nome_tipo,
        "data": data,
        "horario_inicio": horario_inicio,
        "horario_fim": horario_fim,
        "valor": valor,
      }

  def pega_dados_procedimento(self, profissional_existe=None):
    self._exibir_listagem("Procedimentos")

    layout = [
      [sg.Text("Dados do Procedimento", font=("Helvetica", 14))],
      [sg.Text("CPF do profissional:", size=(24, 1)), sg.Input(key="cpf_profissional", size=(28, 1))],
      [sg.Text("Descrição:", size=(24, 1)), sg.Input(key="descricao", size=(28, 1))],
      [sg.Text("Custo (R$):", size=(24, 1)), sg.Input(key="custo", size=(28, 1))],
      [sg.Button("Salvar", key="Salvar"), sg.Button("Cancelar", key="Cancelar")],
    ]
    window = sg.Window("Cadastro de Procedimento", layout, modal=True)

    while True:
      event, values = window.read()
      if event in self.EVENTOS_FECHAMENTO or event == "Cancelar":
        window.close()
        return None
      if event != "Salvar":
        continue

      cpf_profissional = values["cpf_profissional"].strip()
      descricao = values["descricao"].strip()
      custo_texto = values["custo"].strip().replace(",", ".")

      if not cpf_profissional or not descricao or not custo_texto:
        self._mostra_erro("Todos os campos são obrigatórios.")
        continue

      if profissional_existe is not None and not profissional_existe(cpf_profissional):
        self._mostra_erro("Profissional não encontrado. Tente novamente.")
        continue

      try:
        custo = float(custo_texto)
        if custo < 0.01:
          raise ValueError
      except ValueError:
        self._mostra_erro("Valor incorreto! Informe um número válido maior ou igual a 0.01.")
        continue

      window.close()
      return {
        "cpf_profissional": cpf_profissional,
        "descricao": descricao,
        "custo": custo,
      }

  def pega_dados_alteracao_pagamento(self, modalidade: str, valor_maximo=None, data_atendimento=None):
    return self._formulario_pagamento(modalidade, valor_maximo, data_atendimento, alteracao=True)

  def pega_dados_pagamento(self, valor_maximo=None, data_atendimento=None):
    layout = [
      [sg.Text("Dados do Pagamento", font=("Helvetica", 14))],
      [sg.Text("Modalidade:")],
      [
        sg.Radio("Dinheiro", "modalidade", key="1", default=True),
        sg.Radio("PIX", "modalidade", key="2"),
        sg.Radio("Cartão de crédito", "modalidade", key="3"),
      ],
      [sg.Button("Continuar", key="Continuar"), sg.Button("Cancelar", key="Cancelar")],
    ]
    window = sg.Window("Modalidade de Pagamento", layout, modal=True)
    modalidade = None
    while True:
      event, values = window.read()
      if event in self.EVENTOS_FECHAMENTO or event == "Cancelar":
        window.close()
        return None
      if event == "Continuar":
        for opcao in ("1", "2", "3"):
          if values[opcao]:
            modalidade = opcao
            break
        window.close()
        break

    return self._formulario_pagamento(modalidade, valor_maximo, data_atendimento)

  def _formulario_pagamento(self, modalidade, valor_maximo=None, data_atendimento=None, alteracao=False):
    self._exibir_listagem("Pagamentos")
    nomes = {"1": "Dinheiro", "2": "PIX", "3": "Cartão de crédito"}

    layout = [
      [sg.Text("Dados do Pagamento", font=("Helvetica", 14))],
      [sg.Text(f"Modalidade: {nomes[modalidade]}")],
      [sg.Text("Data (DD/MM/AAAA):", size=(24, 1)), sg.Input(key="data", size=(28, 1))],
      [sg.Text("Valor pago (R$):", size=(24, 1)), sg.Input(key="valor", size=(28, 1))],
    ]

    if modalidade == "2":
      layout.append(
        [sg.Text("CPF do pagador:", size=(24, 1)), sg.Input(key="cpf_pagador", size=(28, 1))]
      )
    elif modalidade == "3":
      layout.extend([
        [sg.Text("Número do cartão:", size=(24, 1)), sg.Input(key="numero_cartao", size=(28, 1))],
        [sg.Text("Bandeira:", size=(24, 1)), sg.Input(key="bandeira", size=(28, 1))],
      ])

    layout.append([sg.Button("Salvar", key="Salvar"), sg.Button("Cancelar", key="Cancelar")])
    titulo = "Alterar Pagamento" if alteracao else "Registrar Pagamento"
    window = sg.Window(titulo, layout, modal=True)

    while True:
      event, values = window.read()
      if event in self.EVENTOS_FECHAMENTO or event == "Cancelar":
        window.close()
        return None
      if event != "Salvar":
        continue

      data_texto = values["data"].strip()
      valor_texto = values["valor"].strip().replace(",", ".")

      if not data_texto or not valor_texto:
        self._mostra_erro("Data e valor são obrigatórios.")
        continue

      try:
        data = datetime.strptime(data_texto, "%d/%m/%Y").date()
      except ValueError:
        self._mostra_erro("Data inválida! Use o formato DD/MM/AAAA.")
        continue

      if data_atendimento and data > data_atendimento:
        self._mostra_erro(
          f"Pagamento deve ser realizado até a data do atendimento "
          f"({data_atendimento.strftime('%d/%m/%Y')}). Tente novamente."
        )
        continue

      try:
        valor = float(valor_texto)
        if valor < 0.01:
          raise ValueError
      except ValueError:
        self._mostra_erro("Valor incorreto! Informe um número válido maior ou igual a 0.01.")
        continue

      if valor_maximo is not None and valor > valor_maximo:
        self._mostra_erro(
          f"Valor não pode exceder R$ {valor_maximo:.2f} restantes. Tente novamente."
        )
        continue

      cpf_pagador = ""
      numero_cartao = ""
      bandeira = ""

      if modalidade == "2":
        cpf_pagador = values.get("cpf_pagador", "").strip()
        if not cpf_pagador:
          self._mostra_erro("CPF do pagador é obrigatório.")
          continue
      elif modalidade == "3":
        numero_cartao = values.get("numero_cartao", "").strip()
        bandeira = values.get("bandeira", "").strip()
        if not numero_cartao or not bandeira:
          self._mostra_erro("Número do cartão e bandeira são obrigatórios.")
          continue

      window.close()
      return {
        "data": data,
        "valor": valor,
        "modalidade": modalidade,
        "cpf_pagador": cpf_pagador,
        "numero_cartao": numero_cartao,
        "bandeira": bandeira,
      }

  def mostra_atendimento(self, dados_atendimento):
    self._init_listagem()
    self._listagem_buffer.append(
      f"CÓDIGO: {dados_atendimento['codigo']}\n"
      f"CLÍNICA: {dados_atendimento['clinica']}\n"
      f"PACIENTE: {dados_atendimento['paciente']}\n"
      f"PROFISSIONAL: {dados_atendimento['profissional']}\n"
      f"TIPO: {dados_atendimento['tipo']}\n"
      f"DATA/HORÁRIO: {dados_atendimento['data_horario']}\n"
      f"VALOR TOTAL: {dados_atendimento['valor_total']}\n"
      f"TOTAL PAGO: {dados_atendimento['total_pago']}\n"
      f"VALOR RESTANTE: {dados_atendimento['valor_restante']}"
    )

  def mostra_procedimento(self, dados):
    self._init_listagem()
    self._listagem_buffer.append(
      f"CÓDIGO: {dados['codigo']}\n"
      f"DESCRIÇÃO: {dados['descricao']}\n"
      f"PROFISSIONAL: {dados['profissional']}\n"
      f"CUSTO: {dados['custo']}"
    )

  def mostra_pagamento(self, dados):
    self._init_listagem()
    self._listagem_buffer.append(
      f"CÓDIGO: {dados['codigo']}\n"
      f"DATA: {dados['data']}\n"
      f"VALOR: {dados['valor']}\n"
      f"DETALHES: {dados['detalhes']}"
    )

  def seleciona_atendimento(self, total_atendimentos):
    self._exibir_listagem("Atendimentos")
    return self.le_num_inteiro(
      "Código do atendimento que deseja selecionar: ",
      list(range(1, total_atendimentos + 1)),
    )

  def seleciona_procedimento(self, total_procedimentos):
    self._exibir_listagem("Procedimentos")
    return self.le_num_inteiro(
      "Código do procedimento que deseja selecionar: ",
      list(range(1, total_procedimentos + 1)),
    )

  def seleciona_pagamento(self, total_pagamentos):
    self._exibir_listagem("Pagamentos")
    return self.le_num_inteiro(
      "Código do pagamento que deseja selecionar: ",
      list(range(1, total_pagamentos + 1)),
    )

  def seleciona_clinica(self, total_clinicas):
    self._exibir_listagem("Clínicas")
    return self.le_num_inteiro(
      "Código da clínica que deseja selecionar: ",
      list(range(1, total_clinicas + 1)),
    )
