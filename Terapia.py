class Terapia:
    def __init__(self, farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine):
        self.farmaco = farmaco
        self.id_paz = id_paz
        self.inizio = inizio
        self.qtaxdose = qtaxdose
        self.ndosi = ndosi
        self.ind = ind
        self.tipo = tipo
        self.fine = fine

    # Getter methods
    def get_farmaco(self):
        return self.farmaco
    
    def get_id_paz(self):
        return self.id_paz

    def get_inizio(self):
        return self.inizio
    
    def get_qtaxdose(self):
        return self.qtaxdose
    
    def get_ndosi(self):
        return self.ndosi
    
    def get_ind(self):
        return self.ind
    
    def get_tipo(self):
        return self.tipo
    
    def get_fine(self):
        return self.fine
    
    # Setter methods
    def set_farmaco(self, farmaco):
        self.farmaco = farmaco
    
    def set_id_paz(self, id_paz):
        self.id_paz = id_paz
    
    def set_inizio(self, inizio):
        self.inizio = inizio
    
    def set_qtaxdose(self, qtaxdose):
        self.qtaxdose = qtaxdose
    
    def set_ndosi(self, ndosi):
        self.ndosi = ndosi
    
    def set_ind(self, ind):
        self.ind = ind
    
    def set_tipo(self, tipo):
        self.tipo = tipo

    def set_fine(self, fine):
        self.fine = fine

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
            return Terapia(farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine)

    # Metodo che ritorna la tupla contenente gli attributi dell'oggetto
    def to_tupla(self):
        return (self.farmaco, self.id_paz, self.inizio, self.qtaxdose, self.ndosi, self.ind, self.tipo, self.fine)
