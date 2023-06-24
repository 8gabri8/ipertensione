from abc import ABC, abstractmethod

class Patologia(ABC):
    # costruttore
    def __init__(self, nome, id_paz, inizio):
        self.nome= nome
        self.id_paz = id_paz
        self.inizio = inizio

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def get_id_paz(self):
        return self.id_paz

    def set_id_paz(self, id_paz):
        self.id_paz = id_paz

    def get_inizio(self):
        return self.inizio

    def set_inizio(self, inizio):
        self.inizio = inizio
    

    #METODI ASTRATTI DA FORZARE
    @abstractmethod
    def create_patologia():
        pass
    
    @abstractmethod
    def to_tupla(self):
        pass
    
###################################################################################################à

class PatConc(Patologia):

    #costruttre è stesso del apdre

    #METODI ASTRATTI DA FORZARE
    @staticmethod
    def create_patologia(nome, id_paz, inizio):
        if():
            pass
        else:
            return PatConc(nome, id_paz, inizio)
        
    def to_tupla(self):
        #DB vuole (nome, id_paz, inizio, tipo, fine)
        return (self.nome, self.id_paz, self.inizio, "conc", None)
    
    def to_tupla_update(self):
        return (self.nome , self.inizio)
    
####################################################################################################
class PatPreg(Patologia):

    def __init__(self, nome, id_paz, inizio, fine):
        super().__init__(nome, id_paz, inizio)
        self.fine = fine

    def get_fine(self):
        return self.fine
    
    def set_fine(self, fine):
        self.fine = fine
        
    #METODI ASTRATTI DA FORZARE
    @staticmethod
    def create_patologia(nome, id_paz, inizio, fine):
        if():
            pass
        else:
            return PatPreg(nome, id_paz, inizio, fine)
        
    def to_tupla(self):
        #DB vuole (nome, id_paz, inizio, tipo, fine)
        return (self.nome, self.id_paz, self.inizio, "preg", self.fine)
    
    def to_tupla_update(self):
        #DB vuole (nome, id_paz, inizio, tipo, fine)
        return (self.nome , self.inizio, self.fine)
    
####################################################################################################
class SegnPatConc(Patologia):

    #costruttre è stesso del apdre
    #atributo nel DB:
    # nome_pat, id_paz, inizio, tipo, fine
    #METODI ASTRATTI DA FORZARE
    @staticmethod
    def create_patologia(nome, id_paz, inizio):
        if():
            pass
        else:
            return SegnPatConc(nome, id_paz, inizio)
        
    def to_tupla(self):
        #DB vuole (nome, id_paz, inizio, tipo, fine)
        return (self.nome, self.id_paz, self.inizio, "segn_pat_conc", None)
    
    def to_tupla_update(self):
        return (self.nome , self.inizio)