from my_library import *
from Medico import *
from Segnalazione import *
from Patologia import *
from Terapia import *

class HomePaz(tk.Frame):

    def __init__(self, parent, controller, utente):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        if(utente != None): #ovverro non sto solo inzializadno la pagina per il dizionario
            dati = controller.DB.my_query("SELECT Nome, Cognome, Mail FROM utente WHERE id = %s", (utente.get_id_med_ref(),))
            label = tk.Label(self, text=f"Buongiorno, {utente.get_nome()} {utente.get_cognome()}\nMedico di Riferimento: {dati[0][0]} {dati[0][1]}\n Contattalo alla mail: {dati[0][2]}", font=controller.title_font, foreground="black")
            label.pack(side="top", fill="x", pady=10)

################## MISRUAZIONE DI PRESSIONI #####################

            ttk.Button(self, text="Nuova misurazione giornaliera", style='Custom.TButton',
                            command=lambda: controller.verifica_esistenza_dati_gior(utente, parent), width=30).pack(pady=10)
            
################## AGGIUNGI PAT CONC #####################

            ttk.Button(self, text="Segnala patologia concomitante", style='Custom.TButton',
                            command=lambda: controller.segnala_pat_conc(utente, parent), width=30).pack(pady=10)

################## SEGNALA TERAPIA CONC #####################

            ttk.Button(self, text="Segnala terapia concomitante", style='Custom.TButton',
                            command=lambda: controller.segnala_ter_conc(utente, parent), width=30).pack(pady=10)

################## SEGNALA SINTOMI #####################

            ttk.Button(self, text="Segnala Sintomo", style='Custom.TButton',
                            command=lambda: controller.add_sintomo(utente, parent), width=30).pack(pady=10)
            
################## VIS DATI PERSONALI #####################

            ttk.Button(self, text="Dati personali", style='Custom.TButton',
                            command=lambda: controller.show_frame("DatiPersonali", parent, utente), width=30).pack(pady=10)

##################### TABELLA SEGNALAZIONI #####################

            datiP = controller.DB.my_query("SELECT Nome_sint, Inizio FROM occ_sintomo WHERE id_paz=%s AND Tipo='conc'", (utente.get_ID(),))
        
            # soluzione con treeview
            colonne_sin = ('Nome', 'Inizio')
            tabella_sin = ttk.Treeview(self, columns=colonne_sin, show='headings', style="Custom.Treeview") 
            # denominazione delle colonne
            tabella_sin.column('Inizio', anchor=CENTER)
            tabella_sin.heading('Inizio', text='Inizio')
            tabella_sin.column('Nome', anchor=CENTER)
            tabella_sin.heading('Nome', text='Sintomo in corso')

            #COTNROLA CHE DATIP NON SIA VUPOTA!!!!!!!
            # aggiungo i record che mi ritornano dalla query
            for record in datiP:
                tabella_sin.insert('', END, values=record)

            tabella_sin.pack()

            # aggiungo la scrollbar
            # s1 = ttk.Scrollbar(self, orient=VERTICAL, command=tabella_sin.yview)
            # s1.grid(row=0, column=1, sticky='ns')
            # tabella_sin.configure(yscrollcommand=s1.set)

            tabella_sin.bind("<Double-1>", lambda event: controller.OnDoubleClick_rendi_sintomo_preg(event, utente, tabella_sin, parent))


################## INDIETRO #####################

            # bottone di logout
            def indietro():
                controller.show_frame("StartPage", parent, utente)
            ttk.Button(self, text="logout", command=indietro, style='Custom.TButton', width=30).pack(pady=10)