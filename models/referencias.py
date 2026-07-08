class ResolvedorReferencias:
  def __init__(self, buscar_paciente, buscar_profissional, buscar_tipo):
    self.__buscar_paciente = buscar_paciente
    self.__buscar_profissional = buscar_profissional
    self.__buscar_tipo = buscar_tipo

  def paciente(self, cpf: str):
    paciente = self.__buscar_paciente(cpf)
    if paciente is None:
      raise ValueError(f"Paciente com CPF {cpf} não encontrado.")
    return paciente

  def profissional(self, cpf: str):
    profissional = self.__buscar_profissional(cpf)
    if profissional is None:
      raise ValueError(f"Profissional com CPF {cpf} não encontrado.")
    return profissional

  def tipo_atendimento(self, nome: str):
    tipo = self.__buscar_tipo(nome)
    if tipo is None:
      raise ValueError(f"Tipo de atendimento '{nome}' não encontrado.")
    return tipo
