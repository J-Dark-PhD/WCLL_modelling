import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

red_W = (171 / 255, 15 / 255, 26 / 255)
grey_eurofer = (153 / 255, 153 / 255, 153 / 255)
green_lipb = (146 / 255, 196 / 255, 125 / 255)

folder = "../../parametric_studies/varying_source/transient/"
data_both_traps = np.genfromtxt(
    folder + "/both_traps/derived_quantities.csv", delimiter=",", names=True
)
data_both_no_traps = np.genfromtxt(
    folder + "/both_no_traps/derived_quantities.csv", delimiter=",", names=True
)

data_breeder_traps = np.genfromtxt(
    folder + "/breeder_traps/derived_quantities.csv", delimiter=",", names=True
)
data_breeder_no_traps = np.genfromtxt(
    folder + "/breeder_no_traps/derived_quantities.csv", delimiter=",", names=True
)

data_plasma_traps = np.genfromtxt(
    folder + "/plasma_traps/derived_quantities.csv", delimiter=",", names=True
)
data_plasma_no_traps = np.genfromtxt(
    folder + "/plasma_no_traps/derived_quantities.csv", delimiter=",", names=True
)

t = data_both_traps["ts"]
fw_cooling_channel_both_traps = data_both_traps["Flux_surface_39_solute"] * -1
fw_cooling_channel_both_no_traps = data_both_no_traps["Flux_surface_39_solute"] * -1

fw_cooling_channel_breeder_traps = data_breeder_traps["Flux_surface_39_solute"] * -1
fw_cooling_channel_breeder_no_traps = (
    data_breeder_no_traps["Flux_surface_39_solute"] * -1
)

fw_cooling_channel_plasma_traps = data_plasma_traps["Flux_surface_39_solute"] * -1
fw_cooling_channel_plasma_no_traps = data_plasma_no_traps["Flux_surface_39_solute"] * -1

plt.figure()

plt.plot(t, fw_cooling_channel_both_traps, label="Both", color="black")
plt.plot(t, fw_cooling_channel_both_no_traps, color="black", linestyle="dashed")
plt.plot(t, fw_cooling_channel_breeder_traps, label="Breeder", color=green_lipb)
plt.plot(t, fw_cooling_channel_breeder_no_traps, color=green_lipb, linestyle="dashed")
plt.plot(t, fw_cooling_channel_plasma_traps, label="Plasma", color=red_W)
plt.plot(t, fw_cooling_channel_plasma_no_traps, color=red_W, linestyle="dashed")

plt.annotate("Both", (2e4, 2e15), color="black")
plt.annotate("Breeder", (2e5, 1e15), color=green_lipb)
plt.annotate("Plasma", (2e5, 5e12), color=red_W)

plt.ylabel("First wall cooling channels \n Surface flux (T m$^{-1}$ s$^{-1}$)")


plt.yscale("log")
plt.xlabel(r"Time (s)")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.xscale("log")
plt.ylim(1e10, 1e16)
custom_lines = (
    Line2D([0], [0], color="grey", linestyle="solid"),
    Line2D([0], [0], color="grey", linestyle="dashed"),
)
plt.legend(custom_lines, ["Traps", "No traps"], loc="upper left")
plt.tight_layout()
plt.show()
