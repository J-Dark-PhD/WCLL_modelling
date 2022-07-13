import matplotlib.pyplot as plt
import numpy as np


plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=12)

grey_eurofer = (204/255, 204/255, 204/255)
green_lipb = (200/255, 225/255, 190/255)
orange = (231/255, 122/255, 47/255)

data = np.genfromtxt("velocity_profile.csv", delimiter=",", names=True)

y = data["arc_length"]
vel = data["u0"]
indexes = np.where(abs(vel) < 1e-5)
vel[indexes] = float('nan')

plt.figure(figsize=(6.4, 4.8/2))
plt.plot(y*1e3, vel*1e3, color='black')

plt.xlabel("y (mm)")
plt.ylabel("$u_x$ (mm/s)")

plt.hlines(0, 0, 132, color=orange, linestyle="dashed")

y_range = [-0.3, 0.3]
plt.fill_betweenx(y_range, 0, 4, facecolor=grey_eurofer)
plt.fill_betweenx(y_range, 4, 65, facecolor=green_lipb)
plt.fill_betweenx(y_range, 65, 67, facecolor=grey_eurofer)
plt.fill_betweenx(y_range, 67, 128, facecolor=green_lipb)
plt.fill_betweenx(y_range, 128, 132, facecolor=grey_eurofer)


plt.yticks(ticks=[-0.2, 0, 0.2])
plt.xlim(0, 132)
plt.ylim(-0.22, 0.22)
plt.tight_layout()
plt.show()
