class Terapia:
    def __init__(self, farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine):
        self.__farmaco = farmaco
        self.__id_paz = id_paz
        self.__inizio = inizio
        self.__qtaxdose = qtaxdose
        self.__ndosi = ndosi
        self.__ind = ind
        self.__tipo = tipo
        self.__fine = fine

    # Getter methods
    def get_farmaco(self):
        return self.__farmaco
    
    def get_id_paz(self):
        return self.__id_paz

    def get_inizio(self):
        return self.__inizio
    
    def get_qtaxdose(self):
        return self.__qtaxdose
    
    def get_ndosi(self):
        return self.__ndosi
    
    def get_ind(self):
        return self.__ind
    
    def get_tipo(self):
        return self.__tipo
    
    def get_fine(self):
        return self.__fine
    
    # Setter methods
    def set_farmaco(self, farmaco):
        self.__farmaco = farmaco
    
    def set_id_paz(self, id_paz):
        self.__id_paz = id_paz
    
    def set_inizio(self, inizio):
        self.__inizio = inizio
    
    def set_qtaxdose(self, qtaxdose):
        self.__qtaxdose = qtaxdose
    
    def set_ndosi(self, ndosi):
        self.__ndosi = ndosi
    
    def set_ind(self, ind):
        self.ind = ind
    
    def set_tipo(self, tipo):
        self.__tipo = tipo

    def set_fine(self, fine):
        self.__fine = fine

    # Metodo statico per creare un oggetto Terapia
    @staticmethod
    def create_terapia(farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine):
        if farmaco == "" or farmaco is None or farmaco.isdigit():
            return "Campo farmaco non corretto"
        elif qtaxdose == "" or qtaxdose is None or qtaxdose.isdigit():
            return "Campo quantità per dose non corretto, deve essere una stirnga, es: \"2 pastiglie\""
        elif ndosi == "" or ndosi is None or not ndosi.isdigit():
            return "Il numero di dosi deve essere un numero intero"
        elif int(ndosi) > 4:
            return "Il numero massimo di dosi gionaliere è 4"
        else:
            print(ndosi, type(ndosi))
            print((farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine))
            return Terapia(farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine)

    # Metodo che ritorna la tupla contenente gli attributi dell'oggetto
    def to_tupla(self):
        return (self.get_farmaco(), self.get_id_paz(), self.get_inizio(), self.get_qtaxdose(), self.get_ndosi(), self.get_ind(), self.get_tipo(), self.get_fine())
