from my_library import *
from Paziente import *
from Patologia import *
from Terapia import *

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt 

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class VisPaz(tk.Frame):

    def __init__(self, parent, controller, utente):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        if(utente != None):
            
            dati = controller.DB.my_query("SELECT * FROM utente WHERE ID = %s", (utente.get_id_paz_selezionato(),) )
            #(id, nome, cognome, mail, dataN, hash_psw, fatt_risc, id_med_ref)
            
            frame = LabelFrame(self, text="Paziente", font=controller.font)
            frame.pack(fill="x", padx=10)
            Label(frame, text=f"Stai osservando il paziente:\n{dati[0][1]} {dati[0][2]}, ID: {dati[0][0]}", font=controller.font).pack()

        
    ################ MODIFICA DATI PAZIENT E #######################
            f2 = LabelFrame(self, text='Modifica dati', font=controller.font)
            f2.pack(fill=BOTH, expand=True, padx=10)

            f2.grid_columnconfigure(0, weight=1)
            f2.grid_columnconfigure(1, weight=1)
            f2.grid_columnconfigure(2, weight=1)

            ttk.Button(f2, text="Gestisci patologie", command=lambda: controller.show_frame("ModPaz", parent, utente), style='Custom.TButton',).grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            ttk.Button(f2, text="Gestisci Terapie", command=lambda: controller.show_frame("ShowTerapie", parent, utente), style='Custom.TButton',).grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            ttk.Button(f2, text="Modifica fattori di rischio", command=lambda: controller.mod_fatt_risc(utente, utente.get_id_paz_selezionato(), parent), style='Custom.TButton').grid(row=0, column=2, sticky="nsew", padx=20, pady=20)

    ################ GRAFICI PRESSIONI #######################

            def vis_sett(tipoP):

                top = Toplevel()
                top.title(f'Pressioni {tipoP} dell''ultima settimana')
                top.geometry("1000x500")

                c_n, y_n = controller.get_pressioni_sett(utente.get_id_paz_selezionato(), tipoP, parent)

                # create a figure
                figure = Figure(figsize=(3,1), dpi=100)
                # create FigureCanvasTkAgg object
                figure_canvas = FigureCanvasTkAgg(figure, top)
                # create the toolbar
                NavigationToolbar2Tk(figure_canvas, top)
                # create axes
                axes = figure.add_subplot()

                penguin_means = {} #PINGUINI VOLUTI!!!!!!
                for i, n_mis in enumerate(y_n):
                    penguin_means[i] = n_mis

                x = np.arange(len(c_n))  # the label locations
                width = 0.2  # the width of the bars
                multiplier = 0

                for attribute, measurement in penguin_means.items():
                    offset = width * multiplier
                    rects = axes.bar(x + offset, measurement, width, label=attribute)
                    #axes.bar_label(rects, padding=3)
                    multiplier += 1

                axes.set_ylabel(f'Pressione {tipoP}')
                axes.set_title(f'Andamento pressione {tipoP} ultima settimana')
                axes.set_xticks(x + width, c_n)
                #axes.legend(loc='upper left', ncols=3)
                axes.set_ylim(0, 300)

                figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

                # Center the Toplevel widget on the screen
                top.update_idletasks()
                w = top.winfo_screenwidth()
                h = top.winfo_screenheight()
                size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
                x = w/2 - size[0]/2
                y = h/2 - size[1]/2
                top.geometry("%dx%d+%d+%d" % (size + (x, y)))

                top.grab_set() 

            def vis_mese():
                
                window = Toplevel()
                window.title('Pressioni nel mese')
                window.geometry("800x500")
                window.protocol("WM_DELETE_WINDOW", window.destroy)

                frame1 = Frame(window)
                frame1.pack()

                Label(frame1, text="scegli l'anno: ").grid(row=0, column=0)
                anno=StringVar()
                cb_anno = ttk.Combobox(frame1, textvariable=anno)
                cb_anno["values"] = [i for i in range(2023, 1900, -1)]
                cb_anno.grid(row=0, column=1)
                cb_anno["state"] = "readonly"

                Label(frame1, text="scegli il mese: ").grid(row=1, column=0)
                mese=StringVar()
                cb_mese = ttk.Combobox(frame1, textvariable=mese)
                cb_mese["values"] = [f"{i:02}" for i in range(1, 13)]
                cb_mese.grid(row=1, column=1, pady=10)
                cb_mese["state"] = "readonly"

                def grafico_mese():

                    frame1.destroy()

                    c_n, min, max = controller.get_pressioni_mese(utente.get_id_paz_selezionato(), anno.get(), mese.get(), parent)

                    # create a figure
                    figure = Figure(figsize=(3,1), dpi=100)
                    # create FigureCanvasTkAgg object
                    figure_canvas = FigureCanvasTkAgg(figure, window)
                    # create the toolbar
                    NavigationToolbar2Tk(figure_canvas, window)
                    # create axes
                    axes = figure.add_subplot()

                    penguin_means = {'1': min,'2': max}
                    x = np.arange(len(c_n))  # the label locations
                    width = 0.2  # the width of the bars
                    multiplier = 0

                    for attribute, measurement in penguin_means.items():
                        offset = width * multiplier
                        rects = axes.bar(x + offset, measurement, width, label=attribute)
                        #axes.bar_label(rects, padding=3) #mete valoir sopra colonne
                        multiplier += 1

                    # Add some text for labels, title and custom x-axis tick labels, etc.
                    axes.set_ylabel('media pressioni minime e massime nel mese')
                    axes.set_title('Andamento media pressioni minime e massime nel mese')
                    axes.set_xticks(x + width, c_n)
                    #axes.legend(loc='upper left', ncols=3)
                    axes.set_ylim(0, 300)

                    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


                b_andamento = ttk.Button(frame1, text="Mostra andamento", 
                                command=lambda: grafico_mese() if anno.get() and mese.get() else None) #solo se hanno isneirto mese a anno grafico_nmese è invocata
                b_andamento.grid(row=3, column=1, pady=10)

                window.grab_set() 

            f3 = LabelFrame(self, text='Visualiza pressioni', font=controller.font)
            f3.pack(fill=BOTH, expand=True, padx=10)

            f3.grid_columnconfigure(0, weight=1)
            f3.grid_columnconfigure(1, weight=1)
            f3.grid_columnconfigure(2, weight=1)
            b_sett_min = ttk.Button(f3, text="Pressioni Minime ultimi sette giorni", command=lambda: vis_sett("minima"), style='Custom.TButton',)
            b_sett_min.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            b_sett_min = ttk.Button(f3, text="Pressioni massime ultimi sette giorni",  command=lambda: vis_sett("massima"), style='Custom.TButton',)
            b_sett_min.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            b_mese = ttk.Button(f3, text="Pressioni mensili", command=lambda: vis_mese(), style='Custom.TButton',)
            b_mese.grid(row=0, column=2, sticky="nsew", padx=20, pady=20)
            
    #######TABELLA SEGNALZIONI P_ANOMALE E NO_SEGUE############

            #NB non essendoci operazioni, inutili portarla nel controller
            frame2 = LabelFrame(self, text="Segnalazione del paziente", font=controller.font)
            frame2.pack(fill="x", padx=10)
            # (cod, data, id_paz, tipo, gravita)
            datiP = controller.DB.my_query("SELECT * FROM Segnalazione WHERE id_paz = %s ORDER BY data DESC", (utente.get_id_paz_selezionato(),))

            #print(datiP)
            # soluzione con treeview
            colonne_segn =  ('Cod', 'Data', 'id_paz', 'Tipo', 'Gravita')
            tabella_segn = ttk.Treeview(frame2, columns=colonne_segn, show='headings', style="Custom.Treeview", height=5) 
            # denominazione delle colonne
            tabella_segn.column('Cod', anchor=CENTER); tabella_segn.heading('Cod', text='Codice')
            tabella_segn.column('Data', anchor=CENTER); tabella_segn.heading('Data', text='Data')
            tabella_segn.column('Tipo', anchor=CENTER); tabella_segn.heading('Tipo', text='Tipo')
            tabella_segn.column('Gravita', anchor=CENTER); tabella_segn.heading('Gravita', text='Gravita')
            tabella_segn["displaycolumns"]=("Cod", "Data", "Tipo")

            # aggiungo i record che mi ritornano dalla query
            for record in datiP:
                #if(record[3] == "p_anomala" or record[3] == "no_segue"):
                tabella_segn.insert('', END, values=record)

            frame2.grid_columnconfigure(0, weight=1)
            tabella_segn.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

            # # aggiungo la scrollbar
            s1 = ttk.Scrollbar(frame2, orient=VERTICAL, command=tabella_segn.yview)
            s1.grid(row=0, column=2, sticky='ns')
            tabella_segn.configure(yscrollcommand=s1.set)

            def OnDoubleClick_info(event):
                item = tabella_segn.selection()[0]
                values = tabella_segn.item(item, "values")
                tipo = values[3]
                top = Toplevel()
                frame = LabelFrame(top, text="Segnalazione")
                frame.pack(fill="both", expand=True, padx=10, pady=10)                

                if(tipo == "p_anomala"):
                    Label(frame, text="Il giorno {}, il paziente {} ha avuto valori di pressioni anomali, con gravità: {}".format(
                                        values[1], values[2], values[4] )).grid(row=0, columnspan=2)
                if(tipo == "no_segue"):
                    Label(frame, text="In data {}, il paziente {} non ha seguito la terapia per più di tre giorni.".format(values[1], values[2])).grid(row=0, columnspan=2)
                # Center the Toplevel widget on the screen
                top.update_idletasks()
                w = top.winfo_screenwidth()
                h = top.winfo_screenheight()
                size = tuple(int(_) for _ in top.geometry().split('+')[0].split('x'))
                x = w/2 - size[0]/2
                y = h/2 - size[1]/2
                top.geometry("%dx%d+%d+%d" % (size + (x, y)))

                top.grab_set()

            tabella_segn.bind("<Double-1>", OnDoubleClick_info)

    #######TABELLA SINTOMI IN CORSO############

            #NB non essendoci operazioni, inutili portarla nel controller
            frame3 = LabelFrame(self, text="Sintomi in corso e Assunzioni farmacologiche", font=controller.font)
            frame3.pack(fill="x", padx=10)
            frame3.grid_columnconfigure(0, weight=1)
            frame3.grid_columnconfigure(2, weight=1)
            # (nome_sint, id_paz, inizio, tipo, fine)
            datiP = controller.DB.my_query("SELECT * FROM occ_sintomo WHERE id_paz = %s AND tipo='conc' ORDER BY inizio", (utente.get_id_paz_selezionato(),))

            #print(datiP)
            # soluzione con treeview
            colonne_sint =  ('Sintomo', 'Data Inizio')
            tabella_sint = ttk.Treeview(frame3, columns=colonne_sint, show='headings', style="Custom.Treeview", height=5)
            # denominazione delle colonne
            tabella_sint.column('Sintomo', anchor=CENTER, width=150); tabella_sint.heading('Sintomo', text='Sintomo')
            tabella_sint.column('Data Inizio', anchor=CENTER, width=100); tabella_sint.heading('Data Inizio', text='Data Inizio')
            tabella_sint["displaycolumns"]=("Sintomo", "Data Inizio")


            # aggiungo i record che mi ritornano dalla query
            for record in datiP:
                tabella_sint.insert('', END, values=[record[0], record[2]])

            tabella_sint.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

            # aggiungo la scrollbar
            s1 = ttk.Scrollbar(frame3, orient=VERTICAL, command=tabella_sint.yview)
            s1.grid(row=0, column=1, sticky='ns')
            tabella_sint.configure(yscrollcommand=s1.set)
          
    #######TABELLA ASSUNZIONI ############

            #(nome_farm, id_paz, inizio_ter, giorno, dose, ora, corretta)
            datiP = controller.DB.my_query("SELECT * FROM assunzione WHERE id_paz = %s ORDER BY giorno DESC", (utente.get_id_paz_selezionato(),))

            # soluzione con treeview
            colonne_assunzione =  ('Giorno', 'Farmaco', 'Dose', 'Ora', 'Corretta')
            tabella_assunzione = ttk.Treeview(frame3, columns=colonne_assunzione, show='headings', style="Custom.Treeview", height=5) 
            # denominazione delle colonne
            tabella_assunzione.column('Giorno', anchor=CENTER, width=100); tabella_assunzione.heading('Giorno', text='Giorno')
            tabella_assunzione.column('Farmaco', anchor=CENTER, width=100); tabella_assunzione.heading('Farmaco', text='Farmaco')
            tabella_assunzione.column('Dose', anchor=CENTER, width=100); tabella_assunzione.heading('Dose', text='Dose')
            tabella_assunzione.column('Ora', anchor=CENTER, width=100); tabella_assunzione.heading('Ora', text='Ora')
            tabella_assunzione.column('Corretta', anchor=CENTER, width=100); tabella_assunzione.heading('Corretta', text='Corretta')
            tabella_assunzione["displaycolumns"]=('Giorno', 'Farmaco', 'Dose', 'Ora')


            # aggiungo i record che mi ritornano dalla query
            for record in datiP:
                c = "No"
                if record[6]:
                    c="Sì"
                if record[6]: #solo se è cioreeta la metto, altrimi tutte quelle sbalgiate che hanno assunzione a mezzantote ci sono tutte!!!!!
                    tabella_assunzione.insert('', END, values=[ record[3], record[0], record[4], record[5], c])

            tabella_assunzione.grid(row=0, column=2, sticky="nsew", padx=20, pady=20)

            # aggiungo la scrollbar
            s2 = ttk.Scrollbar(frame3, orient=VERTICAL, command=tabella_assunzione.yview)
            s2.grid(row=0, column=3, sticky='ns')
            tabella_assunzione.configure(yscrollcommand=s2.set)


############### INDIETRO ###############################à
            def indietro():
                    controller.show_frame("HomeMed", parent, utente)
            ttk.Button(self, text="Indietro", command=indietro, style='Custom.TButton', width=30).pack(pady=10)


