"""
File: SIR_model.py
Author: Aiden Telgenhof
Description: Baseline model for this problem, this file also runs a bunch of simulations
and reports the average number of infected in the model
"""
import numpy as np
import matplotlib.pyplot as plt

def stochastic_sir(N, I0, R0, beta, gamma, days):
    S = np.zeros(days, dtype=int)
    I = np.zeros(days, dtype=int)
    R = np.zeros(days, dtype=int)
    S[0] = N - I0 - R0
    I[0] = I0
    R[0] = R0
    
    rng = np.random.default_rng()

    for t in range(1, days):
        if I[t-1] == 0:
            S[t], I[t], R[t] = S[t-1], 0, R[t-1]
            continue

        p_inf = 1 - np.exp(-beta * I[t-1] / N)

        new_inf = rng.binomial(S[t-1], p_inf)
        new_rec = rng.binomial(I[t-1], 1 - np.exp(-gamma))

        S[t] = S[t-1] - new_inf
        I[t] = I[t-1] + new_inf - new_rec
        R[t] = R[t-1] + new_rec

    return S, I, R

N_RUNS = 200
N = 300
I0 = 1
R0 = 0
beta = 0.3 # This number represents the transmission probability
gamma = 0.1 # This number represents the recovery rate
days = 100

peak_infected = []

for _ in range(N_RUNS):
    S, I, R = stochastic_sir(N, I0, R0, beta, gamma, days)
    peak = max(I)
    if peak <= 5:
        continue
    peak_infected.append(peak)

peak_infected = np.array(peak_infected)

mean_peak = np.mean(peak_infected)
std_peak = np.std(peak_infected)

print("----- SIR Peak Infection Statistics -----")
print(f"Runs: {N_RUNS}")
print(f"Mean peak infected: {mean_peak:.2f}")
print(f"Standard deviation: {std_peak:.2f}")
print("-----------------------------------------")

plt.hist(peak_infected, bins=20)
plt.xlabel("Maximum infected in run")
plt.ylabel("Frequency")
plt.show()