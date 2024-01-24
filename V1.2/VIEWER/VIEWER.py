import PIL as pl
from PIL import ImageTk
import tkinter as tk
from tkinter import *
import csv
import os
from os import *
from os.path import isfile, join
import pandas as pd


class display(tk.Canvas):

    def __init__(self, master):

        self.first_lap = 0

        self.pair_all = [f for f in listdir(os.getcwd().replace("/VIEWER","") + str("/DATA/")) if isfile(join(os.getcwd().replace("/VIEWER","") + str("/DATA/"), f))]
        self.pair_all_len = len(self.pair_all)

        self.n_pair = 0

        self.candles_number = 40

        self.load_new_pair()

        self.index_indic = [
                                True,  #indic_sma
                                True,  #indic_wma
                                True,  #indic_ema
                                True,  #indic_rsi
                                False, #indic_stoch
                                False  #indic_ichomoku
                            ]
        self.all_indic = [
                            'sma',
                            'wma',
                            'ema',
                            'rsi',
                            'stoch',
                            'ichomoku'
                        ]

        root.geometry('1200x720')
        root.configure(bg='#4F4F4F')

        self.width_canvas = 1200
        self.height_canvas = 720

        self.width_canvas_graph = 1200
        self.height_canvas_graph = self.height_canvas

        print(self.path)

        self.reglage_overlay = False
        self.reglage_icon = PhotoImage(file='img/bouton_de_reglage.png')
        self.checkbox_on_icon = PhotoImage(file='img/checkbox_on.png')
        self.checkbox_off_icon = PhotoImage(file='img/checkbox_off.png')
        self.croix_icon = PhotoImage(file='img/croix.png')

        self.canvas_graph = Canvas(root, width=self.width_canvas, height=self.height_canvas, background='#1B202B')
        self.canvas_graph.pack(side=TOP,fill=BOTH,expand=YES)

        self.images = []

        self.canvas_indic = True

        self.canvas_graph_def()
        root.bind('<Motion>', self.motion)
        root.bind("<Configure>", self.configure)
        root.bind("<Key>", self.key)
        root.bind("<Button-1>", self.callback)

    def motion(self, event):

        self.x, self.y = event.x , event.y

        if self.first_lap == 1:
            self.canvas_graph.delete(self.line_y, self.line_x)
            self.canvas_graph.delete(self.text_test)
            self.line_x = None

        if self.reglage_overlay == False:

            self.line_y = self.canvas_graph.create_line(0, self.y, self.width_canvas_graph, self.y, dash=(4, 2), fill='#3F4B66')
            self.line_x = self.canvas_graph.create_line(self.x, 0, self.x, self.height_canvas, dash=(4, 2), fill='#3F4B66')

            if self.y < self.height_canvas_graph:

                self.text = self.diff_max_graph / self.height_canvas_graph * (self.height_canvas_graph-self.y) + self.low_graph
                self.text_test = self.canvas_graph.create_text(self.x + 10, self.y - 10,text=self.text, fill='white', anchor="sw")


            if self.y > self.height_canvas_graph and self.y < self.height_canvas_indic+self.height_canvas_graph:

                self.text = self.diff_max_indic / self.height_canvas_indic * (self.height_canvas_indic+self.height_canvas_graph-self.y) + self.low_indic
                self.text_test = self.canvas_graph.create_text(self.x + 10, self.y - 10,text=self.text, fill='white', anchor="sw")

            self.first_lap = 1

    def configure(self, event):
        self.canvas_graph.delete("all")
        self.height_canvas, self.width_canvas = event.height, event.width

        if self.canvas_indic == True:
            self.width_canvas_graph = self.width_canvas
            self.height_canvas_graph = self.height_canvas * 3/4

            self.width_canvas_indic = self.width_canvas
            self.height_canvas_indic = self.height_canvas * 1/4

        else:
            self.width_canvas_graph = self.width_canvas
            self.height_canvas_graph = self.height_canvas

        self.canvas_graph_def()
        self.canvas_indic_def()
        self.canvas_reglage_def()

    def key(self, event):
        key_pressed = event.keysym
        if key_pressed == 'Right' and self.candles_decalage+self.candles_number < self.candles_len-1:
            self.candles_decalage += 1
        if key_pressed == 'Left' and self.candles_decalage > 0:
            self.candles_decalage -= 1
        if key_pressed == 'Up' and self.candles_decalage+self.candles_number < self.candles_len-1 and self.candles_decalage > 0:
            self.candles_number += 2
            self.candles_decalage -= 1
        if key_pressed == 'Down' and self.candles_number > 3:
            self.candles_number -= 2
            self.candles_decalage += 1
        if key_pressed == 'z' and self.n_pair < self.pair_all_len-1:
            self.n_pair += 1
            self.load_new_pair()

        if key_pressed == 's' and self.n_pair > 0:
            self.n_pair -= 1
            self.load_new_pair()

        self.canvas_graph.delete("all")
        self.canvas_graph_def()
        self.canvas_indic_def()
        self.canvas_reglage_def()

    def callback(self, event):

        self.x, self.y = event.x , event.y

        if self.x < self.width_canvas_graph-10 and self.x > self.width_canvas_graph-10-50 and self.y > 10 and self.y < 10+50 and self.reglage_overlay == False:
            self.reglage_overlay = True
            self.canvas_graph.delete("reglage_overlay")
            self.canvas_reglage_def()

        if self.reglage_overlay == True:
            for xx, bool in enumerate(self.index_indic):
                if self.x > self.width_canvas/3*1.05 and self.x < self.width_canvas/3*1.05+25 and self.y > self.height_canvas/4*1.25+xx*self.height_canvas/14 and self.y < self.height_canvas/4*1.25+xx*self.height_canvas/14+25:
                    if bool == True:
                        self.index_indic[xx] = False
                    else:
                        self.index_indic[xx] = True

                    if self.index_indic[3] == False and self.index_indic[4] == False and self.canvas_indic == True:
                        self.canvas_indic = False
                        self.width_canvas_graph = self.width_canvas
                        self.height_canvas_graph = self.height_canvas
                        self.height_canvas_indic = 0

                    if self.index_indic[3] == True or self.index_indic[4] == True and self.canvas_indic == False:
                        self.canvas_indic = True
                        self.width_canvas_graph = self.width_canvas
                        self.height_canvas_graph = self.height_canvas * 3/4
                        self.height_canvas_indic = self.height_canvas * 1/4

                    self.canvas_graph.delete("all")
                    self.canvas_graph_def()
                    self.canvas_indic_def()
                    self.canvas_reglage_def()

            if self.x < self.width_canvas/3*2-8 and self.x > self.width_canvas/3*2-8-20 and self.y > self.height_canvas/4*1+8 and self.y < self.height_canvas/4*1+8+20:
                self.reglage_overlay = False

                self.canvas_graph.delete("reglage_overlay")



    def canvas_graph_def(self):

        a = str(self.candles_decalage+self.candles_number)


        self.canvas_graph.create_text(10, 10,text=self.pair_all[self.n_pair] + "    " + a, fill='white', anchor="nw", tags='graph')

        auto_focus_indic = []
        auto_focus_indic.append(self.candles_bidhigh)
        auto_focus_indic.append(self.candles_bidlow)

        for x in [0,1,2,5]:
            if self.index_indic[x] == True:
                if x == 0:
                    auto_focus_indic.append(self.candles_sma)
                if x == 1:
                    auto_focus_indic.append(self.candles_wma)
                if x == 2:
                    auto_focus_indic.append(self.candles_ema)
                if x == 5:
                    auto_focus_indic.append(self.candles_tenkan)
                    auto_focus_indic.append(self.candles_kijun_sen)
                    auto_focus_indic.append(self.candles_ssa)
                    auto_focus_indic.append(self.candles_ssb)

        self.diff_max_graph, self.high_graph, self.low_graph  = self.auto_focus(self.candles_bidhigh, self.candles_bidlow, self.candles_number+1  , self.candles_decalage, data=auto_focus_indic)

        for x in range(self.candles_number+1):

            self.x_high  = self.height_canvas_graph*(self.candles_bidhigh[x+self.candles_decalage]-self.low)/-self.diff_max_graph + self.height_canvas_graph
            self.x_low   = self.height_canvas_graph*(self.candles_bidlow[x+self.candles_decalage]-self.low)/-self.diff_max_graph + self.height_canvas_graph
            self.x_close = self.height_canvas_graph*(self.candles_bidclose[x+self.candles_decalage]-self.low)/-self.diff_max_graph + self.height_canvas_graph
            self.x_open  = self.height_canvas_graph*(self.candles_bidopen[x+self.candles_decalage]-self.low)/-self.diff_max_graph + self.height_canvas_graph

            if self.x_close < self.x_open:
                self.candles_color = 'green'
            else:
                self.candles_color = 'red'

            self.canvas_graph.create_rectangle(((self.width_canvas_graph/self.candles_number)*x-(self.width_canvas_graph/self.candles_number)/2.5, self.x_open, (self.width_canvas_graph/self.candles_number)*x+(self.width_canvas_graph/self.candles_number)/2.5, self.x_close), fill=self.candles_color, tags='graph')
            self.canvas_graph.create_line(((self.width_canvas_graph/self.candles_number)*x, self.x_close, (self.width_canvas_graph/self.candles_number)*x, self.x_low), fill=self.candles_color, tags='graph')
            self.canvas_graph.create_line(((self.width_canvas_graph/self.candles_number)*x, self.x_close, (self.width_canvas_graph/self.candles_number)*x, self.x_high), fill=self.candles_color, tags='graph')

        if self.index_indic[0] == True:
            for x in range(self.candles_number+1):
                if x+self.candles_decalage > 14:

                    self.x_sma_1  = self.height_canvas_graph*(self.candles_sma[x+self.candles_decalage-1]-self.low)/-self.diff_max_graph + self.height_canvas_graph
                    self.x_sma_2  = self.height_canvas_graph*(self.candles_sma[x+self.candles_decalage]-self.low)/-self.diff_max_graph + self.height_canvas_graph
                    self.canvas_graph.create_line((self.width_canvas_graph/self.candles_number)*(x-1), self.x_sma_1, (self.width_canvas_graph/self.candles_number)*x, self.x_sma_2, fill='#00BFFF', tags='graph')

        if self.index_indic[1] == True:
            for x in range(self.candles_number+1):
                if x+self.candles_decalage > 14:

                    self.x_wma_1  = self.height_canvas_graph*(self.candles_wma[x+self.candles_decalage-1]-self.low)/-self.diff_max_graph + self.height_canvas_graph
                    self.x_wma_2  = self.height_canvas_graph*(self.candles_wma[x+self.candles_decalage]-self.low)/-self.diff_max_graph + self.height_canvas_graph
                    self.canvas_graph.create_line((self.width_canvas_graph/self.candles_number)*(x-1), self.x_wma_1, (self.width_canvas_graph/self.candles_number)*x, self.x_wma_2, fill='#FFA500', tags='graph')

        if self.index_indic[2] == True:
            for x in range(self.candles_number+1):
                if x+self.candles_decalage > 14:

                    self.x_ema_1  = self.height_canvas_graph*(self.candles_ema[x+self.candles_decalage-1]-self.low)/-self.diff_max_graph + self.height_canvas_graph
                    self.x_ema_2  = self.height_canvas_graph*(self.candles_ema[x+self.candles_decalage]-self.low)/-self.diff_max_graph + self.height_canvas_graph
                    self.canvas_graph.create_line((self.width_canvas_graph/self.candles_number)*(x-1), self.x_ema_1, (self.width_canvas_graph/self.candles_number)*x, self.x_ema_2, fill='#FA8072', tags='graph')

        if self.index_indic[5] == True:
            for x in range(self.candles_number+1):
                if x+self.candles_decalage > 14:

                    self.x_tenkan_1  = self.height_canvas_graph*(self.candles_tenkan[x+self.candles_decalage-1]-self.low)/-self.diff_max_graph + self.height_canvas_graph
                    self.x_tenkan_2  = self.height_canvas_graph*(self.candles_tenkan[x+self.candles_decalage]-self.low)/-self.diff_max_graph + self.height_canvas_graph
                    self.canvas_graph.create_line((self.width_canvas_graph/self.candles_number)*(x-1), self.x_tenkan_1, (self.width_canvas_graph/self.candles_number)*x, self.x_tenkan_2, fill='#FD6C9E', tags='graph')

            for x in range(self.candles_number+1):
                if x+self.candles_decalage > 14:

                    self.x_kijun_sen_1  = self.height_canvas_graph*(self.candles_kijun_sen[x+self.candles_decalage-1]-self.low)/-self.diff_max_graph + self.height_canvas_graph
                    self.x_kijun_sen_2  = self.height_canvas_graph*(self.candles_kijun_sen[x+self.candles_decalage]-self.low)/-self.diff_max_graph + self.height_canvas_graph
                    self.canvas_graph.create_line((self.width_canvas_graph/self.candles_number)*(x-1), self.x_kijun_sen_1, (self.width_canvas_graph/self.candles_number)*x, self.x_kijun_sen_2, fill='#2C75FF', tags='graph')

            for x in range(self.candles_number+1):
                if x+self.candles_decalage > 14:

                    self.x_ssa_1  = self.height_canvas_graph*(self.candles_ssa[x+self.candles_decalage-1]-self.low)/-self.diff_max_graph + self.height_canvas_graph
                    self.x_ssa_2  = self.height_canvas_graph*(self.candles_ssa[x+self.candles_decalage]-self.low)/-self.diff_max_graph + self.height_canvas_graph
                    self.canvas_graph.create_line((self.width_canvas_graph/self.candles_number)*(x-1), self.x_ssa_1, (self.width_canvas_graph/self.candles_number)*x, self.x_ssa_2, fill='#57D53B',width=2, tags='graph')
    
            for x in range(self.candles_number+1):
                if x+self.candles_decalage > 14:

                    self.x_ssb_1  = self.height_canvas_graph*(self.candles_ssb[x+self.candles_decalage-1]-self.low)/-self.diff_max_graph + self.height_canvas_graph
                    self.x_ssb_2  = self.height_canvas_graph*(self.candles_ssb[x+self.candles_decalage]-self.low)/-self.diff_max_graph + self.height_canvas_graph
                    self.canvas_graph.create_line((self.width_canvas_graph/self.candles_number)*(x-1), self.x_ssb_1, (self.width_canvas_graph/self.candles_number)*x, self.x_ssb_2, fill='#FE1B00',width=2, tags='graph')


    def canvas_indic_def(self):

        if self.canvas_indic == True:
        
            self.line_separate = self.canvas_graph.create_line(0, self.height_canvas_graph, self.width_canvas_graph, self.height_canvas_graph, fill='#3F4B66', width=3)

            if self.index_indic[3] == True:
                self.diff_max_indic, self.high_indic, self.low_indic = self.auto_focus(self.candles_rsi, self.candles_rsi, self.candles_number, self.candles_decalage)
                for x in range(self.candles_number+1):
                    if x+self.candles_decalage > 14:

                        self.x_rsi_1  = self.height_canvas_indic*(self.candles_rsi[x+self.candles_decalage-1]-self.low)/-self.diff_max_indic + self.height_canvas_indic + self.height_canvas_graph
                        self.x_rsi_2  = self.height_canvas_indic*(self.candles_rsi[x+self.candles_decalage]-self.low)/-self.diff_max_indic + self.height_canvas_indic + self.height_canvas_graph
                        self.line_ema = self.canvas_graph.create_line((self.width_canvas_graph/self.candles_number)*(x-1), self.x_rsi_1, (self.width_canvas_graph/self.candles_number)*x, self.x_rsi_2, fill='#FA8072')

                        if self.high_indic >= 70:
                            self.x_overbought_rsi = self.height_canvas_indic*(70-self.low)/-self.diff_max_indic + self.height_canvas_indic + self.height_canvas_graph
                            self.overbought_rsi = self.canvas_graph.create_line(0, self.x_overbought_rsi, self.width_canvas_indic, self.x_overbought_rsi, fill='#e6e6e6', dash=(8, 4))

                        if self.low_indic <= 30:
                            self.x_oversell_rsi = self.height_canvas_indic*(30-self.low)/-self.diff_max_indic + self.height_canvas_indic + self.height_canvas_graph
                            self.oversell_rsi = self.canvas_graph.create_line(0, self.x_oversell_rsi, self.width_canvas_indic, self.x_oversell_rsi, fill='#e6e6e6', dash=(8, 4))

            if self.index_indic[4] == True:
                self.diff_max_indic, self.high_indic, self.low_indic = self.auto_focus(self.candles_k, self.candles_k, self.candles_number, self.candles_decalage)
                for x in range(self.candles_number+1):
                    if x+self.candles_decalage > 14:

                        self.x_stoch_1  = self.height_canvas_indic*(self.candles_k[x+self.candles_decalage-1]-self.low)/-self.diff_max_indic + self.height_canvas_indic + self.height_canvas_graph
                        self.x_stoch_2  = self.height_canvas_indic*(self.candles_k[x+self.candles_decalage]-self.low)/-self.diff_max_indic + self.height_canvas_indic + self.height_canvas_graph
                        self.line_stoch = self.canvas_graph.create_line((self.width_canvas_graph/self.candles_number)*(x-1), self.x_stoch_1, (self.width_canvas_graph/self.candles_number)*x, self.x_stoch_2, fill='#2962FF')

                        self.x_stoch_1  = self.height_canvas_indic*(self.candles_d[x+self.candles_decalage-1]-self.low)/-self.diff_max_indic + self.height_canvas_indic + self.height_canvas_graph
                        self.x_stoch_2  = self.height_canvas_indic*(self.candles_d[x+self.candles_decalage]-self.low)/-self.diff_max_indic + self.height_canvas_indic + self.height_canvas_graph
                        self.line_stoch = self.canvas_graph.create_line((self.width_canvas_graph/self.candles_number)*(x-1), self.x_stoch_1, (self.width_canvas_graph/self.candles_number)*x, self.x_stoch_2, fill='#FA8072')

                        if self.high_indic >= 80:
                            self.x_overbought_stoch = self.height_canvas_indic*(80-self.low)/-self.diff_max_indic + self.height_canvas_indic + self.height_canvas_graph
                            self.overbought_stoch = self.canvas_graph.create_line(0, self.x_overbought_stoch, self.width_canvas_indic, self.x_overbought_stoch, fill='#e6e6e6', dash=(8, 4))

                        if self.low_indic <= 20:
                            self.x_oversell_stoch = self.height_canvas_indic*(20-self.low)/-self.diff_max_indic + self.height_canvas_indic + self.height_canvas_graph
                            self.oversell_stoch = self.canvas_graph.create_line(0, self.x_oversell_stoch, self.width_canvas_indic, self.x_oversell_stoch, fill='#e6e6e6', dash=(8, 4))

        else:
            pass

    def canvas_reglage_def(self):

        if self.reglage_overlay == False:

            self.icon = self.canvas_graph.create_image(self.width_canvas_graph-10, 10, image=self.reglage_icon, anchor=NE)

        elif self.reglage_overlay == True: 

            self.create_rectangle(0, 0, self.width_canvas, self.height_canvas, fill='Black', alpha=.5, tags='reglage_overlay')
            self.create_rectangle(self.width_canvas/3, self.height_canvas/4, self.width_canvas/3*2, self.height_canvas/4*3, fill='#1B202B', tags='reglage_overlay')
            self.canvas_graph.create_line(self.width_canvas/3, self.height_canvas/4*1.2, self.width_canvas/3*2, self.height_canvas/4*1.2, fill='grey', tags='reglage_overlay')
            self.canvas_graph.create_text(self.width_canvas/3*1.05, self.height_canvas/4*1.15,text='Réglage', fill='white', anchor="sw", tags='reglage_overlay')
            self.checkbox = self.canvas_graph.create_image(self.width_canvas/3*2-8, self.height_canvas/4*1+8, image=self.croix_icon, anchor=NE, tags='reglage_overlay')

            for x, index in enumerate(self.all_indic):

                self.canvas_graph.create_text(self.width_canvas/3*1.15, self.height_canvas/4*1.25+x*self.height_canvas/14+5,text=index, fill='white', anchor="nw", tags='reglage_overlay')

                if self.index_indic[x] == True:
                    self.checkbox = self.canvas_graph.create_image(self.width_canvas/3*1.05, self.height_canvas/4*1.25+x*self.height_canvas/14, image=self.checkbox_on_icon, anchor=NW, tags='reglage_overlay')

                else:
                    self.checkbox = self.canvas_graph.create_image(self.width_canvas/3*1.05, self.height_canvas/4*1.25+x*self.height_canvas/14, image=self.checkbox_off_icon, anchor=NW, tags='reglage_overlay')



    def auto_focus(self, source_high, source_low, lenght, decalage, **kwargs):

        if 'data' in kwargs:
            data = kwargs.pop('data')
            self.maxi = 0.0
            self.mini = 9999999999 #valeurs élever car sinon ca na marche pas.
            for data_x in data:
                for x in range(lenght):
                    self.i = data_x[x+decalage]
                    if self.i >= self.maxi:
                        self.maxi = self.i
                for x in range(lenght):
                    self.i = data_x[x+decalage]
                    if self.i <= self.mini:
                        self.mini = self.i

        else:
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

        return self.diff_max, self.high, self.low

    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = root.winfo_rgb(fill) + (alpha,)
            tags = kwargs.pop('tags')
            image = pl.Image.new('RGBA', (x2-x1, y2-y1), fill)
            self.images.append(ImageTk.PhotoImage(image))
            self.canvas_graph.create_image(x1, y1, image=self.images[-1], anchor='nw', tags=tags)
        self.canvas_graph.create_rectangle(x1, y1, x2, y2, **kwargs)

    def load_new_pair(self):
        self.path = os.getcwd().replace("/VIEWER","") + str("/DATA/") + str(self.pair_all[self.n_pair]) #créeation de la direction du fichier.
        self.bars = pd.read_csv(self.path)
        self.X = self.bars.copy()
        self.candles_bidopen = self.X.pop('bidopen')
        self.candles_bidclose = self.X.pop('bidclose')
        self.candles_bidhigh = self.X.pop('bidhigh')
        self.candles_bidlow = self.X.pop('bidlow')
        self.candles_sma = self.X.pop('sma')
        self.candles_wma = self.X.pop('wma')
        self.candles_ema = self.X.pop('ema')
        self.candles_rsi = self.X.pop('rsi')
        self.candles_k = self.X.pop('stoch_k')
        self.candles_d = self.X.pop('stoch_d')
        self.candles_tenkan = self.X.pop('tenkan')
        self.candles_kijun_sen = self.X.pop('kijun_sen')
        self.candles_ssa = self.X.pop('ssa')
        self.candles_ssb = self.X.pop('ssb')

        self.candles_len = len(self.candles_bidopen)
        self.candles_decalage = len(self.candles_bidhigh)-(self.candles_number+1)

root = tk.Tk()
root.title('Ping Pong Interface')
class_display = display(root)
root.mainloop()