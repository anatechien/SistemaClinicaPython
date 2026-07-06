from exceptions.tipo_atendimento_repetido_exception import TipoAtendimentoRepetidoException
from telas.tela_tipo_atendimento import TelaTipoAtendimento
from models.tipo_atendimento import TipoAtendimento


class ControladorTiposAtendimento:
  def __init__(self, controlador_sistema, tela=None):
    self.__tipos = []
    self.__tela_tipo = tela or TelaTipoAtendimento()
    self.__controlador_sistema = controlador_sistema

  @property
  def tipos(self):
    return self.__tipos

  def pega_tipo_por_nome(self, nome: str):
    for tipo in self.__tipos:
      if tipo.nome == nome:
        return tipo
    return None

  def _dados_tipo(self, tipo: TipoAtendimento):
    return {"nome": tipo.nome, "descricao": tipo.descricao}

  def _garantir_nome_disponivel(self, nome: str, nome_atual: str = None):
    if self.pega_tipo_por_nome(nome) is not None and nome != nome_atual:
      raise TipoAtendimentoRepetidoException(nome)

  def incluir_tipo(self):
    while True:
      dados = self.__tela_tipo.pega_dados_tipo()
      if dados is None:
        return
      try:
        self._garantir_nome_disponivel(dados["nome"])
        tipo = TipoAtendimento(dados["nome"], dados["descricao"])
        self.__tipos.append(tipo)
        self.__tela_tipo.mostra_mensagem("Tipo de atendimento cadastrado com sucesso!")
        break
      except TipoAtendimentoRepetidoException as erro:
        self.__tela_tipo.mostra_mensagem(f"ATENCAO: {erro}")

  def alterar_tipo(self):
    if not self.__tipos:
      self.__tela_tipo.mostra_mensagem("ATENCAO: Nenhum tipo de atendimento cadastrado.")
      return

    while True:
      self.lista_tipos()
      nome = self.__tela_tipo.seleciona_tipo()
      if nome is None:
        return
      tipo = self.pega_tipo_por_nome(nome)
      if tipo is not None:
        break
      self.__tela_tipo.mostra_mensagem("ATENCAO: Tipo de atendimento não existente. Tente novamente.")

    while True:
      dados = self.__tela_tipo.pega_dados_tipo()
      if dados is None:
        return
      try:
        self._garantir_nome_disponivel(dados["nome"], tipo.nome)
        tipo.atualizar(dados["nome"], dados["descricao"])
        self.lista_tipos()
        break
      except TipoAtendimentoRepetidoException as erro:
        self.__tela_tipo.mostra_mensagem(f"ATENCAO: {erro}")

  def lista_tipos(self):
    if not self.__tipos:
      self.__tela_tipo.mostra_mensagem("ATENCAO: Nenhum tipo de atendimento cadastrado.")
      return
    for tipo in self.__tipos:
      self.__tela_tipo.mostra_tipo(self._dados_tipo(tipo))

  def excluir_tipo(self):
    if not self.__tipos:
      self.__tela_tipo.mostra_mensagem("ATENCAO: Nenhum tipo de atendimento cadastrado.")
      return

    while True:
      self.lista_tipos()
      nome = self.__tela_tipo.seleciona_tipo()
      if nome is None:
        return
      tipo = self.pega_tipo_por_nome(nome)
      if tipo is not None:
        self.__tipos.remove(tipo)
        self.lista_tipos()
        return
      self.__tela_tipo.mostra_mensagem("ATENCAO: Tipo de atendimento não existente. Tente novamente.")

  def retornar(self):
    self.__controlador_sistema.abre_tela()

  def abre_tela(self):
    lista_opcoes = {
      1: self.incluir_tipo,
      2: self.alterar_tipo,
      3: self.lista_tipos,
      4: self.excluir_tipo,
      0: self.retornar,
    }

    while True:
      lista_opcoes[self.__tela_tipo.tela_opcoes()]()
