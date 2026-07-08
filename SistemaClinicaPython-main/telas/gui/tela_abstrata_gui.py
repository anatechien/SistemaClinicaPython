from datetime import datetime

import FreeSimpleGUI as sg

from exceptions.paciente_menor_idade_exception import PacienteMenorDeIdadeException
from models.paciente import validar_maior_idade
from telas.tela_abstrata import TelaAbstrata


class TelaAbstrataGUI(TelaAbstrata):
  EVENTOS_FECHAMENTO = (sg.WIN_CLOSED, sg.WINDOW_CLOSED)

  def _init_listagem(self):
    if not hasattr(self, "_listagem_buffer"):
      self._listagem_buffer = []

  def _exibir_listagem(self, titulo="Listagem"):
    self._init_listagem()
    if self._listagem_buffer:
      sg.popup_scrolled(
        "\n\n".join(self._listagem_buffer),
        title=titulo,
        size=(70, 20),
        non_blocking=False,
      )
      self._listagem_buffer = []

  def _menu_botoes(self, titulo, opcoes, titulo_janela, titulo_listagem=None):
    if titulo_listagem:
      self._exibir_listagem(titulo_listagem)
    layout = [[sg.Text(titulo, font=("Helvetica", 16))]]
    for key, label in opcoes:
      layout.append([sg.Button(label, key=key, size=(30, 1))])
    window = sg.Window(titulo_janela, layout, modal=True, finalize=True)
    while True:
      event, _ = window.read()
      chaves_validas = [key for key, _ in opcoes]
      if event in (*self.EVENTOS_FECHAMENTO, 0) and 0 in chaves_validas:
        window.close()
        return 0
      if event in chaves_validas:
        window.close()
        return event

  def mostra_mensagem(self, msg):
    sg.popup(msg, title="Aviso")

  def _mostra_erro(self, msg):
    sg.popup_error(msg, title="Erro")

  def le_num_inteiro(self, mensagem=" ", ints_validos=None):
    while True:
      valor_lido = sg.popup_get_text(mensagem, title="Entrada")
      if valor_lido is None:
        return None
      try:
        valor_int = int(valor_lido)
        if ints_validos and valor_int not in ints_validos:
          raise ValueError
        return valor_int
      except ValueError:
        erro = "Valor incorreto!"
        if ints_validos:
          erro += f"\nValores válidos: {ints_validos}"
        self._mostra_erro(erro)

  def le_float(self, mensagem=" ", minimo=None):
    while True:
      valor_lido = sg.popup_get_text(mensagem, title="Entrada")
      if valor_lido is None:
        continue
      try:
        valor = float(valor_lido.strip().replace(",", "."))
        if minimo is not None and valor < minimo:
          raise ValueError
        return valor
      except ValueError:
        if minimo is not None:
          self._mostra_erro(
            f"Valor incorreto! Informe um número válido maior ou igual a {minimo}."
          )
        else:
          self._mostra_erro("Valor incorreto! Informe um número válido.")

  def le_texto(self, mensagem=" "):
    while True:
      valor = sg.popup_get_text(mensagem, title="Entrada")
      if valor is None:
        return None
      valor = valor.strip()
      if valor:
        return valor
      self._mostra_erro("Valor não pode ser vazio! Tente novamente.")

  def le_texto_validado(self, mensagem, validador, mensagem_erro):
    while True:
      valor = self.le_texto(mensagem)
      if valor is None:
        return None
      if validador(valor):
        return valor
      self._mostra_erro(mensagem_erro)

  def le_data(self, mensagem=" "):
    while True:
      valor_lido = sg.popup_get_text(mensagem, title="Entrada")
      if valor_lido is None:
        continue
      try:
        return datetime.strptime(valor_lido.strip(), "%d/%m/%Y").date()
      except ValueError:
        self._mostra_erro("Data inválida! Use o formato DD/MM/AAAA.")

  def le_data_nascimento_paciente(
    self,
    mensagem="Data de nascimento (DD/MM/AAAA) - paciente deve ser maior de 18 anos: ",
  ):
    while True:
      data = self.le_data(mensagem)
      try:
        validar_maior_idade(data)
        return data
      except PacienteMenorDeIdadeException as erro:
        self._mostra_erro(str(erro))

  def le_horario(self, mensagem=" "):
    while True:
      valor_lido = sg.popup_get_text(mensagem, title="Entrada")
      if valor_lido is None:
        continue
      try:
        return datetime.strptime(valor_lido.strip(), "%H:%M").time()
      except ValueError:
        self._mostra_erro("Horário inválido! Use o formato HH:MM.")

  def le_horario_fechamento(self, horario_abertura, mensagem="Horário de fechamento (HH:MM): "):
    while True:
      horario_fechamento = self.le_horario(mensagem)
      if horario_abertura < horario_fechamento:
        return horario_fechamento
      self._mostra_erro(
        "Horário de fechamento deve ser posterior ao de abertura. Tente novamente."
      )

  def le_horario_fim(self, horario_inicio, mensagem="Horário de término (HH:MM): "):
    while True:
      horario_fim = self.le_horario(mensagem)
      if horario_inicio < horario_fim:
        return horario_fim
      self._mostra_erro(
        "Horário de término deve ser posterior ao de início. Tente novamente."
      )

  def le_horarios_atendimento(self, validador=None):
    while True:
      horario_inicio = self.le_horario("Horário de início (HH:MM): ")
      horario_fim = self.le_horario_fim(horario_inicio)
      if validador is None or validador(horario_inicio, horario_fim):
        return horario_inicio, horario_fim
      self._mostra_erro(
        "Atendimento fora do horário de funcionamento da clínica. Tente novamente."
      )
