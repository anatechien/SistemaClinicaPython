import FreeSimpleGUI as sg

from telas.gui.tela_abstrata_gui import TelaAbstrataGUI


class TelaTipoAtendimentoGUI(TelaAbstrataGUI):
  def tela_opcoes(self):
    return self._menu_botoes(
      "Tipos de Atendimento",
      [
        (1, "Incluir Tipo"),
        (2, "Alterar Tipo"),
        (3, "Listar Tipos"),
        (4, "Excluir Tipo"),
        (0, "Retornar"),
      ],
      "Tipos de Atendimento",
      "Tipos de Atendimento",
    )

  def pega_dados_tipo(self, nome_disponivel=None):
    self._exibir_listagem("Tipos de Atendimento")

    layout = [
      [sg.Text("Dados do Tipo de Atendimento", font=("Helvetica", 14))],
      [sg.Text("Nome:", size=(18, 1)), sg.Input(key="nome", size=(30, 1))],
      [sg.Text("Descrição:", size=(18, 1)), sg.Input(key="descricao", size=(30, 1))],
      [sg.Button("Salvar", key="Salvar"), sg.Button("Cancelar", key="Cancelar")],
    ]
    window = sg.Window("Cadastro de Tipo", layout, modal=True)

    while True:
      event, values = window.read()
      if event in self.EVENTOS_FECHAMENTO or event == "Cancelar":
        window.close()
        return None
      if event != "Salvar":
        continue

      nome = values["nome"].strip()
      descricao = values["descricao"].strip()

      if not nome or not descricao:
        self._mostra_erro("Todos os campos são obrigatórios.")
        continue

      if nome_disponivel is not None and not nome_disponivel(nome):
        self._mostra_erro("Já existe um tipo com esse nome. Tente novamente.")
        continue

      window.close()
      return {"nome": nome, "descricao": descricao}

  def mostra_tipo(self, dados_tipo):
    self._init_listagem()
    self._listagem_buffer.append(
      f"NOME: {dados_tipo['nome']}\n"
      f"DESCRIÇÃO: {dados_tipo['descricao']}"
    )

  def seleciona_tipo(self):
    self._exibir_listagem("Tipos de Atendimento")
    return self.le_texto("Nome do tipo de atendimento que deseja selecionar: ")
