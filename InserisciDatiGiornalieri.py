from my_library import *

class InserisciDatiGiornalieri(tk.Frame):

    c = 2 #per contare a che punto sono arrivato a ripeire il singolo array
    def __init__(self, parent, controller, utente):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        if(utente != None):

        ###### DATA DI OGGI ###############
            oggi = f"{datetime.now().day}-{datetime.now().month}-{datetime.now().year}"
            Label(self, text=f"Giorno: {oggi}", font=controller.title_font, foreground="black").pack()

            pmin = []; pmin.append(StringVar(value="inserisci"))
            pmax = []; pmax.append(StringVar(value="inserisci"))
            ore_pressioni = []; ore_pressioni.append(StringVar(value="inserisci"))

            fp = Frame(self)
            fp.pack()
            Label(fp, text=f"Misurazione numero 1" ,foreground="black", font=controller.font).grid(row=1,column=0, pady=3)

            Label(fp, text="Pmin" ,foreground="black", font=controller.font).grid(row=0,column=1)
            pmin_entry = ttk.Entry(fp, textvariable=pmin[0], width=30, font=controller.font) #così psw è nascosta
            pmin_entry.grid(row=1,column=1, padx=10, pady=3)
            pmin_entry.focus()

            Label(fp, text="Pmax" ,foreground="black", font=controller.font).grid(row=0,column=2)
            pmax_entry = ttk.Entry(fp, textvariable=pmax[0], width=30, font=controller.font) #così psw è nascosta
            pmax_entry.grid(row=1,column=2, padx=10, pady=3)

            Label(fp, text="Ora" ,foreground="black", font=controller.font).grid(row=0,column=3)
            cb = ttk.Combobox(fp, textvariable=ore_pressioni[0], width=30, font=controller.font)
            cb["values"] =['00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30','06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30']
            cb.grid(row=1,column=3, padx=10, pady=3)
            cb["state"] = "readonly"

            widget = [] # contiene gli oggetti widget

            def addP():
                if(self.c>5):
                    messagebox.showinfo(message="Non puoi immettre più di 5 misurazioni al giorno.")
                else:
                    pmin.append(StringVar(value="inserisci"))
                    pmax.append(StringVar(value="inserisci"))
                    ore_pressioni.append(StringVar(value="inserisci"))
                    riga=self.c
                    
                    l = Label(fp, text=f"Misurazione numero {riga}" ,foreground="black", font=controller.font)
                    l.grid(row=riga,column=0, padx=10, pady=3)
                    widget.append(l)
                    
                    pmin_entry = ttk.Entry(fp, textvariable=pmin[self.c-1], width=30, font=controller.font) #così psw è nascosta
                    pmin_entry.grid(row=riga,column=1, padx=10, pady=3)
                    widget.append(pmin_entry)

                    pmax_entry = ttk.Entry(fp, textvariable=pmax[self.c-1], width=30, font=controller.font) #così psw è nascosta
                    pmax_entry.grid(row=riga,column=2, padx=10, pady=3)
                    widget.append(pmax_entry)

                    # ora_entry = Entry(fp, textvariable=ora[self.c-1]) #così psw è nascosta
                    # ora_entry.grid(row=riga,column=3)
                    cb = ttk.Combobox(fp, textvariable=ore_pressioni[self.c-1], width=30, font=controller.font)
                    cb["values"] =['00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30','06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30']
                    cb.grid(row=riga,column=3)
                    cb["state"] = "readonly"
                    widget.append(cb)
 
                    self.c +=1 
                    
            def remP():
                if(self.c == 2):
                    return #almeno un apresisone ci deve essere
                pmin.pop()
                pmax.pop()
                ore_pressioni.pop()
                # ora tocca ai widget
                print(len(widget), widget)
                for w in widget[-4:]: # mi prendo gli ultimo quattro widget e li distruggo
                    w.destroy()
                del widget[-4:]    # tolgo gli ultimo quattro wi
                print(len(widget))
                
                # widget_pmin = self.grid_slaves(row=self.c-1, column=0)
                # widget_pmin[0].destory()
                self.c -=1


            ttk.Button(fp, text="+", command=addP, style='Custom.TButton', width=5).grid(row=0, column=4, pady=10)
            ttk.Button(fp, text="-", command=remP, style='Custom.TButton', width=5).grid(row=1, column=4, pady=4)

            Label(self, text="Hai seguito le seguenti assunzioni di farmaci, relativi alle tue terapie?" ,foreground="black", font=controller.font).pack(pady=10)

            terapie = controller.DB.my_query("SELECT * FROM terapia WHERE id_paz=%s", (utente.get_ID(),)) 
            #print(terapie)
            #a(farmaco, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine)

            cluster_farmaco = []
            cluster_inizio_ter = []
            cluster_dosi = []
            cluster_yn = []
            assunzioni = []
            cluster_ore_assunzioni = []
            if(terapie!=[]): #se paz ha almeno una terapia
                
                for terapia in terapie: #predno una tupla della rispostya del DB, che sorripodne a un a singola terapia
                    if(terapia[6] == "iper"):
                        for dose in range(terapia[4]): #ripeto la singola terpaia tamnte volte qunte sono le NDOSI
                            assunzioni.append(f"{terapia[3]} di {terapia[0]}, dose {dose+1} ") #dose deve aprtier da 1!!!
                            cluster_dosi.append(dose+1)
                            cluster_farmaco.append(f"{terapia[0]}")
                            cluster_inizio_ter.append(f"{terapia[2]}")

                    
                
                for _ in range(len(assunzioni)): cluster_yn.append(StringVar())
                
                for _ in range(len(assunzioni)): cluster_ore_assunzioni.append(StringVar())

                for i in range(0, len(assunzioni)):
                    frame = Frame(self)
                    frame.pack()
                    Label(frame, text=assunzioni[i], foreground="black", font=controller.font).pack(side="left")

                    style_radio = ttk.Style()
                    style_radio.configure('Custom.TRadiobutton', font=controller.font)

                    ttk.Radiobutton(frame, text="Sì", variable=cluster_yn[i], value="si", style='Custom.TRadiobutton').pack(side="left")
                    ttk.Radiobutton(frame, text="No", variable=cluster_yn[i], value="no", style='Custom.TRadiobutton').pack(side="left")
                    cb = ttk.Combobox(frame, textvariable=cluster_ore_assunzioni[i], width=30, font=controller.font)
                    cb["values"] =["", '00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30',
                                   '04:00','04:30','05:00','05:30','06:30','07:00','07:30','08:00',
                                   '08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00',
                                   '12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00',
                                   '16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00',
                                   '20:30','21:00','21:30','22:00','22:30','23:00','23:30']
                    cb.pack(side="left")
                    cb["state"] = "readonly"
                    #Entry(frame, textvariable=cluster_ora[i]).pack(side="left")


            button = ttk.Button(self, text="Invia", style='Custom.TButton', width=20,
                                 command=lambda: controller.invia( pmin, pmax, ore_pressioni, cluster_yn, 
                                                                                cluster_farmaco, cluster_inizio_ter, 
                                                                                cluster_dosi, cluster_ore_assunzioni, assunzioni, utente, parent))
            button.pack(side="right", padx=20)

            def indietro():
                controller.show_frame("HomePaz", parent, utente)  


            button = ttk.Button(self, text="Indietro", command=indietro,  style='Custom.TButton', width=20,)
            button.pack(side="left", padx=20)