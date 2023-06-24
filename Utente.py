from abc import ABC, abstractmethod

class Utente(ABC):
    # costruttore
    def __init__(self, ID, nome, cognome, mail, dataN):
        self.ID = ID
        #self.pws = pws #non verrà mai usata
        self.nome = nome
        self.cognome = cognome
        self.mail = mail
        self.dataN = dataN
    
    # definizione di altri metodi della classe
    # get
    def get_ID(self):
        return self.ID
    
    def get_nome(self):
        return self.nome
    
    def get_cognome(self):
        return self.cognome
    
    def get_mail(self):
        return self.mail
    
    def get_dataN(self):
        return self.dataN
    
    # metodi set
    def set_ID(self, id):
        self.ID = id
    
    def set_nome(self, nome):
        self.nome = nome
    
    def set_cognome(self, cognome):
        self.cognome = cognome
    
    def set_mail(self, mail):
        self.mail = mail
    
    def set_dataN(self, dataN):
        self.dataN = dataN
        
    #METODI ASTRATTI DA FORZARE
    @abstractmethod
    def create_utente():
        pass

    @abstractmethod
    def to_tupla(self):
        return (self.ID, self.nome, self.cognome, self.mail, self.dataN)


