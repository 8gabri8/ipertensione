class Sintomo:
    def __init__(self, nome_sint, id_paz, inizio, tipo, fine):
        self.__nome_sint = nome_sint
        self.__id_paz = id_paz
        self.__inizio = inizio
        self.__tipo = tipo
        self.__fine = fine

    def get_nome_sint(self):
        return self.__nome_sint

    def set_nome_sint(self, nome_sint):
        self.__nome_sint = nome_sint

    def get_id_paz(self):
        return self.__id_paz

    def set_id_paz(self, id_paz):
        self.__id_paz = id_paz

    def get_inizio(self):
        return self.__inizio

    def set_inizio(self, inizio):
        self.__inizio = inizio

    def get_tipo(self):
        return self.__tipo

    def set_tipo(self, tipo):
        self.__tipo = tipo

    def get_fine(self):
        return self.__fine

    def set_fine(self, fine):
        self.__fine = fine


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
        return (self.get_nome_sint(), self.get_id_paz(), self.get_inizio(), self.get_tipo(), self.get_fine())