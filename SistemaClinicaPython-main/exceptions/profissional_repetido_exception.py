class ProfissionalRepetidoException(Exception):
  def __init__(self, cpf: str):
    super().__init__(f"O profissional com CPF {cpf} já existe.")