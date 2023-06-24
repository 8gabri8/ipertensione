class Sintomo:
    def __init__(self, nome_sint, id_paz, inizio, tipo, fine):
        self.nome_sint = nome_sint
        self.id_paz = id_paz
        self.inizio = inizio
        self.tipo = tipo
        self.fine = fine

    def get_nome_sint(self):
        return self.nome_sint

    def set_nome_sint(self, nome_sint):
        self.nome_sint = nome_sint

    def get_id_paz(self):
        return self.id_paz

    def set_id_paz(self, id_paz):
        self.id_paz = id_paz

    def get_inizio(self):
        return self.inizio

    def set_inizio(self, inizio):
        self.inizio = inizio

    def get_tipo(self):
        return self.tipo

    def set_tipo(self, tipo):
        self.tipo = tipo

    def get_fine(self):
        return self.fine

    def set_fine(self, fine):
        self.fine = fine


    # Metodo statico per creare un oggetto Terapia
    @staticmethod
    def create_sintomo(nome_sint, id_paz, inizio, tipo, fine):
        if nome_sint == "" or nome_sint is None or nome_sint.isdigit():
            return "Nome del sintomo non corretto"
        if tipo not in ["conc", "preg"]:
            return "Tipo non esistente"
        #controlli più spoecifici sono ftti dla controller/MViewModel
        else:
            return Sintomo(nome_sint, id_paz, inizio, tipo, fine)

    # Metodo che ritorna la tupla contenente gli attributi dell'oggetto
    def to_tupla(self):
        return (self.nome_sint, self.id_paz, self.inizio, self.tipo, self.fine)