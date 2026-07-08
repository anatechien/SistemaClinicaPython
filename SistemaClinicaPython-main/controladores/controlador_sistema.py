from controladores.controlador_atendimento import ControladorAtendimentos
from controladores.controlador_clinica import ControladorClinica
from controladores.controlador_pacientes import ControladorPacientes
from controladores.controlador_profissionais import ControladorProfissionais
from controladores.controlador_relatorios import ControladorRelatorios
from controladores.controlador_tipos_atendimento import ControladorTiposAtendimento
from telas.tela_sistema import TelaSistema


class ControladorSistema:
  def __init__(self, telas=None):
    telas = telas or {}
    self.__tela_sistema = telas.get("sistema", TelaSistema())
    self.__controlador_clinica = ControladorClinica(self, telas.get("clinica"))
    self.__controlador_pacientes = ControladorPacientes(self, telas.get("paciente"))
    self.__controlador_profissionais = ControladorProfissionais(self, telas.get("profissional"))
    self.__controlador_tipos_atendimento = ControladorTiposAtendimento(
      self, telas.get("tipo_atendimento")
    )
    self.__controlador_atendimentos = ControladorAtendimentos(self, telas.get("atendimento"))
    self.__controlador_relatorios = ControladorRelatorios(self, telas.get("relatorio"))

  @property
  def controlador_clinica(self):
    return self.__controlador_clinica

  @property
  def controlador_pacientes(self):
    return self.__controlador_pacientes

  @property
  def controlador_profissionais(self):
    return self.__controlador_profissionais

  @property
  def controlador_tipos_atendimento(self):
    return self.__controlador_tipos_atendimento

  @property
  def controlador_atendimentos(self):
    return self.__controlador_atendimentos

  def inicializa_sistema(self):
    self.abre_tela()

  def abre_menu_clinica(self):
    self.__controlador_clinica.abre_tela()

  def abre_menu_pacientes(self):
    self.__controlador_pacientes.abre_tela()

  def abre_menu_profissionais(self):
    self.__controlador_profissionais.abre_tela()

  def abre_menu_tipos_atendimento(self):
    self.__controlador_tipos_atendimento.abre_tela()

  def abre_menu_atendimentos(self):
    self.__controlador_atendimentos.abre_tela()

  def abre_menu_relatorios(self):
    self.__controlador_relatorios.abre_tela()

  def encerra_sistema(self):
    exit(0)

  def abre_tela(self):
    lista_opcoes = {
      1: self.abre_menu_clinica,
      2: self.abre_menu_pacientes,
      3: self.abre_menu_profissionais,
      4: self.abre_menu_tipos_atendimento,
      5: self.abre_menu_atendimentos,
      6: self.abre_menu_relatorios,
      0: self.encerra_sistema,
    }

    while True:
      opcao = self.__tela_sistema.tela_opcoes()
      lista_opcoes[opcao]()
