from daos.dao import DAO

class ClinicaDAO(DAO):
    def __init__(self):
        super().__init__("clinicas.pkl")