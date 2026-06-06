class ProfissionalRepetidoException(Exception):
  def __init__(self, cpf: str):
    self.mensagem = "O profissional com CPF {} já existe"
    super().__init__(self.mensagem.format(cpf))
