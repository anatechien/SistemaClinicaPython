from datetime import datetime

import FreeSimpleGUI as sg

from telas.gui.tela_abstrata_gui import TelaAbstrataGUI


class TelaClinicaGUI(TelaAbstrataGUI):
  def tela_opcoes(self):
    return self._menu_botoes(
      "Clínica",
      [
        (1, "Incluir Clínica"),
        (2, "Alterar Clínica"),
        (3, "Listar Clínicas"),
        (4, "Excluir Clínica"),
        (0, "Retornar"),
      ],
      "Clínica",
      "Clínicas",
    )

  def pega_dados_clinica(self, nome_disponivel=None):
    self._exibir_listagem("Clínicas")

    layout = [
      [sg.Text("Dados da Clínica", font=("Helvetica", 14))],
      [sg.Text("Nome:", size=(18, 1)), sg.Input(key="nome", size=(30, 1))],
      [sg.Text("Cidade:", size=(18, 1)), sg.Input(key="cidade", size=(30, 1))],
      [sg.Text("Descrição:", size=(18, 1)), sg.Input(key="descricao", size=(30, 1))],
      [sg.Text("Abertura (HH:MM):", size=(18, 1)), sg.Input(key="abertura", size=(30, 1))],
      [sg.Text("Fechamento (HH:MM):", size=(18, 1)), sg.Input(key="fechamento", size=(30, 1))],
      [sg.Button("Salvar", key="Salvar"), sg.Button("Cancelar", key="Cancelar")],
    ]
    window = sg.Window("Cadastro de Clínica", layout, modal=True)

    while True:
      event, values = window.read()
      if event in self.EVENTOS_FECHAMENTO or event == "Cancelar":
        window.close()
        return None
      if event != "Salvar":
        continue

      nome = values["nome"].strip()
      cidade = values["cidade"].strip()
      descricao = values["descricao"].strip()
      abertura = values["abertura"].strip()
      fechamento = values["fechamento"].strip()

      if not nome or not cidade or not descricao or not abertura or not fechamento:
        self._mostra_erro("Todos os campos são obrigatórios.")
        continue

      if nome_disponivel is not None and not nome_disponivel(nome):
        self._mostra_erro("Já existe uma clínica com esse nome. Tente novamente.")
        continue

      try:
        horario_abertura = datetime.strptime(abertura, "%H:%M").time()
      except ValueError:
        self._mostra_erro("Horário de abertura inválido! Use o formato HH:MM.")
        continue

      try:
        horario_fechamento = datetime.strptime(fechamento, "%H:%M").time()
      except ValueError:
        self._mostra_erro("Horário de fechamento inválido! Use o formato HH:MM.")
        continue

      if horario_abertura >= horario_fechamento:
        self._mostra_erro(
          "Horário de fechamento deve ser posterior ao de abertura. Tente novamente."
        )
        continue

      window.close()
      return {
        "nome": nome,
        "cidade": cidade,
        "descricao": descricao,
        "horario_abertura": horario_abertura,
        "horario_fechamento": horario_fechamento,
      }

  def mostra_clinica(self, dados_clinica):
    self._init_listagem()
    self._listagem_buffer.append(
      f"CÓDIGO: {dados_clinica['codigo']}\n"
      f"NOME: {dados_clinica['nome']}\n"
      f"CIDADE: {dados_clinica['cidade']}\n"
      f"DESCRIÇÃO: {dados_clinica['descricao']}\n"
      f"HORÁRIO: {dados_clinica['horario']}\n"
      f"ATENDIMENTOS: {dados_clinica['total_atendimentos']}"
    )

  def seleciona_clinica(self, total_clinicas=None):
    self._exibir_listagem("Clínicas")
    ints_validos = list(range(1, total_clinicas + 1)) if total_clinicas else None
    return self.le_num_inteiro("Código da clínica que deseja selecionar: ", ints_validos)
