from exceptions.paciente_menor_idade_exception import PacienteMenorDeIdadeException
from exceptions.paciente_repetido_exception import PacienteRepetidoException
from telas.tela_paciente import TelaPaciente
from models.paciente import Paciente


class ControladorPacientes:
  def __init__(self, controlador_sistema):
    self.__pacientes = []
    self.__tela_paciente = TelaPaciente()
    self.__controlador_sistema = controlador_sistema

  @property
  def pacientes(self):
    return self.__pacientes

  def pega_paciente_por_cpf(self, cpf: str):
    for paciente in self.__pacientes:
      if paciente.cpf == cpf:
        return paciente
    return None

  def _dados_paciente(self, paciente: Paciente):
    return {
      "nome": paciente.nome,
      "celular": paciente.celular,
      "cpf": paciente.cpf,
      "data_nascimento": paciente.data_nascimento.strftime("%d/%m/%Y"),
    }

  def _garantir_cpf_disponivel(self, cpf: str, cpf_atual: str = None):
    if self.pega_paciente_por_cpf(cpf) is not None and cpf != cpf_atual:
      raise PacienteRepetidoException(cpf)

  def incluir_paciente(self):
    while True:
      dados = self.__tela_paciente.pega_dados_paciente()
      try:
        self._garantir_cpf_disponivel(dados["cpf"])
        paciente = Paciente(
          dados["nome"],
          dados["celular"],
          dados["cpf"],
          dados["data_nascimento"],
        )
        self.__pacientes.append(paciente)
        self.__tela_paciente.mostra_mensagem("Paciente cadastrado com sucesso!")
        break
      except (PacienteRepetidoException, PacienteMenorDeIdadeException) as erro:
        self.__tela_paciente.mostra_mensagem(f"ATENCAO: {erro}")

  def alterar_paciente(self):
    if not self.__pacientes:
      self.__tela_paciente.mostra_mensagem("ATENCAO: Nenhum paciente cadastrado.")
      return

    while True:
      self.lista_pacientes()
      cpf = self.__tela_paciente.seleciona_paciente()
      paciente = self.pega_paciente_por_cpf(cpf)
      if paciente is not None:
        break
      self.__tela_paciente.mostra_mensagem("ATENCAO: Paciente não existente. Tente novamente.")

    while True:
      dados = self.__tela_paciente.pega_dados_paciente()
      try:
        self._garantir_cpf_disponivel(dados["cpf"], paciente.cpf)
        paciente.atualizar(
          dados["nome"],
          dados["celular"],
          dados["data_nascimento"],
        )
        self.lista_pacientes()
        break
      except (PacienteRepetidoException, PacienteMenorDeIdadeException) as erro:
        self.__tela_paciente.mostra_mensagem(f"ATENCAO: {erro}")

  def lista_pacientes(self):
    if not self.__pacientes:
      self.__tela_paciente.mostra_mensagem("ATENCAO: Nenhum paciente cadastrado.")
      return
    for paciente in self.__pacientes:
      self.__tela_paciente.mostra_paciente(self._dados_paciente(paciente))

  def excluir_paciente(self):
    if not self.__pacientes:
      self.__tela_paciente.mostra_mensagem("ATENCAO: Nenhum paciente cadastrado.")
      return

    while True:
      self.lista_pacientes()
      cpf = self.__tela_paciente.seleciona_paciente()
      paciente = self.pega_paciente_por_cpf(cpf)
      if paciente is not None:
        self.__pacientes.remove(paciente)
        self.lista_pacientes()
        return
      self.__tela_paciente.mostra_mensagem("ATENCAO: Paciente não existente. Tente novamente.")

  def retornar(self):
    self.__controlador_sistema.abre_tela()

  def abre_tela(self):
    lista_opcoes = {
      1: self.incluir_paciente,
      2: self.alterar_paciente,
      3: self.lista_pacientes,
      4: self.excluir_paciente,
      0: self.retornar,
    }

    while True:
      lista_opcoes[self.__tela_paciente.tela_opcoes()]()
