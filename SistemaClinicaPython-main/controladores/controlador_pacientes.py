from exceptions.paciente_menor_idade_exception import PacienteMenorDeIdadeException
from exceptions.paciente_repetido_exception import PacienteRepetidoException
from telas.tela_paciente import TelaPaciente
from models.paciente import Paciente
from daos.paciente_dao import PacienteDAO

class ControladorPacientes:
  def __init__(self, controlador_sistema, tela=None):
    self.__paciente_dao = PacienteDAO()
    self.__tela_paciente = tela or TelaPaciente()
    self.__controlador_sistema = controlador_sistema

  @property
  def pacientes(self):
    return self.__paciente_dao.get_all()

  def pega_paciente_por_cpf(self, cpf: str):
    return self.__paciente_dao.get(cpf)

  def _dados_paciente(self, paciente: Paciente):
    responsavel_str = f" (Acomp.: {paciente.responsavel})" if paciente.responsavel else ""
    return {
      "nome": paciente.nome + responsavel_str,
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
      if dados is None:
        return
      try:
        self._garantir_cpf_disponivel(dados["cpf"])
        
        responsavel = dados.get("responsavel", None)
        
        try:
          paciente = Paciente(
            dados["nome"],
            dados["celular"],
            dados["cpf"],
            dados["data_nascimento"],
            responsavel=responsavel
          )
          self.__paciente_dao.add(paciente.cpf, paciente)
          self.__tela_paciente.mostra_mensagem("Paciente cadastrado com sucesso!")
          break
        except PacienteMenorDeIdadeException:
          self.__tela_paciente.mostra_mensagem("AVISO: Paciente menor de idade necessita de um adulto responsável!")
          
          if hasattr(self.__tela_paciente, 'pega_responsavel'):
            resp = self.__tela_paciente.pega_responsavel()
          else:
            resp = dados.get("responsavel")
          
          if resp:
            paciente = Paciente(
              dados["nome"],
              dados["celular"],
              dados["cpf"],
              dados["data_nascimento"],
              responsavel=resp
            )
            self.__paciente_dao.add(paciente.cpf, paciente)
            self.__tela_paciente.mostra_mensagem("Paciente menor cadastrado com sucesso acompanhado de responsável!")
            break
          else:
            self.__tela_paciente.mostra_mensagem("Cadastro cancelado por falta de responsável legal.")
            break
            
      except (PacienteRepetidoException, PacienteMenorDeIdadeException) as erro:
        self.__tela_paciente.mostra_mensagem(f"ATENCAO: {erro}")

  def alterar_paciente(self):
    if not self.pacientes:
      self.__tela_paciente.mostra_mensagem("ATENCAO: Nenhum paciente cadastrado.")
      return

    while True:
      self.lista_pacientes()
      cpf = self.__tela_paciente.seleciona_paciente()
      if cpf is None:
        return
      paciente = self.pega_paciente_por_cpf(cpf)
      if paciente is None:
        self.__tela_paciente.mostra_mensagem("ATENCAO: Paciente não existente. Tente novamente.")
        continue

      dados = self.__tela_paciente.pega_dados_paciente()
      if dados is None:
        return
      try:
        self._garantir_cpf_disponivel(dados["cpf"], paciente.cpf)
        responsavel = dados.get("responsavel", paciente.responsavel)
        
        cpf_antigo = paciente.cpf
        paciente.atualizar(
          dados["nome"],
          dados["celular"],
          dados["data_nascimento"],
          responsavel=responsavel
        )
        
        if dados["cpf"] != cpf_antigo:
          paciente.cpf = dados["cpf"]
          self.__paciente_dao.remove(cpf_antigo)
          self.__paciente_dao.add(paciente.cpf, paciente)
        else:
          self.__paciente_dao.update()
          
        self.lista_pacientes()
        break
      except (PacienteRepetidoException, PacienteMenorDeIdadeException) as erro:
        self.__tela_paciente.mostra_mensagem(f"ATENCAO: {erro}")

  def lista_pacientes(self):
    if not self.pacientes:
      self.__tela_paciente.mostra_mensagem("ATENCAO: Nenhum paciente cadastrado.")
      return
    for paciente in self.pacientes:
      self.__tela_paciente.mostra_paciente(self._dados_paciente(paciente))

  def excluir_paciente(self):
    if not self.pacientes:
      self.__tela_paciente.mostra_mensagem("ATENCAO: Nenhum paciente cadastrado.")
      return

    while True:
      self.lista_pacientes()
      cpf = self.__tela_paciente.seleciona_paciente()
      if cpf is None:
        return
      paciente = self.pega_paciente_por_cpf(cpf)
      if paciente is not None:
        self.__paciente_dao.remove(paciente.cpf)
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
      opcao = self.__tela_paciente.tela_opcoes()
      lista_opcoes[opcao]()