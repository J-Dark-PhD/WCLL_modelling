import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress


def arrhenius_equation(K_0, E_K, T):
    return K_0 * np.exp(-E_K/k_B/T)


def fit_arrhenius(k, T):
    res = linregress(1000/T, np.log(k))
    print(res)
    a = res.slope
    b = res.intercept
    E = -a * k_B * 1000
    k_0 = np.exp(b)
    return k_0, E


# Liu 2021 https://doi.org/10.1016/j.jnucmat.2020.152647 
data = [
    (1.2253164556962024, 5.775301640089365e-25),
    (1.3034358047016272, 6.547822574773743e-25),
    (1.3891500904159129, 8.59034755268989e-25),
    (1.4759493670886075, 1.147748472629671e-24),
    (1.5877034358047015, 1.589372293363363e-24),
    (1.7200723327305605, 2.545797953008882e-24),
    (1.8448462929475586, 3.932327443532908e-24),
    (1.9641952983725135, 4.7904087393876894e-24),
    (2.074864376130199, 6.513723648130968e-24),
]

Avogadro = 6.022e23
R = 8.314
k_B = 8.617e-5

data = np.array(data)

T = np.linspace(500, 800)

k_0, E = fit_arrhenius(data[:, 1], 1000/data[:, 0])
plt.plot(1000/T, arrhenius_equation(k_0, E, T), label="$K_0 = {:.1e}$ , $E = {:.1f} $ eV".format(k_0, E))
plt.scatter(data[:, 0], data[:, 1], label="Liu")


# Braun 1980 https://doi.org/10.1016/0022-3115(80)90219-6 
data = [
    (1.1600985221674875, 3.8067929322953515e-21),
    (1.2746305418719213, 9.037713888850643e-22),
    (1.3596059113300494, 1.2819060338683778e-22),
    (1.4261083743842364, 2.6756548681770336e-23),
    (1.5073891625615763, 4.135340914084958e-24),
    (1.5960591133004927, 4.047533135048169e-24),
    (1.5295566502463056, 1.069779507321862e-24),
    (1.536945812807882, 4.835270471355741e-25),
    (1.6995073891625618, 2.827470847307085e-25),
    (1.7770935960591134, 6.671666889001258e-25),
    (1.8583743842364533, 4.94016754000614e-25),
    (1.8103448275862069, 1.84068734560933e-25),
    (2.20935960591133, 2.5011274284692738e-26),
    (2.3977832512315276, 3.8656011690087476e-27),
]

data = np.array(data)
k_0, E = fit_arrhenius(data[:, 1], 1000/data[:, 0])
T = np.linspace(400, 1000)
plt.plot(1000/T, arrhenius_equation(k_0, E, T), label="$K_0 = {:.1e}$ , $E = {:.1f} $ eV".format(k_0, E))
plt.scatter(data[:, 0], data[:, 1], label="Braun")


# Esteban https://doi.org/10.1016/S0022-3115(00)00485-2
K_r = 2.838e-7 / Avogadro * np.exp(-28679/R/T)
k_0 = 2.838e-7 / Avogadro
E = 28679*k_B
plt.plot(1000/T, K_r, label="Esteban $K_0 = {:.1e}$ , $E = {:.1f} $ eV".format(k_0, E))

# plt.plot(1000/T, arrhenius_equation(2.9e-14, 1.92, T), label="CuCrZr")
plt.yscale("log")
plt.legend()

plt.xlabel("1000/T (K$^{-1}$)")
plt.ylabel("Recombination coefficient $K_r$ (m$^{-4}$.s$^{-1}$)")

plt.show()
