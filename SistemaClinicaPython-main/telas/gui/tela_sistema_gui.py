from telas.gui.tela_abstrata_gui import TelaAbstrataGUI


class TelaSistemaGUI(TelaAbstrataGUI):
  def tela_opcoes(self):
    return self._menu_botoes(
      "Sistema de Clínicas",
      [
        (1, "Clínica"),
        (2, "Pacientes"),
        (3, "Profissionais"),
        (4, "Tipos de Atendimento"),
        (5, "Atendimentos"),
        (6, "Relatórios"),
        (0, "Finalizar"),
      ],
      "Menu Principal",
    )
