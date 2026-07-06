from exceptions.profissional_repetido_exception import ProfissionalRepetidoException
from telas.tela_profissional import TelaProfissional
from models.profissional import ProfissionalSaude


class ControladorProfissionais:
  def __init__(self, controlador_sistema, tela=None):
    self.__profissionais = []
    self.__tela_profissional = tela or TelaProfissional()
    self.__controlador_sistema = controlador_sistema

  @property
  def profissionais(self):
    return self.__profissionais

  def pega_profissional_por_cpf(self, cpf: str):
    for profissional in self.__profissionais:
      if profissional.cpf == cpf:
        return profissional
    return None

  def _dados_profissional(self, profissional: ProfissionalSaude):
    return {
      "nome": profissional.nome,
      "celular": profissional.celular,
      "cpf": profissional.cpf,
      "especialidade": profissional.especialidade,
      "registro_profissional": profissional.registro_profissional,
    }

  def _garantir_cpf_disponivel(self, cpf: str, cpf_atual: str = None):
    if self.pega_profissional_por_cpf(cpf) is not None and cpf != cpf_atual:
      raise ProfissionalRepetidoException(cpf)

  def incluir_profissional(self):
    while True:
      dados = self.__tela_profissional.pega_dados_profissional()
      if dados is None:
        return
      try:
        self._garantir_cpf_disponivel(dados["cpf"])
        profissional = ProfissionalSaude(
          dados["nome"],
          dados["celular"],
          dados["cpf"],
          dados["especialidade"],
          dados["registro_profissional"],
        )
        self.__profissionais.append(profissional)
        self.__tela_profissional.mostra_mensagem("Profissional cadastrado com sucesso!")
        break
      except ProfissionalRepetidoException as erro:
        self.__tela_profissional.mostra_mensagem(f"ATENCAO: {erro}")

  def alterar_profissional(self):
    if not self.__profissionais:
      self.__tela_profissional.mostra_mensagem("ATENCAO: Nenhum profissional cadastrado.")
      return

    while True:
      self.lista_profissionais()
      cpf = self.__tela_profissional.seleciona_profissional()
      if cpf is None:
        return
      profissional = self.pega_profissional_por_cpf(cpf)
      if profissional is not None:
        break
      self.__tela_profissional.mostra_mensagem("ATENCAO: Profissional não existente. Tente novamente.")

    while True:
      dados = self.__tela_profissional.pega_dados_profissional()
      if dados is None:
        return
      try:
        self._garantir_cpf_disponivel(dados["cpf"], profissional.cpf)
        profissional.atualizar(
          dados["nome"],
          dados["celular"],
          dados["especialidade"],
          dados["registro_profissional"],
        )
        self.lista_profissionais()
        break
      except ProfissionalRepetidoException as erro:
        self.__tela_profissional.mostra_mensagem(f"ATENCAO: {erro}")

  def lista_profissionais(self):
    if not self.__profissionais:
      self.__tela_profissional.mostra_mensagem("ATENCAO: Nenhum profissional cadastrado.")
      return
    for profissional in self.__profissionais:
      self.__tela_profissional.mostra_profissional(self._dados_profissional(profissional))

  def excluir_profissional(self):
    if not self.__profissionais:
      self.__tela_profissional.mostra_mensagem("ATENCAO: Nenhum profissional cadastrado.")
      return

    while True:
      self.lista_profissionais()
      cpf = self.__tela_profissional.seleciona_profissional()
      if cpf is None:
        return
      profissional = self.pega_profissional_por_cpf(cpf)
      if profissional is not None:
        self.__profissionais.remove(profissional)
        self.lista_profissionais()
        return
      self.__tela_profissional.mostra_mensagem("ATENCAO: Profissional não existente. Tente novamente.")

  def retornar(self):
    self.__controlador_sistema.abre_tela()

  def abre_tela(self):
    lista_opcoes = {
      1: self.incluir_profissional,
      2: self.alterar_profissional,
      3: self.lista_profissionais,
      4: self.excluir_profissional,
      0: self.retornar,
    }

    while True:
      lista_opcoes[self.__tela_profissional.tela_opcoes()]()
