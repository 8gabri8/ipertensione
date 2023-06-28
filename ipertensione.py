# CONTORLLER

from my_library import *
from my_frames import *
import logging
from ManagerDB import *
from UtenteFactory import *
from Sintomo import * 

class App(tk.Tk): 
    #App è specializzazione di classe Tk, ovvero classe che crea l'allizaione in tkinter (essenzialmete crea la prima finestra iniziale)
    #crea la "root windows"

    def __init__(self, *args, **kwargs): #ovverride cotruttore
        tk.Tk.__init__(self, *args, **kwargs) #chiamo costruttore superclasse

        #controller ha dentro oggetto pèer parlare con DB
        self.DB = ManagerDB()
        self.factory = UtenteFactory()

        self.title("App Ipertensione")
        self.resizable(False, False)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = screen_width -100
        window_height = screen_height -100
        x = ((screen_width - window_width) // 2)-50
        y = ((screen_height - window_height) // 2)-30
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        
        #titolo dei font
        self.title_font = tkfont.Font(family='Helvetica', size=30, weight="bold", slant="italic") #scrivo titolo 
        self.font = tkfont.Font(family='Helvetica', size=15)
        self.style = ttk.Style()
        self.style.configure('Custom.TButton', font=self.font, background='lightblue')
        self.tab = ttk.Style()
        self.tab.configure("Custom.Treeview.Heading", font=self.font)

        # the container is where we'll stack a bunch of frame on top of each other, then the one we want visible
        # will be raised above the others
        #cointainer è il frame padre a cui altri frame(pagine successive) fanno riferimto
        container = tk.Frame(self) #container è un frame (che è dentro la finestra App(classe Tk crea la fienstra))
        container.pack(side="top", fill="both", expand=True) #faccio occupare tutto lo spazio al frame (lo spazio occupabile è quello della fonstra App)
        container.grid_rowconfigure(0, weight=1) #così widget si adattono a grandezza schermo!!!!!fanno outameticmete biding
        container.grid_columnconfigure(0, weight=1)

        # inizializzazione i 2 dizionari
        self.frames = {} #creoun dizionario, così posso accedere alle pagine più semplicemte (le ho tutte nella classe principale)
        #contiene le pagine/frames correnti
        #FARE IL DIZIOPONARIO SEREV COSì QUANDO SONO IN ALTRE CLASSI BASTA CHE SCRIVO LA STRINGA "PAGINA_NUOVA" E NON DEVO IMPORTARE LA CLASSE VERA E PROPRIO DELLA NUOVA PAGINA
        #SE IMPORTASSI LA CLASSE PTREBBERO SVILUSPPARSI PRBLEMI DI 

        self.str2class = {} #dizionario con classe e noem della classe

        for F in (StartPage, HomePaz, InserisciDatiGiornalieri, VisPaz, ModPaz, HomeMed, AddUtente, HomeResp, ShowTerapie, DatiPersonali):
  
            frame = F(container, self, None) #all'inziio creo solo apina, senza utente dentroi

            self.frames[F.__name__] = frame

            self.str2class[F.__name__] = F
  
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame("StartPage", container, None)

    def show_frame(self, page_name, container, utente):#gli dò il nome (c'ènel dizioneio) della pagina che volgio aprire, e apro paina con onoem
        '''Show a frame for the given page name'''
        #LO DEVO FARE PER FARE RERESH DI èPAGINA
        F = self.str2class[page_name]#predno la classe della pgina che sto cancellando e rifacendo
        del self.frames[page_name]#distruggo vecchi frame
        #print("\n", self.frames)
        #ricreo nuova pagin adello stesso tipo
        frame = F(container, self, utente)
        self.frames[F.__name__] = frame
        frame.grid(row = 0, column = 0, sticky ="nsew") #NECESSATIO SE NPON NON LO FACCIO GRANDE!!!!!!!!!!!!
        frame.tkraise()

################## START_PAGE #####################################
    
    def login(self, id_utente, psw_inserita, parent):

        if(id_utente == "" or psw_inserita == ""):
            messagebox.showinfo(message="Alcuni dati non sono stati inseriti")
            return

        if(id_utente[0] == "P"): #sono unm paziente, POTREBBE DARE PROBLREMI SE NON SCRIVO NULLA
            hash_psw = self.DB.my_query("SELECT hash_psw FROM utente WHERE id = %s", (id_utente,)) #ritorna la psw
            if(len(hash_psw) != 0): #ovvero utente esiste
                if(self.check_psw(psw_inserita, hash_psw[0][0])):

                    dati = self.DB.my_query("SELECT * FROM utente WHERE ID = %s", (id_utente,) )
                    #print(dati) --> (id, nome, cognome, mail, dataN, hash_psw, fatt_risc, id_med_ref)
                    paz = self.factory.crea_utente("paziente", ID = dati[0][0], nome = dati[0][1], cognome = dati[0][2], mail = dati[0][3], dataN = dati[0][4].strftime("%Y-%m-%d"),
                                                    fatt_risc = dati[0][6], id_med_ref = dati[0][7])

                    self.show_frame("HomePaz", parent, paz) 
                else:
                    # inserimeto della password errata 
                    messagebox.showinfo(message="Passord errata!")
                    #DEVO CANCELLARE QUESTA FINETRACHE NON USO PIù?????
            else:
                # l'utente ha inserito un utente inesistente
                messagebox.showinfo(message="Utente inesistente!") 
        
        elif(id_utente[0] == "M"): #sono unm paziente, POTREBBE DARE PROBLREMI SE NON SCRIVO NULLA
            hash_psw = self.DB.my_query("SELECT hash_psw FROM utente WHERE id = %s", (id_utente,)) #ritorna la psw
            if(len(hash_psw) != 0): #ovvero utente esiuste
                if(self.check_psw(psw_inserita, hash_psw[0][0])):

                    dati = self.DB.my_query("SELECT * FROM utente WHERE ID = %s", (id_utente,) )
                    #dati --Z (id, nome, cognome, mail, dataN, hash_psw, fatt_risc, id_med_ref)
                    med = self.factory.crea_utente("medico", ID = dati[0][0], nome = dati[0][1], cognome = dati[0][2], mail = dati[0][3], dataN = dati[0][4].strftime("%Y-%m-%d"))
                    self.show_frame("HomeMed", parent, med)
                else:
                    messagebox.showinfo(message="Passord errata!")
            else:
                messagebox.showinfo(message="Utente inesistente!") 

        elif(id_utente[0] == "R"): #sono unm paziente, POTREBBE DARE PROBLREMI SE NON SCRIVO NULLA
            hash_psw = self.DB.my_query("SELECT hash_psw FROM utente WHERE id = %s", (id_utente,)) #ritorna la psw
            if(len(hash_psw) != 0): #ovvero utente esiuste
                if(self.check_psw(psw_inserita, hash_psw[0][0])):

                    dati = self.DB.my_query("SELECT * FROM utente WHERE ID = %s", (id_utente,) )
                    resp = self.factory.crea_utente("responsabile", ID = dati[0][0], nome = dati[0][1], cognome = dati[0][2], mail = dati[0][3], dataN = dati[0][4].strftime("%Y-%m-%d"))
                    self.show_frame("HomeResp", parent, resp)
                else:
                    messagebox.showinfo(message="Passord errata!")
        else:
            messagebox.showinfo(message="Utente inesistente!") 

################## HOME PAZIENTE ##################################

    ############## VERIFICA ESISTENZA DATI GIOR ####################
    def verifica_esistenza_dati_gior(self, utente, parent):
        oggi = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year}"
        oggifatto = self.DB.my_query("SELECT * FROM assunzione WHERE id_paz=%s AND giorno = %s", (utente.get_ID(), oggi) )
        
        if(oggifatto == []): #la lista è vuot,a quindi oggi non ho inserito nulla
            self.show_frame("InserisciDatiGiornalieri", parent, utente)
        else:
            top = Toplevel()
            top.title("Nuova segnalazione")

            frame = LabelFrame(top, text="Nuova segnalazione")
            frame.pack(fill="both", expand=True, padx=10, pady=10)
            Label(frame, text="Vuoi sovrascrivere i dati di oggi?").grid(row=0, columnspan=2)

            def nuova_mis():
                top.destroy()
                self.show_frame("InserisciDatiGiornalieri", parent, utente)
            # Create a button to close the Toplevel widget
            Button(frame, text="Sì",command = nuova_mis, width=20).grid(row=1, column=1, pady=10,padx=5)
            Button(frame, text="No",command = lambda: top.destroy(), width=20).grid(row=1, column=0, pady=10,padx=10)

            # Center the Toplevel widget on the screen
            top.update_idletasks()
            w = top.winfo_screenwidth()
            h = top.winfo_screenheight()
            size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
            x = w/2 - size[0]/2
            y = h/2 - size[1]/2
            top.geometry("%dx%d+%d+%d" % (size + (x, y)))

            top.grab_set()    
      
    ################ AGGIUNGI PAT CONC #####################
    def segnala_pat_conc(self, utente, parent):
        top = Toplevel()
        top.title("Segnala patologia concomitante")

        frame = LabelFrame(top, text="Segnala patologia concomitante")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        Label(frame, text="Nome patologia:").grid(row=0, column=0, sticky="e")
        cb_pat = ttk.Combobox(frame)
        pat = self.DB.my_query("SELECT Nome FROM Patologia", None)
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

        def add_to_DB():
            nome_pat = cb_pat.get()
            data_pat_conc = datetime.strptime(cal.selection_get().strftime('%Y-%m-%d'), '%Y-%m-%d')

            #controlli:
            #patologia conc NON pridi oggi
            #non prima di prima ter iper
            #non deve mettere stessa pat concomitnati che ho già
            if(nome_pat == ""):
                messagebox.showinfo(message="Non hai inserito alcuna patologia")
                return

            #prima controllo la data: NO dopo di oggi, NO prima di prima terapia ipetensivaterapie_ipre
            #NS INUTOLE SPECIFICATEE TIPO, PERCHè èPRIMA TER è SEMPRE IPER
            terapie_iper = self.DB.my_query("SELECT * FROM Terapia WHERE id_paz=%s ORDER BY inizio", (utente.get_ID(),))
            #print(terapie_iper)
            #controllo che il paziente abbia alemno una ter iper
            if(terapie_iper == []):
                messagebox.showinfo(message="Non puoi avere una patologia concomitante se non ha iniziato ancora una terapia ipertensiva")
                return
            
            #controllo che pa non abbia messo data del sintomo dopo di oggi, o prima di prima ter iper
            data_patologia_conc_dt = data_pat_conc
            data_prima_terapia_iper_dt =  datetime.strptime(terapie_iper[0][2].strftime('%Y-%m-%d'), '%Y-%m-%d')
            data_oggi_dt = datetime.today()

            #print(data_oggi_dt, data_patologia_conc_dt, data_prima_terapia_iper_dt)

            pat_preg = self.DB.my_query("SELECT inizio, fine FROM occ_patologia WHERE id_paz = %s and tipo='preg' and nome_pat = %s", (utente.get_ID(), nome_pat))
            if(len(pat_preg) != 0):
                for ter_preg in pat_preg:
                    start_dt =  datetime.strptime(ter_preg[0].strftime('%Y-%m-%d'), '%Y-%m-%d')
                    end_dt =  datetime.strptime(ter_preg[1].strftime('%Y-%m-%d'), '%Y-%m-%d')
                    if(data_patologia_conc_dt <= end_dt and data_patologia_conc_dt >= start_dt):
                        messagebox.showinfo(message="In quel periodo stavi già soffrendo di questa patologia.")
                        return

                    #non deve esistere una terapia conc con uguale
            pat_conc = self.DB.my_query("SELECT * FROM occ_patologia WHERE (tipo = %s OR tipo =%s) AND id_paz = %s", ("conc", "segn_pat_conc", utente.get_ID()))
            #farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine)
            for pat in pat_conc:
                if(nome_pat == pat[0]):
                    messagebox.showinfo(message="Stai già soffrendo o hai già segnalato questa patologia")
                    return
            if(data_patologia_conc_dt < data_prima_terapia_iper_dt): #devo controllare che la data non sia qu
                messagebox.showinfo(message="Non puoi avere uina patologia concomitante prima di aver seguito una terampia ipertensiva")
                return
            if(data_patologia_conc_dt > data_oggi_dt):
                messagebox.showinfo(message="Non puoi saper che patologia avrai nel futuro")
                return
            
            #creo ogetto segn_pat
            segn_pat = SegnPatConc.create_patologia(nome_pat, utente.get_ID(), data_pat_conc, )
            #aggiungo cose a DB, bisogna fare un metodo nella classe terapia
            self.DB.my_query("INSERT INTO occ_patologia (nome_pat, id_paz, inizio, tipo, fine) VALUES(%s,%s,%s,%s,%s)", 
                    segn_pat.to_tupla())
            
            top.destroy() #distruggo pop up
            #self.top_pop = False #una finestra per inserire terapia è già aperta
            self.show_frame("HomePaz", parent, utente)

        ttk.Button(f1, text="Conferma",command = add_to_DB).pack(side='right', padx=10, pady=10)
        
        
        # Center the Toplevel widget on the screen
        top.update_idletasks()
        w = top.winfo_screenwidth()
        h = top.winfo_screenheight()
        size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        top.geometry("%dx%d+%d+%d" % (size + (x, y)))

        top.grab_set() # per bloccare la finestram pop up
        

    ################# aggiunta sintomo ####################################################
    def add_sintomo(self, utente, parent):
        # Create a new Toplevel widget
        top = Toplevel()
        top.title("Segnala Sintomo")

        # Create a LabelFrame for the patient information
        frame = LabelFrame(top, text="Segnala Sintomo")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create Labels for each piece of information
        Label(frame, text="Sintomo:").grid(row=0, column=0, sticky="e")
        cb_sintomo = ttk.Combobox(frame)
        sintomi = self.DB.my_query("SELECT Nome FROM Sintomo", None)
        sintomi = [str(item[0]) for item in sintomi]
        cb_sintomo["values"] = sintomi
        cb_sintomo.grid(row=0,column=1, pady=5)
        cb_sintomo["state"] = "readonly"
        
        Label(frame, text="Data di inizio del Sintomo:").grid(row=1, columnspan=2, pady=5)

        #controlla prima di oggi e non prim a di inzio ter conc
        cal = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd') # Change the date pattern here
        cal.grid(row=2, columnspan=2)
        cal.grid(pady=5, padx=10)

        def modDB():
            if(cb_sintomo.get() == ""):
                messagebox.showinfo(message="Non hai inserito alcun sintomo")
                return
            
            #NS INUTOLE SPECIFICATEE TIPO, PERCHè èPRIMA TER è SEMPRE IPER
            terapie_iper = self.DB.my_query("SELECT * FROM Terapia WHERE id_paz=%s ORDER BY inizio", (utente.get_ID(),))
            #controllo che il paziente abbia alemno una ter iper
            if(terapie_iper == []):
                messagebox.showinfo(message="Non puoi avere un sintomo concomitante se non ha iniziato ancora una terapia ipertensiva")
                return
            
            terapie_iper = self.DB.my_query("SELECT inizio FROM Terapia WHERE id_paz = %s ORDER BY inizio", (utente.get_ID(),)) 
            data_sintomo_dt = datetime.strptime(cal.selection_get().strftime('%Y-%m-%d'), '%Y-%m-%d')
            data_prima_terapia_dt =  datetime.strptime(terapie_iper[0][0].strftime('%Y-%m-%d'), '%Y-%m-%d')
            data_oggi_dt = datetime.today()
            
            sint_preg = self.DB.my_query("SELECT inizio, fine FROM occ_sintomo WHERE id_paz = %s and tipo='preg' and nome_sint = %s", (utente.get_ID(), cb_sintomo.get()))
            if(len(sint_preg) != 0):
                for ter_preg in sint_preg:
                    start_dt =  datetime.strptime(ter_preg[0].strftime('%Y-%m-%d'), '%Y-%m-%d')
                    end_dt =  datetime.strptime(ter_preg[1].strftime('%Y-%m-%d'), '%Y-%m-%d')
                    if(data_sintomo_dt <= end_dt and data_sintomo_dt >= start_dt):
                        messagebox.showinfo(message="In quel periodo stavi già soffrendo di questo sintomo.")
                        return

            #non deve esistere una terapia conc con uguale
            sint_conc = self.DB.my_query("SELECT * FROM occ_sintomo WHERE tipo = %s AND id_paz = %s", ("conc", utente.get_ID()))
            #farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine)
            for sint in sint_conc:
                if(cb_sintomo.get() == sint[0]):
                    messagebox.showinfo(message="Stai già soffrendo o hai già segnalato questo sintomo")
                    return
                if(data_sintomo_dt < data_prima_terapia_dt): #devo controllare che la data non sia qu
                    messagebox.showinfo(message="Non puoi avere un sintomo prima di aver seguito una terampia ipertensiva")
                    return
                if(data_sintomo_dt > data_oggi_dt):
                    messagebox.showinfo(message="Non puoi saper che patologia avrai nel futuro")
                    return


            #aggiungo cose a DB, bisogna fare un metodo nella classe terapia
            sint = Sintomo.create_sintomo(cb_sintomo.get(), utente.get_ID(), cal.selection_get().strftime('%Y-%m-%d'), "conc", None)
            if(type(sint) == str):
                messagebox.showinfo(message=sint)
                return
            
            self.DB.my_query("INSERT INTO occ_sintomo (nome_sint, id_paz, inizio, tipo, fine) VALUES(%s,%s,%s,%s,%s)", 
                    sint.to_tupla())
            
            top.destroy() #distruggo pop up
            self.show_frame("HomePaz", parent, utente)

        # Create a button to close the Toplevel widget
        f1 = Frame(top)
        f1.pack()
        ttk.Button(f1, text="Conferma",command = modDB).pack(side='right', padx=10, pady=10)

        # Center the Toplevel widget on the screen
        top.update_idletasks()
        w = top.winfo_screenwidth()
        h = top.winfo_screenheight()
        size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        top.geometry("%dx%d+%d+%d" % (size + (x, y)))

        top.grab_set() # per bloccare la finestram pop up

    ################# SEGNALA TER CONC #############################################   
    def segnala_ter_conc(self, utente, parent):
        # Create a new Toplevel widget
        top = Toplevel()

        # Set the title of the Toplevel widget
        top.title("Segnala terapia concomitante")

        # Create a LabelFrame for the patient information
        frame = LabelFrame(top, text="Segnala terapia concomitante")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create Labels for each piece of information
        Label(frame, text="Farmaco:").grid(row=0, column=0, sticky="e")
        #Label(frame, text=values[0]).grid(row=0, column=1, sticky="w")
        ter = self.DB.my_query("SELECT Nome FROM Farmaco WHERE tipo='altro'", None)
        ter = [str(item[0]) for item in ter]
        cb_ter = ttk.Combobox(frame)
        cb_ter["values"] = ter
        cb_ter.grid(row=0,column=1, sticky="w")
        cb_ter["state"] = "readonly"

        Label(frame, text="Quantità per dose:").grid(row=1, column=0, sticky="e")
        qta = StringVar()
        qta_entry = ttk.Entry(frame, width=30, textvariable=qta)
        qta_entry.grid(row=1, column=1, sticky="w")
        qta_entry.grid(pady=10)
        
        Label(frame, text="Numero di dosi al dì:").grid(row=3, column=0, sticky="e")
        ndosi = StringVar()
        ndosi_entry = ttk.Entry(frame, width=30, textvariable=ndosi)
        ndosi_entry.grid(row=3, column=1, sticky="w")
        ndosi_entry.grid(pady=10)

        Label(frame, text="Eventuali Indicazioni:").grid(row=4, columnspan=2)
        # = Entry(frame, text=values[3]).grid(row=3, column=1, sticky="w")_
        text_ind = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=4)
        text_ind.grid(row=5, columnspan=2)
        text_ind.grid(pady=10)
        Label(frame, text="Data inzio della terapia:").grid(row=6, columnspan=2)
        cal = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd') # Change the date pattern here
        cal.grid(row=7, columnspan=2)
        cal.grid(pady=10, padx=10)

        def modDB():
            #NS INUTOLE SPECIFICATEE TIPO, PERCHè èPRIMA TER è SEMPRE IPER
            terapie_iper = self.DB.my_query("SELECT * FROM Terapia WHERE id_paz=%s ORDER BY inizio", (utente.get_ID(),))
            #controllo che il paziente abbia alemno una ter iper
            if(terapie_iper == []):
                messagebox.showinfo(message="Non puoi avere un terapia concomitante se non ha iniziato ancora una terapia ipertensiva")
                return

            #predno la data della prima ter iper
            terapie_iper = self.DB.my_query("SELECT inizio FROM Terapia WHERE id_paz = %s ORDER BY inizio", (utente.get_ID(),))
            data_prima_terapia_dt =  datetime.strptime(terapie_iper[0][0].strftime('%Y-%m-%d'), '%Y-%m-%d')
            data_inizio_terapia_dt = datetime.strptime(cal.selection_get().strftime('%Y-%m-%d'), '%Y-%m-%d')

            terapie_preg = self.DB.my_query("SELECT inizio, fine FROM Terapia WHERE id_paz = %s and tipo='preg' and nome_farm = %s", (utente.get_ID(), cb_ter.get()))
            if(len(terapie_preg) != 0):
                for ter_preg in terapie_preg:
                    start_dt =  datetime.strptime(ter_preg[0].strftime('%Y-%m-%d'), '%Y-%m-%d')
                    end_dt =  datetime.strptime(ter_preg[1].strftime('%Y-%m-%d'), '%Y-%m-%d')
                    if(data_inizio_terapia_dt <= end_dt and data_inizio_terapia_dt >= start_dt):
                        messagebox.showinfo(message="In quel periodo stavi già seguendo questa terapia")
                        return
            
            #non deve esistere una terapia conc con uguale
            terapie_conc = self.DB.my_query("SELECT * FROM Terapia WHERE (tipo = %s OR tipo =%s) AND id_paz = %s", ("conc", "segn_ter_conc", utente.get_ID()))
            #farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine)
            for terapia in terapie_conc:
                if(cb_ter.get() == terapia[0]):
                    messagebox.showinfo(message="Stai già seguendo o hai già segnalato questa terapia")
                    return
            if(data_inizio_terapia_dt < data_prima_terapia_dt): #devo controllare che la data non sia qu
                messagebox.showinfo(message="Non puoi seguire una terapia concomitante prima di aver seguito una terampia ipertensiva")
                return

            ter = Terapia.create_terapia(
                            cb_ter.get(),
                            utente.get_ID(),
                            cal.selection_get().strftime('%Y-%m-%d'),
                            qta.get(),
                            ndosi.get(), #farmaco in MAIUSCOLO
                            text_ind.get("1.0", tk.END), 
                            "segn_ter_conc",
                            None)

            #verifoc che oggewtto sia stao crato, altirmeti faccio popUp di errore
            if(type(ter) == str): # perchè se è stringa vuol dire che è un errore
                messagebox.showinfo(message=ter, parent=top)  
            else:
                #aggiungo cose a DB, bisogna fare un metodo nella classe terapia
                self.DB.my_query("INSERT INTO Terapia(nome_farm, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", 
                        ter.to_tupla())
                top.destroy() #distruggo pop up
                self.top_pop = False #una finestra per inserire terapia è già aperta
                self.show_frame("HomePaz", parent, utente)

        # Create a button to close the Toplevel widget
        f1 = Frame(top)
        f1.pack()
        ttk.Button(f1, text="Conferma",command = modDB).pack(side='right', padx=10, pady=10)

        # Center the Toplevel widget on the screen
        top.update_idletasks()
        w = top.winfo_screenwidth()
        h = top.winfo_screenheight()
        size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        top.geometry("%dx%d+%d+%d" % (size + (x, y)))

        top.grab_set() 

    ################ RENDI SINOTMO PREG ################################à
    def OnDoubleClick_rendi_sintomo_preg(self, event, utente, tabella_sin, parent):
        id_riga= tabella_sin.selection()[0]
        values = tabella_sin.item(id_riga, "values")

        # Create a new Toplevel widget
        top = Toplevel()
        top.title("Sintomo")

        # Create a LabelFrame for the patient information
        frame = LabelFrame(top, text="Sintomo")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create Labels for each piece of information
        Label(frame, text=f"Sintomo: {values[0]}").grid(row=0, column=0, sticky="w")
        
        Label(frame, text=f"Data di inizio del Sintomo: {values[1]}").grid(row=1, column=0, sticky="w")

        #controlla prima di oggi e non prim a di inzio ter conc
        Label(frame, text="Data di fine del Sintomo: ").grid(row=2, column=0, sticky="w")

        cal = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd') # Change the date pattern here
        cal.grid(row=3, columnspan=2, sticky="w")
        cal.grid(pady=10, padx=10)

        def modDB():
            #controlo che:
                #la fine sia dopo l'inixio del sintomo  
                #la fine non sia dopo di oggi
            
            data_fine_sintomo_dt = datetime.strptime(cal.selection_get().strftime('%Y-%m-%d'), '%Y-%m-%d')
            data_inizio_sintomo_dt =  datetime.strptime(values[1], '%Y-%m-%d')
            data_oggi_dt = datetime.today()

            sint_preg = self.DB.my_query("SELECT inizio, fine FROM occ_sintomo WHERE id_paz = %s and tipo='preg' and nome_sint = %s", (utente.get_ID(), values[0]))
            if(len(sint_preg) != 0):
                for ter_preg in sint_preg:
                    start_dt =  datetime.strptime(ter_preg[0].strftime('%Y-%m-%d'), '%Y-%m-%d')
                    end_dt =  datetime.strptime(ter_preg[1].strftime('%Y-%m-%d'), '%Y-%m-%d')
                    if(data_fine_sintomo_dt <= end_dt and data_fine_sintomo_dt >= start_dt):
                        messagebox.showinfo(message="In quel periodo stavi già soffrendo di questo sintomo.")
                        return

            if(data_fine_sintomo_dt > data_oggi_dt):
                messagebox.showinfo(message="Non puoi sapere quando sintomo finierà")
                return
            elif(data_inizio_sintomo_dt > data_fine_sintomo_dt):
                messagebox.showinfo(message="Un sintomo non può finire prima di inizare")
                return
            #aggiungo cose a DB, bisogna fare un metodo nella classe terapia
            self.DB.my_query("UPDATE occ_sintomo SET tipo = 'preg', fine=%s where inizio=%s AND id_paz=%s AND nome_sint=%s", (cal.selection_get().strftime('%Y-%m-%d'), values[1], utente.get_ID(), values[0]))
            
            top.destroy() #distruggo pop up
            self.top_pop = False #una finestra per inserire terapia è già aperta
            self.show_frame("HomePaz", parent, utente)

        # Create a button to close the Toplevel widget
        f1 = Frame(top)
        f1.pack()
        ttk.Button(f1, text="Rendi pregresso",command = modDB).grid(row=0, column=0, padx=10, pady=10)

        def canc_sint():
            self.DB.my_query("DELETE FROM occ_sintomo WHERE nome_sint = %s AND id_paz = %s AND inizio=%s",
                        (values[0], utente.get_ID(), values[1]))
            
            top.destroy() #distruggo pop up
            self.top_pop = False #una finestra per inserire terapia è già aperta
            self.show_frame("HomePaz", parent, utente)
            

        ttk.Button(f1, text="Cancella",command = canc_sint).grid(row=0, column=1,padx=10, pady=10)

        # Center the Toplevel widget on the screen
        top.update_idletasks()
        w = top.winfo_screenwidth()
        h = top.winfo_screenheight()
        size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        top.geometry("%dx%d+%d+%d" % (size + (x, y)))

        top.grab_set() 

################ INSERISCI DATI GIORNALIERI########################

    def invia(self,  pmin, pmax, ore_pressioni, cluster_yn, 
            cluster_farmaco, cluster_inizio_ter, cluster_dosi,
            cluster_ore_assunzioni, assunzioni, utente, parent):
        
        #CONTROLLARE CORRETEZZA DATI INSERITI
        # nelle entry delle pressioni solo caratteri numerici
        cluster_corr=[]
        for _ in range(len(assunzioni)): cluster_corr.append(True)
    
        #trasfrormo da array di srirngvar ad array di int
        ore = []
        for o in ore_pressioni:
            ore.append(o.get())
            if(o.get() == "" or o.get() == "inserisci"):
                messagebox.showinfo(message="Le misurazioni di pressioni devono essere accompagnate da un orario.")
                return
        if(not (len(ore) == len(set(ore)))): #trafromo array in insieme, quindi duplivcati se ne vanno e lunghezza doiminuice
            messagebox.showinfo(message="Le misurazioni di pressioni devono essere compiute ad orari differenti.")
            return
        
        # if(all.(cluster_ore_assunzioni == "")): #ovvero ho fatto delle assuznioni
        #     ore = []
        #     for o in cluster_ore_assunzioni:
        #         ore.append(o.get())
        #     if(not (len(ore) == len(set(ore)))): #trafromo array in insieme, quindi duplivcati se ne vanno e lunghezza doiminuice
        #         messagebox.showinfo(message="Assunzioni di dosi differenti dello stesso farmaco devono essere compiute in orari differenti-")
        #         return

        isNumber = True
        for min, max in zip(pmin, pmax):
            if(not min.get().isdigit()): #ritona folaso se strringa NON è un numero O è vuota
                isNumber=False
            if(not max.get().isdigit()): #ritona folaso se strringa NON è un numero O è vuota
                isNumber=False
        if(not isNumber):
            messagebox.showinfo(message="Pressioni inserite NON sono valori numerici.")
            return

        isCorrect = True
        maxmin = True #è vero se la minima è minore della massima
        for min, max in zip(pmin, pmax):
            if(int(min.get()) < 30 or int(min.get()) > 250): #ritona folaso se strringa NON è un numero O è vuota
                isCorrect=False
            if(int(max.get()) < 30 or int(max.get()) > 250): #ritona folaso se strringa NON è un numero O è vuota
                isCorrect=False
            if(int(max.get()) < int(min.get())):
                maxmin=False
        if(not isCorrect):
            messagebox.showinfo(message="pressioni inserite NON sono compatibili con la vita :(.")
            return
        if(not maxmin):
            messagebox.showinfo(message="La pressione massima non può essere minore della minima ;).")
            return
            
        okTer = True
        for ter,i in zip(cluster_yn, range(len(cluster_yn))):
            if(ter.get() == ""): 
                okTer=False #infatti SWtringVAr non settata è stirng avuot
            if(ter.get() == "no"):
                cluster_corr[i]=False
        if(not okTer):
            messagebox.showinfo(message="Non hai specificato se ha seguito la tua terapia.")
            return
            
        # controllo ore sulla terapia
        #NB L'ASSUNZIONE DELLA STESS ATERPAIA DEVE AVERE ORE DIVERSE!!!!!!!
        okOra = True
        for ora, ter in zip(cluster_ore_assunzioni, cluster_yn):
            if(ora.get() == "" and ter.get()=="si"):  #se mi hai deto che ha preso la pastiglia, MA non mi dici l'0ra MI ARRABBIO
                okOra=False #infatti SWtringVAr non settata è stirng avuot
        if(not okOra):
            messagebox.showinfo(message="Non hai inserito tutti gli orari.")
            return
        okOra = True
        for ora, ter in zip(cluster_ore_assunzioni, cluster_yn):
            if(ora.get() != "" and ter.get()=="no"):  #se mi hai deto che ha NON hai preso la pastiglia, MA MI dici l'0ra MI ARRABBIO
                okOra=False #infatti SWtringVAr non settata è stirng avuot
        if(not okOra):
            messagebox.showinfo(message="Non puoi mettere un orario, se non hai seguito la terapia.")
            return

        #non devo fare controllo sull'0ra, perchèm ho usato cobo box

        #AGGIONARE DB!!!!!!!!!
        #NB OGNI MISRAZIONE DI PRESSIONE è UNA TUPLA A Sè IN DATI_GIOR
        oggi = f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}"
        # cancello la tupla da assunzione --> ATTEMZIONE ALL'ORDINE DELLE QUERY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.DB.my_query("DELETE FROM assunzione WHERE id_paz=%s AND giorno=%s", (utente.get_ID(), oggi))
        # canceello la tupla da dati gior
        self.DB.my_query("DELETE FROM dati_gior WHERE id_paz=%s AND giorno=%s", (utente.get_ID(), oggi))
        #cencello evtnuali segnalzione rpecdneti #(data, id_paz, tipo, gravita)
        self.DB.my_query("DELETE FROM segnalazione WHERE id_paz=%s AND data=%s AND tipo='p_anomala'", (utente.get_ID(), oggi))


        #(giorno, id_paz, pmin, pmax, sintomi, ass_corr, ora)
        pminima = []
        pmassima = []
        ore = []
        for p in pmin: #all'inziuo pmin è una stirnfVAr
            pminima.append(p.get())
        for p in pmax: #all'inziuo pmin è una stirnfVAr
            pmassima.append(p.get())
        for o in ore_pressioni:
            ore.append(o.get())
            
        #AGGIUNGO A DB L'INSERIMENTO GIRONALIERO
        for min, max, o in zip(pminima, pmassima, ore): #seve solo per scorrere tutte, potrei usarte anche pma, o ore
            #(giorno, id_paz, ora, pmin, pmax)
            self.DB.my_query("INSERT INTO dati_gior(giorno, id_paz, ora, pmin, pmax) VALUES (%s,%s,%s,%s,%s)", 
                    (oggi, utente.get_ID(), o, min, max))
        #AGIUNGO A DB LE ASSUNZIONI DI FARMCI FATTE
        for dose, ora, farmaco, inizio, corr in zip(cluster_dosi, cluster_ore_assunzioni, cluster_farmaco, cluster_inizio_ter, cluster_corr):
            #(nome_farm, id_paz, inizio_ter, giorno, ora, qtaxdose, corretta)
            ora_str=""
            if ora.get()=="":
                ora_str = '00:00:00' #NON VIPOLE NONE , PERCHE?????????????
            else:
                ora_str =  ora.get()
            #(nome_farm, id_paz, inizio_ter, giorno, dose, ora, corretta)
            self.DB.my_query("INSERT INTO assunzione(nome_farm, id_paz, inizio_ter, giorno, ora, dose, corretta) VALUES (%s,%s,%s,%s,%s,%s,%s)", 
                        (farmaco, utente.get_ID(), inizio, oggi, ora_str, dose, corr))

        #AGGIUNGO A DB EVENTUALI SEGNALAZIONI DI P TROPPO ALTE
        self.segn_p_anomala(utente, pminima, pmassima, parent)

        #FINALMENTE CAMBIO PAGINA
        self.show_frame("HomePaz", parent, utente)  

################## HOME MEDICO ###################################

    def OnDoubleClick_vis_paz(self, event, utente, tabella_seg, parent):
        id_riga= tabella_seg.selection()[0]
        values = tabella_seg.item(id_riga, "values")

        utente.set_id_paz_selezionato(values[0])

        self.show_frame("VisPaz", parent, utente)
    
    ################### VISULIZZA TABELLA SEGNALAZIONI #################################

    def OnDoubleClick_vis_segnalazione(self, event, utente, tabella_seg, parent):
        id_riga= tabella_seg.selection()[0]
        values = tabella_seg.item(id_riga, "values")

        #(data, id_paz, tipo, gravita)
        tipo = values[3]
        # Create a new Toplevel widget
        top = Toplevel()

        # Create a LabelFrame for the patient information
        frame = LabelFrame(top, text="Segnalazione")
        frame.pack(fill="both", expand=True, padx=10, pady=10)                

        if(tipo == "Pressione anomala"):
            #(data, id_paz, tipo, gravita)      
            Label(frame, text="Il giorno {}, il paziente {} ha avuto valori di pressioni anomali, \ncon gravità: {}".format(
                                values[1], values[2], values[4] )).grid(row=0, columnspan=2)
        else:
            Label(frame, text="In data {}, il paziente {} non ha seguito la terapia per più di tre giorni.".format(
                                values[1], values[2])).grid(row=0, columnspan=2)
            
        def delete_segn():
            #tolgo dal DB la segnalazione
            self.DB.my_query("DELETE FROM Segnalazione WHERE cod = %s", (values[0],))
            top.destroy() #distruggo pop up
            self.show_frame("HomeMed", parent, utente)  #così pagina si refresha!!!!!!!!!

        def vai_paz():
            #prendo ID paz che voglio vedere
            utente.set_id_paz_selezionato(values[2])
            #distruggo pop up
            top.destroy()
            #vado a vis paz
            self.show_frame("VisPaz", parent, utente)  #così pagina si refresha!!!!!!!!!

        # Create a button to close the Toplevel widget
        ttk.Button(frame, text="Vai a paziente", command=vai_paz).grid(row=1, column=0, pady=10)

        # Create a button to close the Toplevel widget
        ttk.Button(frame, text="Cancella", command=delete_segn).grid(row=1, column=1, pady=10)

        # Center the Toplevel widget on the screen
        top.update_idletasks()
        w = top.winfo_screenwidth()
        h = top.winfo_screenheight()
        size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        top.geometry("%dx%d+%d+%d" % (size + (x, y)))

        top.grab_set() 

################## VIS_PAZ #######################################

    ####### MOD FATT RISC ##################################
    def mod_fatt_risc(self, utente, id_paziente, parent):

        top = Toplevel()
        top.title(f'Modifica fattori di rischio')

        #creo oggetto paziente
        dati = self.DB.my_query("SELECT * FROM utente WHERE ID = %s", (utente.get_id_paz_selezionato(),) )
            #print(dati) --> (id, nome, cognome, mail, dataN, hash_psw, fatt_risc, id_med_ref)
        paziente = self.factory.crea_utente("paziente", ID = dati[0][0], nome = dati[0][1], cognome = dati[0][2], mail = dati[0][3], dataN = dati[0][4].strftime("%Y-%m-%d"),
                                fatt_risc = dati[0][6], id_med_ref = dati[0][7])

        frame1 = LabelFrame(top, text="Visualizza fattori di rischio")
        frame1.pack(fill="x")
        text_pat = scrolledtext.ScrolledText(frame1, wrap=tk.WORD, width=40, height=4)
        if( paziente.get_fatt_risc() != None):
            text_pat.insert(tk.INSERT, paziente.get_fatt_risc())
        text_pat.pack()

            ######## MODIFICA FATTORI DI RISACHIO ############à
        def cambia_fattori(utente, testo_fattori, parent):
            #INSERIRE NEL db COSE CMABIATE
            self.DB.my_query("UPDATE utente SET fatt_risc=%s WHERE id=%s", (testo_fattori, utente.get_id_paz_selezionato()))

            logging.basicConfig(filename='storico.log', encoding='utf-8', level=logging.DEBUG)
            logging.info(f'Il medico {utente.get_ID()} ha modificato i fattori di riscchio del paziente: {utente.get_id_paz_selezionato()}')

            top.destroy() #distruggo pop up
            self.show_frame("VisPaz", parent, utente)

        ttk.Button(frame1, text="Modifica Fattori di Rischio", command=lambda: cambia_fattori(utente, text_pat.get("1.0", tk.END), parent)).pack(padx=10, pady=10)

        # Center the Toplevel widget on the screen
        top.update_idletasks()
        w = top.winfo_screenwidth()
        h = top.winfo_screenheight()
        size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        top.geometry("%dx%d+%d+%d" % (size + (x, y)))

        top.grab_set() 
      
    ####### PRESSIONE SETTIMANALE ###################
    def get_pressioni_sett(self, id_paz, tipoP, parent):

        #SE PER SETT, DEVO PREDNERE SOLO ULTIMI SETTE GIORNI
        # sevenAgo = datetime.now() - timedelta(days=7) #sttenzione qui c'è anche orario
        # sevenAgo = sevenAgo.strftime("%Y-%m-%d")
        #print(f"{datetime.now().year}-{datetime.now().month:02}-{datetime.now().day:02}", "\n", sevenAgo)
        c_n = [] #dove mettere etichette per asase x
        y = [] #array che contine 7 array, ogni singlolo array contine i valor di ogni gionro
        
        for i in range(7, -1, -1):    
            #(giorno, id_paz, ora, pmin, pmax)
            giorno = (datetime.now() - timedelta(days=i))
            giorno = giorno.strftime("%Y-%m-%d")

            #traduzione per rpendere giusta colonne
            idx = 0
            if(tipoP == "minima"):  
                idx = 3
            else:
                idx = 4

            misurazioni_in_giono = self.DB.my_query("SELECT * FROM dati_gior WHERE id_paz=%s AND giorno=%s", 
                            (id_paz, giorno))
            mis_oggi =[]
            if(misurazioni_in_giono != []):
                for m in misurazioni_in_giono: #(giorno, id_paz, ora, pmin, pmax)
                    mis_oggi.append(m[idx])

            y.append(mis_oggi)
            c_n.append(giorno)

        max_length = max(len(subarray) for subarray in y)

        for i in range(8):
            y[i] = (y[i] + [0] * max_length)[:max_length]

        y_n = [] #lista di array, con dentro array che cointinefono tytte le i-esime misyrazionei della settimana
        for i in range(max_length):
            y_n.append([subarray[i] for subarray in y])

        return c_n, y_n

    ###### PRESSIONE MENSILE ###################
    def get_pressioni_mese(self, id_paz, anno, mese, parent):
        
        def last_day_of_month(year, month): #ritona lìltimo girono del mese
            return 31 - (month == 2 and (not year % 4 and year % 100 or not year % 400) or month in {4, 6, 9, 11})
        
        last_day = last_day_of_month(int(anno), int(mese))
        last_day_str = f"{last_day:02}"
        
        min = [0 for i in range(last_day)] #cconeinte la medie delle minime di ogni giorno
        max = [0 for i in range(last_day)]

        for i in range(1, last_day+1):
            dati = self.DB.my_query("select * from dati_gior WHERE id_paz=%s AND giorno=%s", 
                            (id_paz, anno + '-' + mese + f'-{i:02}'))
            if(dati != []):
                min[i-1] = np.mean([sublist[3] for sublist in dati]) #(giorno, id_paz, ora, pmin, pmax)
                max[i-1] = np.mean([sublist[4] for sublist in dati])
                #elemteni rimane 0

        c_n = [str(i) for i in range(1, last_day+1)] #dove mettere etichette per asase x

        return c_n, min, max
 
################## SHOW_TERAPIE ###################################

    ########### AGGIUNGI TER IPER ############
    
    def aggiungi_ter_iper(self, utente, parent):
        top = Toplevel()
        top.title("Aggiungi terapia")

        frame = LabelFrame(top, text="Aggiungi terapia")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create Labels for each piece of information
        Label(frame, text="Farmaco:").grid(row=0, column=0, sticky="e")
        #Label(frame, text=values[0]).grid(row=0, column=1, sticky="w")
        ter = self.DB.my_query("SELECT Nome FROM Farmaco WHERE tipo='iper'", None)
        ter = [str(item[0]) for item in ter]
        cb_farmaco = ttk.Combobox(frame)
        cb_farmaco["values"] = ter
        cb_farmaco.grid(row=0,column=1, sticky="w")
        cb_farmaco["state"] = "readonly"
        
        Label(frame, text="Quantità per dose:").grid(row=1, column=0, sticky="e")
        #Label(frame, text=values[1]).grid(row=1, column=1, sticky="w")
        qtaxdose = StringVar()
        qtaxdose_entry = ttk.Entry(frame, width=30, textvariable=qtaxdose)
        qtaxdose_entry.grid(row=1, column=1, sticky="w")

        Label(frame, text="Numero dosi al di:").grid(row=2, column=0, sticky="e")
        #Label(frame, text=values[2]).grid(row=2, column=1, sticky="w")
        ndosi = StringVar()
        ndosi_entry = ttk.Entry(frame, width=30, textvariable=ndosi)
        ndosi_entry.grid(row=2, column=1, sticky="w")
        
        # il tipo non va specificato perchè il medico inserisce solamnte terapie ipertensive

        Label(frame, text="Indicazioni:").grid(row=3, columnspan=2)
        # = Entry(frame, text=values[3]).grid(row=3, column=1, sticky="w")_
        text_ind = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=4)
        text_ind.grid(row=4, columnspan=2)

        Label(frame, text="Data Inizio:").grid(row=5, columnspan=2)
        cal_inizio = Calendar(frame, date_pattern='yyyy-mm-dd') # Change the date pattern here
        cal_inizio.grid(row=6, columnspan=2)

        def add_ter_iper(): 
            #CONTROLLI:
                #SEMRPE IMMETTERE TUTTI DATI, CON GISUTA FORMATTAZOIONE
                #DATA INZIO > DATAN --> ok
                #NO CONTROLLO DI PRIMA TER IPER  --> ok
                # DATA INZIO IN RNAGE DI STESSA PREGRESSA --> ok
                #SI PUò ESSERE DATA INZIO DOPO OGGI --> ok
                #NON POSSO IMMETERE LA TSESSA IN CORSO --> ok
            
            data_inizio_terapia_new_dt = datetime.strptime(cal_inizio.selection_get().strftime('%Y-%m-%d'), '%Y-%m-%d')
            nome_farmaco_new = cb_farmaco.get()

           #controllo range
            terapie_preg = self.DB.my_query("SELECT inizio, fine FROM Terapia WHERE id_paz = %s and tipo='preg' and nome_farm = %s", (utente.get_id_paz_selezionato(), nome_farmaco_new))
            if(len(terapie_preg) != 0):
                for ter_preg in terapie_preg:
                    start_dt =  datetime.strptime(ter_preg[0].strftime('%Y-%m-%d'), '%Y-%m-%d')
                    end_dt =  datetime.strptime(ter_preg[1].strftime('%Y-%m-%d'), '%Y-%m-%d')
                    if(data_inizio_terapia_new_dt <= end_dt and data_inizio_terapia_new_dt >= start_dt):
                        messagebox.showinfo(message="In quel periodo stavi già seguendo questa terapia")
                        return
            
            #controllo se stai già segiuendo altor
            terapie_iper = self.DB.my_query("SELECT * FROM Terapia WHERE tipo = %s AND id_paz = %s", ("iper", utente.get_id_paz_selezionato()))
            #farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine)
            for terapia in terapie_iper:
                if(nome_farmaco_new == terapia[0]):
                    messagebox.showinfo(message="Il paziente sta già seguendo questa terapia")
                    return
            
            #controllo che la data terapia non deve essere minotre della dataN paz
            dataN = self.DB.my_query("select dataN from utente where id = %s", (utente.get_id_paz_selezionato(),))
            if(data_inizio_terapia_new_dt.date() < dataN[0][0]):
                messagebox.showinfo(message="La terapia non può iniziare prima della data di nascita del paziente! Il paziente è nato: {}".format(dataN[0][0].strftime("%Y-%m-%d")))
                return

            ter = Terapia.create_terapia(
                            cb_farmaco.get(),
                            utente.get_id_paz_selezionato(),
                            cal_inizio.selection_get().strftime('%Y-%m-%d'),
                            qtaxdose.get(),
                            ndosi.get(), #farmaco in MAIUSCOLO
                            text_ind.get("1.0", tk.END), 
                            "iper",
                            None)

            #verifoc che oggewtto sia stao crato, altirmeti faccio popUp di errore
            if(type(ter) == str): # perchè se è stringa vuol dire che è un errore
                messagebox.showinfo(message=ter, parent=top)
                return
                
            #aggiungo cose a DB, bisogna fare un metodo nella classe terapia
            self.DB.my_query("INSERT INTO Terapia(nome_farm, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", 
                    ter.to_tupla())
            
            #update file log
            logging.basicConfig(filename='storico.log', encoding='utf-8', level=logging.DEBUG)
            logging.info(f'Il medico {utente.get_ID()} ha aggiunto la seguente terapia ipertensiva:{ter.get_farmaco()}, {ter.get_inizio()} per il paziente {utente.get_id_paz_selezionato()}')

            top.destroy() #distruggo pop up
            self.show_frame("ShowTerapie", parent, utente)

        # Create a button to close the Toplevel widget
        f1 = Frame(top)
        f1.pack()
        ttk.Button(f1, text="Conferma", command=add_ter_iper).pack(side='right', padx=10, pady=10)

        # Center the Toplevel widget on the screen
        top.update_idletasks()
        w = top.winfo_screenwidth()
        h = top.winfo_screenheight()
        size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        top.geometry("%dx%d+%d+%d" % (size + (x, y)))
        
        top.grab_set()

    ###### GESTISCI TER IPER ##################################

    def OnDoubleClick_mod_ter_iper(self, event, utente, tabella_iper, parent):
        id_riga= tabella_iper.selection()[0]
        values = tabella_iper.item(id_riga, "values")

        top = Toplevel()
        top.title("Modifica terapia ipertensiva")

        # Create a LabelFrame for the patient information
        frame = LabelFrame(top, text="Modifica terapia ipertensiva")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create Labels for each piece of information
        Label(frame, text="Farmaco:").grid(row=0, column=0, sticky="e")
        ter = self.DB.my_query("SELECT Nome FROM Farmaco WHERE tipo='iper'", None)
        ter = [str(item[0]) for item in ter]
        cb_farmaco = ttk.Combobox(frame)
        cb_farmaco["values"] = ter
        cb_farmaco.grid(row=0,column=1, sticky="w")
        cb_farmaco["state"] = "readonly"
        cb_farmaco.set(values[0])
        #Label(frame, text=values[0]).grid(row=0, column=1, sticky="w")
        
        Label(frame, text="Quantità per dose:").grid(row=1, column=0, sticky="e")
        #Label(frame, text=values[1]).grid(row=1, column=1, sticky="w")
        qtaxdose = StringVar(value=values[2])
        qtaxdose_entry = ttk.Entry(frame, width=30, textvariable=qtaxdose)
        qtaxdose_entry.grid(row=1, column=1, sticky="w")

        Label(frame, text="Numero dosi al di:").grid(row=2, column=0, sticky="e")
        #Label(frame, text=values[2]).grid(row=2, column=1, sticky="w")
        ndosi = StringVar(value=values[3])
        ndosi_entry = ttk.Entry(frame, width=30, textvariable=ndosi)
        ndosi_entry.grid(row=2, column=1, sticky="w")

        Label(frame, text="Data Inizio:").grid(row=3, columnspan=2)
        date_format = "%Y-%m-%d"
        initial_date = datetime.strptime(values[1], date_format).date() #contine data ianzilae
        cal_inizio = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd', year=initial_date.year,
                                month=initial_date.month, day=initial_date.day) # Change the date pattern here
        cal_inizio.grid(row=4, columnspan=2)
        #cal_inizio.configure(state="disabled")

        
        Label(frame, text="Indicazioni:").grid(row=5, columnspan=2)
        # = Entry(frame, text=values[3]).grid(row=3, column=1, sticky="w")_
        text_ind = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=4)
        if(values[4] != None):
            text_ind.insert(tk.INSERT, values[4])
        text_ind.grid(row=6, columnspan=2)

        Label(frame, text="Data Fine:").grid(row=7, columnspan=2)
        cal_fine = Calendar(frame, date_pattern='yyyy-mm-dd') # Change the date pattern here
        cal_fine.grid(row=8, columnspan=2)

        def mod_ter_iper():
            #CONTROLLI PER MODFICA:
                #SE CAMBIO NOME TER, NON CI DEVE ESSERE ALTRA TER IN CORSO CON STESSO NOME
                    #IN PIù C'è DA MODIFICARE LA TABELL ASSUNZIONE ON CASCADE
                # NO!! CONTORLLO SU PRIMA DELL APRIMA TER IPER
                # INZIO MAGGIOR DI DATAN
                # INIZIO NON IN RNAGE DI PREG
                # DATA INZIO NEW >= DATA INZIO OLD --> PAZ POTRBBE AVER GIà RPESO DEI FARMACI
                    #CADCADE MODIFICA INZIO TER IN TABELLA ASSUNZIONE
            
            data_inizio_terapia_new_dt = datetime.strptime(cal_inizio.selection_get().strftime('%Y-%m-%d'), '%Y-%m-%d')
            data_inizio_terapia_old_dt = initial_date
            nome_farmaco_new = cb_farmaco.get()
            nome_farmaco_old = values[0]

           #controllo range
            terapie_preg = self.DB.my_query("SELECT inizio, fine FROM Terapia WHERE id_paz = %s and tipo='preg' and nome_farm = %s", (utente.get_id_paz_selezionato(), nome_farmaco_new))
            if(len(terapie_preg) != 0):
                for ter_preg in terapie_preg:
                    start_dt =  datetime.strptime(ter_preg[0].strftime('%Y-%m-%d'), '%Y-%m-%d')
                    end_dt =  datetime.strptime(ter_preg[1].strftime('%Y-%m-%d'), '%Y-%m-%d')
                    if(data_inizio_terapia_new_dt <= end_dt and data_inizio_terapia_new_dt >= start_dt):
                        messagebox.showinfo(message="In quel periodo stavi già seguendo questa terapia")
                        return
            
            #controllo se stai già segiuendo altor
            terapie_iper = self.DB.my_query("SELECT * FROM Terapia WHERE tipo = %s AND id_paz = %s", ("iper", utente.get_id_paz_selezionato()))
            #farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine)
            for terapia in terapie_iper:
                if(nome_farmaco_new == terapia[0]  and nome_farmaco_new != nome_farmaco_old):
                    messagebox.showinfo(message="Il paziente sta già seguendo questa terapia")
                    return
            
            #controllo che la terapia non deve essere minotre della patologia
            dataN = self.DB.my_query("select dataN from utente where id = %s", (utente.get_id_paz_selezionato(),))
            if(data_inizio_terapia_new_dt.date() < dataN[0][0]):
                messagebox.showinfo(message="La terapia non può iniziare prima della data di nascita del paziente! Il paziente è nato: {}".format(dataN[0][0].strftime("%Y-%m-%d")))
                return
            
            ass = self.DB.my_query("select * from assunzione where id_paz = %s and nome_farm = %s and inizio_ter=%s", (utente.get_id_paz_selezionato(),
                                                                                                                    nome_farmaco_old, 
                                                                                                                    data_inizio_terapia_old_dt.strftime("%Y-%m-%d")))
            if(data_inizio_terapia_new_dt.date() > data_inizio_terapia_old_dt and len(ass) != 0):
                messagebox.showinfo(message="Il paziente ha già assunto questa terapia, quindi la sua data di inizio non può essere posticipata.")
                return
            
            #farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine
            ter = Terapia.create_terapia(
                            nome_farmaco_new,
                            utente.get_id_paz_selezionato(),
                            cal_inizio.selection_get().strftime('%Y-%m-%d'),
                            qtaxdose.get(),
                            ndosi.get(), #farmaco in MAIUSCOLO
                            text_ind.get("1.0", tk.END), 
                            "iper",
                            None)

            #verifoc che oggewtto sia stao crato, altirmeti faccio popUp di errore
            if(type(ter) == str): # perchè se è stringa vuol dire che è un errore
                messagebox.showinfo(message=ter, parent=top)
                return
            
            #aggiungo cose a DB, bisogna fare un metodo nella classe terapia
            self.DB.my_query("UPDATE terapia SET nome_farm = %s, id_paz = %s, inizio=%s, qtaxdose = %s, ndosi = %s, ind = %s, tipo = %s, fine=%s WHERE id_paz=%s AND nome_farm=%s AND inizio=%s", 
                    ter.to_tupla() + (utente.get_id_paz_selezionato(), nome_farmaco_old, data_inizio_terapia_old_dt.strftime('%Y-%m-%d')))
            
            #update file log
            logging.basicConfig(filename='storico.log', encoding='utf-8', level=logging.DEBUG)
            logging.info(f'Il medico {utente.get_ID()} ha modificato la seguente terapia ipertensiva:{ter.get_farmaco()}, {ter.get_inizio()} per il paziente {utente.get_id_paz_selezionato()}')

            top.destroy() #distruggo pop up
            self.show_frame("ShowTerapie", parent, utente)

        # Create a button to close the Toplevel widget
        f1 = Frame(top)
        f1.pack()
        ttk.Button(f1, text="Modifica", command=mod_ter_iper).pack(side='right', padx=10, pady=10)

        def iper2preg():
            # controlli sulla dataF ok
            # la dataF > dataI ok
            # dataF non rirntra nel RANGE di un'altra terapia uguale pregressa  ok
            # gestione della sovrapposizzioen dataI_new > data_oldI e dataF_old > dataF_old ok
            # ok posso dire ache che finirà mnel futuro
            
            data_fine_ter_iper_dt = cal_fine.selection_get() #ritona datetimew
            data_inizio_ter_iper_dt = datetime.strptime(values[1], "%Y-%m-%d")

            ter_pregS = self.DB.my_query("SELECT inizio, fine FROM terapia WHERE id_paz = %s and tipo='preg' and nome_farm = %s", (utente.get_id_paz_selezionato(), values[0]))
            if(len(ter_pregS) != 0):
                for ter_preg in ter_pregS:
                    start_dt =  datetime.strptime(ter_preg[0].strftime('%Y-%m-%d'), '%Y-%m-%d')
                    end_dt =  datetime.strptime(ter_preg[1].strftime('%Y-%m-%d'), '%Y-%m-%d')
                    if(data_fine_ter_iper_dt <= end_dt.date() and data_fine_ter_iper_dt >= start_dt.date()): #range
                        messagebox.showinfo(message="In quel periodo stava già soffrendo di questa patologia.")
                        return
                    elif(data_inizio_ter_iper_dt.date() <= start_dt.date() and data_fine_ter_iper_dt >= end_dt.date()): #scoreppoazione
                        messagebox.showinfo(message="C'è uan sovrapposzione temporale della stessa patologia.")
                        return

            if (data_fine_ter_iper_dt < data_inizio_ter_iper_dt.date()):
                messagebox.showinfo(message="La patologia non può finire prima di iniziare!")
                return   

            #creazione oggetto ter
            #(farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine):
            ter = Terapia.create_terapia(  
                            values[0], 
                            utente.get_id_paz_selezionato(), 
                            values[1],
                            qtaxdose.get(), 
                            ndosi.get(), 
                            text_ind.get("1.0", tk.END), 
                            "preg", 
                            cal_fine.selection_get().strftime('%Y-%m-%d'),)

            # update
            if(type(ter) == str):
                messagebox.showinfo(message=ter, parent=top)
                return
            else:
                #mdidico teraspai
                self.DB.my_query("UPDATE terapia SET fine=%s, tipo = %s WHERE id_paz=%s AND nome_farm =%s AND inizio=%s", 
                        (ter.get_fine(), ter.get_tipo(), utente.get_id_paz_selezionato(), values[0], values[1])) #NB devo mettere valori vecchi come chiamve
                
                logging.basicConfig(filename='storico.log', encoding='utf-8', level=logging.DEBUG)
                logging.info(f'Il medico {utente.get_ID()} ha reso pregressa la seguente terapia ipertensiva:{ter.get_farmaco()}, {ter.get_inizio()} per il paziente {utente.get_id_paz_selezionato()}')
                
                top.destroy() #distruggo pop up
                self.show_frame("ShowTerapie", parent, utente)
                
        ttk.Button(f1, text="Rendi Pregressa", command=iper2preg).pack(side='right', padx=10, pady=10)

        ####### cencella ter iper ######
        def cancella_ter_iper():
            #se paz ha ghià fatto una assunzioone, allora non si può cancellare
            ass = self.DB.my_query("select * from assunzione where id_paz = %s and nome_farm = %s and inizio_ter=%s", (utente.get_id_paz_selezionato(),
                                                                                                                    values[0], 
                                                                                                                    values[1]))
            if(len(ass) != 0):
                messagebox.showinfo(message="Il paziente ha già assunto questa terapia, quindi può essere solo resa pregressa.")
                return

            self.DB.my_query("DELETE FROM terapia WHERE nome_farm = %s AND id_paz = %s AND inizio=%s",
                        (values[0], utente.get_id_paz_selezionato(), values[1]))
            
            logging.basicConfig(filename='storico.log', encoding='utf-8', level=logging.DEBUG)
            logging.info(f'Il medico {utente.get_ID()} ha cancellato la seguente terapia ipertensiva:{values[0]}, {values[1]} per il paziente {utente.get_id_paz_selezionato()}')
            
            top.destroy() #distruggo pop up
            self.show_frame("ShowTerapie", parent, utente)

        ttk.Button(f1, text="Cancella", command= cancella_ter_iper).pack(side='right', padx=10, pady=10)

        # Center the Toplevel widget on the screen
        top.update_idletasks()
        w = top.winfo_screenwidth()
        h = top.winfo_screenheight()
        size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        top.geometry("%dx%d+%d+%d" % (size + (x, y)))

        top.grab_set() 

    ########## GESTISCI TER CONC ############################

    def OnDoubleClick_mod_ter_conc(self, event, utente, tabella_ter_conc, parent):
        id_riga= tabella_ter_conc.selection()[0]
        values = tabella_ter_conc.item(id_riga, "values")

        top = Toplevel()
        top.title("Modifica terapia concomitante")

        frame = LabelFrame(top, text="Modifica terapia concomitante")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        if(values[5] == "Segnalata"):
            Label(frame, text=f"Il paziente ha segnalato la seguente terapia concomitante:\nFarmaco: {values[0]}\nQuantità per dose: {values[2]}\nNumero di dosi: {values[3]}\nIndicazioni: {values[4]}\nVuoi accetarla?").grid(row=0, columnspan=2)
            
            def accetta_ter_conc():
                #creazione oggetto ter
                ter = Terapia.create_terapia(  
                                values[0], 
                                utente.get_id_paz_selezionato(), 
                                values[1],
                                values[2], 
                                values[3], 
                                values[4], 
                                "conc", 
                                None)

                # update
                if(type(ter) == str):
                    messagebox.showinfo(message=ter, parent=top)
                    return
                else:
                    #(nome_farm, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine)
                    self.DB.my_query("UPDATE terapia SET nome_farm = %s, id_paz = %s, inizio=%s, qtaxdose = %s, ndosi = %s, ind = %s, tipo = %s, fine=%s WHERE id_paz=%s AND nome_farm=%s AND inizio=%s", 
                            ter.to_tupla() + (utente.get_id_paz_selezionato(), values[0], values[1]))
                    
                    logging.basicConfig(filename='storico.log', encoding='utf-8', level=logging.DEBUG)
                    logging.info(f'Il medico {utente.get_ID()} ha aggiunto la seguente terapia concomitante:{ter.get_farmaco()}, {ter.get_inizio()} per il paziente {utente.get_id_paz_selezionato()}')

                    top.destroy() #distruggo pop up
                    self.show_frame("ShowTerapie", parent, utente)

            ttk.Button(frame, text="Accetta", command = accetta_ter_conc).grid(row=1, column=0, pady=10)

            def rifiuta_ter_conc():
                self.DB.my_query("DELETE FROM terapia WHERE nome_farm=%s AND id_paz=%s AND inizio=%s", (values[0], utente.get_id_paz_selezionato(), values[1]))

                logging.basicConfig(filename='storico.log', encoding='utf-8', level=logging.DEBUG)
                logging.info(f'Il medico {utente.get_ID()} ha rifiutato la seguente terapia concomitante:{values[0]}, {values[1]} per il paziente {utente.get_id_paz_selezionato()}')

                top.destroy() #distruggo pop up
                self.show_frame("ShowTerapie", parent, utente)

            ttk.Button(frame, text="Rifiuta", command = rifiuta_ter_conc).grid(row=1, column=1, pady=10)

        else: # è GIà ACCETTATA
            Label(frame, text="Farmaco:").grid(row=0, column=0, sticky="e")
            Label(frame, text=values[0]).grid(row=0, column=1, sticky="w")
            
            Label(frame, text="Quantità per dose:").grid(row=1, column=0, sticky="e")
            #Label(frame, text=values[1]).grid(row=1, column=1, sticky="w")
            qtaxdose = StringVar(value=values[2])
            qtaxdose_entry = ttk.Entry(frame, width=30, textvariable=qtaxdose)
            qtaxdose_entry.grid(row=1, column=1, sticky="w")

            Label(frame, text="Numero dosi al di:").grid(row=2, column=0, sticky="e")
            #Label(frame, text=values[2]).grid(row=2, column=1, sticky="w")
            ndosi = StringVar(value=values[3])
            ndosi_entry = ttk.Entry(frame, width=30, textvariable=ndosi)
            ndosi_entry.grid(row=2, column=1, sticky="w")

            Label(frame, text="Data Inizio:").grid(row=3, columnspan=2)
            date_format = "%Y-%m-%d"
            initial_date = datetime.strptime(values[1], date_format).date() #contine data ianzilae
            cal_inizio = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd', year=initial_date.year,
                                    month=initial_date.month, day=initial_date.day) # Change the date pattern here
            cal_inizio.grid(row=4, columnspan=2)
            cal_inizio.configure(state="disabled")
            
            Label(frame, text="Indicazioni:").grid(row=5, columnspan=2)
            # = Entry(frame, text=values[3]).grid(row=3, column=1, sticky="w")_
            text_ind = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=4)
            if(values[4] != None):
                text_ind.insert(tk.INSERT, values[4])
            text_ind.grid(row=6, columnspan=2)

            Label(frame, text="Data Fine:").grid(row=7, columnspan=2)
            date_format = "%Y-%m-%d"
            cal_fine = Calendar(frame, date_pattern='yyyy-mm-dd') # Change the date pattern here
            cal_fine.grid(row=8, columnspan=2)

            def mod_ter_conc():
                #creazione oggetto ter
                # farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine):
                ter = Terapia.create_terapia(  
                                values[0], 
                                utente.get_id_paz_selezionato(), 
                                cal_inizio.selection_get().strftime('%Y-%m-%d'),
                                qtaxdose.get(), 
                                ndosi.get(), 
                                text_ind.get("1.0", tk.END), 
                                "conc", 
                                None)

                # update
                if(type(ter) == str):
                    messagebox.showinfo(message=ter, parent=top)
                    return
                else:
                    #(nome_farm, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine)
                    self.DB.my_query("UPDATE terapia SET nome_farm = %s, id_paz = %s, inizio=%s, qtaxdose = %s, ndosi = %s, ind = %s, tipo = %s, fine=%s WHERE id_paz=%s AND nome_farm=%s AND inizio=%s", 
                            ter.to_tupla() + (utente.get_id_paz_selezionato(), values[0], values[1]))
                    
                    logging.basicConfig(filename='storico.log', encoding='utf-8', level=logging.DEBUG)
                    logging.info(f'Il medico {utente.get_ID()} ha modificato la seguente terapia concomitante:{ter.get_farmaco()}, {ter.get_inizio()} per il paziente {utente.get_id_paz_selezionato()}')

                    top.destroy() #distruggo pop up
                    self.show_frame("ShowTerapie", parent, utente)

            def conc2preg():
                #creazione oggetto ter
                ter = Terapia.create_terapia(  
                                values[0], 
                                utente.get_id_paz_selezionato(), 
                                cal_inizio.selection_get().strftime('%Y-%m-%d'),
                                qtaxdose.get(), 
                                ndosi.get(), 
                                text_ind.get("1.0", tk.END), 
                                "preg", 
                                cal_fine.selection_get().strftime('%Y-%m-%d'),)

                #controllo: data fine deve essere maggiore di ddata inizio
                data_fine_ter_dt = datetime.strptime(cal_fine.selection_get().strftime('%Y-%m-%d'), '%Y-%m-%d')
                data_inizio_ter_dt =  datetime.strptime(values[1], '%Y-%m-%d')

                if (data_fine_ter_dt < data_inizio_ter_dt):
                    messagebox.showinfo(message="La terapia non può finire prima di iniziare!", parent=top)
                    return       

                # update
                if(type(ter) == str):
                    messagebox.showinfo(message=ter, parent=top)
                    return
                else:
                    #mdidico teraspai
                    self.DB.my_query("UPDATE terapia SET nome_farm = %s, id_paz = %s, inizio=%s, qtaxdose = %s, ndosi = %s, ind = %s, tipo = %s, fine=%s WHERE id_paz=%s AND nome_farm =%s AND inizio=%s", 
                            ter.to_tupla() + (utente.get_id_paz_selezionato(), values[0], values[1]))
                    
                    logging.basicConfig(filename='storico.log', encoding='utf-8', level=logging.DEBUG)
                    logging.info(f'Il medico {utente.get_ID()} ha reso pregressa la seguente terapia concomitante pregressa:{ter.get_farmaco()}, {ter.get_inizio()} per il paziente {utente.get_id_paz_selezionato()}')
                    
                    top.destroy() #distruggo pop up
                    self.show_frame("ShowTerapie", parent, utente)
        
            # Create a button to close the Toplevel widget
            f1 = Frame(top)
            f1.pack()
            ttk.Button(f1, text="Modifica terapia", command=mod_ter_conc).pack(side='right', padx=10, pady=10) 
            ttk.Button(f1, text="Rendi Pregressa", command=conc2preg).pack(side='right', padx=10, pady=10)

        # Center the Toplevel widget on the screen
        top.update_idletasks()
        w = top.winfo_screenwidth()
        h = top.winfo_screenheight()
        size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        top.geometry("%dx%d+%d+%d" % (size + (x, y)))

        top.grab_set() 

################## MOD_PAZ ###################################
    
    ######### MODIFCIA PATOLOGIE CONCOMITANTI #################à

    def accetta_pat_conc(self, utente, nome_pat_conc, inizio_pat_conc, popup, parent):
        self.DB.my_query("UPDATE occ_patologia SET tipo='conc' WHERE nome_pat=%s AND id_paz=%s AND inizio=%s", 
                (nome_pat_conc, utente.get_id_paz_selezionato(), inizio_pat_conc)) 

        logging.basicConfig(filename='storico.log', encoding='utf-8', level=logging.DEBUG)
        logging.info(f'Il medico {utente.get_ID()} ha accettato la seguente patologia concomitante:{nome_pat_conc}, {inizio_pat_conc} per il paziente {utente.get_id_paz_selezionato()}')

        popup.destroy() #distruggo pop up
        self.show_frame("ModPaz", parent, utente)

    def rifiuta_pat_conc(self, utente, nome_pat_conc, inizio_pat_conc, popup, parent):
        self.DB.my_query("DELETE FROM occ_patologia WHERE id_paz = %s AND inizio = %s and nome_pat = %s",
                (utente.get_id_paz_selezionato(), inizio_pat_conc, nome_pat_conc))
        
        logging.basicConfig(filename='storico.log', encoding='utf-8', level=logging.DEBUG)
        logging.info(f'Il medico {utente.get_ID()} ha reso rifiutato la seguente patologia concomitante:{nome_pat_conc}, {inizio_pat_conc} per il paziente {utente.get_id_paz_selezionato()}')
        
        popup.destroy() #distruggo pop up
        self.show_frame("ModPaz", parent, utente)   
    
    def modifica_pat_conc(self, utente, data_inizio_pat_conc_new, nome_pat_conc_new, data_inizio_pat_conc_old, nome_pat_conc_old, popup, parent):

        if(nome_pat_conc_new== ""):
                messagebox.showinfo(message="Non hai inserito alcuna patologia")
                return

        #prima controllo la data: NO dopo di oggi, NO prima di prima terapia ipetensivaterapie_ipre
        #NS INUTOLE SPECIFICATEE TIPO, PERCHè èPRIMA TER è SEMPRE IPER
        terapie_iper = self.DB.my_query("SELECT * FROM Terapia WHERE id_paz=%s ORDER BY inizio", (utente.get_id_paz_selezionato(),))

        #controllo che il paziente abbia alemno una ter iper
        if(terapie_iper == []):
            messagebox.showinfo(message="Non puoi avere una patologia concomitante se non ha iniziato ancora una terapia ipertensiva")
            return
        
        #controllo che pa non abbia messo data del sintomo dopo di oggi, o prima di prima ter iper
        data_patologia_conc_new_dt = data_inizio_pat_conc_new
        data_inizio_pat_conc_old =  datetime.strptime(data_inizio_pat_conc_old, '%Y-%m-%d')
        data_prima_terapia_iper_dt =  datetime.strptime(terapie_iper[0][2].strftime('%Y-%m-%d'), '%Y-%m-%d')
        data_oggi_dt = datetime.today()

        #print(data_oggi_dt, data_patologia_conc_dt, data_prima_terapia_iper_dt)

        #paziente immette nuova nome di pat.
        #controllo che data di inzio nmon sia in range di una apt conc PREG con stesso nome
        pat_pregS = self.DB.my_query("SELECT inizio, fine FROM occ_patologia WHERE id_paz = %s and tipo='preg' and nome_pat = %s", (utente.get_id_paz_selezionato(), nome_pat_conc_new))
        if(len(pat_pregS) != 0):
            for pat_preg in pat_pregS:
                start_dt =  datetime.strptime(pat_preg[0].strftime('%Y-%m-%d'), '%Y-%m-%d')
                end_dt =  datetime.strptime(pat_preg[1].strftime('%Y-%m-%d'), '%Y-%m-%d')
                if(data_patologia_conc_new_dt <= end_dt and data_patologia_conc_new_dt>= start_dt):
                    messagebox.showinfo(message="In quel periodo stava già soffrendo di questa patologia.")
                    return

        #non deve esistere una patologia conc con uguale
        pat_conc = self.DB.my_query("SELECT * FROM occ_patologia WHERE tipo = %s AND id_paz = %s", ("conc", utente.get_id_paz_selezionato()))
        #farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine)
        for pat in pat_conc:
            if(nome_pat_conc_new == pat[0] and data_inizio_pat_conc_new >= data_inizio_pat_conc_old):
                messagebox.showinfo(message="Il paziente sta già soffrendo di questa patologia")
                return
        if(data_patologia_conc_new_dt < data_prima_terapia_iper_dt): #devo controllare che la data non sia qu
            messagebox.showinfo(message="Non puoi avere una patologia concomitante prima di aver seguito una terampia ipertensiva")
            return
        if(data_patologia_conc_new_dt > data_oggi_dt):
            messagebox.showinfo(message="Non puoi saper che patologia avrà il paziente nel futuro")
            return
            
         #creo ogetto segn_pat
        pat_conc = PatConc.create_patologia(nome_pat_conc_new, utente.get_ID(), data_inizio_pat_conc_new)
        
        #values[0] contine il nome della aptologia prima che enga moficiata, quindi il nome che c'0è sul DB
        self.DB.my_query("UPDATE occ_patologia SET nome_pat =%s, inizio=%s WHERE id_paz=%s AND nome_pat=%s AND inizio=%s", 
        pat_conc.to_tupla_update() + (utente.get_id_paz_selezionato(), nome_pat_conc_old, data_inizio_pat_conc_old))
        popup.destroy() #distruggo pop up
        self.show_frame("ModPaz", parent, utente)

        logging.basicConfig(filename='storico.log', encoding='utf-8', level=logging.DEBUG)
        logging.info(f'Il medico {utente.get_ID()} ha modificato la seguente patologia concomitante:{pat_conc.get_nome()}, {pat_conc.get_inizio()} per il paziente {utente.get_id_paz_selezionato()}')

    def conc2preg(self, utente, data_inizio, data_fine, nome_pat, popup, parent):
        #NB quando si pregrssa solo data di fine viene presa in cosiderazione, ALTRI DATI VARIATI IGNORATI
        # controllo che data fine sia maggiore di dati inzio

        #controllo: data fine deve essere maggiore di ddata inizio
        data_fine_ter_conc_dt =data_fine
        data_inizio_ter_conc_dt = data_inizio
        data_oggi_dt = datetime.today()

        pat_pregS = self.DB.my_query("SELECT inizio, fine FROM occ_patologia WHERE id_paz = %s and tipo='preg' and nome_pat = %s", (utente.get_id_paz_selezionato(), nome_pat))
        if(len(pat_pregS) != 0):
            for pat_preg in pat_pregS:
                start_dt =  datetime.strptime(pat_preg[0].strftime('%Y-%m-%d'), '%Y-%m-%d')
                end_dt =  datetime.strptime(pat_preg[1].strftime('%Y-%m-%d'), '%Y-%m-%d')
                if(data_fine_ter_conc_dt  <= end_dt and data_fine_ter_conc_dt >= start_dt):
                    messagebox.showinfo(message="In quel periodo stava già soffrendo di questa patologia.")
                    return
                elif(data_inizio_ter_conc_dt  <= start_dt and data_fine_ter_conc_dt >= end_dt):
                    messagebox.showinfo(message="C'è uan sovrapposzione temporale della stessa patologia.")
                    return

        if (data_fine_ter_conc_dt < data_inizio_ter_conc_dt):
            messagebox.showinfo(message="La patologia non può finire prima di iniziare!", parent=popup)
            return  
        elif(data_fine_ter_conc_dt > data_oggi_dt):
            messagebox.showinfo(message="Noi puoi sapere quando finirà una patologia", parent=popup)
            return   
        
        pat_preg = PatPreg.create_patologia(nome_pat, 
                                            utente.get_id_paz_selezionato(), 
                                            data_inizio, 
                                            data_fine )
        
        #print(pat_preg.to_tupla())
        # update
        if(type(pat_preg) == str):
            messagebox.showinfo(message=pat_preg, parent=popup)
            return
        else:
            #values[0] contine il nome della aptologia prima che enga moficiata, quindi il nome che c'0è sul DB
            #ATTENZIONE FANCOD UPDATE SOLO DI TIPO E FINE, ANCHE SE UTENTE MDOFICA INZIO E NOME:PAT,Q EUSTO NON VIENE CE CMABAITO
            #QIESTO è UN BENEE, COS' NON POSSO FARE LOS CHERZO DI METTERE DUE PAT PREG NELLO STESSO PERIODO
            self.DB.my_query("UPDATE occ_patologia SET tipo = 'preg', fine = %s WHERE id_paz=%s AND nome_pat=%s AND inizio=%s", 
            (pat_preg.get_fine(), utente.get_id_paz_selezionato(), pat_preg.get_nome(), pat_preg.get_inizio()))

            logging.basicConfig(filename='storico.log', encoding='utf-8', level=logging.DEBUG)
            logging.info(f'Il medico {utente.get_ID()} ha reso pregressa la seguente patologia concomitante:{pat_preg.get_nome()}, {pat_preg.get_inizio()} per il paziente {utente.get_id_paz_selezionato()}')

            popup.destroy() #distruggo pop up
            self.show_frame("ModPaz", parent, utente)

################## ADD_UTENTE ##################################

    def crea_utente(self, utente, id, nome, cognome, mail, dataN, id_med_ref, psw, parent):
        # mancano i controlli
        if (utente.get_tipo_utente_aggiunto() == 'R'): # se riesponsabile
            # id, nome, cognome, mail, dataN, hash_psw, fatt_risc, id_med_ref
            # creo l'oggetto reseponsabile  ID, nome, cognome, mail, dataN
            r = self.factory.crea_utente("responsabile", id, nome, cognome, mail, dataN)
            if(type(r) == str):
                messagebox.showinfo(message=r)
                return
            # aggiungo al DB un nuovo responsabile
            self.DB.my_query("INSERT INTO utente(id, nome, cognome, mail, dataN, hash_psw, fatt_risc, id_med_ref) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                    (r.to_tupla() + (self.to_hash(psw.encode('utf-8')), None, None)))
        
        elif (utente.get_tipo_utente_aggiunto() == 'M'): # se medico
            # creo l'oggetto medico
            m = self.factory.crea_utente("medico", id, nome, cognome, mail, dataN)
            print(id, nome, cognome, mail, dataN)
            print(type(m), m)
            if(type(m) == str):
                messagebox.showinfo(message=m)
                return
            # aggiungo al DB un nuovo responsabile
            self.DB.my_query("INSERT INTO utente(id, nome, cognome, mail, dataN, hash_psw, fatt_risc, id_med_ref) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                    (m.to_tupla() + (self.to_hash(psw.encode('utf-8')), None, None)))
        
        elif (utente.get_tipo_utente_aggiunto() == 'P'):
            # creo l'oggetto paziente  ID, nome, cognome, mail, da
            p = self.factory.crea_utente("paziente", id, nome, cognome, mail, dataN, fatt_risc=None, id_med_ref=id_med_ref)
            # aggiungo al DB un nuovo responsabile
            if(type(p) == str):
                messagebox.showinfo(message=p)
                return
            self.DB.my_query("INSERT INTO utente(id, nome, cognome, mail, dataN, fatt_risc, id_med_ref, hash_psw) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                        p.to_tupla() + (self.to_hash(psw.encode('utf-8')),) )

        self.show_frame("HomeResp", parent, utente)

################## CONTROLLI ###################################
    
    ############### P_ANOMALE ####################à

    def segn_p_anomala(self, utente, pminima, pmassima, parent):
        pminima = [int(x) for x in pminima]
        pmassima = [int(x) for x in pmassima]
        #print(pminima, pmassima)
        oggi = datetime.now()
        segnalazioni = [] #(data, id_paz, tipo, gravita)
        for min, max in zip(pminima, pmassima):
            # abbiamo deciso di inserire nel DB solamente le segnalazioni con categoria >= a normale -alta
            # if(min < 80 and max < 120):
            #     segnalazioni.append((oggi, utente.get_ID(), "p_anomala", "Ottimale"))
            # elif(min < 85 and max < 130):
            #     segnalazioni.append((oggi, utente.get_ID(), "p_anomala", "Normale"))
            if(min in range(85,89+1) and max in range(130,139+1)):
                segnalazioni.append((oggi, utente.get_ID(), "p_anomala", "Normale-alta"))
            elif(min in range(90,94+1) and max in range(140,149+1)):
                segnalazioni.append((oggi, utente.get_ID(), "p_anomala", "Ipertensione di grado I borderline"))
            elif(min in range(95,99+1) and max in range(150,159+1)):
                segnalazioni.append((oggi, utente.get_ID(), "p_anomala", "Ipertensione di grado I lieve"))
            elif(min in range(100,109+1) and max in range(160,169+1)):
                segnalazioni.append((oggi, utente.get_ID(), "p_anomala", "Ipertensione di grado II moderata"))
            elif(min >= 110 and max >= 180):
                segnalazioni.append((oggi, utente.get_ID(), "p_anomala", "Ipertensione di grado III grave"))
            elif(min <90 and max in range(140,149+1)):
                segnalazioni.append((oggi, utente.get_ID(), "p_anomala", "Ipertensione sistolica isolata borderline"))
            elif(min <90 and max >= 150):
                segnalazioni.append((oggi, utente.get_ID(), "p_anomala", "Ipertensione sistolica isolata"))
            elif(max > 230):
                segnalazioni.append((oggi, utente.get_ID(), "p_anomala", "Presione massima alta generica"))

        for segn in segnalazioni:
            s = Segnalazione.create_segnalazione(segn[0], segn[1], segn[2], segn[3])
            if(type(s) == str):
                messagebox.showinfo(message=s)
                return
            else:
                self.DB.my_query("INSERT INTO Segnalazione (data, id_paz, tipo, gravita) VALUES (%s,%s,%s,%s)", s.to_tupla())

    ############### NO_SEGUE ####################à

    def segn_no_segue(self, oggi, parent): #NB VUOLE STI
        
        oggi_str = oggi.strftime("%Y-%m-%d")
        r = self.DB.my_query("SELECT * FROM controlli_fatti WHERE giorno = %s", (oggi_str,))

        if(r == []):
            self.DB.my_query("INSERT INTO controlli_fatti (giorno) VALUES (%s)", (oggi_str,))

            pazienti = self.DB.my_query("SELECT id FROM utente WHERE id LIKE 'P%'", None)
            pazienti = [paz[0] for paz in pazienti]

            for paz in pazienti:

                no_log=0
                no_corr=0

                #1 fa
                ieri = oggi - timedelta(days=1) #sttenzione qui c'è anche orario
                ieri_str = ieri.strftime("%Y-%m-%d")

                r = self.DB.my_query("SELECT dg.giorno, ass.corretta FROM dati_gior AS dg JOIN assunzione AS ass ON (dg.giorno = ass.giorno) AND dg.id_paz = %s AND dg.giorno=%s", (paz, ieri_str))

                if(r == []): 
                    no_log +=1
                else:
                    corretti = [ass[1] for ass in r] # creao una lista con i valori bolenani delle liste ritonate dalla query
                    if not all(corretti):
                        no_corr += 1

                #2 fa
                ieri = oggi - timedelta(days=2) #sttenzione qui c'è anche orario
                ieri_str = ieri.strftime("%Y-%m-%d")

                r = self.DB.my_query("SELECT dg.giorno, ass.corretta FROM dati_gior AS dg JOIN assunzione AS ass ON (dg.giorno = ass.giorno) AND dg.id_paz = %s AND dg.giorno=%s", (paz, ieri_str))
                if(r == []): 
                    no_log +=1
                else:
                    corretti = [ass[1] for ass in r] # creao una lista con i valori bolenani delle liste ritonate dalla query
                    if not all(corretti):
                        no_corr += 1

                #3 fa
                ieri = oggi - timedelta(days=3) #sttenzione qui c'è anche orario
                ieri_str = ieri.strftime("%Y-%m-%d")

                r = self.DB.my_query("SELECT dg.giorno, ass.corretta FROM dati_gior AS dg JOIN assunzione AS ass ON (dg.giorno = ass.giorno) AND dg.id_paz = %s AND dg.giorno=%s", (paz, ieri_str))

                if(r == []): 
                    no_log +=1
                else:
                    corretti = [ass[1] for ass in r] # creao una lista con i valori bolenani delle liste ritonate dalla query
                    if not all(corretti):
                        no_corr += 1           

                if(no_log+no_corr == 3):
                    s = Segnalazione.create_segnalazione(oggi_str, paz, 'no_segue', None)
                    if(type(s) == str):
                        messagebox.showinfo(message=s)
                        return
                    else:
                        self.DB.my_query("INSERT INTO Segnalazione (data, id_paz, tipo, gravita) VALUES (%s,%s,%s,%s)", s.to_tupla())

    ################ gestione pse #############################àà
        # funzione che crea le password criptate per inserirle nel DB, chiamata quando si crea un nuovo utente
    def to_hash(self, chiaro):
        # creo la pssword hashata
        hashed = bcrypt.hashpw(chiaro, bcrypt.gensalt())
        # ritorno la pssword ascata e il sale
        return (hashed.decode('utf-8'))

    # funzione che mi permette di controllare le psw nel momento do login chiamata in Start Page
    def check_psw(self, psw, hashed):
        if bcrypt.checkpw(psw.encode('utf-8'), hashed.encode('utf-8')):
            return True
        return False

#SE IL NOME DEL FILE è MAIN VIENE ESEGUITO QUESTA APRTE
if __name__ == "__main__":
    app = App() #creo la mia applicazione (istanza di TK, ovvero finestra)
    app.mainloop()
