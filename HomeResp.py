from my_library import *
from tkinter import messagebox

class HomeResp(tk.Frame):

    def __init__(self, parent, controller, utente): #utente è medico
        tk.Frame.__init__(self, parent)
        self.controller = controller

        if(utente != None):

            # aggiungo il bottone che permette di aggiungere un nuovo utente
            Label(self, text='Inserisci utente', foreground='black', font=('Helvetica', 30)).pack()

            def add_paz():
                utente.set_tipo_utente_aggiunto("P")
                controller.show_frame("AddUtente", parent, utente)
            b1 = ttk.Button(self, text='Nuovo paziente', style='Custom.TButton', command=add_paz) # al posto di saluta ci fa la funzione che chiama la finestra dell'inserimento e la stampa sopra aquesta
            b1.pack(pady=10)

            def add_med():
                utente.set_tipo_utente_aggiunto("M")
                controller.show_frame("AddUtente", parent, utente)
            b2 = ttk.Button(self, text='Nuovo medico', style='Custom.TButton', command=add_med) # al posto di saluta ci fa la funzione che chiama la finestra dell'inserimento e la stampa sopra aquesta
            b2.pack(pady=10)

            def add_resp():
                utente.set_tipo_utente_aggiunto("R")
                controller.show_frame("AddUtente", parent, utente)  
            b3 = ttk.Button(self, text='Nuovo responsabile', style='Custom.TButton', command=add_resp) # al posto di saluta ci fa la funzione che chiama la finestra dell'inserimento e la stampa sopra aquesta
            b3.pack(pady=10)

        def logout():
            controller.show_frame("StartPage", parent, utente)
        ttk.Button(self, text="Logout", command=logout, style='Custom.TButton',).pack(padx=10)
