import FreeSimpleGUI as sg

TEMA = "SandyBeach"
_tema_configurado = False


def configurar_tema():
  global _tema_configurado
  if _tema_configurado:
    return

  sg.theme(TEMA)
  _tema_configurado = True
