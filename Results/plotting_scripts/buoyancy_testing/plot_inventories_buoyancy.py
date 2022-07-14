import matplotlib.pyplot as plt
import numpy as np

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

red_W = (171 / 255, 15 / 255, 26 / 255)
grey_eurofer = (153 / 255, 153 / 255, 153 / 255)
green_lipb = (146 / 255, 196 / 255, 125 / 255)


# ## Read data
volumes_bz_pipes = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

folder = "../../parametric_studies/varying_buoyancy/transient"

# without buoyancy
data_without_buoyancy = np.genfromtxt(
    folder + "/without_buoyancy/derived_quantities.csv", delimiter=",", names=True
)
t_without_buoyancy = data_without_buoyancy["ts"] / 86400
lipb_without_buoyancy = data_without_buoyancy["Total_solute_volume_6"]
structure_without_buoyancy = (
    data_without_buoyancy["Total_retention_volume_8"]
    + data_without_buoyancy["Total_retention_volume_9"]
)
first_wall_without_buoyancy = data_without_buoyancy["Total_retention_volume_7"]
bz_pipes_without_buoyancy = sum(
    [
        data_without_buoyancy["Total_retention_volume_{}".format(vol)]
        for vol in volumes_bz_pipes
    ]
)

# Breeder source
data_with_buoyancy = np.genfromtxt(
    folder + "/with_buoyancy/derived_quantities.csv", delimiter=",", names=True
)
t_with_buoyancy = data_with_buoyancy["ts"] / 86400
lipb_with_buoyancy = data_with_buoyancy["Total_solute_volume_6"]
structure_with_buoyancy = (
    data_with_buoyancy["Total_retention_volume_8"]
    + data_with_buoyancy["Total_retention_volume_9"]
)
first_wall_with_buoyancy = data_with_buoyancy["Total_retention_volume_7"]
bz_pipe_with_buoyancy = data_with_buoyancy["Total_retention_volume_10"]
bz_pipes_with_buoyancy = sum(
    [
        data_with_buoyancy["Total_retention_volume_{}".format(vol)]
        for vol in volumes_bz_pipes
    ]
)


# ## Plot
fig = plt.figure(figsize=(4.5, 9))
linestyle_no_trap = "dashed"

# create one big plot to have a common y label
ax = fig.add_subplot(111)
ax.spines["top"].set_color("none")
ax.spines["bottom"].set_color("none")
ax.spines["left"].set_color("none")
ax.spines["right"].set_color("none")
ax.tick_params(labelcolor="w", top=False, bottom=False, left=False, right=False)
ax.set_ylabel(r"Inventory (T m$^{-1}$)")

# LiPb
ax1 = fig.add_subplot(411)
plt.sca(ax1)

plt.plot(t_without_buoyancy, lipb_without_buoyancy, color="black")
plt.plot(t_with_buoyancy, lipb_with_buoyancy, color="red")
# plt.annotate(
#     "LiPb", (t_both[-1], lipb_both[-1]),
#     xytext=(t_both[-1]*1.1, lipb_both[-1]), color= 'black')


# Structure
ax2 = fig.add_subplot(412)
plt.sca(ax2)
plt.plot(t_without_buoyancy, structure_without_buoyancy, color="black")
plt.plot(t_with_buoyancy, structure_with_buoyancy, color="red")
# plt.annotate(
#     "Structure", (t_both[-1], structure_both[-1]),
#     xytext=(t_both[-1]*1.1, structure_both[-1]), color='black')

# Pipes
ax3 = fig.add_subplot(413)
plt.sca(ax3)
plt.plot(t_without_buoyancy, bz_pipes_without_buoyancy, color="black")
plt.plot(t_with_buoyancy, bz_pipes_with_buoyancy, color="red")
# plt.annotate(
#     "BZ pipes", (t_both[-1], bz_pipes_both[-1]),
#     xytext=(t_both[-1]*1.1, bz_pipes_both[-1]), color='black')


# FW
ax4 = fig.add_subplot(414)
plt.sca(ax4)
plt.plot(t_without_buoyancy, first_wall_without_buoyancy, color="black")
plt.plot(t_with_buoyancy, first_wall_with_buoyancy, color="red")
# plt.annotate(
#     "First wall", (t_both[-1], first_wall_both[-1]),
#     xytext=(t_both[-1]*1.1, first_wall_both[-1]), color='black')

# axs[-1].set_ylabel(r"Inventory (T m$^{-1}$)")

plt.xlabel(r"Time (days)")

for ax in [ax1, ax2, ax3, ax4]:
    plt.sca(ax)
    ax.get_shared_x_axes().join(ax, ax4)
    # plt.ylabel(r"Inventory (T m$^{-1}$)")  # "Inventory \n" + r"(T m$^{-1}$)"
    # plt.ylim(bottom=0)
    plt.yscale("log")
    # plt.xlim(left=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# remove the xticks for top plots
ax1.set_xticklabels([])
ax2.set_xticklabels([])
ax3.set_xticklabels([])

plt.tight_layout()

plt.show()
