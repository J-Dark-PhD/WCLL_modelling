import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

folder = "../../reference_case/transient"
data_traps = np.genfromtxt(
    folder + "/with_traps/derived_quantities.csv", delimiter=",", names=True
)

t = data_traps["ts"]
eurofer = data_traps["Flux_surface_39_solute"] * -1
pipe_1 = data_traps["Flux_surface_40_solute"] * -1
pipe_2 = data_traps["Flux_surface_41_solute"] * -1
pipe_3 = data_traps["Flux_surface_42_solute"] * -1
pipe_4 = data_traps["Flux_surface_43_solute"] * -1
pipe_5 = data_traps["Flux_surface_44_solute"] * -1
pipe_6 = data_traps["Flux_surface_45_solute"] * -1
pipe_7 = data_traps["Flux_surface_46_solute"] * -1
pipe_8 = data_traps["Flux_surface_47_solute"] * -1
pipe_9 = data_traps["Flux_surface_48_solute"] * -1
pipe_10 = data_traps["Flux_surface_49_solute"] * -1


data_no_traps = np.genfromtxt(
    folder + "/without_traps/derived_quantities.csv", delimiter=",", names=True
)
t_no_traps = data_no_traps["ts"]
eurofer_no_traps = data_no_traps["Flux_surface_39_solute"] * -1
pipe_1_no_traps = data_no_traps["Flux_surface_40_solute"] * -1
pipe_2_no_traps = data_no_traps["Flux_surface_41_solute"] * -1
pipe_3_no_traps = data_no_traps["Flux_surface_42_solute"] * -1
pipe_4_no_traps = data_no_traps["Flux_surface_43_solute"] * -1
pipe_5_no_traps = data_no_traps["Flux_surface_44_solute"] * -1
pipe_6_no_traps = data_no_traps["Flux_surface_45_solute"] * -1
pipe_7_no_traps = data_no_traps["Flux_surface_46_solute"] * -1
pipe_8_no_traps = data_no_traps["Flux_surface_47_solute"] * -1
pipe_9_no_traps = data_no_traps["Flux_surface_48_solute"] * -1
pipe_10_no_traps = data_no_traps["Flux_surface_49_solute"] * -1


# fig, axs = plt.subplots(1, 1, sharey=True, figsize=(9.6, 4.8))

plt.figure()

# plt.sca(axs[0])
x_annotation = t[-1] * 1.15

colour = "black"
plt.plot(t, eurofer, color=colour)
plt.plot(t_no_traps, eurofer_no_traps, color=colour, linestyle="dashed", alpha=0.5)
plt.annotate("FW cooling", (x_annotation, eurofer[-1]), color=colour)

plt.ylabel(r"Surface flux (T m$^{-1}$ s$^{-1}$)")

colour = "forestgreen"
front = pipe_1 + pipe_5 + pipe_7
front_no_traps = pipe_1_no_traps + pipe_5_no_traps + pipe_7_no_traps
plt.plot(t, front, color=colour)
plt.plot(t_no_traps, front_no_traps, color=colour, linestyle="dashed", alpha=0.5)
plt.annotate("Front BZ pipes", (x_annotation, front[-1]), color=colour)


colour = "purple"
middle_flux = pipe_2 + pipe_6 + pipe_8
middle_flux_no_traps = pipe_2_no_traps + pipe_6_no_traps + pipe_8_no_traps
plt.plot(t, middle_flux, color=colour)
plt.plot(t_no_traps, middle_flux_no_traps, color=colour, linestyle="dashed", alpha=0.5)
plt.annotate("Middle BZ pipes", (x_annotation, middle_flux[-1] * 0.85), color=colour)

colour = "steelblue"
rear_flux = pipe_3 + pipe_4 + pipe_9 + pipe_10
rear_flux_no_traps = (
    pipe_3_no_traps + pipe_4_no_traps + pipe_9_no_traps + pipe_10_no_traps
)
plt.plot(t, rear_flux, color=colour)
plt.plot(t_no_traps, rear_flux_no_traps, color=colour, linestyle="dashed", alpha=0.5)
plt.annotate("Rear BZ pipes", (x_annotation, rear_flux[-1] * 0.9), color=colour)


# plt.annotate("BZ pipes", (x_annotation + 300, middle_flux[-1]*1.1))

plt.yscale("log")
plt.xlabel(r"Time (s)")
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.xscale("log")
# plt.xlim(right=5e1)
plt.xlim(right=5e6)
plt.ylim(bottom=1e14, top=2e16)
custom_lines = (
    Line2D([0], [0], color="grey", linestyle="solid"),
    Line2D([0], [0], color="grey", linestyle="dashed"),
)
plt.legend(custom_lines, ["Traps", "No traps"])

plt.show()
