import matplotlib.pyplot as plt
import numpy as np

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=12)

data_traps = np.genfromtxt(
    'pipe_1_traps_steady_state.csv',
    delimiter=',', names=True)

data_no_traps = np.genfromtxt(
    'pipe_1_no_traps_steady_state.csv',
    delimiter=',', names=True)


plt.figure()

y_traps = data_traps["retention"]
pipe_traps = data_traps['Points0']*1000

y_no_traps = data_no_traps["solute"]
pipe_no_traps = data_no_traps['Points0']*1000

# plt.annotate('PbLi', (7.5, 1.5e22), color='white', weight = 'bold')
# plt.annotate('EUROFER', (4, 1.5e22), color='white', weight = 'bold')

pipe_traps = np.array(pipe_traps)
pipe_no_traps = np.array(pipe_no_traps)

plt.plot(pipe_traps-40.5, y_traps, color='black')
plt.annotate('traps', (-5.5, 3e22), color='black')
plt.plot(
    pipe_no_traps-40.5, y_no_traps,
    color='black', linestyle='dashed', alpha=0.6)
plt.annotate(
    'no traps', (-7.25, 8e21), color='black', alpha=0.6)

grey_eurofer = (153/255, 153/255, 153/255)
green_lipb = (146/255, 196/255, 125/255)
red_W = {171/255, 15/255, 26/255}

y_range = [1e18, 1e26]

plt.ylabel(r"Retention (T m$^{-3}$)")
plt.yscale("log")
plt.xlabel(r"Distance from pipe centre (mm)")
# plt.legend()
plt.tight_layout()
plt.fill_betweenx(y_range, -9.5, -6.75, facecolor=green_lipb, alpha=0.5)
plt.fill_betweenx(y_range, -6.75, -4, facecolor=grey_eurofer, alpha=0.5)
plt.fill_betweenx(y_range, 4, 6.75, facecolor=grey_eurofer, alpha=0.5)
plt.fill_betweenx(y_range, 6.75, 9.5, facecolor=green_lipb, alpha=0.5)
plt.ylim(3e20, 1e24)
plt.xlim(left=-9.5, right=9.5)

plt.show()
