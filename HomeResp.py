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
            ttk.Button(self, text='Nuovo paziente', style='Custom.TButton', command=add_paz, width=30).pack(pady=10) # al posto di saluta ci fa la funzione che chiama la finestra dell'inserimento e la stampa sopra aquesta


            def add_med():
                utente.set_tipo_utente_aggiunto("M")
                controller.show_frame("AddUtente", parent, utente)
            ttk.Button(self, text='Nuovo medico', style='Custom.TButton', command=add_med, width=30).pack(pady=10) # al posto di saluta ci fa la funzione che chiama la finestra dell'inserimento e la stampa sopra aquesta

            def add_resp():
                utente.set_tipo_utente_aggiunto("R")
                controller.show_frame("AddUtente", parent, utente)  
            ttk.Button(self, text='Nuovo responsabile', style='Custom.TButton', command=add_resp, width=30).pack(pady=10) # al posto di saluta ci fa la funzione che chiama la finestra dell'inserimento e la stampa sopra aquesta

        ####TABELLA TUTTI UTENTI
            frame3 = LabelFrame(self, text="Utenti", font=controller.font)
            frame3.pack(fill="x", padx=10)
            datiC = controller.DB.my_query("SELECT * FROM UTENTE")
            #(id, nome, cognome, mail, dataN, hash_psw, fatt_risc, id_med_ref)

            colonneC = ["ID", "Nome", "Cognome", "mail", "Data di Nascita"]
            tabella_conc = ttk.Treeview(frame3, columns=colonneC, show="headings", style="Custom.Treeview") #la prima riga della tabell ha nome dellecoloenn

            tabella_conc.column('ID', anchor=CENTER, width=100)
            tabella_conc.heading('ID', text='ID')
            tabella_conc.column('Nome', anchor=CENTER, width=100)
            tabella_conc.heading('Nome', text='Nome')
            tabella_conc.column('Cognome', anchor=CENTER, width=100)
            tabella_conc.heading('Cognome', text='Cognome')
            tabella_conc.column('mail', anchor=CENTER, width=100)
            tabella_conc.heading('mail', text='mail')
            tabella_conc.column('Data di Nascita', anchor=CENTER, width=100)
            tabella_conc.heading('Data di Nascita', text='Data di Nascita')

            frame3.grid_columnconfigure(0, weight=1)
            tabella_conc.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            s2 = ttk.Scrollbar(frame3, orient=VERTICAL, command=tabella_conc.yview)
            s2.grid(row=0, column=1, sticky='ns')

            # aggiungo i record che mi ritornano dalla query
            for record in datiC:
                tabella_conc.insert('', END, values=[record[0], record[1], record[2], record[3], record[4]])
        
        
        def logout():
            controller.show_frame("StartPage", parent, utente)
        ttk.Button(self, text="Logout", command=logout, style='Custom.TButton', width=30).pack(pady=10)
