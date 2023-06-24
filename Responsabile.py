from Utente import *
from datetime import datetime

# classe responsabile
class Responsabile(Utente):
    def __init__(self, ID, nome, cognome, mail, dataN):
        Utente.__init__(self, ID, nome, cognome, mail, dataN)
        
    # metodi get
    def get_tipo_utente_aggiunto(self):
        return self.tipo_utente_aggiunto
    
    # metodi set
    def set_tipo_utente_aggiunto(self, tipo_utente_aggiunto):
        self.tipo_utente_aggiunto = tipo_utente_aggiunto
    
    @staticmethod
    def create_utente(ID, nome, cognome, mail, dataN):
        dataN_dt = datetime.strptime(dataN, '%Y-%m-%d').date()
        data_min_dt = datetime.strptime("1900-01-01", '%Y-%m-%d').date()
        data_oggi_dt = datetime.now().date()
     
        if(dataN_dt < data_min_dt or dataN_dt > data_oggi_dt):
            return "Data non valida!"
        elif (any(char.isdigit() for char in nome) or any(char.isdigit() for char in cognome)):
            return "Nome e cognome non possono contenere cifre!"
        elif(nome == "" or cognome == "" or mail == ""):
            return "Dati mancanti"
        else:
            return Responsabile(ID, nome, cognome, mail, dataN)
        
    def to_tupla(self):
        return super().to_tupla()