from my_library import *
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import re 

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class DatiPersonali(tk.Frame):

    def __init__(self, parent, controller, utente):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        if(utente != None): #ovverro non sto solo inzializadno la pagina per il dizionario
            terapie = controller.DB.my_query("SELECT * FROM terapia WHERE id_paz = %s AND (tipo='preg' OR tipo='conc' OR tipo='iper') ORDER BY tipo", (utente.get_ID(),))
            patologie = controller.DB.my_query("SELECT * FROM occ_patologia WHERE id_paz = %s AND (tipo='conc' OR tipo='preg')", (utente.get_ID(),))

            
##################### TABELLA TERAPIE #####################
        
            # soluzione con treeview
            f1 = LabelFrame(self, text='Terapie', font=controller.font)
            f1.pack(fill=BOTH, expand=True, padx=10)
            # faccio il treeview
            colonne_ter = ('Farmaco', 'Inizio', 'Qxdose', 'Ndosi', 'Tipo', 'Ind')
            tabella_ter = ttk.Treeview(f1, columns=colonne_ter, show='headings', style="Custom.Treeview") 
            # denominazione delle colonne
            tabella_ter.column('Farmaco', anchor=CENTER)
            tabella_ter.heading('Farmaco', text='Farmaco')
            tabella_ter.column('Inizio', anchor=CENTER, width=100)
            tabella_ter.heading('Inizio', text='Inizio')
            tabella_ter.column('Qxdose', anchor=CENTER)
            tabella_ter.heading('Qxdose', text='Qxdose')
            tabella_ter.column('Ndosi', anchor=CENTER, width=100)
            tabella_ter.heading('Ndosi', text='Ndosi')
            tabella_ter.column('Tipo', anchor=CENTER, width=100)
            tabella_ter.heading('Tipo', text='Tipo')
            tabella_ter.column('Ind', anchor=CENTER, width=100)
            tabella_ter.heading('Ind', text='Ind')
            tabella_ter["displaycolumns"]=("Farmaco", "Inizio", "Qxdose", "Ndosi", "Tipo")

            #COTNROLA CHE DATIP NON SIA VUPOTA!!!!!!!
            # aggiungo i record che mi ritornano dalla query
            for record in terapie:
                t = ""
                if(record[6] == "preg"): t="Pregressa"
                elif(record[6] == "conc"): t = "Concomitante"
                else: t="Ipertensiva"
                ind = record[5]
                if(record[5] == "" or record[5] == None or re.match(r'^[ \n\t]*$', record[5]) is not None): ind = "Nessuna indicazione specificata"
                tabella_ter.insert('', END, values=[record[0], record[2], record[3], record[4], t, ind])

            tabella_ter.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # aggiungo la scrollbar
            # s1 = ttk.Scrollbar(self, orient=VERTICAL, command=tabella_sin.yview)
            # s1.grid(row=0, column=1, sticky='ns')
            # tabella_sin.configure(yscrollcommand=s1.set)

            def popup(event):
                id_riga= tabella_ter.selection()[0]
                values = tabella_ter.item(id_riga, "values")
                messagebox.showinfo(title= "Indicazioni", message=values[5])#NB indice della tabella
            tabella_ter.bind("<Double-1>",lambda event: popup(event))


##################### TABELLA PATOLOGIE #####################
        
            # soluzione con treeview
            f2 = LabelFrame(self, text='Patologie', font=controller.font)
            f2.pack(fill=BOTH, expand=True, padx=10)
            # (nome_pat, id_paz, inizio, tipo, fine)
            colonne_pat = ('Patologia', 'Tipo', 'Inizio','Fine')
            tabella_pat = ttk.Treeview(f2, columns=colonne_pat, show='headings', style="Custom.Treeview") 
            # denominazione delle colonne
            tabella_pat.column('Patologia', anchor=CENTER)
            tabella_pat.heading('Patologia', text='Patologia')
            tabella_pat.column('Tipo', anchor=CENTER, width=100)
            tabella_pat.heading('Tipo', text='Tipo')
            tabella_pat.column('Inizio', anchor=CENTER, width=100)
            tabella_pat.heading('Inizio', text='Inizio')
            tabella_pat.column('Fine', anchor=CENTER, width=100)
            tabella_pat.heading('Fine', text='Fine')
            tabella_pat["displaycolumns"]=('Patologia', 'Tipo', 'Inizio','Fine')

            # aggiungo i record che mi ritornano dalla query
            for record in patologie:  # (nome_pat, id_paz, inizio, tipo, fine)
                t = ""
                if(record[3] == "preg"): t="Pregressa"
                elif(record[3] == "conc"): t = "Concomitante"
                fine = record[4]
                if (fine  is None): fine = "Non terminata"
                tabella_pat.insert('', END, values=[record[0], t, record[2], fine])

            tabella_pat.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # aggiungo la scrollbar
            # s1 = ttk.Scrollbar(self, orient=VERTICAL, command=tabella_sin.yview)
            # s1.grid(row=0, column=1, sticky='ns')
            # tabella_sin.configure(yscrollcommand=s1.set)
        
        ####### BOTTONI PER VISULIZZARE PRESSIONI #####
            f3 = LabelFrame(self, text='Visualiza pressioni', font=controller.font)
            f3.pack(fill=BOTH, expand=True, padx=10)

            def vis_sett(tipoP):

                top = Toplevel()
                top.title(f'Pressioni {tipoP} dell''ultima settimana')
                top.geometry("1000x500")

                c_n, y_n = controller.get_pressioni_sett(utente.get_ID(), tipoP, parent)

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

                    c_n, min, max = controller.get_pressioni_mese(utente.get_ID(), anno.get(), mese.get(), parent)

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
                                command=lambda: grafico_mese() if anno.get() and mese.get() else None,)
                b_andamento.grid(row=3, column=1, pady=10)

                window.grab_set() 

            f3.grid_columnconfigure(0, weight=1)
            f3.grid_columnconfigure(1, weight=1)
            f3.grid_columnconfigure(2, weight=1)
            b_sett_min = ttk.Button(f3, text="Pressioni Minime ultimi sette giorni", command=lambda: vis_sett("minima"), style='Custom.TButton',)
            b_sett_min.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            b_sett_min = ttk.Button(f3, text="Pressioni massime ultimi sette giorni",  command=lambda: vis_sett("massima"), style='Custom.TButton',)
            b_sett_min.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            b_mese = ttk.Button(f3, text="Pressioni mensili", command=lambda: vis_mese(), style='Custom.TButton',)
            b_mese.grid(row=0, column=2, sticky="nsew", padx=20, pady=20)

################## INDIETRO #####################

            # bottone di logout
            def indietro():
                controller.show_frame("HomePaz", parent, utente)
            ttk.Button(self, text="Indietro", command=indietro, style='Custom.TButton', width=30).pack(pady=10)