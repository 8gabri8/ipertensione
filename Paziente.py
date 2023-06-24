from Utente import *
from datetime import datetime

# faccio una prova con la classe Paziente
class Paziente(Utente):
    def __init__(self, ID, nome, cognome, mail, dataN, fatt_risc, id_med_ref):
        Utente.__init__(self, ID, nome, cognome, mail, dataN)
        
        self.fatt_risc = fatt_risc
        self.id_med_ref = id_med_ref

    # metodi get
    def get_fatt_risc(self):
        return self.fatt_risc
    def get_id_med_ref(self):
        return self.id_med_ref

    # metodi set
    def set_fatt_risc(self, fatt_risc):
        self.fatt_risc = fatt_risc
    def set_id_med_ref(self, id_med_ref):
        self.id_med_ref = id_med_ref

    @staticmethod
    #NB dataN è stringa!!!
    def create_utente(ID, nome, cognome, mail, dataN, fatt_risc, id_med_ref):
        dataN_dt = datetime.strptime(dataN, '%Y-%m-%d').date()
        data_min_dt = datetime.strptime("1900-01-01", '%Y-%m-%d').date()
        data_oggi_dt = datetime.now().date()
     
        if(dataN_dt < data_min_dt or dataN_dt > data_oggi_dt):
            return "Data non valida!"
        elif (any(char.isdigit() for char in nome) or any(char.isdigit() for char in cognome)):
            return "Nome e cognome non possono contenere cifre!"
        elif(nome == "" or cognome == "" or mail == "" or id_med_ref == ""):
            return "Dati mancanti"
        else:
            return Paziente(ID, nome, cognome, mail, dataN, fatt_risc, id_med_ref)
        
        #controllo su id_med_ref non serve perchè il combo box fornisc egià le scletre possbili
        
    def to_tupla(self):
        return super().to_tupla() + (self.fatt_risc, self.id_med_ref)
    
    
   