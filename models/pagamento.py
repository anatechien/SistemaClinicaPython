from abc import ABC
from datetime import date

from paciente import Paciente

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from atendimento import Atendimento
        


class Pagamento(ABC):


    def __init__(
            self,
            data_pagamento: date,
            atendimento: 'Atendimento',
            paciente: Paciente,
            valor_pago: float
            
    ):
            if data_pagamento > atendimento.data_hora.date():
                  raise ValueError("O pagamento deve ser realizado antes da data do atendimento!")
            

            self.__data_pagamento = data_pagamento
            self.__atendimento = atendimento
            self.__paciente = paciente
            self.__valor_pago = valor_pago

    @property
    def data_pagamento(self):
          return self.__data_pagamento
    
    @property
    def atendimento(self):
          return self.__atendimento
    
    @property
    def paciente(self):
        return self.__paciente
    
    @property
    def valor_pago(self):
        return self.__valor_pago

    @data_pagamento.setter
    def data_pagamento(self, data_pagamento: date):
        self.__data_pagamento = data_pagamento

    @valor_pago.setter
    def valor_pago(self, valor_pago: float):
        self.__valor_pago = valor_pago

    def calcular_valor_restante(self):
        total = self.__atendimento.calcular_valor_total()
              
        total_pago = 0

        for pagamento in self.__atendimento.pagamentos:
            total_pago += pagamento.valor_pago

        return total - total_pago
    

class PagamentoPix(Pagamento):
    def __init__(
        self,
        data_pagamento: date,
        atendimento: 'Atendimento',
        paciente: Paciente,
        valor_pago: float,
        cpf_pagador: str
    ):

        super().__init__(
            data_pagamento,
            atendimento,
            paciente,
            valor_pago
        )

        self.__cpf_pagador = cpf_pagador

    @property
    def cpf_pagador(self):
        return self.__cpf_pagador

    @cpf_pagador.setter
    def cpf_pagador(self, cpf_pagador: str):
        self.__cpf_pagador = cpf_pagador

class PagamentoDinheiro(Pagamento):
    def __init__(
        self,
        data_pagamento,
        atendimento: 'Atendimento',
        paciente,
        valor_pago
    ):
        super().__init__(
            data_pagamento,
            atendimento,
            paciente,
            valor_pago
        )

class PagamentoCartaoCredito(Pagamento):
    def __init__(
        self,
        data_pagamento,
        atendimento: 'Atendimento',
        paciente,
        valor_pago,
        numero_cartao: str,
        bandeira: str
    ):

        super().__init__(
            data_pagamento,
            atendimento,
            paciente,
            valor_pago
        )

        self.__numero_cartao = numero_cartao
        self.__bandeira = bandeira

    @property
    def numero_cartao(self):
        return self.__numero_cartao

    @property
    def bandeira(self):
        return self.__bandeira

    @numero_cartao.setter
    def numero_cartao(self, numero_cartao: str):
        self.__numero_cartao = numero_cartao

    @bandeira.setter
    def bandeira(self, bandeira: str):
        self.__bandeira = bandeira