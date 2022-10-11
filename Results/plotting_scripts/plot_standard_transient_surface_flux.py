import matplotlib.pyplot as plt
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

# folder = "../standard_cas/transient/"
folder = "../"
data = np.genfromtxt(folder + "derived_quantities.csv", delimiter=",", names=True)

t = data["ts"]
fw_coolant_interface_1_4 = data["Flux_surface_24_solute"] * -1
fw_coolant_interface_1_3 = data["Flux_surface_25_solute"] * -1
fw_coolant_interface_1_2 = data["Flux_surface_26_solute"] * -1
fw_coolant_interface_1_1 = data["Flux_surface_27_solute"] * -1
pipe_1_1_coolant_interface = data["Flux_surface_28_solute"] * -1
pipe_1_2_coolant_interface = data["Flux_surface_29_solute"] * -1
pipe_1_3_coolant_interface = data["Flux_surface_30_solute"] * -1
pipe_2_1_coolant_interface = data["Flux_surface_31_solute"] * -1
pipe_2_2_coolant_interface = data["Flux_surface_32_solute"] * -1
pipe_2_3_coolant_interface = data["Flux_surface_33_solute"] * -1
pipe_2_4_coolant_interface = data["Flux_surface_34_solute"] * -1
pipe_3_1_coolant_interface = data["Flux_surface_35_solute"] * -1
pipe_3_2_coolant_interface = data["Flux_surface_36_solute"] * -1
pipe_3_3_coolant_interface = data["Flux_surface_37_solute"] * -1
pipe_3_4_coolant_interface = data["Flux_surface_38_solute"] * -1

fw_cooling_channels = (
    np.array(fw_coolant_interface_1_4)
    + np.array(fw_coolant_interface_1_3)
    + np.array(fw_coolant_interface_1_2)
    + np.array(fw_coolant_interface_1_1)
)

bz_pipes_front = (
    np.array(pipe_1_1_coolant_interface)
    + np.array(pipe_1_2_coolant_interface)
    + np.array(pipe_1_3_coolant_interface)
)

bz_pipes_mid = (
    np.array(pipe_2_1_coolant_interface)
    + np.array(pipe_2_2_coolant_interface)
    + np.array(pipe_2_3_coolant_interface)
    + np.array(pipe_2_4_coolant_interface)
)

bz_pipes_rear = (
    np.array(pipe_3_1_coolant_interface)
    + np.array(pipe_3_2_coolant_interface)
    + np.array(pipe_3_3_coolant_interface)
    + np.array(pipe_3_4_coolant_interface)
)

# plot

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

plt.figure()
plt.plot(t, fw_cooling_channels, label="FW cooling channels", color="black")
plt.plot(t, bz_pipes_front, label="BZ pipes front", color="forestgreen")
plt.plot(t, bz_pipes_mid, label="BZ pipes mid", color="purple")
plt.plot(t, bz_pipes_rear, label="BZ pipes rear", color="dodgerblue")
plt.legend(loc="upper left")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.ylim(1e14, 2e16)
plt.xlim(1e2, 2e6)
plt.yscale("log")
plt.xscale("log")
plt.ylabel(r"Surface Flux (T m$^{-1}$ s$^{-1}$)")
plt.xlabel(r"Time (s)")
plt.tight_layout()


plt.figure()
t = t / 86400
plt.plot(t, fw_cooling_channels, label="FW cooling channels", color="black")
plt.plot(t, bz_pipes_front, label="BZ pipes front", color="forestgreen")
plt.plot(t, bz_pipes_mid, label="BZ pipes mid", color="purple")
plt.plot(t, bz_pipes_rear, label="BZ pipes rear", color="dodgerblue")
plt.legend(loc="upper left")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.ylim(1e14, 2e16)
plt.xlim(left=0)
plt.yscale("log")
plt.ylabel(r"Surface Flux (T m$^{-1}$ s$^{-1}$)")
plt.xlabel(r"Time (days)")
plt.tight_layout()

plt.show()
