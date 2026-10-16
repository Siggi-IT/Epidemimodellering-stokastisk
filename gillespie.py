#==================================
import numpy as np
import random
import SIR_modell as sir
import matplotlib.pyplot as plt


def SSA(prop, stoch, X0, tspan, coeff):
    tvec = np.zeros(1)
    tvec[0] = tspan[0]
    Xarr = np.zeros([1, len(X0)])
    Xarr[0, :] = X0
    t = tvec[0]
    X = X0
    sMat = stoch()
    
    while t < tspan[1]:
        re = prop(X, coeff)
        a0 = sum(re)
        if a0 > 1e-10:
            # Bestäm reaktionstid
            r1 = random.random()
            tau = -np.log(r1) / a0
            t += tau
            tvec = np.append(tvec, t)
            
            # Bestäm vilken reaktion
            r2 = random.random()
            cre = np.cumsum(re)
            cre = cre / cre[-1]
            r = 0
            while cre[r] < r2:
                r += 1
            
            X = X + sMat[r, :]
            Xarr = np.vstack([Xarr, X])
        else: # Alla reaktionshastigheter 0
            print('Simuleringen avslutad vid t=', t)
            return tvec, Xarr

    return tvec, Xarr

plt.figure(figsize=(10, 6))

# Kör 10 oberoende simuleringar och plotta dem i samma diagram
antal_forsok = 10
for i in range(antal_forsok):
    tvec, Xarr = SSA(
        sir.propensitetsfunktioner_SEIRDV, 
        sir.stockiomatris_SEIRDV, 
        # sir.propensitetsfunktioner_SEIRDVM, 
        # sir.stockiomatris_SEIRDVM, 
        sir.Y0, 
        sir.tspan, 
        sir.c)

    

    if i == 0:
        plt.plot(tvec, Xarr[:, 0], 'b-', label='Mottagliga (S)', alpha=0.5)
        plt.plot(tvec, Xarr[:, 1], 'm-', label='Exponerade (E)', alpha=0.5)
        plt.plot(tvec, Xarr[:, 2], 'r-', label='Infekterade (I)', alpha=0.5)
        plt.plot(tvec, Xarr[:, 3], 'g-', label='Tillfrisknade (R)', alpha=0.6)
        plt.plot(tvec, Xarr[:, 4], 'k-', label='Döda (D)', alpha=0.6)
        plt.plot(tvec, Xarr[:, 5], 'c-', label='Vaccinerade (V)', alpha=0.6)
        #plt.plot(tvec, Xarr[:, 6], 'o-', label='Mökertal (M)', alpha=0.6)
    else:
        plt.plot(tvec, Xarr[:, 0], 'b-', alpha=0.3)
        plt.plot(tvec, Xarr[:, 1], 'm-', alpha=0.3)
        plt.plot(tvec, Xarr[:, 2], 'r-', alpha=0.3)
        plt.plot(tvec, Xarr[:, 3], 'g-', alpha=0.2)
        plt.plot(tvec, Xarr[:, 4], 'k-', alpha=0.2)
        plt.plot(tvec, Xarr[:, 5], 'c-', alpha=0.2)
        #plt.plot(tvec, Xarr[:, 6], 'o-', alpha=0.2)

plt.xlabel('Tid (t)')
plt.ylabel('Antal individer')
plt.title('Stokastisk simulering av SEIRDV')
plt.legend()
plt.grid(True)
plt.show()