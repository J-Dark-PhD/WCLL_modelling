import matplotlib.pyplot as plt
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

red_W = (171 / 255, 15 / 255, 26 / 255)
grey_eurofer = (153 / 255, 153 / 255, 153 / 255)
green_lipb = (146 / 255, 196 / 255, 125 / 255)

data_both_traps = np.genfromtxt("fw_eurofer_both_traps.csv", delimiter=",", names=True)

data_breeder_traps = np.genfromtxt(
    "fw_eurofer_breeder_traps.csv", delimiter=",", names=True
)

data_plasma_traps = np.genfromtxt(
    "fw_eurofer_plasma_traps.csv", delimiter=",", names=True
)

retention_both_traps = data_both_traps["retention"]
x_position = data_both_traps["Points0"] * 1000

retention_breeder_traps = data_breeder_traps["retention"]
retention_plasma_traps = data_plasma_traps["retention"]


plt.figure()

plt.plot(x_position, retention_both_traps, color=colour)
# plt.annotate('Both', (1.25, 5e21), color='black')

plt.plot(x_position, retention_breeder_traps, color=green_lipb)
# plt.annotate('Breeder', (1.25, 5e21), color=green_lipb)

plt.plot(x_position, retention_plasma_traps, color=red_W)
# plt.annotate('Breeder', (1.25, 5e21), color=green_lipb)

# y_range = [1e17, 1e23]
# plt.fill_betweenx(y_range, 0, 2, facecolor=red_W, alpha=0.5)
# plt.fill_betweenx(y_range, 2, 4, facecolor=grey_eurofer, alpha=0.5)

plt.annotate("Tungsten", (0.7, 6e22), color="black")
plt.annotate("EUROFER", (2.65, 6e22), color="black")

plt.ylabel(r"Retention (T m$^{-3}$)")
plt.yscale("log")
plt.xlabel(r"Distance from plasma facing surface (mm)")
plt.tight_layout()
plt.xlim(0, 4)
# plt.ylim(1e18, 1e23)

plt.show()
