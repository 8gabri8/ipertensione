class Segnalazione():
    # costruttore
    #una segnala zione creata in questa classe può essere solo: no_segue, p_anomala
    def __init__(self, data, id_paz, tipo, gravita): 
        #cod serve solo per DB 
        self.__data = data
        self.__id_paz = id_paz
        self.__tipo = tipo
        self.__gravita = gravita
    
    # getter methods
    def get_data(self):
        return self.__data

    def get_id_paz(self):
        return self.__id_paz

    def get_tipo(self):
        return self.__tipo
    
    def get_gravita(self):
        return self.__gravita

    # setter methodas
    def set_data(self, data):
        self.__data = data

    def set_id_paz(self, id_paz):
        self.__id_paz = id_paz

    def set_tipo(self, tipo):
        self.__tipo = tipo

    def set_gravita(self, gravita):
        self.__gravita = gravita

    @staticmethod
    def create_segnalazione(data, id_paz, tipo, gravita):
        # if (): #essendo ter_conc , farmaco NON deve essere scelto da dizionario
        #     pass
        # if tipo not in ["conc", "preg"]:
        #     return "Tipo non esistente"
        if tipo == "" or tipo is None or tipo.isdigit() or tipo not in ["p_anomala", "no_segue"]:
            return "Campo tipo non corretto"
        elif id_paz == "" or id_paz is None:
            return "Campo ID paziente non corretto"
        #elif data àcontrollato nel main, inoltre è sempre data odierna 
        #elif gravità àcontrollato nel main, qiuando si controller che data di iznio sia maggiore di prima terapia ipertiensiva
        else:
            return Segnalazione(data, id_paz, tipo, gravita)

    def to_tupla(self):
        return (self.get_data(), self.get_id_paz(), self.get_tipo(), self.get_gravita())

























































###########################################################################################################################################

# class SegnAggTerConc(Segnalazione):
#     # costruttore
#     def __init__(self, data, id_paz, tipo, farmaco, qtaxdose, ndosi, ind, inizio):
#         super().__init__(data, id_paz, tipo)
#         self.inizio = inizio
#         self.farmaco = farmaco
#         self.qtaxdose = qtaxdose
#         self.ndosi = ndosi
#         self.ind = ind

#     # Getter methods
#     def get_inizio(self):
#         return self._inizio

#     def get_farmaco(self):
#         return self._farmaco

#     def get_qtaxdose(self):
#         return self._qtaxdose

#     def get_ndosi(self):
#         return self._ndosi

#     def get_ind(self):
#         return self._ind

#     # Setter methods
#     def set_inizio(self, inizio):
#         self.inizio = inizio

#     def set_farmaco(self, farmaco):
#         self.farmaco = farmaco

#     def set_qtaxdose(self, qtaxdose):
#         self.qtaxdose = qtaxdose

#     def set_ndosi(self, ndosi):
#         self.ndosi = ndosi

#     def set_ind(self, ind):
#         self.ind = ind

#     @staticmethod
#     def create_segnalazione(data, id_paz, tipo, farmaco, qtaxdose, ndosi, ind, inizio):
#         if (farmaco == "" and farmaco is None and farmaco.isdigit()): #essendo ter_conc , farmaco NON deve essere scelto da dizionario
#             return "Campo farmaco non è corretto"
#         elif (qtaxdose == "" and qtaxdose is None and qtaxdose.isdigit()):
#             return "Campo qtaxdose non è corretto"
#         elif (ndosi == "" and ndosi is None and not ndosi.isdigit()):
#             return "Il numero di dosi deve essere un numero"
#         elif int(ndosi) > 4:
#             return "Il numero massimo di dosi gionaliere è 4"
#         else:
#             return SegnAggTerConc(data, id_paz, tipo, farmaco, qtaxdose, ndosi, ind, inizio)
            
#     def to_tupla(self):
#         return super().to_tupla() + (None, None, None, self.farmaco, self.qtaxdose, self.ndosi, self.ind, self.inizio)
    
#############################################################################################################################

# Segnalazione aggiunta patologia concomitatntenome, inixio
# class SegnAggPatConc(Segnalazione):
#     # costruttore
#     def __init__(self, data, id_paz, tipo, nome, inizio):
#         super().__init__(data, id_paz, tipo, None) #lui non ha gravità
#         self.inizio = inizio
#         self.nome = nome

#     def get_nome(self):
#         return self.nome
    
#     def get_inizio(self):
#         return self.inizio

#     def set_nome(self, nome):
#         self.nome = nome

#     def set_inzio(self, inizio):
#         self.inizio = inizio

#     @staticmethod
#     def create_segnalazione(data, id_paz, tipo, nome, inizio):
#         if (nome == "" and nome is None and nome.isdigit()): #essendo ter_conc , farmaco NON deve essere scelto da dizionario
#             return "Campo nome terapia non è corretto"
#         #controll su inizio!!!!!!!!!!!!! NO prima di essere nato, NO dopo di oggi
#         else:
#             return SegnAggPatConc(data, id_paz, tipo, nome, inizio)
            
#     def to_tupla(self):
#         #super: (self.data, self.id_paz, self.tipo, self.gravita)
#         return super().to_tupla() + (None, self.nome, self.inizio, None, None, None, None, None)
    
#     def to_tupla_segn_occ_pat(self):
#         return (self.nome, self.id_paz, self.inizio, self.tipo, None) #la fine non è data


############################################################################################################################

# class SegPressAn(Segnalazione):
#     def __init__(self, cod, data, id_paz, id_med, gravita):
#         super().__init__(cod, data, id_paz, id_med)
#         self.gravita = gravita

#     # getter
#     def get_gravita(self):
#         return self._gravita

#     # setter
#     def set_gravita(self, gravita):
#         self.gravita = gravita

#     # override
#     def create_segnalazione(self, cod, data, id_paz, id_med, gravita):
#         #non devo controllare nulla perchè tutto messo dal sistema, utente non può isneire questi valoir, quindi non si può absagliare
#         self.__init__(cod, data, id_paz, id_med, gravita)

#     # metodo che ritona la tupla contenente gli attributo dell'oggetto
#     def to_tupla(self):
#         return super().to_tupla() + (self.gravita)  