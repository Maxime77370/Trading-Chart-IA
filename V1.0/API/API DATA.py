import fxcmpy
import socketio
import csv
import os
import pandas as pd
import datetime as dt

BARS_BACK = 10000

print("in Log in")

con = fxcmpy.fxcmpy(access_token='89fe82889b3cf4288e36c17248c53f3a69aa4480', log_level='error', server='demo', log_file='log.txt')
print("Log in complete")

try:	#l'on essaye de crée un ficher si celui-ci est deja crée alors ne rien faire
	os.mkdir('DATA')
	print('creation DATA file')
except:
	pass

instruments = con.get_instruments_for_candles()
print("pair : ALL") # l'on teste toute les pairs


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


	fullpath = "DATA/" + str(instruments[x]).replace("/", "-") + ".csv"

	with open(fullpath, 'w') as csvfile:

		print('{0} in creation'.format(fullpath))

		fieldnames = ['x','bidopen','bidclose','bidhigh','bidlow','askopen','askclose', 'askhigh', 'asklow', 'tickqty']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writeheader()
		for y in range(BARS_BACK):
			writer.writerow({'x': y,'bidopen': candles_bidopen[y], 'bidclose': candles_bidclose[y], 'bidhigh': candles_bidhigh[y], 'bidlow': candles_bidlow[y], 'askopen': candles_askopen[y], 'askclose': candles_askclose[y], 'askhigh': candles_askhigh[y], 'asklow': candles_asklow[y], 'tickqty': candles_tickqty[y]})

	print("{0}%".format(round((x+1)/len(instruments)*100, 2)))

print('creation ALL complete')