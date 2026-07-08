class PacienteMenorDeIdadeException(Exception):
  def __init__(self, idade: int, idade_minima: int = 18):
    super().__init__(
      f"Paciente deve ser maior de {idade_minima} anos (idade na data: {idade} anos)."
    )
