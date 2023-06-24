from UtenteFactory import *
from my_library import *
from datetime import datetime

factory = UtenteFactory()

p = factory.crea_utente("paziente", "P000001", "luigi", "rossi", "@@@", "1900-09-22", "ansia", "M000001" )
print(p)
print(p.to_tupla())
m = factory.crea_utente("medico", "M000001", "luigi", "rossi", "@@@", "1900-09-22" )
print(m.to_tupla())
r = factory.crea_utente("responsabile", "R000001", "luigi", "rossi", "@@@", "1900-09-22" )
print(r.to_tupla())

d = datetime.strptime("2023-05-22", '%Y-%m-%d').date()
print(type(d))