class PacienteRepetidoException(Exception):
  def __init__(self, cpf: str):
    self.mensagem = "O paciente com CPF {} já existe"
    super().__init__(self.mensagem.format(cpf))
