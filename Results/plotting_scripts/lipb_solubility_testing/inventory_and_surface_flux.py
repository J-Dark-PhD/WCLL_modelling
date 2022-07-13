import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import FormatStrFormatter
from matplotlib.colors import LogNorm, ListedColormap
import numpy as np

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=12)

fig, axs = plt.subplots(2, 2, sharex=True, sharey='row', figsize=(10, 6.4))
time_dict = {}
pipes_inv_dict = {}
pipes_flux_dict = {}
structure_dict = {}
baffle_dict = {}
FW_channels_dict = {}


def S(S_0):
    k_B = 8.6e-5
    E_S = 0.133
    T = 600
    return S_0*np.exp(-E_S/k_B/T)


S_0_values = [
    2.0e21, 3.9e21, 7.5e21, 1.5e22, 2.8e22, 5.5e22, 1.1e23, 2.1e23, 4.0e23]
S_values = S(np.array(S_0_values))

folder = "../../parametric_studies/varying_lipb_S_0/transient"
for S_0 in S_0_values:
    filename = folder + "/S_0={:.1e}/derived_quantities.csv".format(S_0)
    data = np.genfromtxt(filename, delimiter=",", names=True)
    time_dict[S_0] = data['ts']/86400
    pipes_inv_dict[S_0] = \
        sum([data['Total_retention_volume_{}'.format(i)]
             for i in range(10, 20)])
    pipes_flux_dict[S_0] = \
        sum([data['Flux_surface_{}_solute'.format(i)]*-1
             for i in range(40, 50)])
    structure_dict[S_0] = data['Total_retention_volume_8']
    baffle_dict[S_0] = data['Total_retention_volume_9']
    FW_channels_dict[S_0] = data['Flux_surface_39_solute']*-1

k_B = 8.6e-5
S_values = np.array(S_0_values)*np.exp(-0.133/k_B/600)

norm = LogNorm(vmin=min(S_values), vmax=max(S_values))
colorbar = cm.Blues(np.linspace(0, 1, 200))
# needed to avoidhaving white lines
colorbar = ListedColormap(colorbar[50:, :-1])
# https://stackoverflow.com/questions/51034408/how-to-make-the-color-of-one-end-of-colorbar-darker-in-matplotlib
sm = plt.cm.ScalarMappable(cmap=colorbar, norm=norm)

colours = [colorbar(norm(S_value)) for S_value in S_values]

# ##### Inventories ##### #
# structure
plt.sca(axs[0, 0])
max_inv = float("-inf")
min_inv = float("inf")
for S_0, colour in zip(S_0_values, colours):
    t = time_dict[S_0]
    structure = structure_dict[S_0] + baffle_dict[S_0]
    max_inv = max(max_inv, structure[-1])
    min_inv = min(min_inv, structure[-1])
    plt.plot(t, structure, color=colour)
print('max_inv/min_inv FW cooling channels = {}'.format(max_inv/min_inv))

plt.ylabel(r"Inventory (T m$^{-1}$)")
plt.annotate(r"Structure", (3, 3e19))

# BZ Pipes
plt.sca(axs[0, 1])
max_inv = float("-inf")
min_inv = float("inf")
for S_0, colour in zip(S_0_values, colours):
    t = time_dict[S_0]
    pipes_inv = pipes_inv_dict[S_0]
    max_inv = max(max_inv, pipes_inv[-1])
    min_inv = min(min_inv, pipes_inv[-1])
    plt.plot(t, pipes_inv, color=colour)
    x_ticks = np.linspace(1, 15, num=8, endpoint=True)
print('max_inv/min_inv FW cooling channels = {}'.format(max_inv/min_inv))
axs[0, 1].set_xticks([0] + x_ticks.tolist())
axs[0, 1].xaxis.set_major_formatter(FormatStrFormatter('%.f'))
plt.annotate(r"BZ pipes", (3, 4e19))

for ax in [axs[0, 0], axs[0, 1]]:
    plt.sca(ax)
    plt.yscale("log")
    plt.ylim(bottom=1e18, top=5e21)
    plt.xlim(left=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


# ##### Surface Flux ##### #
# FW Cooling Channels
plt.sca(axs[1, 0])
max_flux = float("-inf")
min_flux = float("inf")
for S_0, colour in zip(S_0_values, colours):
    t = time_dict[S_0]
    fw_flux = FW_channels_dict[S_0]
    max_flux = max(max_flux, fw_flux[-1])
    min_flux = min(min_flux, fw_flux[-1])
    plt.plot(t, fw_flux, color=colour)

print('max_flux/min_flux FW cooling channels = {}'.format(max_flux/min_flux))
plt.ylabel(r"Surface flux (T m$^{-1}$s$^{-1}$)")
plt.xlabel(r"Time (days)")
plt.annotate(r"FW channels", (3, 1.5e16))

# BZ pipes coolant surface
plt.sca(axs[1, 1])
max_flux = float("-inf")
min_flux = float("inf")
for S_0, colour in zip(S_0_values, colours):
    t = time_dict[S_0]
    pipes_flux = pipes_flux_dict[S_0]
    max_flux = max(max_flux, pipes_flux[-1])
    min_flux = min(min_flux, pipes_flux[-1])
    plt.plot(t, pipes_flux, color=colour)

print('max_flux/min_flux BZ cooling channels = {}'.format(max_flux/min_flux))

x_ticks = np.linspace(1, 15, num=8, endpoint=True)
plt.xlabel(r"Time (days)")
plt.annotate(r"BZ cooling channels", (3, 6e15))

for ax in [axs[1, 0], axs[1, 1]]:
    plt.sca(ax)
    plt.yscale("log")
    plt.ylim(bottom=1e15, top=5e16)
    plt.xlim(left=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.subplots_adjust(wspace=0.112, hspace=0.071)
cb = plt.colorbar(
    sm, ax=axs,
    label=r"$K_{S_\mathrm{LiPb}}$(600 K) (m$^{-3}$ Pa$^{-0.5}$)")
# plt.tight_layout()
plt.show()
