import numpy as np 

def evolution(source):
    candles_evolution = []
    for x in range(len(source)):
        if x < len(source)-1: 
            if source[x] < source[x+1]:
                candles_evolution.append(1)
            else:
                candles_evolution.append(0)
        else:
            candles_evolution.append(0)
    return candles_evolution

def SMA(source, lenght): #Moyenne mobile
    candles_sma = []
    for w in range(len(source)):
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
    for w in range(len(source)):
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
    source_sma = SMA(source, lenght)
    for w in range(len(source)):
        alpha = 2/(lenght+1)
        if w < lenght-1:
            candles_ema.append(0)
        elif w <= lenght:
            candles_ema.append((source[w]-source_sma[w])*alpha+source_sma[w])
        else:
            candles_ema.append((source[w]-candles_ema[w-1])*alpha+candles_ema[w-1])
    return(candles_ema)

def STOCH(source_C, source_L, source_H, lenght):
    candles_k = []
    candles_d = []
    for w in range(len(source_C)):
        if w < lenght-1:
            candles_k.append(0)
        else:
            low = []
            high = []
            for z in range(0, lenght):
                low.append(source_L[w-z])
                high.append(source_H[w-z])
            stoch_calc = ((source_C[w]-(np.amin(low)))/((np.amax(high))-(np.amin(low))))*100
            candles_k.append(stoch_calc)
    candles_d = SMA(candles_k, 3)

    return(candles_k, candles_d)

def ICHIMOKU(source_C, source_L, source_H, lenght_1, lenght_2, lenght_3):
    candles_tenkan = []
    candles_kijun_sen = []
    candles_ssa = [] #Senkou Span A
    candles_ssb = [] #Senkou Span B
    candles_kumo = []
    for v in range(lenght_2):
        candles_ssa.append(0)
        candles_ssb.append(0)
    for w in range(len(source_C)):
        calc = []
        for x in [lenght_1, lenght_2, lenght_3]:
            low = []
            high = []
            for z in range(x):
                if w > z-1:
                    low.append(source_L[w-z])
                    high.append(source_H[w-z])
                    calc.append((np.amax(high)+np.amin(low))/2)
                else:
                    calc.append(0)
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

# def RSI(source):
#     rsi = []
#     for w in range(len(source)):
#         H = []
#         B = []
#         for z in range(0, 14):
#             print(z)
#             print(w)
#             dif = source[w-z] - source[w-z-1]
#             if dif >= 0:
#                 H.append(dif)
#             else:
#                 H.append(0)
#             if dif <= 0:
#                 B.append(-dif)
#             else:
#                 B.append(0)
#         H_mean = np.mean(H)
#         B_mean = np.mean(B)
#         if H_mean != 0 and B_mean != 0:
#             RS = H_mean / B_mean
#             RSI = 100 - (100 / (1 + RS))
#             rsi.append(RSI)
#         else:
#             rsi.append(0)
#     return rsi
