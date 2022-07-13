import matplotlib.pyplot as plt
from matplotlib import cm, colors
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d
from matplotx import line_labels
import numpy as np
import sys

sys.path.append("../../../")
from parametric_study_varying_mass_flow import (
    mass_flow_range_bz,
    mass_flow_range_fw,
    temp_range,
    no_values,
    lower_bound,
    upper_bound,
)

bz_ids = range(28, 39)
fw_ids = range(24, 28)


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
    orig_cmap = cm.get_cmap("RdBu_r")
    shifted_cmap = shiftedColorMap(
        orig_cmap,
        midpoint=abs(0 - data.min()) / abs(data.max() - data.min()),
    )
    return shifted_cmap


def filename_from_T_flowrate(T, bz_flowrate, fw_flowrate):
    results_folder = "../../../../data/parametric_studies/varying_h_coeff/results/"
    filename = (
        results_folder
        + "bz_mass_flow={:.3e}_fw_mass_flow={:.3e}_T={:.1f}K/derived_quantities.csv".format(
            bz_flowrate, fw_flowrate, T
        )
    )
    return filename


def get_bz_flux(filename):
    data = np.genfromtxt(filename, delimiter=",", names=True)
    flux_value = sum([data["Flux_surface_{}_solute".format(i)] * -1 for i in bz_ids])
    return flux_value


def get_fw_flux(filename):
    data = np.genfromtxt(filename, delimiter=",", names=True)
    flux_value = sum([data["Flux_surface_{}_solute".format(i)] * -1 for i in fw_ids])
    return flux_value


def get_avg_T_bz(filename):
    data = np.genfromtxt(filename, delimiter=",", names=True)
    avg_T = np.mean([data["Average_T_surface_{}".format(i)] for i in bz_ids])
    return avg_T


def get_avg_T_fw(filename):
    data = np.genfromtxt(filename, delimiter=",", names=True)
    avg_T = np.mean([data["Average_T_surface_{}".format(i)] for i in fw_ids])
    return avg_T


def get_max_T_structure(filename):
    data = np.genfromtxt(filename, delimiter=",", names=True)
    max_T = data["Maximum_T_volume_7"]
    return max_T


def get_max_T_bz_pipes(filename):
    data = np.genfromtxt(filename, delimiter=",", names=True)
    T_values = np.array(
        [data["Maximum_T_volume_{}".format(i)] for i in np.arange(10, 21)]
    )
    max_T = T_values.max()
    return max_T


def get_data(T_range, bz_flow_range, fw_flow_range):
    bz_pipes_total_fluxes, fw_channels_total_fluxes = [], []
    bz_surf_temperature, fw_surf_temperature = [], []
    structure_max_temperature, bz_pipes_max_temperature = [], []
    for T in T_range:
        bz_flux_at_given_temperature = []
        fw_flux_at_given_temperature = []
        bz_avg_surface_temperature_at_given_temperature = []
        fw_avg_surface_temperature_at_given_temperature = []
        structure_max_temperature_at_given_temperature = []
        bz_pipes_max_temperature_at_given_temperature = []
        for mass_flow_bz, mass_flow_fw in zip(bz_flow_range, fw_flow_range):

            filename = filename_from_T_flowrate(T, mass_flow_bz, mass_flow_fw)
            bz_flux_at_given_temperature.append(get_bz_flux(filename))
            fw_flux_at_given_temperature.append(get_fw_flux(filename))
            bz_avg_surface_temperature_at_given_temperature.append(
                get_avg_T_bz(filename)
            )
            fw_avg_surface_temperature_at_given_temperature.append(
                get_avg_T_fw(filename)
            )
            structure_max_temperature_at_given_temperature.append(
                get_max_T_structure(filename)
            )
            bz_pipes_max_temperature_at_given_temperature.append(
                get_max_T_bz_pipes(filename)
            )
        bz_pipes_total_fluxes.append(bz_flux_at_given_temperature)
        fw_channels_total_fluxes.append(fw_flux_at_given_temperature)
        bz_surf_temperature.append(bz_avg_surface_temperature_at_given_temperature)
        fw_surf_temperature.append(fw_avg_surface_temperature_at_given_temperature)
        structure_max_temperature.append(structure_max_temperature_at_given_temperature)
        bz_pipes_max_temperature.append(bz_pipes_max_temperature_at_given_temperature)

    bz_pipes_total_fluxes = np.array(bz_pipes_total_fluxes)
    fw_channels_total_fluxes = np.array(fw_channels_total_fluxes)
    bz_surf_temperature = np.array(bz_surf_temperature)
    fw_surf_temperature = np.array(fw_surf_temperature)
    structure_max_temperature = np.array(structure_max_temperature)
    bz_pipes_max_temperature = np.array(bz_pipes_max_temperature)

    return (
        bz_pipes_total_fluxes,
        fw_channels_total_fluxes,
        bz_surf_temperature,
        fw_surf_temperature,
        structure_max_temperature,
        bz_pipes_max_temperature,
    )


def shaded_area(X, Y, Z, sampling_size=200):
    interpolated_z = interp2d(X, Y, Z)

    smooth_x = np.linspace(X.min(), X.max(), num=sampling_size)
    smooth_y = np.linspace(Y.min(), Y.max(), num=sampling_size)

    smooth_z = interpolated_z(smooth_x, smooth_y)

    smooth_xx, smooth_yy = np.meshgrid(smooth_x, smooth_y)

    indexes = np.where(smooth_z <= 823)  # criteria

    shaded_XX, shaded_YY, shaded_ZZ = (
        np.copy(smooth_xx),
        np.copy(smooth_yy),
        np.copy(smooth_z),
    )
    # remove values where criteria is not fulfilled
    shaded_XX[indexes] = np.nan
    shaded_YY[indexes] = np.nan
    shaded_ZZ[indexes] = np.nan

    return shaded_XX, shaded_YY, shaded_ZZ


# ##### PROCESS DATA ##### #
# compute for standard case
standard_results_file = (
    "../../../../data/parametric_studies/varying_h_coeff/results/"
    + "standard_case/derived_quantities.csv"
)

standard_bz_pipes_flux = get_bz_flux(standard_results_file)
standard_fw_channels_flux = get_fw_flux(standard_results_file)
standard_bz_surf_temperature = get_avg_T_bz(standard_results_file)
standard_fw_surf_temperature = get_avg_T_fw(standard_results_file)
standard_structure_max_temperature = get_max_T_structure(standard_results_file)
standard_bz_pipes_max_temperature = get_max_T_bz_pipes(standard_results_file)

(
    bz_pipes_total_fluxes,
    fw_channels_total_fluxes,
    bz_surf_temperature,
    fw_surf_temperature,
    structure_max_temperature,
    bz_pipes_max_temperature,
) = get_data(temp_range, mass_flow_range_bz, mass_flow_range_fw)
Z_bz_normalised = bz_pipes_total_fluxes / standard_bz_pipes_flux - 1
Z_fw_normalised = fw_channels_total_fluxes / standard_fw_channels_flux - 1
Z_bz_surf_temp_normalised = bz_surf_temperature / standard_bz_surf_temperature - 1
Z_fw_surf_temp_normalised = fw_surf_temperature / standard_fw_surf_temperature - 1
Z_structure_max_temp_normalised = (
    structure_max_temperature / standard_fw_surf_temperature
) - 1
Z_bz_pipes_max_temp_normalised = (
    bz_pipes_max_temperature / standard_bz_pipes_max_temperature
) - 1

# in %
Z_bz_normalised *= 100
Z_fw_normalised *= 100
Z_bz_pipes_max_temp_normalised *= 100
Z_structure_max_temp_normalised *= 100
Z_fw_surf_temp_normalised *= 100
Z_bz_surf_temp_normalised *= 100

# ##### PLOTTING ##### #

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

mass_flow_modification_range = np.linspace(lower_bound, upper_bound, num=no_values)

shifted_cmap_bz_flux = shifted_cmap(Z_bz_normalised)
shifted_cmap_fw_flux = shifted_cmap(Z_fw_normalised)
shifted_cmap_bz_temperature = shifted_cmap(Z_bz_surf_temp_normalised)
shifted_cmap_fw_temperature = shifted_cmap(Z_fw_surf_temp_normalised)

X, Y = np.meshgrid(mass_flow_modification_range, temp_range)
shaded_X, shaded_Y, shaded_Z = shaded_area(
    X, Y, structure_max_temperature, sampling_size=1000
)

# ##### MAX TEMPERATURE PLOTS ##### #

fig, ax = plt.subplots(figsize=[6, 4.5])
CS = ax.contourf(
    X,
    Y,
    structure_max_temperature,
    levels=1000,
    cmap="inferno",
)
for c in CS.collections:
    c.set_edgecolor("face")
CS2 = ax.contour(X, Y, structure_max_temperature, levels=[823], colors="white")
CS3 = ax.contour(X, Y, structure_max_temperature, levels=8, colors="white", alpha=0.5)
ax.clabel(CS2, inline=True, fontsize=10, fmt="%.0f")
ax.clabel(CS3, inline=True, fontsize=10, fmt="%.0f")

# contour shaded area
# CS4 = plt.contourf(
#     shaded_X,
#     shaded_Y,
#     shaded_Z,
#     levels=0,
#     colors="white",
#     alpha=0.6,
# )
# for c in CS4.collections:
#     c.set_edgecolor("face")

plt.scatter(1, 585, color="white", marker="*", s=10)
plt.colorbar(CS, label=r"Maximum temperature (K)", format="%.0f")
plt.xlabel(r"Mass flow rate modifcation factor")
plt.ylabel(r"Coolant bulk temperature (K)")
plt.title("Maximum temperature in structure")
plt.tight_layout()


fig, ax = plt.subplots(figsize=[6, 4.5])
CS = ax.contourf(
    X,
    Y,
    bz_pipes_max_temperature,
    levels=1000,
    cmap="inferno",
)
for c in CS.collections:
    c.set_edgecolor("face")
CS2 = ax.contour(X, Y, bz_pipes_max_temperature, levels=[823], colors="white")
CS3 = ax.contour(X, Y, bz_pipes_max_temperature, levels=8, colors="white", alpha=0.5)
ax.clabel(CS2, inline=True, fontsize=10, fmt="%.0f")
ax.clabel(CS3, inline=True, fontsize=10, fmt="%.0f")

# contour shaded area
# CS4 = plt.contourf(
#     shaded_X,
#     shaded_Y,
#     shaded_Z,
#     levels=1,
#     colors="white",
#     alpha=0.6,
# )
# for c in CS4.collections:
#     c.set_edgecolor("face")

plt.scatter(1, 585, color="white", marker="*", s=10)
plt.colorbar(CS, label=r"Average surface temperture (K)", format="%.0f")
plt.xlabel(r"Mass flow rate modifcation factor")
plt.ylabel(r"Coolant bulk temperature (K)")
plt.title("Maximum temperature in breeding zone pipes")
plt.tight_layout()

# ##### SURFACE FLUX PLOTS ##### #

fig, ax = plt.subplots(figsize=[6, 4.5])
CS = ax.contourf(
    X,
    Y,
    Z_bz_normalised,
    levels=1000,
    cmap=shifted_cmap_bz_flux,
)
for c in CS.collections:
    c.set_edgecolor("face")
CS2 = ax.contour(
    X, Y, Z_bz_normalised, levels=10, colors="black", linestyles="solid", alpha=0.5
)
plt.clabel(CS2, fmt="%.0f")

# contour shaded area
# CS4 = plt.contourf(
#     shaded_X,
#     shaded_Y,
#     shaded_Z,
#     levels=1,
#     colors="grey",
#     alpha=0.6,
# )
# for c in CS4.collections:
#     c.set_edgecolor("face")

# plt.scatter(X, Y, color="black", marker="x", s=9)
plt.scatter(1, 585, color="black", marker="x", s=10)
plt.colorbar(CS, label=r"Surface flux difference (\%)", format="%.1f ")
plt.xlabel(r"Mass flow rate modifcation factor")
plt.ylabel(r"Coolant bulk temperature (K)")
ax.set_title("Breeding Zone Pipes")
plt.tight_layout()

fig, ax = plt.subplots(figsize=[6, 4.5])
CS = ax.contourf(
    X,
    Y,
    Z_fw_normalised,
    levels=1000,
    cmap=shifted_cmap_fw_flux,
)
for c in CS.collections:
    c.set_edgecolor("face")
CS2 = ax.contour(
    X, Y, Z_fw_normalised, levels=10, colors="black", linestyles="solid", alpha=0.5
)
plt.clabel(CS2, fmt="%.0f")

# contour shaded area
# CS4 = plt.contourf(
#     shaded_X,
#     shaded_Y,
#     shaded_Z,
#     levels=1,
#     colors="grey",
#     alpha=0.6,
# )
# for c in CS4.collections:
#     c.set_edgecolor("face")

# plt.scatter(X, Y, color="black", marker="x", s=9)
plt.scatter(1, 585, color="black", marker="x", s=10)
cb = plt.colorbar(CS, label=r"Surface flux difference (\%)", format="%.1f")
plt.xlabel(r"Mass flow rate modifcation factor")
plt.ylabel(r"Coolant bulk temperature (K)")
ax.set_title("First Wall Channels")
plt.tight_layout()

# ##### AVERAGE SURFACE TEMPERATURE PLOTS ##### #

fig, ax = plt.subplots(figsize=[6, 4.5])
CS = ax.contourf(
    X,
    Y,
    Z_bz_surf_temp_normalised,
    levels=1000,
    cmap=shifted_cmap_bz_temperature,
)
for c in CS.collections:
    c.set_edgecolor("face")
CS2 = ax.contour(
    X,
    Y,
    Z_bz_surf_temp_normalised,
    levels=10,
    colors="black",
    linestyles="solid",
    alpha=0.5,
)
plt.clabel(CS2, fmt="%.0f")

# contour shaded area
# CS4 = plt.contourf(
#     shaded_X,
#     shaded_Y,
#     shaded_Z,
#     levels=1,
#     colors="grey",
#     alpha=0.6,
# )
# for c in CS4.collections:
#     c.set_edgecolor("face")

plt.scatter(1, 585, color="black", marker="x", s=10)
# plt.scatter(X, Y, color="black", marker="x", s=9)
plt.colorbar(CS, label=r"Average surface temperture difference (\%)", format="%.1f")
plt.xlabel(r"Mass flow rate modifcation factor")
plt.ylabel(r"Coolant bulk temperature (K)")
ax.set_title("Breeding Zone Pipes")
plt.tight_layout()

fig, ax = plt.subplots(figsize=[6, 4.5])
CS = ax.contourf(
    X,
    Y,
    Z_fw_surf_temp_normalised,
    levels=1000,
    cmap=shifted_cmap_fw_temperature,
)
for c in CS.collections:
    c.set_edgecolor("face")
CS2 = ax.contour(
    X,
    Y,
    Z_fw_surf_temp_normalised,
    levels=10,
    colors="black",
    linestyles="solid",
    alpha=0.5,
)
plt.clabel(CS2, fmt="%.0f")

# contour shaded area
# CS4 = plt.contourf(
#     shaded_X,
#     shaded_Y,
#     shaded_Z,
#     levels=1,
#     colors="grey",
#     alpha=0.6,
# )
# for c in CS4.collections:
#     c.set_edgecolor("face")

plt.scatter(1, 585, color="black", marker="x", s=10)
# plt.scatter(X, Y, color="black", marker="x", s=9)
plt.colorbar(CS, label=r"Average surface temperture difference (\%)", format="%.1f")
plt.xlabel(r"Mass flow rate modifcation factor")
plt.ylabel(r"Coolant bulk temperature (K)")
ax.set_title("First Wall Channels")
plt.tight_layout()

# ##### SHOW PLOTS ##### #

plt.show()
