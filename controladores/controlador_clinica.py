from telas.tela_clinica import TelaClinica
from models.clinica import Clinica
from daos.clinica_dao import ClinicaDAO

class ControladorClinica:
  def __init__(self, controlador_sistema, tela=None):
    self.__clinica_dao = ClinicaDAO()
    self.__tela_clinica = tela or TelaClinica()
    self.__controlador_sistema = controlador_sistema

  @property
  def clinicas(self):
    return self.__clinica_dao.get_all()

  def pega_clinica_por_codigo(self, codigo: int):
    clinicas = self.clinicas
    if 1 <= codigo <= len(clinicas):
      return clinicas[codigo - 1]
    return None

  def pega_clinica_por_nome(self, nome: str):
    for clinica in self.clinicas:
      if clinica.nome == nome:
        return clinica
    return None

  def vincular_referencias(self, resolver):
    for clinica in self.clinicas:
      for atendimento in clinica.atendimentos:
        atendimento.migrar_se_necessario()
        atendimento.vincular_resolver(resolver)

  def atualizar_persistencia(self):
    self.__clinica_dao.update()

  def atualizar_chave_paciente(self, cpf_antigo: str, cpf_novo: str):
    for clinica in self.clinicas:
      for atendimento in clinica.atendimentos:
        if atendimento.paciente_cpf == cpf_antigo:
          atendimento.atualizar_chave_paciente(cpf_novo)
        for pagamento in atendimento.pagamentos:
          if pagamento.paciente_cpf == cpf_antigo:
            pagamento.atualizar_chave_paciente(cpf_novo)
    self.atualizar_persistencia()

  def atualizar_chave_profissional(self, cpf_antigo: str, cpf_novo: str):
    for clinica in self.clinicas:
      for atendimento in clinica.atendimentos:
        if atendimento.profissional_cpf == cpf_antigo:
          atendimento.atualizar_chave_profissional(cpf_novo)
        for procedimento in atendimento.procedimentos:
          if procedimento.profissional_cpf == cpf_antigo:
            procedimento.atualizar_chave_profissional(cpf_novo)
    self.atualizar_persistencia()

  def atualizar_chave_tipo(self, nome_antigo: str, nome_novo: str):
    for clinica in self.clinicas:
      for atendimento in clinica.atendimentos:
        if atendimento.tipo_nome == nome_antigo:
          atendimento.atualizar_chave_tipo(nome_novo)
    self.atualizar_persistencia()

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
    self.__clinica_dao.add(clinica.nome, clinica)
    self.__tela_clinica.mostra_mensagem("Clínica cadastrada com sucesso!")
    self.lista_clinicas()

  def lista_clinicas(self):
    if not self.clinicas:
      self.__tela_clinica.mostra_mensagem("ATENCAO: Nenhuma clínica cadastrada.")
      return
    for codigo, clinica in enumerate(self.clinicas, start=1):
      self.__tela_clinica.mostra_clinica(self._dados_clinica(codigo, clinica))

  def alterar_clinica(self):
    if not self.clinicas:
      self.__tela_clinica.mostra_mensagem("ATENCAO: Nenhuma clínica cadastrada.")
      return
    self.lista_clinicas()
    codigo = self.__tela_clinica.seleciona_clinica(len(self.clinicas))
    if codigo is None:
      return
    clinica = self.pega_clinica_por_codigo(codigo)
    if clinica is None:
      self.__tela_clinica.mostra_mensagem("ATENCAO: Clínica não existente.")
      return
    dados = self.__tela_clinica.pega_dados_clinica(
      nome_disponivel=lambda nome: nome == clinica.nome or self.pega_clinica_por_nome(nome) is None
    )
    if dados is None:
      return

    nome_antigo = clinica.nome
    clinica.atualizar(
      dados["nome"],
      dados["cidade"],
      dados["descricao"],
      dados["horario_abertura"],
      dados["horario_fechamento"],
    )
    if dados["nome"] != nome_antigo:
      self.__clinica_dao.remove(nome_antigo)
      self.__clinica_dao.add(clinica.nome, clinica)
    else:
      self.__clinica_dao.update()
    self.lista_clinicas()

  def excluir_clinica(self):
    if not self.clinicas:
      self.__tela_clinica.mostra_mensagem("ATENCAO: Nenhuma clínica cadastrada.")
      return

    self.lista_clinicas()
    codigo = self.__tela_clinica.seleciona_clinica(len(self.clinicas))
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

    self.__clinica_dao.remove(clinica.nome)
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
      opcao = self.__tela_clinica.tela_opcoes()
      lista_opcoes[opcao]()
