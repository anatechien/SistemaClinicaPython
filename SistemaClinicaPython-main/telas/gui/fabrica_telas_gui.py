from telas.gui.tema_gui import configurar_tema
from telas.gui.tela_atendimento_gui import TelaAtendimentoGUI
from telas.gui.tela_clinica_gui import TelaClinicaGUI
from telas.gui.tela_paciente_gui import TelaPacienteGUI
from telas.gui.tela_profissional_gui import TelaProfissionalGUI
from telas.gui.tela_relatorio_gui import TelaRelatorioGUI
from telas.gui.tela_sistema_gui import TelaSistemaGUI
from telas.gui.tela_tipo_atendimento_gui import TelaTipoAtendimentoGUI


def criar_telas_gui():
  configurar_tema()
  return {
    "sistema": TelaSistemaGUI(),
    "clinica": TelaClinicaGUI(),
    "paciente": TelaPacienteGUI(),
    "profissional": TelaProfissionalGUI(),
    "tipo_atendimento": TelaTipoAtendimentoGUI(),
    "atendimento": TelaAtendimentoGUI(),
    "relatorio": TelaRelatorioGUI(),
  }
