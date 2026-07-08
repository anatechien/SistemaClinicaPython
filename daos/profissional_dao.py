from daos.dao import DAO

class ProfissionalDAO(DAO):
    def __init__(self):
        super().__init__("profissionais.pkl")