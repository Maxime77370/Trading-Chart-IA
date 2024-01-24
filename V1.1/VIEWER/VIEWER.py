import tkinter as tk
from tkinter import *
import csv
import os
import numpy as np 
import pandas as pd


class display(tk.Canvas):

    def __init__(self, pair, master):

        self.first_lap = 0

        self.path = os.getcwd().replace("/VIEWER","") + str("/DATA/") + str(pair) + str(".csv") #créeation de la direction du fichier.
        self.bars = pd.read_csv(self.path)
        self.X = self.bars.copy()
        self.candles_bidopen = self.X.pop('bidopen')
        self.candles_bidclose = self.X.pop('bidclose')
        self.candles_bidhigh = self.X.pop('bidhigh')
        self.candles_bidlow = self.X.pop('bidlow')
        self.candles_sma = self.X.pop('sma')
        self.candles_wma = self.X.pop('wma')
        self.candles_ema = self.X.pop('ema')

        root.geometry('1200x720')
        root.configure(bg='#4F4F4F')

        self.width_canvas_graph = 1200
        self.height_canvas_graph = 720

        self.candles_decalage = 9000
        self.candles_number = 30

        self.canvas_graph = Canvas(root, width=1600, height=720, background='#1B202B')
        self.canvas_graph.pack(side=TOP,fill=BOTH,expand=YES)

        self.canvas_graph_def()
        root.bind('<Motion>', self.motion)
        root.bind("<Configure>", self.configure)
        root.bind("<Key>", self.key)

    def motion(self, event):
        self.x, self.y = event.x , event.y

        if self.first_lap == 1:
            self.canvas_graph.delete(self.line_y, self.line_x)
            self.line_x = None

        self.line_y = self.canvas_graph.create_line(0, self.y, self.width_canvas_graph, self.y, dash=(4, 2), fill='#3F4B66')
        self.line_x = self.canvas_graph.create_line(self.x, 0, self.x, self.height_canvas_graph, dash=(4, 2), fill='#3F4B66')

        self.first_lap = 1

    def configure(self, event):
        self.canvas_graph.delete("all")
        self.height_canvas_graph, self.width_canvas_graph = event.height, event.width
        self.canvas_graph_def()

    def key(self, event):
        key_pressed = event.keysym
        if key_pressed == 'Right' and self.candles_decalage < 10000:
            self.candles_decalage += 1
        if key_pressed == 'Left' and self.candles_decalage > 0:
            self.candles_decalage -= 1
        if key_pressed == 'Up':
            self.candles_number += 1
        if key_pressed == 'Down' and self.candles_number > 0:
            self.candles_number -= 1

        self.canvas_graph.delete("all")
        self.canvas_graph_def()

    def canvas_graph_def(self):

        self.auto_focus(self.candles_bidhigh, self.candles_bidlow, self.candles_number, self.candles_decalage)

        for x in range(1, self.candles_number):
            self.line_background = self.canvas_graph.create_line((self.width_canvas_graph/self.candles_number)*x, 0, (self.width_canvas_graph/self.candles_number)*x, self.height_canvas_graph, fill='#3F4B66')
            self.line_background = self.canvas_graph.create_line(0, (self.height_canvas_graph/self.candles_number)*x, self.width_canvas_graph, (self.height_canvas_graph/self.candles_number)*x, fill='#3F4B66')

            self.price = round(self.high - x*self.diff_max, 3)
            self.text_price = self.canvas_graph.create_text((self.width_canvas_graph/100)*98, (self.height_canvas_graph/self.candles_number)*x, text=self.price, font="Arial 16", fill="#A6A4AB")

        for x in range(self.candles_number):

            self.x_high  = self.height_canvas_graph*(self.candles_bidhigh[x+self.candles_decalage]-self.low)/self.diff_max
            self.x_low   = self.height_canvas_graph*(self.candles_bidlow[x+self.candles_decalage]-self.low)/self.diff_max
            self.x_close = self.height_canvas_graph*(self.candles_bidclose[x+self.candles_decalage]-self.low)/self.diff_max
            self.x_open  = self.height_canvas_graph*(self.candles_bidopen[x+self.candles_decalage]-self.low)/self.diff_max

            if self.x_close < self.x_open:
                self.candles_color = 'green'
            else:
                self.candles_color = 'red'

            self.candles_draw = self.canvas_graph.create_rectangle(((self.width_canvas_graph/self.candles_number)*x-(self.width_canvas_graph/self.candles_number)/2.5, self.x_open, (self.width_canvas_graph/self.candles_number)*x+(self.width_canvas_graph/self.candles_number)/2.5, self.x_close), fill=self.candles_color)
            self.candles_draw = self.canvas_graph.create_line(((self.width_canvas_graph/self.candles_number)*x, self.x_close, (self.width_canvas_graph/self.candles_number)*x, self.x_low), fill=self.candles_color)
            self.candles_draw = self.canvas_graph.create_line(((self.width_canvas_graph/self.candles_number)*x, self.x_close, (self.width_canvas_graph/self.candles_number)*x, self.x_high), fill=self.candles_color)

        for x in range(self.candles_number):
            if x+self.candles_decalage > 14:

                self.x_sma_1  = self.height_canvas_graph*(self.candles_sma[x+self.candles_decalage-1]-self.low)/self.diff_max
                self.x_sma_2  = self.height_canvas_graph*(self.candles_sma[x+self.candles_decalage]-self.low)/self.diff_max
                self.line_sma = self.canvas_graph.create_line((self.width_canvas_graph/self.candles_number)*(x-1), self.x_sma_1, (self.width_canvas_graph/self.candles_number)*x, self.x_sma_2, fill='#00BFFF')

        for x in range(self.candles_number):
            if x+self.candles_decalage > 14:

                self.x_wma_1  = self.height_canvas_graph*(self.candles_wma[x+self.candles_decalage-1]-self.low)/self.diff_max
                self.x_wma_2  = self.height_canvas_graph*(self.candles_wma[x+self.candles_decalage]-self.low)/self.diff_max
                self.line_wma = self.canvas_graph.create_line((self.width_canvas_graph/self.candles_number)*(x-1), self.x_wma_1, (self.width_canvas_graph/self.candles_number)*x, self.x_wma_2, fill='#FFA500')

        for x in range(self.candles_number):
            if x+self.candles_decalage > 14:

                self.x_ema_1  = self.height_canvas_graph*(self.candles_ema[x+self.candles_decalage-1]-self.low)/self.diff_max
                self.x_ema_2  = self.height_canvas_graph*(self.candles_ema[x+self.candles_decalage]-self.low)/self.diff_max
                self.line_ema = self.canvas_graph.create_line((self.width_canvas_graph/self.candles_number)*(x-1), self.x_ema_1, (self.width_canvas_graph/self.candles_number)*x, self.x_ema_2, fill='#FA8072')


    def canvas_indic_def(self):
        pass


    def auto_focus(self, source_high, source_low, lenght, decalage):

        self.maxi = 0.0
        for x in range(lenght):
            self.i = source_high[x+decalage]
            if self.i >= self.maxi:
                self.maxi = self.i

        self.mini = 9999999999 #valeurs élever car sinon ca na marche pas.
        for x in range(lenght):
            self.i = source_low[x+decalage]
            if self.i <= self.mini:
                self.mini = self.i

        self.high = self.maxi
        self.low  = self.mini

        self.diff_max = (self.high - self.low)

        self.high = self.high  + self.diff_max/20
        self.low  = self.low - self.diff_max/20

        self.diff_max = (self.high - self.low)


pair = "EUR-USD"

root = tk.Tk()
root.title('Ping Pong Interface')
class_display = display(pair, root)
root.mainloop()