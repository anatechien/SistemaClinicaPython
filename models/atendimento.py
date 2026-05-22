from datetime import datetime

from paciente import Paciente
from profissional import ProfissionalSaude
from clinica import Clinica
from tipo_atendimento import TipoAtendimento
from procedimento import Procedimento
from pagamento import Pagamento


class Atendimento:
    def __init__(
            self,
            paciente: Paciente,
            profissional: ProfissionalSaude,
            clinica: Clinica,
            tipo_atendimento: TipoAtendimento,
            data_hora: datetime
    ):
            if not paciente.pode_ser_atendido():
                raise ValueError("O paciente deve ter mais de 18 anos.")
            
            horario = data_hora.time()

            if not clinica.esta_em_funcionamento(data_hora.time()):
                raise ValueError("O atendimento deve ocorrer dentro do horario da clinica")
            
            self.__paciente = paciente
            self.__profissional = profissional
            self.__clinica = clinica
            self.__tipo_atendimento = tipo_atendimento
            self.__data_hora = data_hora

            self.__procedimentos = []
            self.__pagamentos = []

    @property
    def paciente(self):
        return self.__paciente

    @property
    def profissional(self):
        return self.__profissional

    @property
    def clinica(self):
        return self.__clinica

    @property
    def tipo_atendimento(self):
        return self.__tipo_atendimento

    @property
    def data_hora(self):
        return self.__data_hora

    @property
    def procedimentos(self):
        return self.__procedimentos

    @property
    def pagamentos(self):
        return self.__pagamentos

    @paciente.setter
    def paciente(self, paciente: Paciente):
        self.__paciente = paciente

    @profissional.setter
    def profissional(self, profissional: ProfissionalSaude):
        self.__profissional = profissional

    @clinica.setter
    def clinica(self, clinica: Clinica):
        self.__clinica = clinica

    @tipo_atendimento.setter
    def tipo_atendimento(self, tipo_atendimento: TipoAtendimento):
        self.__tipo_atendimento = tipo_atendimento

    @data_hora.setter
    def data_hora(self, data_hora: datetime):
        self.__data_hora = data_hora

    def adicionar_procedimento(self, procedimento: Procedimento):
        self.__procedimentos.append(procedimento)

    def adicionar_pagamento(self, pagamento: Pagamento):
        self.__pagamentos.append(pagamento)

    def calcular_valor_total(self):
        total = 0

        for procedimento in self.__procedimentos:
            total += procedimento.valor

        return total