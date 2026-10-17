import numpy as np
import random

# ----------- Startvärden --------------
tspan = [0, 120]
N = 1000       # Startpopulation
b = 0.3        # Beta (smittotakt)
g = 1/7        # Gamma (tillfrisknande)
alfa = 0.2     # Alpha (1 / inkubationstid)
my = 0.005     # My (dödlighet)
v = 5.0        # Vaccinationshastighet (personer/dag)
m = 0.5        # Andel kända/rapporterade fall (p)

# Parametervektorer för olika modeller
# c_SIR = np.array([b/N, g])
# c_SEIR = np.array([b/N, alfa, g])
# c_SEIRD = np.array([b/N, alfa, g, my])
# c_SEIRDV = np.array([b/N, alfa, g, my, v])

# Starttillstånd för olika modeller
# Y0_SIR = np.array([995, 5, 0])          # [S, I, R]
# Y0_SEIR = np.array([995, 0, 5, 0])      # [S, E, I, R]
# Y0_SEIRD = np.array([995, 0, 5, 0, 0])  # [S, E, I, R, D]

# SIERDV
# c = np.array([b/N, alfa, g, my, v]) # propentitestfunktions array
# Y0 = np.array([995, 0, 5, 0, 0, 0]) # 5 är smittade i start 0 resistenta, resten mottaglig

# SIERDVM - Nya modellen
c_SEIRDVM = np.array([b/N, v, alfa, m, g, my])
Y0_SEIRDVM = np.array([990, 0, 5, 0, 0, 0, 5]) # [S, E, I, R, D, V, M]

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
    S1, E1, I1, R1, D1, V1, M1 = Y[0], Y[1], Y[2], Y[3], Y[4], Y[5], Y[6]
    # c1 = b/N, c2 = v, c3 = alfa, c4 = m (p), c5 = g, c6 = my
    c1, c2, c3, c4, c5, c6  = c[0], c[1], c[2], c[3], c[4], c[5] #reaktionshastigheterna

    # Både bekräftade I och okända M bidrar till smittspridningen
    totalt_smittsamma = I1 + M1
    
    a1 = c1 * S1 * totalt_smittsamma  # r1: Smitta (S -> E)
    a2 = c2 if S1 > 0 else 0          # r2: Vaccination (S -> V)
    a3 = c4 * (c3 * E1)               # r3: Känd smitta (E -> I)
    a4 = (1 - c4) * (c3 * E1)         # r4: Mörkertal (E -> M)
    a5 = c5 * I1                      # r5: Tillfrisknande I (I -> R)
    a6 = c5 * M1                      # r6: Tillfrisknande M (M -> R) 
    a7 = c6 * I1                      # r7: Död I (I -> D)
    a8 = c6 * M1                      # r8: Död M (M -> D)

    return np.array([a1, a2, a3, a4, a5, a6, a7, a8])
