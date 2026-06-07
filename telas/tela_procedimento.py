from telas.tela_abstrata import TelaAbstrata


class TelaProcedimento(TelaAbstrata):

    def tela_opcoes(self):
        print("-------- PROCEDIMENTOS ----------")
        print("1 - Adicionar Procedimento")
        print("2 - Listar Procedimentos")
        print("0 - Retornar")

        return self.le_num_inteiro(
            "Escolha a opção: ",
            [0, 1, 2]
        )

    def pega_dados_procedimento(self):

        print("-------- DADOS PROCEDIMENTO ----------")

        nome = self.le_texto("Nome: ")
        descricao = self.le_texto("Descrição: ")
        valor = self.le_float("Valor: ", minimo=0.01)

        return {
            "nome": nome,
            "descricao": descricao,
            "valor": valor
        }

    def mostra_procedimento(self, procedimento):

        print("NOME:", procedimento.nome)
        print("DESCRIÇÃO:", procedimento.descricao)
        print("VALOR:", procedimento.valor)
        print()