import matplotlib.pyplot as plt
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

dpa_values = np.linspace(0, 20, 21)

inv_first_wall = []
FW_cooling_channels = []
folder = "../../parametric_studies/varying_damage/"
for dpa in dpa_values:
    filename = folder + "{:.1f}_dpa/derived_quantities.csv".format(dpa)
    data = np.genfromtxt(filename, delimiter=",", names=True)
    inv_first_wall.append(data["Total_retention_volume_9"])
    FW_cooling_channels.append(
        (sum([data["Flux_surface_{}_solute".format(i)] for i in range(24, 28)])) * -1
    )

# Tungsten inventory

diff_inv = ((inv_first_wall[-1] - inv_first_wall[0]) / inv_first_wall[0]) * 100
demo_case = ((inv_first_wall[9] - inv_first_wall[0]) / inv_first_wall[0]) * 100
print("Inventory difference = {:.1f}%".format(diff_inv))
print("DEMO case = {:.1f}%".format(demo_case))

plt.figure()
plt.plot(dpa_values, inv_first_wall, label="FW", color="black", marker="x")

plt.vlines(9, 0, inv_first_wall[9], color="grey", linestyle="dashed")
plt.hlines(inv_first_wall[9], 0, 9, color="grey", linestyle="dashed")
plt.annotate("DEMO", (9.5, 3.5e17), color="grey")
# plt.yscale("log")
plt.ylim(0, 6e17)
plt.xlim(0, 20)
plt.ylabel(r"Inventory (T m$^{-1}$)")
plt.xlabel(r"Damage rate (dpa/fpy)")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

# FW Cooling pipes flux

diff_flux = (
    (FW_cooling_channels[-1] - FW_cooling_channels[0]) / FW_cooling_channels[0]
) * 100
print("Difference in surface flux = {:.1f}%".format(diff_flux))

plt.figure()
plt.plot(dpa_values, FW_cooling_channels, label="FW", color="black", marker="x")
plt.ylim(bottom=0)
plt.xlim(0, 20)
plt.ylabel(r"Surface Flux (T m$^{-1}$s$^{-1}$)")
plt.xlabel(r"Damage rate (dpa/fpy)")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()


plt.show()
