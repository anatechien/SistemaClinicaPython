from telas.tela_procedimento import TelaProcedimento
from models.procedimento import Procedimento


class ControladorProcedimentos:

    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_procedimento = TelaProcedimento()

def adicionar_procedimento(self):

    atendimentos = self._todos_atendimentos()

    if not atendimentos:
        self.__tela_procedimento.mostra_mensagem(
            "Nenhum atendimento cadastrado."
        )
        return

    codigo = int(input("Código do atendimento: "))

    atendimento = atendimentos[codigo - 1]

    dados = self.__tela_procedimento.pega_dados_procedimento()

    procedimento = Procedimento(
        dados["nome"],
        dados["valor"],
        dados["descricao"]
    )

    atendimento.adicionar_procedimento(
        procedimento
    )