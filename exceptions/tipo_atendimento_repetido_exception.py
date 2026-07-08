class TipoAtendimentoRepetidoException(Exception):
  def __init__(self, nome: str):
    super().__init__(f"O tipo de atendimento '{nome}' já existe.")