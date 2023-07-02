from my_library import *
from Paziente import *
from Medico import *
from Responsabile import *
from tkinter import PhotoImage
import os

class StartPage(tk.Frame): #ogni pagina è un framwe, che semplcietne viene fatto rise quando si vuole vedere

    def __init__(self, parent, controller, utente): 
        tk.Frame.__init__(self, parent) #cortruttore di frame noramle )serve il frame padre)
        self.controller = controller #il controllo,ovvero la finetsra root in cui il frame deve apparire, è quello passato (quindi qulleo inzile, quello creato nella classe pricnipale)
       
 #così widget si adattono a grandezza schermo!!!!!fanno outameticmete biding
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
       
        label = tk.Label(self, text="Inserisci le tue credenziali:", foreground="black", font=controller.title_font)
        label.grid(row=0, columnspan=2)

        label_ID= Label(self, text="Inserisci ID:" ,foreground="black", font=controller.font)
        label_ID.grid(row=1, column=0, sticky="e")

        ID = StringVar()
        ID_entry = ttk.Entry(self, textvariable=ID, width=30, font=controller.font)
        ID_entry.insert(0, "M000001") #SOLO PER TESTING VA T0LTO !!!!!!!!!
        ID_entry.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        ID_entry.focus() #inzio cersore su di lui

        label_psw= Label(self, text="Inserisci psw:" ,foreground="black", font=controller.font)
        label_psw.grid(row=2, column=0, sticky="e")

        psw = StringVar()
        psw_entry = ttk.Entry(self, textvariable=psw, show="*", width=30, font=controller.font) #così psw è nascosta
        psw_entry.insert(0, "m000001") #SOLO PER TESTING VA T0LTO !!!!!!!!!
        psw_entry.grid(row=2, column=1, sticky="w", padx=10, pady=10)


        button = ttk.Button(self, text="Login", style='Custom.TButton',
                        command= lambda: controller.login(ID.get(), psw.get(), parent), width=20)
        button.grid(row=3, columnspan=2, pady=10)

        # cwd = os.getcwd()
        # #image = PhotoImage(file=os.path.join(cwd, "cuore.png"))
        # image = PhotoImage(file="./cuore.png")
        # Label(self, image=image).grid(row=4, columnspan=2)

        from PIL import Image, ImageTk

        image = Image.open("./cuore.png")
        image = image.resize((600, 600), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        

        label = Label(self, image = photo)
        label.image = photo
        label.grid(row=4, columnspan=2)