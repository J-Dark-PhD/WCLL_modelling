import matplotlib.pyplot as plt
import numpy as np

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=12)

data_traps = np.genfromtxt(
    'fw_eurofer_traps_steady_state.csv',
    delimiter=',', names=True)

data_no_traps = np.genfromtxt(
    'fw_eurofer_no_traps_steady_state.csv',
    delimiter=',', names=True)

# print(data_traps.dtype.names)
# exit()

y_traps = data_traps["retention"]
fw_eurofer_traps = data_traps['Points0']*1000

y_no_traps = data_no_traps["solute"]
fw_eurofer_no_traps = data_no_traps['Points0']*1000


plt.figure()

colour = 'black'
plt.plot(fw_eurofer_traps, y_traps, color=colour)
plt.annotate('traps', (1.25, 5e21), color='black')
# plt.plot(
#     y_no_traps, fw_eurofer_traps,
#     color=colour, linestyle="--", label="Traps")
# plt.annotate(
#     "Traps", (x_annotation, fw_eurofer_traps[-1]), color=colour)


colour = 'black'
plt.plot(
    fw_eurofer_no_traps, y_no_traps,
    color=colour, linestyle='dashed', alpha=0.6, label='no traps')
plt.annotate('no traps', (1.25, 2e20), color='black', alpha=0.6)
# plt.plot(
#     y_no_traps, fw_eurofer_no_traps,
#     color=colour, linestyle="-")
# plt.annotate(
#     "No Traps", (x_annotation, fw_eurofer_no_traps[-1]*1.2), color=colour)

grey_eurofer = (153/255, 153/255, 153/255)
green_lipb = (146/255, 196/255, 125/255)
red_W = {171/255, 15/255, 26/255}
y_range = [1e17, 1e23]
plt.fill_betweenx(y_range, 0, 2, facecolor=red_W, alpha=0.5)
plt.fill_betweenx(y_range, 2, 4, facecolor=grey_eurofer, alpha=0.5)

plt.annotate('Tungsten', (0.7, 6e22), color='black')
plt.annotate('EUROFER', (2.65, 6e22), color='black')

plt.ylabel(r"Retention (T m$^{-3}$)")
plt.yscale("log")
plt.xlabel(r"Distance from plasma facing surface (mm)")
# plt.legend()
plt.tight_layout()
# ax = plt.gca()
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
plt.xlim(0, 4)
plt.ylim(1e18, 1e23)

plt.show()
