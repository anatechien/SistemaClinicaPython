import FreeSimpleGUI as sg

from telas.gui.tela_abstrata_gui import TelaAbstrataGUI


class TelaProfissionalGUI(TelaAbstrataGUI):
  def tela_opcoes(self):
    return self._menu_botoes(
      "Profissionais",
      [
        (1, "Incluir Profissional"),
        (2, "Alterar Profissional"),
        (3, "Listar Profissionais"),
        (4, "Excluir Profissional"),
        (0, "Retornar"),
      ],
      "Profissionais",
      "Profissionais",
    )

  def pega_dados_profissional(self, cpf_disponivel=None):
    self._exibir_listagem("Profissionais")

    layout = [
      [sg.Text("Dados do Profissional", font=("Helvetica", 14))],
      [sg.Text("Nome:", size=(22, 1)), sg.Input(key="nome", size=(30, 1))],
      [sg.Text("Celular:", size=(22, 1)), sg.Input(key="celular", size=(30, 1))],
      [sg.Text("CPF:", size=(22, 1)), sg.Input(key="cpf", size=(30, 1))],
      [sg.Text("Especialidade:", size=(22, 1)), sg.Input(key="especialidade", size=(30, 1))],
      [
        sg.Text("Registro profissional:", size=(22, 1)),
        sg.Input(key="registro_profissional", size=(30, 1)),
      ],
      [sg.Button("Salvar", key="Salvar"), sg.Button("Cancelar", key="Cancelar")],
    ]
    window = sg.Window("Cadastro de Profissional", layout, modal=True)

    while True:
      event, values = window.read()
      if event in self.EVENTOS_FECHAMENTO or event == "Cancelar":
        window.close()
        return None
      if event != "Salvar":
        continue

      nome = values["nome"].strip()
      celular = values["celular"].strip()
      cpf = values["cpf"].strip()
      especialidade = values["especialidade"].strip()
      registro = values["registro_profissional"].strip()

      if not nome or not celular or not cpf or not especialidade or not registro:
        self._mostra_erro("Todos os campos são obrigatórios.")
        continue

      if cpf_disponivel is not None and not cpf_disponivel(cpf):
        self._mostra_erro("CPF já cadastrado. Tente novamente.")
        continue

      window.close()
      return {
        "nome": nome,
        "celular": celular,
        "cpf": cpf,
        "especialidade": especialidade,
        "registro_profissional": registro,
      }

  def mostra_profissional(self, dados_profissional):
    self._init_listagem()
    self._listagem_buffer.append(
      f"NOME: {dados_profissional['nome']}\n"
      f"CELULAR: {dados_profissional['celular']}\n"
      f"CPF: {dados_profissional['cpf']}\n"
      f"ESPECIALIDADE: {dados_profissional['especialidade']}\n"
      f"REGISTRO: {dados_profissional['registro_profissional']}"
    )

  def seleciona_profissional(self):
    self._exibir_listagem("Profissionais")
    return self.le_texto("CPF do profissional que deseja selecionar: ")
