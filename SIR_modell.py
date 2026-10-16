import numpy as np
import random

# ----------- Startvärden --------------
tspan = [0, 120]
N = 1000 # startpersoner är 1000 varav 5 smittade (inte med)
b = 0.3 # andelen mottagliga
g = 1/7 # andelen sjuka 
alfa = 0.2 # inkubationstid 
my = 0.005 # dödlighet 
v = 8.0 # vaccinationer
m = 0.5 # andelen mörkertal

c = np.array([b/N, alfa, g, my, v]) # propentitestfunktions array


Y0 = np.array([995, 0, 5, 0, 0, 0]) # 5 är smittade i start 0 resistenta, resten mottaglig
#Y0 = np.array([990, 0, 5, 0, 0, 0, 5]) # 5 bekräftade I, 5 mörkertal M

# ----------- SIR MODELLEN ---------------
def stockiomatris():
    B = np.array([
        [-1, 1, 0], # r1 (smitta)
        [0, -1, 1]  # r2 (inkubation)
    ])
    return B

# Y är en array som innehåller [s(t), I(t), R(t)] Returvärdet är bara propfunktionerna i sin grundform
def propensitetsfunktioner(Y, c):
    S1, I1, R1 = Y[0], Y[1], Y[2]
    c1, c2 = c[0], c[1] #reaktionshastigheterna
    
    a1 = c1 * S1 * I1   # r1: smitta (S -> I)
    a2 = c2 * I1        # r2: tillfrisknande (I -> R)

    return np.array([a1, a2])

#----------------- SIER MODELL ------------------------
def stockiomatris_SEIR():
    B = np.array([
        [-1, 1, 0, 0], # r1 (smitta)
        [0, -1, 1, 0], # r2 (inkubation)
        [0, 0, -1, 1]  # r3 (tillfriskning)
    ])
    return B

def propensitetsfunktioner_SEIR(Y, c):
    S1, E1, I1, R1 = Y[0], Y[1], Y[2], Y[3]

    c1, c2, c3 = c[0], c[1], c[2] #reaktionshastigheterna
    
    a1 = c1 * S1 * I1   # r1: smitta (S -> E)
    a2 = c2 * E1        # r2: inkubation (E -> I)
    a3 = c3 * I1        # r3: tillfrisknande (I -> R)

    return np.array([a1, a2, a3])


#----------------- SIERD MODELL ------------------------
def stockiomatris_SEIRD():
    B = np.array([
        [-1, 1, 0, 0, 0], # r1 (smitta)
        [0, -1, 1, 0, 0], # r2 (inkubation)
        [0, 0, -1, 1, 0], # r3 (tillfrisknande)
        [0, 0, -1, 0, 1]  # r4 (död)
    ])
    return B


def propensitetsfunktioner_SEIRD(Y, c):
    S1, E1, I1, R1, D1 = Y[0], Y[1], Y[2], Y[3], Y[4]
    c1, c2, c3, c4 = c[0], c[1], c[2], c[3]  # reaktionshastigheterna
    
    a1 = c1 * S1 * I1   # r1: smitta (S -> E)
    a2 = c2 * E1        # r2: inkubation (E -> I)
    a3 = c3 * I1        # r3: tillfrisknande (I -> R)
    a4 = c4 * I1        # r4: töd (I -> D)
    
    return np.array([a1, a2, a3, a4])



#----------------- SIERDV MODELL + va ------------------------
def stockiomatris_SEIRDV():
    B = np.array([
        [-1, 1, 0, 0, 0, 0], # r1 (smitta)
        [0, -1, 1, 0, 0, 0], # r2 (inkubation)
        [0, 0, -1, 1, 0, 0], # r3 (tillfrisknande)
        [0, 0, -1, 0, 1, 0], # r4 (död)
        [-1, 0, 0, 0, 0, 1]  # r5 (vaccin)
    ])
    return B

def propensitetsfunktioner_SEIRDV(Y, c):
    S1, E1, I1, R1, D1, V1 = Y[0], Y[1], Y[2], Y[3], Y[4], Y[5]
    c1, c2, c3, c4, c5  = c[0], c[1], c[2], c[3], c[4] #reaktionshastigheterna
    
    a1 = c1 * S1 * I1        # r1: smitta (S -> E)
    a2 = c2 * E1             # r2: inkubation (E -> I)
    a3 = c3 * I1             # r3: tillfrisknande (I -> R)
    a4 = c4 * I1             # r4: död (I -> D)
    a5 = c5 if S1 > 0 else 0 # r5: vaccin (S -> V)

    return np.array([a1, a2, a3, a4, a5])


#----------------- SEIRDVM - MODELL ------------------------
def stockiomatris_SEIRDVM():
    B = np.array([
        [-1, 1, 0, 0, 0, 0, 0], # r1 (smitta)
        [-1, 0, 0, 0, 0 ,1, 0], # r2 (vaccin)
        [0, -1, 1, 0, 0, 0, 0], # r3 (inkubation)
        [0, -1, 0, 0, 0, 0, 1], # r4 (inkubation, mörkertal)
        [0, 0, -1, 1, 0, 0, 0], # r5 (tillfrisknade, rapporterad)
        [0, 0, 0, 1, 0, 0, -1], # r6 (tillfrisknade, mörkertal)
        [0, 0, -1, 0, 1, 0, 0], # r7 (död)
        [0, 0, 0, 0, 1, 0, -1], # r8 (död, mörkertal)
    ])
    return B

def propensitetsfunktioner_SEIRDVM(Y, c):
    S1, E1, I1, R1, D1, V1, M1 = Y[0], Y[1], Y[2], Y[3], Y[4], Y[5]
    c1, c2, c3, c4, c5, c6, c7, c8  = c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7] #reaktionshastigheterna
    
    a1 =   # r1: smitta (S -> E)
    a2 =   # r2: inkubation (E -> I)
    a3 =   # r3: tillfrisknande (I -> R)
    a4 =   # r4: död (I -> D)
    a5 =   # r5: vaccin (S -> V)
    a6 =   # r6: 

    return np.array([a1, a2, a3, a4, a5, a6, a7, a8])
