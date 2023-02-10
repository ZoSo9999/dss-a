
import pandas as pd
import sys
import random

fin = open("input.xlsx", "rb")      # File di input
fout = open("output.txt", "w")     # File di output
#fout = sys.stdout                   # Output per deubg
header = None                       # Non è presente header nel file di input
sname = "DatiOriginali"             # Nome del foglio da leggere
nmacchine = 5                       # Numero di macchine del processo
schedule = []


def creaDizionario(nj,nc,nr):
    dict = {}
    nletture = nj*nc
    for i in range(nletture):
        col = int(i/nj)
        skiprows = (i*nmacchine)%nr
        schedule = pd.read_excel(fin, header=header, sheet_name=sname, skiprows=skiprows, nrows=nmacchine, usecols=[col]).squeeze("columns").array
        id = ((i%20)+1)*100+col+1       # Per trovare una configurazione njob*100+nconfigurazione (njob ∈ [1,20] e ncofigurazione ∈ [1,40]
        dict[id]=schedule
    print("Ho creato il dizionario delle configurazioni con successo")
    return dict


def scegliConfigurazione(nc,dict,job,init):
    global schedule
    id = job*100+random.randint(1, nc)
    config = dict[id]
    if init:
        schedule.append(id)
    else:
        min = job*100
        max = (job+1)*100
        for i in range(len(schedule)):
            if schedule[i] >= min and schedule[i] < max:
                if schedule[i] == job:
                    return scegliConfigurazione(nc,dict,job,init)
                else:
                    schedule[i] = id
                    break
    return config




#####################################################################################################################################


dimensions = pd.read_excel(fin, header=header, sheet_name=sname).shape
nrighe = dimensions[0]              # Numero righe del file
njob = int(nrighe/nmacchine)        # Numero job da eseguire
nconfigrazioni = dimensions[1]      # Numero delle diverse configurazioni trovate

d = creaDizionario(njob,nconfigrazioni,nrighe)
for i in range(1,njob+1):
    config = scegliConfigurazione(nconfigrazioni,d,i,True)
print(schedule)
config = scegliConfigurazione(nconfigrazioni,d,20,False)
print(schedule)

