class TipoAtendimentoRepetidoException(Exception):
  def __init__(self, nome: str):
    self.mensagem = "O tipo de atendimento '{}' já existe"
    super().__init__(self.mensagem.format(nome))
