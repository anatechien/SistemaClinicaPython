from datetime import datetime

import FreeSimpleGUI as sg

from exceptions.paciente_menor_idade_exception import PacienteMenorDeIdadeException
from models.paciente import calcular_idade, validar_maior_idade
from telas.gui.tela_abstrata_gui import TelaAbstrataGUI


class TelaPacienteGUI(TelaAbstrataGUI):
  def tela_opcoes(self):
    return self._menu_botoes(
      "Pacientes",
      [
        (1, "Incluir Paciente"),
        (2, "Alterar Paciente"),
        (3, "Listar Pacientes"),
        (4, "Excluir Paciente"),
        (0, "Retornar"),
      ],
      "Pacientes",
      "Pacientes",
    )

  def pega_responsavel(self):
    responsavel = sg.popup_get_text(
      "Informe o nome do responsável legal:",
      title="Responsável",
    )
    if responsavel is None:
      return None
    responsavel = responsavel.strip()
    return responsavel or None

  def pega_dados_paciente(self, cpf_disponivel=None):
    self._exibir_listagem("Pacientes")

    layout = [
      [sg.Text("Dados do Paciente", font=("Helvetica", 14))],
      [sg.Text("Nome:", size=(22, 1)), sg.Input(key="nome", size=(30, 1))],
      [sg.Text("Celular:", size=(22, 1)), sg.Input(key="celular", size=(30, 1))],
      [sg.Text("CPF:", size=(22, 1)), sg.Input(key="cpf", size=(30, 1))],
      [
        sg.Text("Nascimento (DD/MM/AAAA):", size=(22, 1)),
        sg.Input(key="data_nascimento", size=(30, 1)),
      ],
      [
        sg.Text("Responsável (se menor):", size=(22, 1)),
        sg.Input(key="responsavel", size=(30, 1)),
      ],
      [sg.Button("Salvar", key="Salvar"), sg.Button("Cancelar", key="Cancelar")],
    ]
    window = sg.Window("Cadastro de Paciente", layout, modal=True)

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
      data_texto = values["data_nascimento"].strip()
      responsavel = values["responsavel"].strip() or None

      if not nome or not celular or not cpf or not data_texto:
        self._mostra_erro("Nome, celular, CPF e data de nascimento são obrigatórios.")
        continue

      if cpf_disponivel is not None and not cpf_disponivel(cpf):
        self._mostra_erro("CPF já cadastrado. Tente novamente.")
        continue

      try:
        data_nascimento = datetime.strptime(data_texto, "%d/%m/%Y").date()
      except ValueError:
        self._mostra_erro("Data inválida! Use o formato DD/MM/AAAA.")
        continue

      idade = calcular_idade(data_nascimento)
      if idade < 18 and not responsavel:
        window.close()
        responsavel = self.pega_responsavel()
        if not responsavel:
          return None

      try:
        validar_maior_idade(data_nascimento, possui_responsavel=bool(responsavel))
      except PacienteMenorDeIdadeException as erro:
        self._mostra_erro(str(erro))
        continue

      window.close()
      return {
        "nome": nome,
        "celular": celular,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "responsavel": responsavel,
      }

  def mostra_paciente(self, dados_paciente):
    self._init_listagem()
    texto = (
      f"NOME: {dados_paciente['nome']}\n"
      f"CELULAR: {dados_paciente['celular']}\n"
      f"CPF: {dados_paciente['cpf']}\n"
      f"DATA DE NASCIMENTO: {dados_paciente['data_nascimento']}"
    )
    if dados_paciente.get("responsavel"):
      texto += f"\nRESPONSÁVEL: {dados_paciente['responsavel']}"
    self._listagem_buffer.append(texto)

  def seleciona_paciente(self):
    self._exibir_listagem("Pacientes")
    return self.le_texto("CPF do paciente que deseja selecionar: ")
