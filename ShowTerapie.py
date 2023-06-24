from my_library import *
from Terapia import *


class ShowTerapie(tk.Frame):

    def __init__(self, parent, controller, utente):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # due lableframe  una per terapie  e una per terapie conc


        # frame pazienti
        if(utente != None):
            f1 = LabelFrame(self, text='Terapie ipertensive')
            f1.pack(fill=BOTH, expand=True)
            
            terapie = controller.DB.my_query("SELECT * FROM terapia WHERE id_paz = %s", (utente.get_id_paz_selezionato(),))
            #(nome_farm, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine)
            ter_conc = []
            ter_iper = []
            ter_preg = []
            if(terapie!=None): #se paz ha almeno una terapia
                for terapia in terapie:
                    if(terapia[6] == "iper"):
                        ter_iper.append(terapia)
                    elif(terapia[6] == "conc" or terapia[6] == "segn_ter_conc"):
                        ter_conc.append(terapia)
                    elif(terapia[6] == "preg"):
                        ter_preg.append(terapia)

    ######### TABELLA TERAPIE IPER ###############

            colonne_ter_iper = ('Farmaco', 'Inizio', 'Qxdose', 'Ndosi', 'Ind')
            tabella_ter_iper = ttk.Treeview(f1, columns=colonne_ter_iper, show='headings', )
            # denominazione delle colonne
            tabella_ter_iper.column('Farmaco', anchor=CENTER)
            tabella_ter_iper.heading('Farmaco', text='Farmaco')
            tabella_ter_iper.column('Inizio', anchor=CENTER, width=100)
            tabella_ter_iper.heading('Inizio', text='Inizio')
            tabella_ter_iper.column('Qxdose', anchor=CENTER)
            tabella_ter_iper.heading('Qxdose', text='Qxdose')
            tabella_ter_iper.column('Ndosi', anchor=CENTER, width=100)
            tabella_ter_iper.heading('Ndosi', text='Ndosi')
            tabella_ter_iper["displaycolumns"]=("Farmaco", "Inizio", "Qxdose", "Ndosi")

            # inserimento dati nella tabella
            for record in ter_iper:
                tabella_ter_iper.insert('', END, values=[record[0], record[2], record[3], record[4], record[5]])

            tabella_ter_iper.grid(row=0, column=0)

            tabella_ter_iper.bind("<Double-1>", lambda event: controller.OnDoubleClick_mod_ter_iper(event, utente, tabella_ter_iper, parent))

        ############## AGGIUNGI TER IPER #####################

            b = Button(f1, text="Aggiungi\nterapia", command=lambda : controller.aggiungi_ter_iper(utente, parent)).grid(row=0, column=2)

            # aggiungo la scrollbar
            s1 = ttk.Scrollbar(f1, orient=VERTICAL, command=tabella_ter_iper.yview)
            s1.grid(row=0, column=1, sticky='ns')
            tabella_ter_iper.configure(yscrollcommand=s1.set)

        ####CONCOMITANTI
            f2 = LabelFrame(self, text='Terapie concomitanti')
            f2.pack(fill=BOTH, expand=True)
            # faccio il treeview
            colonne_ter_conc = ('Farmaco', 'Inizio', 'Qxdose', 'Ndosi', 'Ind', 'Tipo')
            tabella_ter_conc = ttk.Treeview(f2, columns=colonne_ter_conc, show='headings', )
            # denominazione delle colonne
            tabella_ter_conc.column('Farmaco', anchor=CENTER)
            tabella_ter_conc.heading('Farmaco', text='Farmaco')
            tabella_ter_conc.column('Inizio', anchor=CENTER, width=100)
            tabella_ter_conc.heading('Inizio', text='Inizio')
            tabella_ter_conc.column('Qxdose', anchor=CENTER)
            tabella_ter_conc.heading('Qxdose', text='Qxdose')
            tabella_ter_conc.column('Ndosi', anchor=CENTER, width=100)
            tabella_ter_conc.heading('Ndosi', text='Ndosi')
            tabella_ter_conc.column('Tipo', anchor=CENTER, width=100)
            tabella_ter_conc.heading('Tipo', text='Tipo')
            tabella_ter_conc["displaycolumns"]=("Farmaco", "Inizio", "Qxdose", "Ndosi", "Tipo")

            tabella_ter_conc.grid(row=0, column=0)

            # inserimento dati nella tabella
            #(nome_farm, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine)
            for record in ter_conc:
                if record[6] == "segn_ter_conc":
                    tabella_ter_conc.insert('', END, values=[record[0], record[2], record[3], record[4], record[5], "Segnalata"])
                else:
                    tabella_ter_conc.insert('', END, values=[record[0], record[2], record[3], record[4], record[5], "Accettata"])

            # aggiungo la scrollbar
            s2 = ttk.Scrollbar(f2, orient=VERTICAL, command=tabella_ter_conc.yview)
            s2.grid(row=0, column=1, sticky='ns')
            tabella_ter_conc.configure(yscrollcommand=s2.set)

            tabella_ter_conc.bind("<Double-1>",lambda event: controller.OnDoubleClick_mod_ter_conc(event, utente, tabella_ter_conc, parent))


        #PREGRESSE
            f3 = LabelFrame(self, text='Terapie pregrese')
            f3.pack(fill=BOTH, expand=True)

            # faccio il treeview
            colonne_ter_preg = ('Farmaco', 'Inizio', 'Qxdose', 'Ndosi', 'Fine')
            tabella_ter_preg = ttk.Treeview(f3, columns=colonne_ter_preg, show='headings', )
            # denominazione delle colonne
            tabella_ter_preg.column('Farmaco', anchor=CENTER)
            tabella_ter_preg.heading('Farmaco', text='Farmaco')
            tabella_ter_preg.column('Inizio', anchor=CENTER, width=100)
            tabella_ter_preg.heading('Inizio', text='Inizio')
            tabella_ter_preg.column('Qxdose', anchor=CENTER)
            tabella_ter_preg.heading('Qxdose', text='Qxdose')
            tabella_ter_preg.column('Ndosi', anchor=CENTER, width=100)
            tabella_ter_preg.heading('Ndosi', text='Ndosi')
            tabella_ter_preg.column('Fine', anchor=CENTER, width=100)
            tabella_ter_preg.heading('Fine', text='Fine')

            for record in ter_preg:
                #(farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine)
                tabella_ter_preg.insert('', END, values=[record[0], record[2], record[3], record[4], record[7]])
                
            tabella_ter_preg.grid(row=0, column=0, sticky="nsew")

            # aggiungo la scrollbar
            s3= ttk.Scrollbar(f3, orient=VERTICAL, command=tabella_ter_preg.yview)
            s3.grid(row=0, column=1, sticky='ns')
            tabella_ter_preg.configure(yscrollcommand=s3.set)

    ####### INDIETRO #####################################
            def indietro():
                controller.show_frame("VisPaz", parent, utente)
            Button(self, text="Indietro", command=indietro).pack()