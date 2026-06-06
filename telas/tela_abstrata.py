from datetime import date, datetime


class TelaAbstrata:
  def le_num_inteiro(self, mensagem=" ", ints_validos=None):
    while True:
      valor_lido = input(mensagem)
      try:
        valor_int = int(valor_lido)
        if ints_validos and valor_int not in ints_validos:
          raise ValueError
        return valor_int
      except ValueError:
        print("Valor incorreto!")
        if ints_validos:
          print("Valores válidos: ", ints_validos)

  def le_float(self, mensagem=" ", minimo=None):
    while True:
      valor_lido = input(mensagem).strip().replace(",", ".")
      try:
        valor = float(valor_lido)
        if minimo is not None and valor < minimo:
          raise ValueError
        return valor
      except ValueError:
        if minimo is not None:
          print(f"Valor incorreto! Informe um número válido maior ou igual a {minimo}.")
        else:
          print("Valor incorreto! Informe um número válido.")

  def le_texto(self, mensagem=" "):
    while True:
      valor = input(mensagem).strip()
      if valor:
        return valor
      print("Valor não pode ser vazio! Tente novamente.")

  def le_texto_validado(self, mensagem, validador, mensagem_erro):
    while True:
      valor = self.le_texto(mensagem)
      if validador(valor):
        return valor
      print(mensagem_erro)

  def le_data(self, mensagem=" "):
    while True:
      valor_lido = input(mensagem).strip()
      try:
        return datetime.strptime(valor_lido, "%d/%m/%Y").date()
      except ValueError:
        print("Data inválida! Use o formato DD/MM/AAAA.")

  def le_data_nascimento_paciente(
    self,
    mensagem="Data de nascimento (DD/MM/AAAA) - paciente deve ser maior de 18 anos: ",
  ):
    while True:
      data = self.le_data(mensagem)
      if self._calcular_idade(data) >= 18:
        return data
      print("Paciente deve ser maior de 18 anos. Tente novamente.")

  def le_horario(self, mensagem=" "):
    while True:
      valor_lido = input(mensagem).strip()
      try:
        return datetime.strptime(valor_lido, "%H:%M").time()
      except ValueError:
        print("Horário inválido! Use o formato HH:MM.")

  def le_horario_fechamento(self, horario_abertura, mensagem="Horário de fechamento (HH:MM): "):
    while True:
      horario_fechamento = self.le_horario(mensagem)
      if horario_abertura < horario_fechamento:
        return horario_fechamento
      print("Horário de fechamento deve ser posterior ao de abertura. Tente novamente.")

  def le_horario_fim(self, horario_inicio, mensagem="Horário de término (HH:MM): "):
    while True:
      horario_fim = self.le_horario(mensagem)
      if horario_inicio < horario_fim:
        return horario_fim
      print("Horário de término deve ser posterior ao de início. Tente novamente.")

  def le_horarios_atendimento(self, validador=None):
    while True:
      horario_inicio = self.le_horario("Horário de início (HH:MM): ")
      horario_fim = self.le_horario_fim(horario_inicio)
      if validador is None or validador(horario_inicio, horario_fim):
        return horario_inicio, horario_fim
      print("Atendimento fora do horário de funcionamento da clínica. Tente novamente.")

  def _calcular_idade(self, data_nascimento: date):
    hoje = date.today()
    idade = hoje.year - data_nascimento.year
    if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
      idade -= 1
    return idade

  def mostra_mensagem(self, msg):
    print(msg)
