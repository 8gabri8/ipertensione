from Utente import *
from Paziente import *
from datetime import datetime

# classe medico
class Medico(Utente):
    def __init__(self, ID, nome, cognome, mail, dataN):
        Utente.__init__(self, ID, nome, cognome, mail, dataN)

    def set_id_paz_selezionato(self, id_paz): #passo Id paz e medico salva in se CODICO di paz selezioanto
        self.__id_paz_selezionato = id_paz

    def get_id_paz_selezionato(self): #passo Id paz e medico salva in se CODICO di paz selezioanto
        return self.__id_paz_selezionato
    
    @staticmethod
    def create_utente(ID, nome, cognome, mail, dataN):
        dataN_dt = datetime.strptime(dataN, '%Y-%m-%d').date()
        data_min_dt = datetime.strptime("1900-01-01", '%Y-%m-%d').date()
        data_oggi_dt = datetime.now().date()
        print(data_oggi_dt, dataN_dt)
     
        if(dataN_dt < data_min_dt or dataN_dt > data_oggi_dt):
            return "Data non valida!"
        elif (any(char.isdigit() for char in nome) or any(char.isdigit() for char in cognome)):
            return "Nome e cognome non possono contenere cifre!"
        elif(nome == "" or cognome == "" or mail == ""):
            return "Dati mancanti"
        else:
            return Medico(ID, nome, cognome, mail, dataN)
        
    def to_tupla(self):
        return super().to_tupla()
    
   