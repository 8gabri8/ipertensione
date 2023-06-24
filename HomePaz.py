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
            label = tk.Label(self, text=f"Medico di Riferimento: {dati[0][0]} {dati[0][1]}\n Contattalo alla mail: {dati[0][2]}", font=controller.title_font, foreground="black")
            label.pack(side="top", fill="x", pady=10)

################## MISRUAZIONE DI PRESSIONI #####################

            ttk.Button(self, text="Nuova misurazione giornaliera", style='Custom.TButton',
                            command=lambda: controller.verifica_esistenza_dati_gior(utente, parent), width=30).pack(pady=10)
            
################## AGGIUNGI PAT CONC #####################
            def add_pat_conc(utente, parent):
                top = Toplevel()
                top.title("Segnala patologia concomitante")

                frame = LabelFrame(top, text="Segnala patologia concomitante")
                frame.pack(fill="both", expand=True, padx=10, pady=10)

                Label(frame, text="Nome patologia:").grid(row=0, column=0, sticky="e")
                cb_pat = ttk.Combobox(frame)
                pat = controller.DB.my_query("SELECT Nome FROM Patologia", None)
                pat = [str(item[0]) for item in pat]
                cb_pat["values"] = pat
                cb_pat.grid(row=0,column=1, sticky="w")
                cb_pat["state"] = "readonly"
                
                Label(frame, text="Data di inizio della patologia:").grid(row=1, column=0, sticky="e")

                cal = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd') # Change the date pattern here
                cal.grid(row=1, column=1, sticky="w")
                cal.grid(pady=10, padx=10)

                # Create a button to close the Toplevel widget
                f1 = Frame(top)
                f1.pack()
                Button(f1, text="Conferma",command = lambda: controller.segnala_pat_conc(utente, cb_pat.get(), datetime.strptime(cal.selection_get().strftime('%Y-%m-%d'), '%Y-%m-%d'),
                                                                                          top, parent)).pack(side='right', padx=10, pady=10)

                # Center the Toplevel widget on the screen
                top.update_idletasks()
                w = top.winfo_screenwidth()
                h = top.winfo_screenheight()
                size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
                x = w/2 - size[0]/2
                y = h/2 - size[1]/2
                top.geometry("%dx%d+%d+%d" % (size + (x, y)))

                top.grab_set() # per bloccare la finestram pop up

            ttk.Button(self, text="Segnala patologia concomitante", style='Custom.TButton',
                            command=lambda: add_pat_conc(utente, parent), width=30).pack(pady=10)

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