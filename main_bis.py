
import pandas as pd
import sys
import random

fin = open("input.xlsx", "rb")      # File di input
fout = open("output.txt", "w")     # File di output
#fout = sys.stdout                   # Output per deubg
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


def scegliConfigurazione(nc,dict,job,init):
    global schedule
    new = job*100+random.randint(1, nc)
    #config = dict[id]
    if init:
        schedule.append(new)
    else:
        min = job*100
        max = (job+1)*100
        for i in range(len(schedule)):
            if schedule[i] >= min and schedule[i] < max:
                if schedule[i] == job:
                    return scegliConfigurazione(nc,dict,job,init)
                else:
                    old = schedule[i]
                    schedule[i] = new
                    break
        return (old,new) 

def creaSchedule(dict):
    global schedule
    cpy = schedule.copy()
    cpy.reverse()
    j1 = dict[cpy.pop()]
    times = []
    times.append(j1[0])
    for i in range(1,nmacchine):
        times.append(j1[i]+times[i-1])
    while cpy:
        j2 = dict[cpy.pop()]
        m = 0
        while m+1 < nmacchine:
            i = 1
            x = j1[m+1]
            y = j2[m]
            while y >= x and m+1+i < nmacchine:
                x += j1[m+1+i]
                y += j2[m+i]
                i += 1
            if (y >= x): break
            m +=1
        times[m] += j2[m]
        for j in range(m-1,-1,-1):
            times[j] = times[j+1]-j2[j+1]
        for k in range(m+1,nmacchine):
            times[k] = times[k-1]+j2[k]
        j1 = j2
    return times[nmacchine-1]


#########################################################################################################################################################


dimensions = pd.read_excel(fin, header=header, sheet_name=sname).shape
nrighe = dimensions[0]              # Numero righe del file
njob = int(nrighe/nmacchine)        # Numero job da eseguire
nconfigurazioni = dimensions[1]     # Numero delle diverse configurazioni trovate
array = [0] * (njob*100+nconfigurazioni)

d = creaDizionario(njob,nconfigurazioni,nrighe)
print("Setup iniziale eseguito correttamente.")

nripetizioni = input("Inserire il numero di ripetizioni che si vogliono eseguire:\n")
niterazioni = input("Inserire il numero di iterazioni che si vogliono eseguire per ciascuna ripetizione:\n")

for i in range(int(nripetizioni)):

    schedule = []
    ottimo_cor = sys.maxsize
    ottimo_schedule = []

    for j in range(1,njob+1):
        scegliConfigurazione(nconfigurazioni,d,j,True)
    time = creaSchedule(d)
    if  (time < ottimo_cor):
        ottimo_cor = time
    ottimo_schedule = schedule.copy()
    # print("Scelta una configurazione iniziale casuale per tutti i job: "+str(schedule)+".", file=fout)
    # print("Il tempo impiegato dalla configurazione iniziale è "+str(time)+".\n", file=fout)



    for j in range(int(niterazioni)):
        # print("Iterazione #"+str(j+1), file=fout)
        (old,new) = scegliConfigurazione(nconfigurazioni,d,(j%njob)+1,False)
        # print(str(old)+" -> "+str(new), file=fout)
        time = creaSchedule(d)
        # print("Il tempo impiegato dalla configurazione attuale è "+str(time), file=fout)
        if  (time < ottimo_cor):
            ottimo_cor = time
            ottimo_schedule = schedule.copy()
        else:
            schedule = ottimo_schedule.copy()
        # print("L'ottimo corrente è pari a "+str(ottimo_cor)+"\n", file=fout)

    # print("Completate "+niterazioni+" iterazioni.", file=fout)
    print("Il valore ottimo ottenuto dalla ripetizione #"+str(i+1)+" è pari a "+str(ottimo_cor)+", con uno schedule che ha la seguente configurazione: "+str(ottimo_schedule)+ ".\n", file=fout)
    for elem in ottimo_schedule:
        array[elem] += 1

for i in range(len(array)):
    val = array[i]
    if val > 3:
        print("La configurazione "+str(i)+" è usata "+str(val)+" volte.", file=fout)