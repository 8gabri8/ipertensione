from my_library import *

class ModPaz(tk.Frame):

    def __init__(self, parent, controller, utente): #utente è medico
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        if(utente != None):
            dati = controller.DB.my_query("SELECT * FROM utente WHERE ID = %s", (utente.get_id_paz_selezionato(),) )
            #(id, nome, cognome, mail, dataN, hash_psw, fatt_risc, id_med_ref)
            
            frame0 = LabelFrame(self, text="Paziente", font=controller.font)
            frame0.pack(fill="x")
            Label(frame0, text=f"Stai osservando il paziente:\n{dati[0][1]} {dati[0][2]}, ID: {dati[0][0]}", font=controller.font).pack()

#################### TABELLA PAT PREGRESSE ###################

            frame2 = LabelFrame(self, text="Patologie pregresse", font=controller.font)
            frame2.pack(fill="x")
            #(nome_pat, id_paz, inizio, tipo, fine)
            datiP = controller.DB.my_query("SELECT Nome_pat, inizio, fine FROM occ_patologia WHERE id_paz = %s AND tipo = %s", (utente.get_id_paz_selezionato(), "preg"))

            colonneP = ["Nome", "Inizio", "Fine"]
            tabella_preg = ttk.Treeview(frame2, columns=colonneP, show="headings", style="Custom.Treeview") #la prima riga della tabell ha nome dellecoloenn

            tabella_preg.column('Nome', anchor=CENTER, width=100)
            tabella_preg.heading('Nome', text='Nome')
            tabella_preg.column('Inizio', anchor=CENTER, width=100)
            tabella_preg.heading('Inizio', text='Inizio')
            tabella_preg.column('Fine', anchor=CENTER, width=100)
            tabella_preg.heading('Fine', text='Fine')

            # aggiungo i record che mi ritornano dalla query
            for record in datiP:
                tabella_preg.insert('', END, values=record)

            frame2.grid_columnconfigure(0, weight=1)
            tabella_preg.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

            tabella_preg.grid(row=0, column=0, pady=10)
            s1 = ttk.Scrollbar(frame2, orient=VERTICAL, command=tabella_preg.yview)
            s1.grid(row=0, column=1, sticky='ns')
                
###################### eventuale modifica pat preg #############################################################
            # def OnDoubleClick_preg(event):
            #     # Get the item ID of the selected row
            #     item = tabella_preg.selection()[0]

            #     # Get the values of the selected row
            #     values = tabella_preg.item(item, "values")

            #     # Create a new Toplevel widget
            #     top = Toplevel()

            #     # Set the title of the Toplevel widget
            #     top.title("Patologia pregressa")

            #     # Create a LabelFrame for the patient information
            #     frame = LabelFrame(top, text="Patologie Pregresse")
            #     frame.pack(fill="both", expand=True, padx=10, pady=10)

            #     # Create Labels for each piece of information
            #     Label(frame, text="Nome:").grid(row=0, column=0, sticky="e")
            #     #Label(frame, text=values[0]).grid(row=0, column=1, sticky="w")
            #     name = StringVar()
            #     name_entry = Entry(frame, width=30, textvariable=name)
            #     name_entry.insert(END, values[0])
            #     name_entry.grid(row=0, column=1, sticky="w")

            #     Label(frame, text="Data Inizio:").grid(row=1, column=0, sticky="e")
            #     date_format = "%Y-%m-%d"
            #     initial_date = datetime.strptime(values[1], date_format).date() #contine data ianzilae
            #     cal_inizio = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd', year=initial_date.year,
            #                           month=initial_date.month, day=initial_date.day) # Change the date pattern here
            #     cal_inizio.grid(row=1, column=1, sticky="w")

            #     Label(frame, text="Data Fine:").grid(row=2, column=0, sticky="e")
            #     date_format = "%Y-%m-%d"
            #     final_date = datetime.strptime(values[2], date_format).date() #contine data ianzilae
            #     #print(final_date)
            #     cal_fine = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd', year=final_date.year,
            #                           month=final_date.month, day=final_date.day) # Change the date pattern here
            #     cal_fine.grid(row=2, column=1, sticky="w")

            #     def modDB():
            #         #modifico cose a DB
            #         # creazione oggetto selezione
            #         pat_preg = PatPreg.create_patologia(name.get(), 
            #                                             utente.get_id_paz_selezionato(), 
            #                                             cal_inizio.selection_get().strftime('%Y-%m-%d'), 
            #                                             cal_fine.selection_get().strftime('%Y-%m-%d'))
                    
                    
            #         if(type(pat_preg) == str):
            #             pass
            #         else:
            #             #values[0] contine il nome della aptologia prima che enga moficiata, quindi il nome che c'0è sul DB
            #             my_query("UPDATE patologia SET nome =%s, inizio=%s, fine=%s WHERE id_paz=%s AND nome=%s AND inizio=%s", 
            #             pat_preg.to_tupla_update() + (pat_preg.get_id_paz(), values[0], values[1]))
            #             top.destroy() #distruggo pop up
            #             controller.show_frame("ModPaz", parent, utente)

            #     # Create a button to close the Toplevel widget
            #     Button(frame, text="Conferma", command=modDB).grid(row=4, column=1, pady=10)

            #     # Center the Toplevel widget on the screen
            #     top.update_idletasks()
            #     w = top.winfo_screenwidth()
            #     h = top.winfo_screenheight()
            #     size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
            #     x = w/2 - size[0]/2
            #     y = h/2 - size[1]/2
            #     top.geometry("%dx%d+%d+%d" % (size + (x, y)))

            # tabella_preg.bind("<Double-1>", OnDoubleClick_preg)
            
            # s1 = ttk.Scrollbar(frame2, orient=VERTICAL, command=tabella_preg.yview)
            # s1.grid(row=0, column=1, sticky='ns')

##################### TABELLA PAT CONCOMITANTI ######################################
            # PATOLOGIA COMCOMINanti
            frame3 = LabelFrame(self, text="Patologie concomitanti", font=controller.font)
            frame3.pack(fill="x")

            #(nome_pat, id_paz, inizio, tipo, fine)
            datiC = controller.DB.my_query("SELECT nome_pat, inizio, tipo FROM occ_patologia WHERE id_paz = %s AND (tipo = 'conc' OR tipo='segn_pat_conc')", (utente.get_id_paz_selezionato(),))

            colonneC = ["Nome", "Inizio", "Tipo"]
            tabella_conc = ttk.Treeview(frame3, columns=colonneC, show="headings", style="Custom.Treeview") #la prima riga della tabell ha nome dellecoloenn

            tabella_conc.column('Nome', anchor=CENTER, width=100)
            tabella_conc.heading('Nome', text='Nome')
            tabella_conc.column('Inizio', anchor=CENTER, width=100)
            tabella_conc.heading('Inizio', text='Inizio')
            tabella_conc.column('Tipo', anchor=CENTER, width=100)
            tabella_conc.heading('Tipo', text='Tipo')

            frame3.grid_columnconfigure(0, weight=1)
            tabella_conc.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            s2 = ttk.Scrollbar(frame3, orient=VERTICAL, command=tabella_conc.yview)
            s2.grid(row=0, column=1, sticky='ns')

            # aggiungo i record che mi ritornano dalla query
            for record in datiC:
                if(record[2] == "conc"):
                    tabella_conc.insert('', END, values=[record[0], record[1], "Confermata"])
                else:
                    tabella_conc.insert('', END, values=[record[0], record[1], "Segnalata"])

            def OnDoubleClick_mod_pat_conc(event):
                id_riga= tabella_conc.selection()[0]
                values = tabella_conc.item(id_riga, "values")

                top = Toplevel()
                top.title("Patologia concomitante")

                # Create a LabelFrame for the patient information
                frame = LabelFrame(top, text="Patologie Concomitante", font=controller.font)
                frame.pack(fill="both", expand=True, padx=10, pady=10)

                if(values[2] == "Segnalata"):
                    Label(frame, text=f"Il paziente ha segnalato la seguente patologia concomitante, vuoi accettrala?\nPatologia: {values[0]}\n Inizio: {values[1]}").grid(row=0, columnspan=2, sticky="e")
                       
                    ttk.Button(frame, text="Accetta", command=lambda: controller.accetta_pat_conc(utente, values[0], values[1], top, parent)).grid(row=1, column=0, pady=10)
                    
                    ttk.Button(frame, text="Rifiuta", command=lambda: controller.cancella_pat_conc(utente, values[0], values[1], top, parent)).grid(row=1, column=1, pady=10)

                else: #confemrata

                    # Create Labels for each piece of information
                    Label(frame, text="Nome Patologia:").grid(row=0, column=0, sticky="w", padx=10)
                    #Label(frame, text=values[0]).grid(row=0, column=1, sticky="w")
                    cb_pat = ttk.Combobox(frame)
                    pat = controller.DB.my_query("SELECT Nome FROM Patologia", None)
                    pat = [str(item[0]) for item in pat]
                    cb_pat["values"] = pat
                    cb_pat.grid(row=0,column=1, sticky="w")
                    cb_pat["state"] = "readonly"
                    cb_pat.set(values[0])

                    Label(frame, text="Data Inizio:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
                    date_format = "%Y-%m-%d"
                    initial_date = datetime.strptime(values[1], date_format).date() #contine data ianzilae
                    cal_inizio = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd', year=initial_date.year,
                                            month=initial_date.month, day=initial_date.day) # Change the date pattern here
                    cal_inizio.grid(row=1, column=1, sticky="w", padx=10, pady=10)

                    Label(frame, text="Data Fine:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
                    cal_fine = Calendar(frame, date_pattern='yyyy-mm-dd') # Change the date pattern here
                    cal_fine.grid(row=2, column=1, sticky="w", padx=10, pady=10)
                    
                    # Create a button to close the Toplevel widget
                    ttk.Button(frame, text="Modifica", command=lambda: controller.modifica_pat_conc(utente, datetime.strptime(cal_inizio.selection_get().strftime('%Y-%m-%d'), '%Y-%m-%d'),
                                                                                                cb_pat.get(), values[1], values[0], top, parent)).grid(row=4, column=0, padx=10, pady=10)

                    ttk.Button(frame, text="Rendi Pregressa", command=lambda: controller.conc2preg(utente, datetime.strptime(values[1], '%Y-%m-%d'),
                                                                                                datetime.strptime(cal_fine.selection_get().strftime('%Y-%m-%d'), '%Y-%m-%d'),
                                                                                                values[0], top, parent)).grid(row=4, column=1, padx=10, pady=10)

                # Center the Toplevel widget on the screen
                top.update_idletasks()
                w = top.winfo_screenwidth()
                h = top.winfo_screenheight()
                size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
                x = w/2 - size[0]/2
                y = h/2 - size[1]/2
                top.geometry("%dx%d+%d+%d" % (size + (x, y)))

                top.grab_set()

            tabella_conc.bind("<Double-1>", lambda event: OnDoubleClick_mod_pat_conc(event))

##############INDIETRO #########################à

            def indietro():
                    controller.show_frame("VisPaz", parent, utente)
            ttk.Button(self, text="Indietro", command=indietro, style='Custom.TButton', width=30).pack(pady=10)




