from telas.tela_abstrata import TelaAbstrata


class TelaPagamento(TelaAbstrata):

    def tela_opcoes(self):
        print("-------- PAGAMENTOS ----------")
        print("1 - Registrar Pagamento")
        print("2 - Listar Pagamentos")
        print("0 - Retornar")

        return self.le_num_inteiro(
            "Escolha a opção: ",
            [0, 1, 2]
        )

def pega_dados_pagamento(self):

    data = self.le_data(
        "Data do pagamento: "
    )

    valor = self.le_float(
        "Valor pago: ",
        minimo=0.01
    )

    print("1 - Dinheiro")
    print("2 - PIX")
    print("3 - Cartão")

    modalidade = self.le_num_inteiro(
        "Modalidade: ",
        [1, 2, 3]
    )

    return {
        "data": data,
        "valor": valor,
        "modalidade": modalidade
    }