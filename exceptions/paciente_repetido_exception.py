class PacienteRepetidoException(Exception):
  def __init__(self, cpf: str):
    super().__init__(f"O paciente com CPF {cpf} já existe.")