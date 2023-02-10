
import pandas as pd
import sys

fin = open("input.xlsx", "rb")      # File di input
#fout = open("output.txt", "w")     # File di output
fout = sys.stdout                   # Output per deubg
header = None                       # Non è presente header nel file di input
sname = "DatiOriginali"             # Nome del foglio da leggere
nmacchine = 5                       # Numero di macchine del processo



def creaDizionario(nj,nc,nr):
    dict = {}
    nletture = nj*nc
    for i in range(nletture):
        col = int(i/nj)
        skiprows = (i*nmacchine)%nr
        schedule = pd.read_excel(fin, header=header, sheet_name=sname, skiprows=skiprows, nrows=nmacchine, usecols=[col]).squeeze("columns").array
        id = ((i%20)+1)*100+col+1       # Per trovare una configurazione njob*100+nconfigurazione (njob ∈ [1,20] e ncofigurazione ∈ [1,40]
        dict[id]=schedule
    return dict


#####################################################################################################################################


dimensions = pd.read_excel(fin, header=header, sheet_name=sname).shape
nrighe = dimensions[0]              # Numero righe del file
njob = int(nrighe/nmacchine)        # Numero job da eseguire
nconfigrazioni = dimensions[1]      # Numero delle diverse configurazioni trovate

d = creaDizionario(njob,nconfigrazioni,nrighe)
print(d)