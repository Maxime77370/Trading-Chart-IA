import tkinter as tk
from tkinter import *
import csv
import os
import numpy as np 

import pandas as pd

pair = "AUD-CAD"
path = os.getcwd().replace("/VIEWER","") + str("/DATA/") + str(pair) + str(".csv") #créeation de la direction du fichier.
bars = pd.read_csv(path)

X = bars.copy()
candles_bidopen = X.pop('bidopen')
candles_bidclose = X.pop('bidclose')
candles_bidhigh = X.pop('bidhigh')
candles_bidlow = X.pop('bidlow')

viewer = tk.Tk()

viewer.title('viewer')

viewer.geometry('1200x720')

viewer.configure(bg='#4F4F4F')



width_canvas2, height_canvas2 = 1170, 690
canvas2 = Canvas(viewer, width=width_canvas2, height=height_canvas2, background='#1B202B')
ligne3 = []
ligne4 = []

open = candles_bidopen
close = candles_bidclose
plusbas = candles_bidhigh
plushaut = candles_bidlow

def max(source, lenght):
    maxi = 0.0
    for x in range(lenght):
        i = source[x]
        if i >= maxi:
            maxi = i
        print(maxi)
    return maxi

def min(source, lenght):
    mini = 0.0
    for x in range(lenght):
        i = source[x]
        if i <= mini:
            mini = i
        print(mini)
    return mini

bas = min(plusbas, 20)-0.001
haut = max(plushaut, 20)+0.001


diff = (haut - bas)/15
#7



for x in range(1, 15):
    ligne3 = canvas2.create_line((width_canvas2/15)*x, 0, (width_canvas2/15)*x, height_canvas2, fill='#3F4B66')
    ligne3 = canvas2.create_line(0, (height_canvas2/15)*x, width_canvas2, (height_canvas2/15)*x, fill='#3F4B66')
    txt2 = canvas2.create_text(60, 30, text=pair, font="Arial 16", fill="#A6A4AB")
    txt = round(haut - x*diff, 3)
    txt2 = canvas2.create_text((width_canvas2/100)*98, (height_canvas2/15)*x, text=txt, font="Arial 16", fill="#A6A4AB")



for x in range(20):

    x1 = 15-(close[x]-bas)/diff
    x2 = 15-(open[x]-bas)/diff
    x3 = 15-(plusbas[x]-bas)/diff
    x4 = 15-(plushaut[x]-bas)/diff

    if x1 < x2:
        color = 'green'
    else:
        color = 'red'

    rect1 = canvas2.create_rectangle((50+(x*50)), (height_canvas2/15)*x2, ((80+(x*50)), (height_canvas2/15)*x1), fill=color)
    ligne3 = canvas2.create_line(((65+(x*50)), (height_canvas2/15)*x1, (65+(x*50)), (height_canvas2/15)*x3), fill=color)
    ligne3 = canvas2.create_line(((65+(x*50)), (height_canvas2/15)*x1, (65+(x*50)), (height_canvas2/15)*x4), fill=color)

canvas2.place(x=10, y=10)

def motion(event):
    x, y = event.x, event.y
    txt2 = canvas2.create_text(60, 60, text=x, font="Arial 16", fill="#A6A4AB")

viewer.bind('<Motion>', motion)

viewer.mainloop()