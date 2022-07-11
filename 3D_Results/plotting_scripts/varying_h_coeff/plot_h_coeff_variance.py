import matplotlib.pyplot as plt
from matplotlib import cm, colors
import matplotlib.pyplot as plt
import numpy as np
import sys

sys.path.append("../../../")
from h_evaluator import (
    para_h_bz,
    para_h_fw,
    para_flow_velocity_bz,
    para_flow_velocity_fw,
)
from parametric_study_varying_mass_flow import (
    mass_flow_range_bz,
    mass_flow_range_fw,
    temp_range,
    no_values,
    lower_bound,
    upper_bound,
)


def shiftedColorMap(cmap, start=0, midpoint=0.5, stop=1, name="shiftedcmap"):
    """
    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero.

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower offset). Should be between
          0.0 and `midpoint`.
      midpoint : The new center of the colormap. Defaults to
          0.5 (no shift). Should be between 0.0 and 1.0. In
          general, this should be  1 - vmax / (vmax + abs(vmin))
          For example if your data range from -15.0 to +5.0 and
          you want the center of the colormap at 0.0, `midpoint`
          should be set to  1 - 5/(5 + 15)) or 0.75
      stop : Offset from highest point in the colormap's range.
          Defaults to 1.0 (no upper offset). Should be between
          `midpoint` and 1.0.
    """
    cdict = {"red": [], "green": [], "blue": [], "alpha": []}

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack(
        [
            np.linspace(0.0, midpoint, 128, endpoint=False),
            np.linspace(midpoint, 1.0, 129, endpoint=True),
        ]
    )

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict["red"].append((si, r, r))
        cdict["green"].append((si, g, g))
        cdict["blue"].append((si, b, b))
        cdict["alpha"].append((si, a, a))

    newcmap = colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap


def shifted_cmap(data):
    orig_cmap = cm.get_cmap("viridis_r")
    # orig_cmap = cm.viridis
    shifted_cmap = shiftedColorMap(
        orig_cmap,
        midpoint=abs(0 - data.min()) / abs(data.max() - data.min()),
    )
    return shifted_cmap


def get_H_values(T_range, fw_flow_range, bz_flow_range):
    H_bz, H_fw = [], []
    for T in T_range:
        H_bz_at_given_temperature = []
        H_fw_at_given_temperature = []
        for mass_flow_fw, mass_flow_bz in zip(fw_flow_range, bz_flow_range):
            u_bz = para_flow_velocity_bz(mass_flow_bz)
            u_fw = para_flow_velocity_fw(mass_flow_fw)

            H_bz_at_given_temperature.append(para_h_bz(T, u=u_bz))
            H_fw_at_given_temperature.append(para_h_fw(T, u=u_fw))

        H_bz.append(H_bz_at_given_temperature)
        H_fw.append(H_fw_at_given_temperature)

    H_bz = np.array(H_bz)
    H_fw = np.array(H_fw)

    return H_bz, H_fw


# Process data
# compute for standard case
T_standard = 585
mass_flow_bz_standard = 0.85491
mass_flow_fw_standard = 0.63189
u_bz_standard = para_flow_velocity_bz(mass_flow_bz_standard)
u_fw_standard = para_flow_velocity_fw(mass_flow_fw_standard)
H_bz_standard = para_h_bz(T=T_standard, u=u_bz_standard)
H_fw_standard = para_h_fw(T=T_standard, u=u_fw_standard)

H_bz, H_fw = get_H_values(temp_range, mass_flow_range_fw, mass_flow_range_bz)

Z_bz_normalised = H_bz / H_bz_standard - 1
Z_fw_normalised = H_fw / H_fw_standard - 1


# in %
Z_bz_normalised *= 100
Z_fw_normalised *= 100

# PLOTTING

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

shifted_cmap_bz = shifted_cmap(Z_bz_normalised)
shifted_cmap_fw = shifted_cmap(Z_fw_normalised)

mass_flow_modification_range = np.linspace(lower_bound, upper_bound, num=no_values)

X_bz, Y = np.meshgrid(mass_flow_range_bz, temp_range)
X_fw, Y = np.meshgrid(mass_flow_range_fw, temp_range)
X, Y = np.meshgrid(mass_flow_modification_range, temp_range)

fig, ax = plt.subplots()
CS = ax.contourf(
    X_bz,
    Y,
    H_bz,
    levels=1000,
    cmap="viridis",
)
for c in CS.collections:
    c.set_edgecolor("face")
CS2 = ax.contour(
    X_bz, Y, H_bz, levels=10, colors="black", linestyles="solid", alpha=0.5
)
plt.clabel(CS2, fmt="%.0f")
# plt.scatter(X, Y, color="black", marker="x", s=9)
plt.scatter(0.85491, 585, color="white", marker="*", zorder=2, s=10)
plt.colorbar(
    CS, label=r"Heat transfer coefficient (W m$^{-2}$ K$^{-1}$)", format="%.0f"
)
plt.xlabel(r"BZ mass flow rate (kg s$^{-1}$)")
plt.ylabel(r"Coolant bulk temperature (K)")
ax.set_title("Breeding Zone Pipes")
plt.tight_layout()

fig, ax = plt.subplots()
CS = ax.contourf(
    X_fw,
    Y,
    H_fw,
    levels=1000,
    cmap="viridis",
)
for c in CS.collections:
    c.set_edgecolor("face")
CS2 = ax.contour(
    X_fw, Y, H_fw, levels=10, colors="black", linestyles="solid", alpha=0.5
)
plt.clabel(CS2, fmt="%.0f")
# plt.scatter(X, Y, color="black", marker="x", s=9)
plt.scatter(0.63189, 585, color="white", marker="*", zorder=2, s=10)
plt.colorbar(
    CS, label=r"Heat transfer coefficient (W m$^{-2}$ K$^{-1}$)", format="%.0f"
)
plt.xlabel(r"FW mass flow rate (kg s$^{-1}$)")
plt.ylabel(r"Coolant bulk temperature (K)")
ax.set_title("FW cooling channels")
plt.tight_layout()


fig, ax = plt.subplots()
plt.scatter(X, Y, color="black", marker="x", s=9)
plt.scatter(1, 585, color="red", marker="*", zorder=2, s=50)
plt.xlabel(r"Mass flow rate modification factor")
plt.ylabel(r"Coolant bulk temperature (K)")
plt.tight_layout()

plt.show()
