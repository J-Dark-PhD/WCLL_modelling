import matplotlib.pyplot as plt
from matplotlib import cm, colors
import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy.interpolate import RectBivariateSpline
from shaded_area import shaded_area

sys.path.append("../../../")
from h_evaluator import (
    para_h_fw,
    para_flow_velocity_fw,
)

no_values = 11
lower_bound = 0.1
upper_bound = 1.9
temp_range = np.linspace(569, 601, num=no_values)
mass_flow_range_fw = 0.63189 * np.linspace(lower_bound, upper_bound, num=no_values)

bz_ids = range(28, 39)
fw_ids = range(24, 28)
results_folder = "../../parametric_studies/varying_h_coeff/results/"


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


def get_data(T_range, fw_flow_range):
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
        for mass_flow_fw in fw_flow_range:
            mass_flow_bz = 0.85491
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


def h_coeff_fw(mass_flow_rate):
    T_standard = 585
    vel = para_flow_velocity_fw(mass_flow_rate)
    h = para_h_fw(T=T_standard, u=vel)
    return h


# ##### PROCESS DATA ##### #
# compute for standard case
standard_results_file = results_folder + "standard_case/derived_quantities.csv"

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
) = get_data(temp_range, mass_flow_range_fw)
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

shifted_cmap_bz_flux = shifted_cmap(Z_bz_normalised)
shifted_cmap_fw_flux = shifted_cmap(Z_fw_normalised)
shifted_cmap_bz_temperature = shifted_cmap(Z_bz_surf_temp_normalised)
shifted_cmap_fw_temperature = shifted_cmap(Z_fw_surf_temp_normalised)

X, Y = np.meshgrid(mass_flow_range_fw, temp_range)
# method for plotting contour of interpolated results
# interpolated_z = RectBivariateSpline(
#     mass_flow_range_fw, temp_range, structure_max_temperature
# )
# smooth_x = np.linspace(mass_flow_range_fw.min(), mass_flow_range_fw.max(), num=1000)
# smooth_y = np.linspace(temp_range.min(), temp_range.max(), num=1000)
# structure_max_temperature_smooth = interpolated_z(smooth_x, smooth_y)

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
CS3 = ax.contour(
    X,
    Y,
    structure_max_temperature,
    levels=8,
    colors="white",
    alpha=0.5,
)

# contour shaded area
# shaded_area(
#     mass_flow_range_fw,
#     temp_range,
#     structure_max_temperature,
#     min_value=823,
#     alpha=0.6,
#     color="white",
#     sampling_size=1000,
# )

ax.clabel(CS2, inline=True, fontsize=10, fmt="%.0f")
ax.clabel(CS3, inline=True, fontsize=10, fmt="%.0f")
plt.scatter(0.63189, 585, color="white", marker="*", s=10)
plt.colorbar(CS, label=r"Maximum temperature (K)", format="%.0f")
ax.set_xlabel(r"FW mass flow rate (kg s$^{-1}$)")
ax.set_ylabel(r"Coolant bulk temperature (K)")
ax_1_ticks = ax.get_xticks()[:-1]
ax2 = ax.twiny()
h_min, h_max = (
    h_coeff_fw(ax.get_xlim()[0]),
    h_coeff_fw(ax.get_xlim()[1]),
)
ax2.set_xlim(h_min, h_max)
ax2.set_xlabel("Heat transfer coefficient at 585K (W m$^{-2}$ K$^{-1}$)")
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
CS3 = ax.contour(X, Y, bz_pipes_max_temperature, levels=8, colors="white", alpha=0.5)

# contour shaded area
# shaded_area(
#     mass_flow_range_fw,
#     temp_range,
#     structure_max_temperature,
#     min_value=823,
#     alpha=0.6,
#     color="white",
#     sampling_size=1000,
# )

ax.clabel(CS2, inline=True, fontsize=10, fmt="%.0f")
ax.clabel(CS3, inline=True, fontsize=10, fmt="%.0f")
plt.scatter(0.63189, 585, color="white", marker="*", s=10)
plt.colorbar(CS, label=r"Average surface temperture (K)", format="%.0f")
ax.set_xlabel(r"FW mass flow rate (kg s$^{-1}$)")
ax.set_ylabel(r"Coolant bulk temperature (K)")
ax_1_ticks = ax.get_xticks()[:-1]
ax2 = ax.twiny()
h_min, h_max = (
    h_coeff_fw(ax.get_xlim()[0]),
    h_coeff_fw(ax.get_xlim()[1]),
)
ax2.set_xlim(h_min, h_max)
ax2.set_xlabel("Heat transfer coefficient at 585K (W m$^{-2}$ K$^{-1}$)")
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

# contour shaded area
# shaded_area(
#     mass_flow_range_fw,
#     temp_range,
#     structure_max_temperature,
#     min_value=823,
#     alpha=0.6,
#     color="grey",
#     sampling_size=1000,
# )

plt.clabel(CS2, fmt="%.0f")
# plt.scatter(X, Y, color="black", marker="*", s=9)
plt.scatter(0.63189, 585, color="black", marker="*", s=10)
plt.colorbar(CS, label=r"Surface flux difference (\%)", format="%.1f ")
ax.set_xlabel(r"FW mass flow rate (kg s$^{-1}$)")
ax.set_ylabel(r"Coolant bulk temperature (K)")
ax_1_ticks = ax.get_xticks()[:-1]
ax2 = ax.twiny()
h_min, h_max = (
    h_coeff_fw(ax.get_xlim()[0]),
    h_coeff_fw(ax.get_xlim()[1]),
)
ax2.set_xlim(h_min, h_max)
ax2.set_xlabel("Heat transfer coefficient at 585K (W m$^{-2}$ K$^{-1}$)")
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

# contour shaded area
# shaded_area(
#     mass_flow_range_fw,
#     temp_range,
#     structure_max_temperature,
#     min_value=823,
#     alpha=0.6,
#     color="grey",
#     sampling_size=1000,
# )

plt.clabel(CS2, fmt="%.0f")
# plt.scatter(X, Y, color="black", marker="*", s=9)
plt.scatter(0.63189, 585, color="black", marker="*", s=10)
cb = plt.colorbar(CS, label=r"Surface flux difference (\%)", format="%.1f")
ax.set_xlabel(r"FW mass flow rate (kg s$^{-1}$)")
ax.set_ylabel(r"Coolant bulk temperature (K)")
ax_1_ticks = ax.get_xticks()[:-1]
ax2 = ax.twiny()
h_min, h_max = (
    h_coeff_fw(ax.get_xlim()[0]),
    h_coeff_fw(ax.get_xlim()[1]),
)
ax2.set_xlim(h_min, h_max)
ax2.set_xlabel("Heat transfer coefficient at 585K (W m$^{-2}$ K$^{-1}$)")
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

# contour shaded area
# shaded_area(
#     mass_flow_range_fw,
#     temp_range,
#     structure_max_temperature,
#     min_value=823,
#     alpha=0.6,
#     color="grey",
#     sampling_size=1000,
# )

plt.clabel(CS2, fmt="%.1f")
plt.scatter(0.63189, 585, color="black", marker="*", s=10)
# plt.scatter(X, Y, color="black", marker="*", s=9)
plt.colorbar(CS, label=r"Average surface temperture difference (\%)", format="%.1f")
ax.set_xlabel(r"FW mass flow rate (kg s$^{-1}$)")
ax.set_ylabel(r"Coolant bulk temperature (K)")
ax_1_ticks = ax.get_xticks()[:-1]
ax2 = ax.twiny()
h_min, h_max = (
    h_coeff_fw(ax.get_xlim()[0]),
    h_coeff_fw(ax.get_xlim()[1]),
)
ax2.set_xlim(h_min, h_max)
ax2.set_xlabel("Heat transfer coefficient at 585K (W m$^{-2}$ K$^{-1}$)")
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

# contour shaded area
# shaded_area(
#     mass_flow_range_fw,
#     temp_range,
#     structure_max_temperature,
#     min_value=823,
#     alpha=0.6,
#     color="grey",
#     sampling_size=1000,
# )

plt.clabel(CS2, fmt="%.0f")
plt.scatter(0.63189, 585, color="black", marker="*", s=10)
# plt.scatter(X, Y, color="black", marker="*", s=9)
plt.colorbar(CS, label=r"Average surface temperture difference (\%)", format="%.1f")
ax.set_xlabel(r"FW mass flow rate (kg s$^{-1}$)")
ax.set_ylabel(r"Coolant bulk temperature (K)")
ax_1_ticks = ax.get_xticks()[:-1]
ax2 = ax.twiny()
h_min, h_max = (
    h_coeff_fw(ax.get_xlim()[0]),
    h_coeff_fw(ax.get_xlim()[1]),
)
ax2.set_xlim(h_min, h_max)
ax2.set_xlabel("Heat transfer coefficient at 585K (W m$^{-2}$ K$^{-1}$)")
plt.tight_layout()

plt.show()
