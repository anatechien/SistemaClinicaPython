from models.profissional import ProfissionalSaude


class Procedimento:
  def __init__(self, descricao: str, custo: float, profissional: ProfissionalSaude):
    if not descricao.strip():
      raise ValueError("A descrição do procedimento é obrigatória.")
    if custo <= 0:
      raise ValueError("O custo do procedimento deve ser maior que zero.")

    self.__descricao = descricao
    self.__custo = custo
    self.__profissional = profissional

  @property
  def descricao(self):
    return self.__descricao

  @property
  def custo(self):
    return self.__custo

  @property
  def profissional(self):
    return self.__profissional

  def atualizar(self, descricao: str, custo: float, profissional: ProfissionalSaude):
    if not descricao.strip():
      raise ValueError("A descrição do procedimento é obrigatória.")
    if custo <= 0:
      raise ValueError("O custo do procedimento deve ser maior que zero.")
    self.__descricao = descricao
    self.__custo = custo
    self.__profissional = profissional
