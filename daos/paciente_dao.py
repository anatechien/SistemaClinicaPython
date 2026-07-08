from daos.dao import DAO

class PacienteDAO(DAO):
    def __init__(self):
        super().__init__("pacientes.pkl")