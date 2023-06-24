from my_library import *
from Paziente import *
from Medico import *
from Responsabile import *
import random

class AddUtente(tk.Frame):
    def __init__(self, parent, controller, utente):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # devo inserire delle etichette delle entry
        if (utente != None):
            #fare controlli su dati iseiti!!!!!!!!!!!!!
            Label(self, text='Dati Utente', foreground='black', font=('Helvetica', 30)).pack()                
            
            #prednere codice non ancora usato
            dati = controller.DB.my_query(f"SELECT ID FROM UTENTE WHERE ID LIKE '{utente.get_tipo_utente_aggiunto()}%'", None)

            codici = []
            for id in dati:
                codici.append(int(id[0][1:])) #metto utta la aprte numerica dei codicei, delgfi utenti fià presenti sul db
            
            def numero_non_presente(lista):
                numero = random.randint(0, 999999)  # Genera un numero casuale compreso tra 1 e 100
                while numero in lista:
                    numero = random.randint(0, 999999)
                return numero
            
            id = numero_non_presente(codici)

            id = f"{utente.get_tipo_utente_aggiunto()}{id:06}" #nuovo id

            Label(self, text=f'Codice:\t{id}', foreground='black', font=controller.font).pack()

            psw = id.lower() #pasw è id in minuscolo self, text="Inserisci ID:" ,foreground="black", font=controller.font
            Label(self, text=f'psw:\t{psw}', foreground='black', font=controller.font).pack()

            Label(self, text="Nome:" ,foreground="black", font=controller.font).pack()
            nome = StringVar()
            ttk.Entry(self, textvariable=nome, width=30, font=controller.font).pack()

            Label(self, text='Cognome:', foreground='black', font=controller.font).pack()
            cognome = StringVar()
            ttk.Entry(self, textvariable=cognome, width=30, font=controller.font).pack()

            Label(self, text='mail:', foreground='black', font=controller.font).pack()
            mail = StringVar()
            ttk.Entry(self, textvariable=mail, width=30, font=controller.font).pack()

            Label(self, text="Data nascita:", foreground='black', font=controller.font).pack()
            #date_format = "%Y-%m-%d"
            #dataN = datetime.strptime(, date_format).date() #contine data ianzilae
            cal_dataN = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd') # Change the date pattern here
            cal_dataN.pack()
            
            id_med_ref = StringVar() #devo definrlo foeri socì anche med e resp lo hanno e non dannoe rrore
            if (utente.get_tipo_utente_aggiunto() == 'P'): # se aggiungo paziente
                # id_med_ref = StringVar()
                Label(self, text='Codice Medico di riferimento:', foreground='black', font=controller.font).pack()

                #prendo ID di tutti medici in DB                    
                dati = controller.DB.my_query("SELECT ID FROM UTENTE WHERE ID LIKE 'M%'", None)
                #print(dati)
                #([Moooo1], [M000002], ....)
                id_meds = []
                for m in dati:
                    id_meds.append(m[0])
                cb = ttk.Combobox(self, textvariable=id_med_ref)
                cb["values"] = id_meds
                cb.pack()
                cb["state"] = "readonly"


            # botton che permette di effetture la insert all'interno della tabella utente
            ttk.Button(self, text='Submit', style='Custom.TButton', command=lambda: controller.crea_utente(utente, id, nome.get(), cognome.get(), mail.get(),
                                                                                cal_dataN.selection_get().strftime('%Y-%m-%d'), id_med_ref.get(), psw, parent)).pack(side="right")

        ####### INDIETRO ################
            def indietro():
                controller.show_frame("HomeResp", parent, utente)  

            ttk.Button(self, text="Indietro", style='Custom.TButton', command=indietro).pack(side="left")