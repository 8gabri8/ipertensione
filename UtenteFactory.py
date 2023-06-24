from Paziente import *
from Medico import *
from Responsabile import *

class UtenteFactory():
    # implementazione sigleton
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UtenteFactory, cls).__new__(cls)
        return cls._instance

    def crea_utente(self, tipo, ID, nome, cognome, mail, dataN, fatt_risc=None, id_med_ref=None):
        if tipo == "paziente":
            return Paziente.create_utente(ID, nome, cognome, mail, dataN, fatt_risc, id_med_ref)
        elif tipo == "medico":
            return Medico.create_utente(ID, nome, cognome, mail, dataN)
        elif tipo == "responsabile":
            return Responsabile.create_utente(ID, nome, cognome, mail, dataN)
        else:
            raise ValueError("Tipo utente non valido.")