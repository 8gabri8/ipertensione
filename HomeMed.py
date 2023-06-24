from my_library import *


class HomeMed(tk.Frame):

    def __init__(self, parent, controller, utente):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # frame pazienti
        if(utente != None):

    ######  CONTROLLO GIONALIERO DI NO_LOG
            controller.segn_no_segue(datetime.now(), parent)

    ######TABELLA PAZIENTE
            f1 = LabelFrame(self, text='I tuoi Pazienti')
            f1.pack(fill=BOTH, expand=True)
            datiP = controller.DB.my_query("SELECT ID, Nome, Cognome FROM utente WHERE ID LIKE 'P%' ORDER BY COGNOME, NOME", None) # va messo None quando non si inserisce nulla nella query
        
            colonne_paz = ('Codice', 'Nome', 'Cognome')
            tabella_paz = ttk.Treeview(f1, columns=colonne_paz, show='headings', style="Custom.Treeview") 
            tabella_paz.column('Codice', anchor=CENTER)
            tabella_paz.heading('Codice', text='Codice')
            tabella_paz.column('Nome', anchor=CENTER)
            tabella_paz.heading('Nome', text='Nome')
            tabella_paz.column('Cognome', anchor=CENTER)
            tabella_paz.heading('Cognome', text='Cognome')

            #COTNROLA CHE DATIP NON SIA VUPOTA!!!!!!!
            # aggiungo i record che mi ritornano dalla query
            for record in datiP:
                tabella_paz.insert('', END, values=record)

            tabella_paz.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # aggiungo la scrollbar
            # s1 = ttk.Scrollbar(f1, orient=VERTICAL, command=tabella_paz.yview)
            # s1.grid(row=0, column=1, sticky='ns')
            # tabella_paz.configure(yscrollcommand=s1.set)

            tabella_paz.bind("<Double-1>", lambda event: controller.OnDoubleClick_vis_paz(event, utente, tabella_paz, parent))

######TABELLA SEGNALAZIONI
            datiS = controller.DB.my_query("SELECT cod, data, id_paz, tipo, gravita FROM segnalazione ORDER BY data DESC",
                             None)
            ## frame segnalazioni
            f2 = LabelFrame(self, text='Segnalazioni')
            f2.pack(fill=BOTH, expand=True)
            # risultato dei dati della query delle segnalazioni 

            # soluzione con treeview
            colonne_seg = ('Codice', 'Data', 'id_paz', 'Tipo', 'Gravita')
            tabella_seg = ttk.Treeview(f2, columns=colonne_seg, show='headings', style="Custom.Treeview") 
            # denominazione delle colonne
            tabella_seg.column('Codice', anchor=CENTER)
            tabella_seg.heading('Codice', text='Codice',anchor=CENTER)
            tabella_seg.column('Data', anchor=CENTER)
            tabella_seg.heading('Data', text='Data', anchor=CENTER)
            tabella_seg.column('id_paz', anchor=CENTER)
            tabella_seg.heading('id_paz', text='Codice paziente', anchor=CENTER)
            tabella_seg.column('Tipo', anchor=CENTER)
            tabella_seg.heading('Tipo', text='Tipo', anchor=CENTER)
            tabella_seg.column('Gravita', anchor=CENTER)
            tabella_seg.heading('Gravita', text='Gravità',anchor=CENTER)
            tabella_seg['displaycolumns'] = ("Codice", "Data", "id_paz", "Tipo")

            # aggiungo i record che mi ritornano dalla query
            for record in datiS:
                tabella_seg.insert('', END, values=record)

            tabella_seg.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # aggiungo la scrollbar
            # s2 = ttk.Scrollbar(f2, orient=VERTICAL, command=tabella_seg.yview)
            # s2.grid(row=0, column=1, sticky='ns')
            # tabella_seg.configure(yscrollcommand=s2.set)

            tabella_seg.bind("<Double-1>", lambda event: controller.OnDoubleClick_vis_segnalazione(event, utente, tabella_seg, parent))

####LOGOUT
            # inserisci il bottone di log out
            def logout():
                controller.show_frame("StartPage", parent, utente)
            ttk.Button(self, text="Logout", command=logout, style='Custom.TButton', width=30).pack(pady=10)
