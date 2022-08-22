import cbpro
import pandas as pd
import numpy as np
import csv
from data import *
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

f = Figure()
a = f.add_subplot(1,1,1)
style.use("ggplot")

global polja
polja=["timestamp","cijena"]

with open("data.csv","w") as csv_file:
    csv_writer=csv.DictWriter(csv_file,fieldnames=polja)
    csv_writer.writeheader()

NewClient=cbpro.AuthenticatedClient(apiKey,apiSecret,passphrase)

currency="BTC-USD"
kolicina=0.0

public_client=cbpro.PublicClient()

global index
index=0

app=Tk()

def ulozi():
        global ul1_int
        ul1=ulog.get()
        ul1_int=float(ul1)

        global kolicina
        kolicina= float(ul1_int) / float(ci1_int)



def loop():

    if True:

        spotCijena=NewClient.get_product_ticker(product_id=currency)
        cijena=StringVar()
        cijena.set(spotCijena["price"])
        part_label=Label(app, textvariable=cijena, font=("bold", 10), width=7)
        part_label.grid(row=0, column=5)

        global index
        index+=1

        ci1=cijena.get()
        global ci1_int
        ci1_int=float(ci1)


        with open("data.csv","a")as csv_file:
            csv_writer=csv.DictWriter(csv_file,fieldnames=polja)
            info={
               "timestamp":index,
               "cijena":ci1_int
            }
            csv_writer.writerow(info)


        c=StringVar()
        c.set(currency)
        part_label=Label(app,textvariable=c)
        part_label.grid(row=5,column=1)

        pd.DataFrame()

        povijest=public_client.get_product_historic_rates(currency)


        redci=["Datum","Open", "Najviša cijena", "Najniža cijena","Close"]

        for row in povijest:
            del row[5:]

        global tablica
        tablica=pd.DataFrame(povijest,columns=redci)





        if kolicina>0:
            global vrijednostPort
            vrijednostPort=float(kolicina)*float(ci1_int)
            global vr_p
            vr_p=StringVar()
            vr_p.set(vrijednostPort)
            part_label=Label(app, textvariable=vr_p)
            part_label.grid(row=1,column=1)

        kolVar=StringVar()
        kolVar.set(kolicina)

        part_label = Label(app, textvariable=kolVar, font=("bold",10))
        part_label.grid(row=5, column=0)
        part_label.config(width=20)



        app.after(1000,loop)

loop()

def izvezi():
    np.savetxt("Povijest Cijena.txt",tablica, fmt="%.2f")

add_btn=Button(app, text="Save-aj povijest cijena", command=izvezi, width=0)
add_btn.grid(row=4, column=0, pady=20)

add_btn=Button(app, text="Uloži", width=3, command=ulozi)
add_btn.grid(row=2, column=0, pady=20)

part_label = Label(app, text="Koliko želite uložiti", font=("bold",10),pady=20, padx=20)
part_label.grid(row=0, column=0, sticky=W)

part_label = Label(app, text="Trenutno stanje", font=("bold",10),pady=20)
part_label.grid(row=0, column=1, sticky=E)

ulog=IntVar()

part_entry=Entry(app,textvariable=ulog)
part_entry.grid(row=1,column=0)


#part_list=Listbox(app, height=8, width=50)
#part_list.grid(row=1, column=1, columnspan=2, rowspan=4, pady=20, padx=20)

part_label = Label(app, text="Odaberi koji crypto želiš trgovati", font=("bold",10))
part_label.grid(row=1, column=5)

def setBTC():
    plt.clf()
    with open("data.csv","w") as csv_file:
        csv_writer=csv.DictWriter(csv_file,fieldnames=polja)
        csv_writer.writeheader()
    global index
    index=0
    global currency
    currency="BTC-USD"

add_btn=Button(app, text="BTC-USD", command=setBTC)
add_btn.grid(row=2, column=5,padx=10)


def setETH():
    plt.clf()
    with open("data.csv","w") as csv_file:
        csv_writer=csv.DictWriter(csv_file,fieldnames=polja)
        csv_writer.writeheader()
    global index
    index=0
    global currency
    currency="ETH-USD"



add_btn=Button(app, text="ETH-USD", command=setETH)
add_btn.grid(row=2, column=6)


def setXLM():
    plt.clf()
    with open("data.csv","w") as csv_file:
        csv_writer=csv.DictWriter(csv_file,fieldnames=polja)
        csv_writer.writeheader()
    global index
    index=0
    global currency
    currency="XLM-USD"


add_btn=Button(app, text="XLM-USD", command=setXLM)
add_btn.grid(row=3, column=6,padx=40)


def setCRO():
    plt.clf()
    with open("data.csv","w") as csv_file:
        csv_writer=csv.DictWriter(csv_file,fieldnames=polja)
        csv_writer.writeheader()
    global index
    index=0
    global currency
    currency="CRO-USD"


add_btn=Button(app, text="CRO-USD", command=setCRO)
add_btn.grid(row=3, column=5,padx=40)

def osiguraj():
    part_label1=Label(app, textvariable=vr_p)
    part_label1.grid(row=1,column=1)
    part_label1.config(width=2)
    global kolicina
    kolicina=0.0


add_btn=Button(app, text="Osiguraj trenutno stanje", command=osiguraj, width=0)
add_btn.grid(row=3, column=0, pady=20)


part_label = Label(app, textvariable="", font=("bold",10))

app.title("trading bot")
app.geometry("800x400")


def animate(i):
    data=pd.read_csv("data.csv")
    x=data["timestamp"]
    y=data["cijena"]
    plt.cla()
    plt.plot(x,y)

ani = anim.FuncAnimation(plt.gcf(), animate, interval=1000)
plt.show()

figure = plt.Figure(figsize=(6,5), dpi=100)
ax = figure.add_subplot(111)


app.mainloop()

