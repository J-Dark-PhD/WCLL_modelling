import matplotlib.pyplot as plt
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

temp_range = np.linspace(569, 601, num=15)

# temp_range = [569.0, 572.2, 575.4, 578.6, 581.8, 585.0, 588.2, 591.4, 594.6, 597.8, 601.0]

bz_pipes, fw_channels = [], []
folder = "../../../../../data/parametric_studies/varying_h_coeff/results/"
for temp in temp_range:
    filename = folder + "run_{:.1f}K/derived_quantities.csv".format(temp)
    data = np.genfromtxt(filename, delimiter=",", names=True)
    bz_pipes.append(
        sum([data["Flux_surface_{}_solute".format(i)] * -1 for i in range(28, 39)])
    )
    fw_channels.append(
        sum([data["Flux_surface_{}_solute".format(j)] * -1 for j in range(24, 28)])
    )

plt.figure()
plt.plot(temp_range, bz_pipes, label="BZ pipes", color="black")
plt.ylim(0, 5e16)
plt.ylabel(r"Surface Flux (W m$^{-1}$s$^{-1}$)")
plt.xlabel(r"Coolant bulk temperature (K)")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

plt.figure()
plt.plot(temp_range, fw_channels, label="FW channels", color="black")
plt.ylim(0, 7e15)
plt.ylabel(r"Surface Flux (T m$^{-1}$s$^{-1}$)")
plt.xlabel(r"Coolant bulk temperature (K)")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

bz_diff = ((bz_pipes[-1] - bz_pipes[0]) / bz_pipes[0]) * 100
fw_diff = ((fw_channels[-1] - fw_channels[0]) / fw_channels[0]) * 100
print("Difference in bz pipes = {:.1f} %".format(bz_diff))
print("Difference in fw_channels = {:.1f} %".format(fw_diff))

plt.show()
