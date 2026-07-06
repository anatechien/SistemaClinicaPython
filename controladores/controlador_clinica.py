from telas.tela_clinica import TelaClinica
from models.clinica import Clinica


class ControladorClinica:
  def __init__(self, controlador_sistema, tela=None):
    self.__clinicas = []
    self.__tela_clinica = tela or TelaClinica()
    self.__controlador_sistema = controlador_sistema

  @property
  def clinicas(self):
    return self.__clinicas

  def pega_clinica_por_codigo(self, codigo: int):
    if 1 <= codigo <= len(self.__clinicas):
      return self.__clinicas[codigo - 1]
    return None

  def pega_clinica_por_nome(self, nome: str):
    for clinica in self.__clinicas:
      if clinica.nome == nome:
        return clinica
    return None

  def _dados_clinica(self, codigo: int, clinica: Clinica):
    return {
      "codigo": codigo,
      "nome": clinica.nome,
      "cidade": clinica.cidade,
      "descricao": clinica.descricao,
      "horario": (
        f"{clinica.horario_abertura.strftime('%H:%M')} às "
        f"{clinica.horario_fechamento.strftime('%H:%M')}"
      ),
      "total_atendimentos": len(clinica.atendimentos),
    }

  def incluir_clinica(self):
    dados = self.__tela_clinica.pega_dados_clinica(
      nome_disponivel=lambda nome: self.pega_clinica_por_nome(nome) is None
    )
    if dados is None:
      return
    clinica = Clinica(
      dados["nome"],
      dados["cidade"],
      dados["descricao"],
      dados["horario_abertura"],
      dados["horario_fechamento"],
    )
    self.__clinicas.append(clinica)
    self.__tela_clinica.mostra_mensagem("Clínica cadastrada com sucesso!")

  def alterar_clinica(self):
    if not self.__clinicas:
      self.__tela_clinica.mostra_mensagem("ATENCAO: Nenhuma clínica cadastrada.")
      return

    self.lista_clinicas()
    codigo = self.__tela_clinica.seleciona_clinica(len(self.__clinicas))
    if codigo is None:
      return
    clinica = self.pega_clinica_por_codigo(codigo)

    if clinica is None:
      self.__tela_clinica.mostra_mensagem("ATENCAO: Clínica não existente.")
      return

    dados = self.__tela_clinica.pega_dados_clinica(
      nome_disponivel=lambda nome: (
        nome == clinica.nome or self.pega_clinica_por_nome(nome) is None
      )
    )
    if dados is None:
      return
    clinica.atualizar(
      dados["nome"],
      dados["cidade"],
      dados["descricao"],
      dados["horario_abertura"],
      dados["horario_fechamento"],
    )
    self.lista_clinicas()

  def lista_clinicas(self):
    if not self.__clinicas:
      self.__tela_clinica.mostra_mensagem("ATENCAO: Nenhuma clínica cadastrada.")
      return
    for codigo, clinica in enumerate(self.__clinicas, start=1):
      self.__tela_clinica.mostra_clinica(self._dados_clinica(codigo, clinica))

  def excluir_clinica(self):
    if not self.__clinicas:
      self.__tela_clinica.mostra_mensagem("ATENCAO: Nenhuma clínica cadastrada.")
      return

    self.lista_clinicas()
    codigo = self.__tela_clinica.seleciona_clinica(len(self.__clinicas))
    if codigo is None:
      return
    clinica = self.pega_clinica_por_codigo(codigo)

    if clinica is None:
      self.__tela_clinica.mostra_mensagem("ATENCAO: Clínica não existente.")
      return

    if clinica.atendimentos:
      self.__tela_clinica.mostra_mensagem(
        "ATENCAO: Não é possível excluir clínica com atendimentos cadastrados."
      )
      return

    self.__clinicas.remove(clinica)
    self.__tela_clinica.mostra_mensagem("Clínica excluída com sucesso!")
    self.lista_clinicas()

  def retornar(self):
    self.__controlador_sistema.abre_tela()

  def abre_tela(self):
    lista_opcoes = {
      1: self.incluir_clinica,
      2: self.alterar_clinica,
      3: self.lista_clinicas,
      4: self.excluir_clinica,
      0: self.retornar,
    }

    while True:
      lista_opcoes[self.__tela_clinica.tela_opcoes()]()
