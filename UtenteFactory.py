from Paziente import *
from Medico import *
from Responsabile import *

class UtenteFactory():
    # implementazione sigleton
    _instance = None

    def __new__(cls): #qui sto facendo un overridden del metodo __new__ di object (infatti tutte clasi sono sotto tipi di Object)
        if cls._instance is None:
            cls._instance = super(UtenteFactory, cls).__new__(cls)
            #.__new__(classe) --> costrusice un oggetto del tipo "classe"
                #a suo volta .__new__() chiama .__init__() che inizializza gli attributi
            #super() ritorna un oggetto padre
                #super(A, B)
                    #A --> specifica nome della sottoclasse
                    #B --Z oggetto della sotto classe

        #ALTRO MODO PER IMPLEMENTARLA
            # class Logger(object):
            #     _instance = None

            #     def __init__(self):
            #         raise RuntimeError('Call instance() instead')

            #     @classmethod
            #     def instance(cls):
            #         if cls._instance is None:
            #             print('Creating new instance')
            #             cls._instance = cls.__new__(cls)
            #             # Put any initialization here.
            #         return cls._instance


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