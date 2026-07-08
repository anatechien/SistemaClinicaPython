class Procedimento:
  def __init__(self, descricao: str, custo: float, profissional):
    if not descricao.strip():
      raise ValueError("A descrição do procedimento é obrigatória.")
    if custo <= 0:
      raise ValueError("O custo do procedimento deve ser maior que zero.")

    self.__descricao = descricao
    self.__custo = custo
    self.__profissional_cpf = profissional.cpf if hasattr(profissional, "cpf") else profissional
    self.__resolver = None

  def migrar_se_necessario(self):
    if hasattr(self, "_Procedimento__profissional"):
      self.__profissional_cpf = self._Procedimento__profissional.cpf
      del self._Procedimento__profissional

  def vincular_resolver(self, resolver):
    self.__resolver = resolver

  def _resolver_ou_erro(self):
    if self.__resolver is None:
      raise ValueError("Resolvedor de referências não vinculado ao procedimento.")
    return self.__resolver

  @property
  def descricao(self):
    return self.__descricao

  @property
  def custo(self):
    return self.__custo

  @property
  def profissional_cpf(self):
    return self.__profissional_cpf

  @property
  def profissional(self):
    return self._resolver_ou_erro().profissional(self.__profissional_cpf)

  def atualizar_chave_profissional(self, cpf_novo: str):
    self.__profissional_cpf = cpf_novo

  def atualizar(self, descricao: str, custo: float, profissional):
    if not descricao.strip():
      raise ValueError("A descrição do procedimento é obrigatória.")
    if custo <= 0:
      raise ValueError("O custo do procedimento deve ser maior que zero.")
    self.__descricao = descricao
    self.__custo = custo
    self.__profissional_cpf = profissional.cpf if hasattr(profissional, "cpf") else profissional
