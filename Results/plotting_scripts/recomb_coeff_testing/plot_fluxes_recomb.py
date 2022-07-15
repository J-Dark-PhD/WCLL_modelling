import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

red_W = (171 / 255, 15 / 255, 26 / 255)
grey_eurofer = (153 / 255, 153 / 255, 153 / 255)
green_lipb = (146 / 255, 196 / 255, 125 / 255)

folder = "../../parametric_studies/varying_recomb_coeff"
data_liu = np.genfromtxt(
    folder + "/liu_standard/derived_quantities.csv", delimiter=",", names=True
)

data_braun = np.genfromtxt(
    folder + "/braun/derived_quantities.csv", delimiter=",", names=True
)

data_esteban = np.genfromtxt(
    folder + "/esteban/derived_quantities.csv", delimiter=",", names=True
)

data_inst = np.genfromtxt(
    folder + "/instantaneous/derived_quantities.csv", delimiter=",", names=True
)

t = data_liu["ts"]
fw_cooling_channel_liu = data_liu["Flux_surface_39_solute"] * -1
pipe_1_flux_liu = data_liu["Flux_surface_40_solute"] * -1
pipe_2_flux_liu = data_liu["Flux_surface_41_solute"] * -1
pipe_3_flux_liu = data_liu["Flux_surface_42_solute"] * -1
pipe_4_flux_liu = data_liu["Flux_surface_43_solute"] * -1
pipe_5_flux_liu = data_liu["Flux_surface_44_solute"] * -1
pipe_6_flux_liu = data_liu["Flux_surface_45_solute"] * -1
pipe_7_flux_liu = data_liu["Flux_surface_46_solute"] * -1
pipe_8_flux_liu = data_liu["Flux_surface_47_solute"] * -1
pipe_9_flux_liu = data_liu["Flux_surface_48_solute"] * -1
pipe_10_flux_liu = data_liu["Flux_surface_49_solute"] * -1
pipes_flux_liu = (
    pipe_1_flux_liu
    + pipe_2_flux_liu
    + pipe_3_flux_liu
    + pipe_4_flux_liu
    + pipe_5_flux_liu
    + pipe_6_flux_liu
    + pipe_7_flux_liu
    + pipe_8_flux_liu
    + pipe_9_flux_liu
    + pipe_10_flux_liu
)

fw_cooling_channel_braun = data_braun["Flux_surface_39_solute"] * -1
pipe_1_flux_braun = data_braun["Flux_surface_40_solute"] * -1
pipe_2_flux_braun = data_braun["Flux_surface_41_solute"] * -1
pipe_3_flux_braun = data_braun["Flux_surface_42_solute"] * -1
pipe_4_flux_braun = data_braun["Flux_surface_43_solute"] * -1
pipe_5_flux_braun = data_braun["Flux_surface_44_solute"] * -1
pipe_6_flux_braun = data_braun["Flux_surface_45_solute"] * -1
pipe_7_flux_braun = data_braun["Flux_surface_46_solute"] * -1
pipe_8_flux_braun = data_braun["Flux_surface_47_solute"] * -1
pipe_9_flux_braun = data_braun["Flux_surface_48_solute"] * -1
pipe_10_flux_braun = data_braun["Flux_surface_49_solute"] * -1
pipes_flux_braun = (
    pipe_1_flux_braun
    + pipe_2_flux_braun
    + pipe_3_flux_braun
    + pipe_4_flux_braun
    + pipe_5_flux_braun
    + pipe_6_flux_braun
    + pipe_7_flux_braun
    + pipe_8_flux_braun
    + pipe_9_flux_braun
    + pipe_10_flux_braun
)

fw_cooling_channel_esteban = data_esteban["Flux_surface_39_solute"] * -1
pipe_1_flux_esteban = data_esteban["Flux_surface_40_solute"] * -1
pipe_2_flux_esteban = data_esteban["Flux_surface_41_solute"] * -1
pipe_3_flux_esteban = data_esteban["Flux_surface_42_solute"] * -1
pipe_4_flux_esteban = data_esteban["Flux_surface_43_solute"] * -1
pipe_5_flux_esteban = data_esteban["Flux_surface_44_solute"] * -1
pipe_6_flux_esteban = data_esteban["Flux_surface_45_solute"] * -1
pipe_7_flux_esteban = data_esteban["Flux_surface_46_solute"] * -1
pipe_8_flux_esteban = data_esteban["Flux_surface_47_solute"] * -1
pipe_9_flux_esteban = data_esteban["Flux_surface_48_solute"] * -1
pipe_10_flux_esteban = data_esteban["Flux_surface_49_solute"] * -1
pipes_flux_esteban = (
    pipe_1_flux_esteban
    + pipe_2_flux_esteban
    + pipe_3_flux_esteban
    + pipe_4_flux_esteban
    + pipe_5_flux_esteban
    + pipe_6_flux_esteban
    + pipe_7_flux_esteban
    + pipe_8_flux_esteban
    + pipe_9_flux_esteban
    + pipe_10_flux_esteban
)

fw_cooling_channel_inst = data_inst["Flux_surface_39_solute"] * -1
pipe_1_flux_inst = data_inst["Flux_surface_40_solute"] * -1
pipe_2_flux_inst = data_inst["Flux_surface_41_solute"] * -1
pipe_3_flux_inst = data_inst["Flux_surface_42_solute"] * -1
pipe_4_flux_inst = data_inst["Flux_surface_43_solute"] * -1
pipe_5_flux_inst = data_inst["Flux_surface_44_solute"] * -1
pipe_6_flux_inst = data_inst["Flux_surface_45_solute"] * -1
pipe_7_flux_inst = data_inst["Flux_surface_46_solute"] * -1
pipe_8_flux_inst = data_inst["Flux_surface_47_solute"] * -1
pipe_9_flux_inst = data_inst["Flux_surface_48_solute"] * -1
pipe_10_flux_inst = data_inst["Flux_surface_49_solute"] * -1
pipes_flux_inst = (
    pipe_1_flux_inst
    + pipe_2_flux_inst
    + pipe_3_flux_inst
    + pipe_4_flux_inst
    + pipe_5_flux_inst
    + pipe_6_flux_inst
    + pipe_7_flux_inst
    + pipe_8_flux_inst
    + pipe_9_flux_inst
    + pipe_10_flux_inst
)

plt.figure()

plt.plot(t, fw_cooling_channel_liu, label="Liu", color="black")
plt.plot(t, fw_cooling_channel_braun, label="Braun")
plt.plot(t, fw_cooling_channel_esteban, label="Esteban")
plt.plot(t, fw_cooling_channel_inst, label="Instantaneous")

plt.ylim(1e14, 1e16)
plt.xlim(1e2, 5e6)
plt.yscale("log")
plt.xscale("log")
plt.xlabel(r"Time (s)")
plt.ylabel("First wall cooling channels \n Surface flux (T m$^{-1}$ s$^{-1}$)")
ax = plt.gca()
plt.legend()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()

plt.figure()
plt.plot(t, pipes_flux_liu, label="Liu", color="black")
plt.plot(t, pipes_flux_braun, label="Braun")
plt.plot(t, pipes_flux_esteban, label="Esteban")
plt.plot(t, pipes_flux_inst, label="Instantaneous")


# plt.annotate(
#     "Both", (2e4, 2e15), color='black')
# plt.annotate(
#     "Breeder", (2e5, 1e15), color=green_lipb)
# plt.annotate(
#     "Plasma", (2e5, 5e12), color=red_W)

plt.ylabel("BZ cooling channels \n Surface flux (T m$^{-1}$ s$^{-1}$)")


plt.yscale("log")
plt.ylim(1e14, 1e17)
plt.xlim(1e2, 5e6)
plt.xlabel(r"Time (s)")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.xscale("log")
plt.legend()
# plt.ylim(1e10, 1e16)
plt.tight_layout()
plt.show()
