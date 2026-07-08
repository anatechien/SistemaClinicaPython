from daos.dao import DAO

class TipoAtendimentoDAO(DAO):
    def __init__(self):
        super().__init__("tipos_atendimento.pkl")