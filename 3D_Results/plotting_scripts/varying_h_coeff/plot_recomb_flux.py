import numpy as np
import matplotlib.pyplot as plt

T_values = np.linspace(590, 660, num=100)

k_B = 8.6173303e-5  # Boltzmann constant eV.K-1
Kr_0 = 1.4143446334700682e-26
E_Kr = -0.25727457261201786

Kr_values = []
for T in T_values:
    Kr = Kr_0 * np.exp(-E_Kr / k_B / T)
    Kr_values.append(Kr)

plt.figure()
plt.plot(T_values, Kr_values, color="black")
plt.ylim(0, 3e-24)
plt.xlabel("Temperature (K)")
plt.ylabel("Recombination Flux (m4 s-1)")
plt.show()

diff = ((Kr_values[-1] - Kr_values[0]) / Kr_values[0]) * 100
print("Difference = {:.1f} %".format(diff))
