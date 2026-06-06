from telas.tela_profissional import TelaProfissional
from models.profissional import ProfissionalSaude


class ControladorProfissionais:
  def __init__(self, controlador_sistema):
    self.__profissionais = []
    self.__tela_profissional = TelaProfissional()
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

  def incluir_profissional(self):
    dados = self.__tela_profissional.pega_dados_profissional(
      cpf_disponivel=lambda cpf: self.pega_profissional_por_cpf(cpf) is None
    )
    profissional = ProfissionalSaude(
      dados["nome"],
      dados["celular"],
      dados["cpf"],
      dados["especialidade"],
      dados["registro_profissional"],
    )
    self.__profissionais.append(profissional)
    self.__tela_profissional.mostra_mensagem("Profissional cadastrado com sucesso!")

  def alterar_profissional(self):
    if not self.__profissionais:
      self.__tela_profissional.mostra_mensagem("ATENCAO: Nenhum profissional cadastrado.")
      return

    while True:
      self.lista_profissionais()
      cpf = self.__tela_profissional.seleciona_profissional()
      profissional = self.pega_profissional_por_cpf(cpf)
      if profissional is not None:
        break
      self.__tela_profissional.mostra_mensagem("ATENCAO: Profissional não existente. Tente novamente.")

    dados = self.__tela_profissional.pega_dados_profissional(
      cpf_disponivel=lambda novo_cpf: (
        novo_cpf == profissional.cpf or self.pega_profissional_por_cpf(novo_cpf) is None
      )
    )
    profissional.atualizar(
      dados["nome"],
      dados["celular"],
      dados["especialidade"],
      dados["registro_profissional"],
    )
    self.lista_profissionais()

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
