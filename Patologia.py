from abc import ABC, abstractmethod

class Patologia(ABC):
    # costruttore
    def __init__(self, nome, id_paz, inizio):
        self.__nome= nome
        self.__id_paz = id_paz
        self.__inizio = inizio

    def get_nome(self):
        return self.__nome

    def set_nome(self, nome):
        self.__nome = nome

    def get_id_paz(self):
        return self.__id_paz

    def set_id_paz(self, id_paz):
        self.__id_paz = id_paz

    def get_inizio(self):
        return self.__inizio

    def set_inizio(self, inizio):
        self.__inizio = inizio
    

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
        if nome == "" or nome is None or nome.isdigit():
            return "Campo nome patologia non corretta"
        elif id_paz == "" or id_paz is None:
            return "Campo ID paziente non corretto"
        #elif inizio àcontrollato nel main, qiuando si controller che data di iznio sia maggiore di prima terapia ipertiensiva
        else:
            return PatConc(nome, id_paz, inizio)
        
    def to_tupla(self):
        #DB vuole (nome, id_paz, inizio, tipo, fine)
        return (self.get_nome(), self.get_id_paz(), self.get_inizio(), "conc", None)
    
    # def to_tupla_update(self):
    #     return (self.__nome , self.__inizio)
    
####################################################################################################
class PatPreg(Patologia):

    def __init__(self, nome, id_paz, inizio, fine):
        super().__init__(nome, id_paz, inizio)
        self.__fine = fine

    def get_fine(self):
        return self.__fine
    
    def set_fine(self, fine):
        self.__fine = fine
        
    #METODI ASTRATTI DA FORZARE
    @staticmethod
    def create_patologia(nome, id_paz, inizio, fine):
        if nome == "" or nome is None or nome.isdigit():
            return "Campo nome patologia non corretta"
        elif id_paz == "" or id_paz is None:
            return "Campo ID paziente non corretto"
        #elif inizio àcontrollato nel main, qiuando si controller che data di iznio sia maggiore di prima terapia ipertiensiva
        # anche fine è controllata nel controller
        else:
            return PatPreg(nome, id_paz, inizio, fine)
        
    def to_tupla(self):
        #DB vuole (nome, id_paz, inizio, tipo, fine)
        return (self.get_nome(), self.get_id_paz(), self.get_inizio(), "preg", self.__fine)
    
    # def to_tupla_update(self):
    #     #DB vuole (nome, id_paz, inizio, tipo, fine)
    #     return (self.__nome , self.__inizio, self.__fine)
    
####################################################################################################
class SegnPatConc(Patologia):

    #costruttre è stesso del apdre
    #atributo nel DB:
    # nome_pat, id_paz, inizio, tipo, fine
    #METODI ASTRATTI DA FORZARE
    @staticmethod
    def create_patologia(nome, id_paz, inizio):
        if nome == "" or nome is None or nome.isdigit():
            return "Campo nome patologia non corretta"
        elif id_paz == "" or id_paz is None:
            return "Campo ID paziente non corretto"
        #elif inizio àcontrollato nel main, qiuando si controller che data di iznio sia maggiore di prima terapia ipertiensiva
        else:
            return SegnPatConc(nome, id_paz, inizio)
        
    def to_tupla(self):
        #DB vuole (nome, id_paz, inizio, tipo, fine)
        return (self.get_nome(), self.get_id_paz(), self.get_inizio(), "segn_pat_conc", None)
    
    # def to_tupla_update(self):
    #     return (self.__nome , self.__inizio)