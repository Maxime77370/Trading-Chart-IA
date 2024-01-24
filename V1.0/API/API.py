import fxcmpy
import socketio
import csv
import os
import numpy as np 
import pandas as pd
import datetime as dt
import time

BARS_BACK = 10000

print("in Log in")

con = fxcmpy.fxcmpy(access_token='89fe82889b3cf4288e36c17248c53f3a69aa4480', log_level='error', server='demo', log_file='log.txt')
print("Log in complete")

try:	# on essaye de crée un ficher si celui-ci est deja crée alors ne rien faire
	os.mkdir('DATA')
	print('creation DATA file')
except:
	pass

instruments = con.get_instruments_for_candles()
print("pair : ALL") # on teste toute les pairs

def evolution(source):
	candles_evolution = []
	for x in range(BARS_BACK):
		if x < BARS_BACK-1: 
			if source[x] < source[x+1]:
				candles_evolution.append(1)
			else:
				candles_evolution.append(0)
		else:
			candles_evolution.append(0)
	return candles_evolution

def RSI(source):
	rsi = []
	for w in range(BARS_BACK):
		H = []
		B = []
		for z in range(0, 14):
			dif = source[w-z] - source[w-z-1]
			if dif >= 0:
				H.append(dif)
			else:
				H.append(0)
			if dif <= 0:
				B.append(-dif)
			else:
				B.append(0)
		H_mean = np.mean(H)
		B_mean = np.mean(B)
		RS = H_mean / B_mean
		RSI = 100 - (100 / (1 + RS))
		rsi.append(RSI)
	return rsi

def SMA(source, lenght): #Moyenne mobile
	candles_sma = []
	for w in range(BARS_BACK):
		if w < lenght-1:
			candles_sma.append(0)
		else:
			C = []
			for z in range(0, lenght):
				C.append(source[w-z])
			sma_calc = np.mean(C)
			candles_sma.append(sma_calc)
	return(candles_sma)

def WMA(source, lenght): #Moyenne mobile pondérée
	candles_wma = []
	for w in range(BARS_BACK):
		if w < lenght-1:
			candles_wma.append(0)
		else:
			C = []
			P_all = 0.0
			for z in range(0, lenght):
				P = (lenght-z)/lenght
				P_all = P + P_all
				C.append(P*source[w-z])
			wma_calc = np.sum(C) / P_all
			candles_wma.append(wma_calc)
	return(candles_wma)

def EMA(source, lenght): #Moyenne mobile exponentielle 
	candles_ema = []
	for w in range(BARS_BACK):
		if w < lenght-1:
			candles_ema.append(0)
		else:
			C = []
			alpha_all = 0.0
			for z in range(0, lenght):
				alpha = (2 / (lenght+1))**z
				alpha_all = alpha+alpha_all
				C.append(alpha*source[w-z])
			ema_calc = np.sum(C) / alpha_all
			candles_ema.append(ema_calc)
	return(candles_ema)

def STOCH(source_C, source_L, source_H, lenght):
	candles_stoch = []
	for w in range(BARS_BACK):
		if w < lenght-1:
			candles_stoch.append(0)
		else:
			low = []
			high = []
			for z in range(0, lenght):
				low.append(source_L[w-z])
				high.append(source_H[w-z])
			stoch_calc = ((source_C[w]-(np.amin(low)))/((np.amax(high))-(np.amin(low))))*100
			candles_stoch.append(stoch_calc)
	return(candles_stoch)

def ICHIMOKU(source_C, source_L, source_H, lenght_1, lenght_2, lenght_3):
	candles_tenkan = []
	candles_kijun_sen = []
	candles_ssa = [] #Senkou Span A
	candles_ssb = [] #Senkou Span B
	candles_kumo = []
	for v in range(lenght_2):
		candles_ssa.append(0)
		candles_ssb.append(0)
	for w in range(BARS_BACK):
		calc = []
		for x in [lenght_1, lenght_2, lenght_3]:
			low = []
			high = []
			for z in range(x):
				low.append(source_L[w-z])
				high.append(source_H[w-z])
			calc.append((np.amax(high)+np.amin(low))/2)
		if w < lenght_2-1:
			candles_ssa.append(0) #Senkou Span A
		else:
			candles_ssa.append((calc[0]+calc[1])/2)
		if w < lenght_3-1:
			candles_ssb.append(0) #Senkou Span B
		else:
			candles_ssb.append(calc[2])
		if w < lenght_1-1:
			candles_tenkan.append(0)
			candles_kijun_sen.append(0)
			candles_kumo.append(0)
		else:
			candles_tenkan.append(calc[0])
			candles_kijun_sen.append(calc[1])
			candles_kumo.append(candles_ssa[w]-candles_ssb[w])
	return(candles_tenkan, candles_kijun_sen, candles_ssa, candles_ssb, candles_kumo)

for x in range(len(instruments)):

	candles = con.get_candles(instruments[x], period='m5',columns=['bidopen','bidclose','bidhigh','bidlow','askopen','askclose','askhigh', 'asklow','tickqty'], number=BARS_BACK)  # daily data
	candles_bidopen = candles['bidopen'].tolist()
	candles_bidclose = candles['bidclose'].tolist()
	candles_bidhigh = candles['bidhigh'].tolist()
	candles_bidlow = candles['bidlow'].tolist()
	candles_askopen = candles['askopen'].tolist()
	candles_askclose = candles['askclose'].tolist()
	candles_askhigh = candles['askhigh'].tolist()
	candles_asklow = candles['asklow'].tolist()
	candles_tickqty = candles['tickqty'].tolist()
	candles_rsi = RSI(candles_bidclose)
	candles_evolution = evolution(candles_bidclose)
	candles_sma = SMA(candles_bidclose, 14)
	candles_wma = WMA(candles_bidclose, 14)
	candles_ema = EMA(candles_bidclose, 9)
	candles_stoch = STOCH(candles_bidclose, candles_bidlow, candles_bidhigh, 14)
	candles_tenkan, candles_kijun_sen, candles_ssa, candles_ssb, candles_kumo = ICHIMOKU(candles_bidclose, candles_bidlow, candles_bidhigh, 9, 26, 52)

	fullpath = "DATA/" + str(instruments[x]).replace("/", "-") + ".csv"

	with open(fullpath, 'w') as csvfile:

		print('{0} in creation'.format(fullpath))

		fieldnames = [	'bidopen', #18
						'bidclose',
						'bidhigh',
						'bidlow',
						'askopen',
						'askclose', 
						'askhigh', 
						'asklow', 
						'rsi', 
						'sma', 
						'wma', 
						'ema', 
						'stoch', 
						'tenkan', 
						'kijun_sen', 
						'ssa', 
						'ssb', 
						'kumo', 
						'evo']

		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		print(len(candles_tenkan))

		writer.writeheader()
		for y in range(BARS_BACK):
			writer.writerow({	'bidopen': candles_bidopen[y],
								'bidclose': candles_bidclose[y], 
								'bidhigh': candles_bidhigh[y], 
								'bidlow': candles_bidlow[y], 
								'askopen': candles_askopen[y], 
								'askclose': candles_askclose[y], 
								'askhigh': candles_askhigh[y], 
								'asklow': candles_asklow[y], 
								'rsi': candles_rsi[y], 
								'sma': candles_sma[y], 
								'wma': candles_wma[y], 
								'ema': candles_ema[y], 
								'stoch': candles_stoch[y], 
								'tenkan': candles_tenkan[y], 
								'kijun_sen': candles_kijun_sen[y], 
								'ssa': candles_ssa[y], 
								'ssb': candles_ssb[y], 
								'kumo': candles_stoch[y],
								'evo': candles_evolution[y]
								})

	print("{0}%".format(round((x+1)/len(instruments)*100, 2)))

print('creation ALL complete')