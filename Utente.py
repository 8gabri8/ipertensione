from abc import ABC, abstractmethod

class Utente(ABC):
    # costruttore
    def __init__(self, ID, nome, cognome, mail, dataN):
        self.__ID = ID
        #self.__pws = pws #non verrà mai usata
        self.__nome = nome
        self.__cognome = cognome
        self.__mail = mail
        self.__dataN = dataN
    
    # definizione di altri metodi della classe
    # get
    def get_ID(self):
        return self.__ID
    
    def get_nome(self):
        return self.__nome
    
    def get_cognome(self):
        return self.__cognome
    
    def get_mail(self):
        return self.__mail
    
    def get_dataN(self):
        return self.__dataN
    
    # metodi set
    def set_ID(self, id):
        self.__ID = id
    
    def set_nome(self, nome):
        self.__nome = nome
    
    def set_cognome(self, cognome):
        self.__cognome = cognome
    
    def set_mail(self, mail):
        self.__mail = mail
    
    def set_dataN(self, dataN):
        self.__dataN = dataN
        
    #METODI ASTRATTI DA FORZARE
    @abstractmethod
    def create_utente():
        pass

    @abstractmethod
    def to_tupla(self):
        return (self.get_ID(), self.get_nome(), self.get_cognome(), self.get_mail(), self.get_dataN())


