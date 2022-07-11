import matplotlib.pyplot as plt
import numpy as np

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)

temp_range = np.linspace(569, 601, num=11)
# temp_range = [569.0, 572.2, 575.4, 578.6, 581.8, 585.0, 588.2, 591.4, 594.6, 597.8, 601.0]

T_bz_pipes, T_fw_channels = [], []
folder = "../../../../../data/parametric_studies/varying_h_coeff/results/"
for temp in temp_range:
    filename = folder + "run_{:.1f}K/derived_quantities.csv".format(temp)
    data = np.genfromtxt(filename, delimiter=",", names=True)
    bz_pipes = np.mean([data["Average_T_surface_{}".format(i)] for i in range(28, 39)])
    T_bz_pipes.append(bz_pipes)
    fw_channles = np.mean(
        [data["Average_T_surface_{}".format(i)] for i in range(24, 28)]
    )
    T_fw_channels.append(fw_channles)

plt.figure()
plt.plot(temp_range, T_bz_pipes, label="BZ Pipes")
plt.plot(temp_range, T_fw_channels, label="FW Channels")
# plt.xscale("log")
# plt.yscale("log")
# plt.ylim(0, 2e19)
# plt.ylim(bottom=0)
plt.ylabel(r"Average temperture (K)")
plt.xlabel(r"Bulk coolant temperature (K)")
plt.legend()
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()


plt.show()
