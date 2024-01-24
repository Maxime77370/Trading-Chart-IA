# -*- coding: utf-8 -*-

import fxcmpy
import socketio
from os import listdir
from os.path import isfile, join
import numpy as np 
import pandas as pd
import datetime as dt
import time
import os
import csv
import sys
import pickle
import platform

from INDIC import * # l'on importe toutes les def qui sert au calcule des indicateur. (Fichier INDIC.py)

"""
    Chemin d'accès expliquer:

    - V1.2 :
        -API :
            -API.py (boucle principal)
            -INDIC.py (bibliotheque de définition des formules d'indicateur)
            -log.txt (fichier qui noté les erreurs du à FXCMPY)
        -DATA :
            -BACKUP : 
                -DATE (date actuelle) :
                    -BASE :
                        -tout les fichiers comportent les données bruts du jours. (env. 245 pairs et 10 000 barsback) 
                    -INDIC :
                        -tout les fichiers comportent les données traités du jours. (env. 245 pairs et 10 000 barsback)
            -DATA :
                -BASE :
                    -tout les fichier comprotent les données bruts récolter jusqu'a présent. (env. 245 pairs et le maximum de barsback)
                -INDIC :
                    -tout les fichier comprotent les données traité récolter jusqu'a présent. (env. 245 pairs et le maximum de barsback)
"""

BARS_BACK = 10000

nb_base = 0
nb_indic = 0


n_erreur = 0
n_actu_erreur = 0

temps_execution_debut = time.time()

_platform = platform.system()

print("os ==", _platform, "\n")

print("VERSION PACKAGE : \n")
print("fxcmpy ==", fxcmpy.__version__)          #1.2.6
print("socketio ==", socketio.__version__)      #4.4.0
print("numpy ==", np.__version__)               #1.20.3
print("pandas ==",pd.__version__)               #1.3.1
print("csv ==",csv.__version__, "\n")           #1.0 

download = True

date = dt.date.today()

currentPath = os.path.dirname(__file__)

TOKEN = 'e8ed111fc13015281d9abd3c3dfc71c50d5db3fe'

def instruments_import():

    try:    # on essaye de crée un ficher si celui-ci est deja crée alors ne rien faire.
        if download == True:
            if _platform == 'Windows':
                path = currentPath.replace("\\API","") + str(u"\\DATA\\BACKUP\\" + str(date)) #créeation de la direction du fichier pour la BASE (fichier des données brut)
                os.mkdir(path)
                path = path + str("\\BASE")
                os.mkdir(path)
                print('creation BASE file')
            elif _platform == 'Darwin':
                path = currentPath.replace("/API","") + str(u"/DATA/BACKUP/" + str(date)) #créeation de la direction du fichier pour la BASE (fichier des données brut)
                os.mkdir(path)
                path = path + str("/BASE")
                os.mkdir(path)
                print('creation BASE file')
            else:
                print('OS {0} incompatible.'.format(_platform))
                sys.exit(0)
        elif download == False:
            if _platform == 'Windows':
                path = currentPath.replace("\\API","") + str(u"\\DATA\\BACKUP\\" + str(date) + str("\\INDIC")) #créeation de la direction du fichier pour les INDIC (fichier de données traiter)
                os.mkdir(path)
                print('creation INDIC file')
            elif _platform == 'Darwin':
                path = currentPath.replace("API","") + str(u"/DATA/BACKUP/" + str(date) + str("/INDIC")) #créeation de la direction du fichier pour les INDIC (fichier de données traiter)
                os.mkdir(path)
                print('creation INDIC file')
            else:
                print('OS {0} incompatible.'.format(_platform))
                sys.exit(0)

    except:
        pass

    if download == True: # mode de connection au serveur.

        print("Download activate ...")
        print("in Log in")

        con = fxcmpy.fxcmpy(access_token=TOKEN, log_level='error')
        instruments = con.get_instruments()
        print(instruments)
        print("Log in complete") 

        return instruments, con

    else:  # mode calcule des indicateur, recherche dans la base de donnée télecharger les différent fichier.

        print("Download desactivate ...")

        if _platform == 'Windows':
            instruments = [f for f in listdir(currentPath.replace("\\API","")  + str(u"\\DATA\\BACKUP\\" + str(date) + str("\\BASE"))) if isfile(join(currentPath.replace("\\API","") + str(u"\\DATA\\BACKUP\\" + str(date) + str("\\BASE")), f))]
        elif _platform == 'Darwin':
            instruments = [f for f in listdir(currentPath.replace("/API","")  + str(u"/DATA/BACKUP/" + str(date) + str("/BASE"))) if isfile(join(currentPath.replace("/API","") + str(u"/DATA/BACKUP/" + str(date) + str("/BASE")), f))]
        
        try:
            instruments.remove(".DS_Store")
        except:
            pass
        try:
            instruments.remove(" ")
        except:
            pass
        pair_all_len = len(instruments)

        con = None

        return instruments, con

instruments, con = instruments_import()

try:

    if _platform == 'Windows':
        save_path = currentPath.replace("\\API","") + str(u"\\DATA\\BACKUP\\" + str(date) + str("\\save.p"))
    if _platform == 'Darwin':
        save_path = currentPath.replace("/API","") + str(u"/DATA/BACKUP/" + str(date) + str("/save.p"))

    save = open(save_path, 'rb')
    nb_base = pickle.load(save)
    nb_indic = pickle.load(save)
    n_erreur = pickle.load(save)
    temps_execution_debut = pickle.load(save)

    save.close()

    save = open(save_path,'wb')
    pickle.dump(nb_base, save)
    pickle.dump(nb_indic, save)
    pickle.dump(n_erreur, save)
    pickle.dump(temps_execution_debut, save)
    save.close()

except:
    pass

print("pair : ALL") # on teste toute les pairs.

while True:

    try: # afin d'empécher les crashs du a des probleme serveur. ou autre.

        if download == True: 

            if nb_base < len(instruments): # on calcule tout les pairs temps qu'il en reste le programme continue.
                print(instruments[nb_base])
    
                candles = con.get_candles(instruments[nb_base], period='m15',columns=['bidopen','bidclose','bidhigh','bidlow','askopen','askclose','askhigh', 'asklow','tickqty'], number=BARS_BACK)  # daily data
                candles_bidopen = candles['bidopen'].tolist()
                candles_bidclose = candles['bidclose'].tolist()
                candles_bidhigh = candles['bidhigh'].tolist()
                candles_bidlow = candles['bidlow'].tolist()
                candles_askopen = candles['askopen'].tolist()
                candles_askclose = candles['askclose'].tolist()
                candles_askhigh = candles['askhigh'].tolist()
                candles_asklow = candles['asklow'].tolist()
                candles_tickqty = candles['tickqty'].tolist()

                if candles_bidopen == []:
                    print('Erreur server: return None ... retry later')
                    break

                if _platform == 'Windows':
                    fullpath = currentPath.replace("\\API","") + str(u"\\DATA\\BACKUP\\" + str(date)) + str("\\BASE\\") + str(instruments[nb_base]).replace("/", "-") + ".csv"
                if _platform == 'Darwin':
                    fullpath = currentPath.replace("/API","") + str(u"/DATA/BACKUP/" + str(date)) + str("/BASE/") + str(instruments[nb_base]).replace("/", "-") + ".csv"

                with open(fullpath, "w") as csvfile:

                    print('{0} in creation'.format(fullpath))

                    fieldnames = [  'bidopen', #18
                                    'bidclose',
                                    'bidhigh',
                                    'bidlow',
                                    'askopen',
                                    'askclose', 
                                    'askhigh', 
                                    'asklow',]

                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for y in range(len(candles_bidopen)):
                        writer.writerow({   'bidopen': candles_bidopen[y],
                                            'bidclose': candles_bidclose[y], 
                                            'bidhigh': candles_bidhigh[y], 
                                            'bidlow': candles_bidlow[y], 
                                            'askopen': candles_askopen[y], 
                                            'askclose': candles_askclose[y], 
                                            'askhigh': candles_askhigh[y], 
                                            'asklow': candles_asklow[y], 
                                            })

                nb_base += 1

                n_actu_erreur = 0

                print("{0}% ({1}/{2})".format(round((nb_base+1)/len(instruments)*100, 2), nb_base+1, len(instruments)))

                time.sleep(1)

            else:
                download = False
                print("ok")
                instruments = instruments_import()

        else:

            if nb_indic < len(instruments): # on calcule tout les pairs temps qu'il en reste le programme continue.

                print(instruments[nb_indic])

                if _platform == 'Windows':
                    bars = pd.read_csv(currentPath.replace("\\API","") + str(u"\\DATA\\BACKUP\\" + str(date) + str("\\BASE\\")) + str(instruments[nb_indic]))
                if _platform == 'Darwin':
                    bars = pd.read_csv(currentPath.replace("/API","") + str(u"/DATA/BACKUP/" + str(date) + str("/BASE/")) + str(instruments[nb_indic]))

                X = bars.copy()
                candles_bidopen = X.pop('bidopen')
                candles_bidclose = X.pop('bidclose')
                candles_bidhigh = X.pop('bidhigh')
                candles_bidlow = X.pop('bidlow')
                candles_askopen = X.pop('askopen')
                candles_askclose = X.pop('askclose')
                candles_askhigh = X.pop('askhigh')
                candles_asklow = X.pop('asklow')

                #candles_rsi = RSI(candles_bidclose)
                candles_evolution = evolution(candles_bidclose)
                candles_sma = SMA(candles_bidclose, 14)
                candles_wma = WMA(candles_bidclose, 14)
                candles_ema = EMA(candles_bidclose, 9)
                candles_k, candles_d = STOCH(candles_bidclose, candles_bidlow, candles_bidhigh, 14)
                candles_tenkan, candles_kijun_sen, candles_ssa, candles_ssb, candles_kumo = ICHIMOKU(candles_bidclose, candles_bidlow, candles_bidhigh, 9, 26, 52)

                if _platform == 'Windows':
                    fullpath = currentPath.replace("\\API","") + str(u"\\DATA\\BACKUP\\" + str(date)) + str("\\INDIC\\") + str(instruments[nb_indic]).replace("/", "-")
                if _platform == 'Darwin':
                    fullpath = currentPath.replace("/API","") + str(u"/DATA/BACKUP/" + str(date)) + str("/INDIC/") + str(instruments[nb_indic]).replace("/", "-")

                with open(fullpath, "w") as csvfile:

                    print('{0} in creation'.format(fullpath))

                    fieldnames = [  'sma', 
                                    'wma', 
                                    'ema', 
                                    'stoch_k', 
                                    'stoch_d', 
                                    'tenkan', 
                                    'kijun_sen', 
                                    'ssa', 
                                    'ssb', 
                                    'kumo', 
                                    'evo']

                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for y in range(len(candles_bidopen)):
                        writer.writerow({   'sma': candles_sma[y], 
                                            'wma': candles_wma[y], 
                                            'ema': candles_ema[y], 
                                            'stoch_k': candles_k[y], 
                                            'stoch_d': candles_d[y],
                                            'tenkan': candles_tenkan[y], 
                                            'kijun_sen': candles_kijun_sen[y], 
                                            'ssa': candles_ssa[y], 
                                            'ssb': candles_ssb[y], 
                                            'kumo': candles_kumo[y],
                                            'evo': candles_evolution[y]
                                            })
                nb_indic += 1

                n_actu_erreur = 0

                print("{0}% ({1}/{2})".format(round((nb_indic+1)/len(instruments)*100, 2), nb_indic+1, len(instruments)))

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        n_erreur += 1
        n_actu_erreur+=1
        if n_actu_erreur > 2:
            nb_base += 1

    save = open(save_path,'wb')

    pickle.dump(nb_base, save)
    pickle.dump(nb_indic, save)
    pickle.dump(n_erreur, save)
    pickle.dump(temps_execution_debut, save)

    save.close()

    if nb_indic > len(instruments):
        break

temps_execution_fin = time.time()

temps_execution_total = temps_execution_fin - temps_execution_debut

print("creation ALL complete: in {0}s with {1} error.".format(round(temps_execution_total, 2), n_erreur))

