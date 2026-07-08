from controladores.controlador_sistema import ControladorSistema
from telas.gui.fabrica_telas_gui import criar_telas_gui
from telas.gui.tema_gui import configurar_tema


if __name__ == "__main__":
  configurar_tema()
  ControladorSistema(telas=criar_telas_gui()).inicializa_sistema()
