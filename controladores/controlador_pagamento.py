from telas.tela_pagamento import TelaPagamento
from models.pagamento import (
    PagamentoDinheiro,
    PagamentoPix,
    PagamentoCartaoCredito
)


def registrar_pagamento(self):

    atendimentos = self._todos_atendimentos()

    codigo = int(
        input("Código do atendimento: ")
    )

    atendimento = atendimentos[codigo - 1]

    dados = self.__tela_pagamento.pega_dados_pagamento()

    if dados["modalidade"] == 1:

        pagamento = PagamentoDinheiro(
            dados["data"],
            atendimento,
            atendimento.paciente,
            dados["valor"]
        )

    elif dados["modalidade"] == 2:

        cpf = input(
            "CPF do pagador: "
        )

        pagamento = PagamentoPix(
            dados["data"],
            atendimento,
            atendimento.paciente,
            dados["valor"],
            cpf
        )

    else:

        numero = input(
            "Número do cartão: "
        )

        bandeira = input(
            "Bandeira: "
        )

        pagamento = PagamentoCartaoCredito(
            dados["data"],
            atendimento,
            atendimento.paciente,
            dados["valor"],
            numero,
            bandeira
        )

    atendimento.adicionar_pagamento(
        pagamento
    )