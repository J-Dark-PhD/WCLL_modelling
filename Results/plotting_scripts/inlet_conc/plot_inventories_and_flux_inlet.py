import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LogNorm
import numpy as np
from scipy.interpolate import interp1d

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)

red_W = (171/255, 15/255, 26/255)
grey_eurofer = (153/255, 153/255, 153/255)
green_lipb = (146/255, 196/255, 125/255)

# ##### Final values ##### #

# eta_values = [np.linspace(0, 1, num=11)]
eta_values = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]

y_first_wall, y_pipes, y_structure, y_lipb, y_fw_flux, y_pipes_flux = [], [], [], [], [], []
y_front_pipes, y_mid_pipes, y_rear_pipes = [], [], []
y_outlet = []
folder = "../../parametric_studies/varying_inlet_conc"
for eta in eta_values:
    filename = folder + "/eta={:.2f}/derived_quantities.csv".format(eta)
    data = np.genfromtxt(filename, delimiter=",", names=True)
    # Inventories
    y_first_wall.append(data['Total_retention_volume_7'])
    y_lipb.append(data['Total_solute_volume_6'])
    y_pipes.append(sum(
        [data['Total_retention_volume_{}'.format(i)]
         for i in range(10, 20)]))
    y_structure.append(
        data['Total_retention_volume_8'] + data['Total_retention_volume_9'])
    # fluxes
    y_fw_flux.append(data['Flux_surface_39_solute']*-1)
    y_pipes_flux.append(sum(
        [data['Flux_surface_{}_solute'.format(i)]*-1
         for i in range(40, 49)]))
    y_front_pipes.append(sum(
        [data['Flux_surface_40_solute']*-1 + data['Flux_surface_44_solute']*-1 + \
            data['Flux_surface_46_solute']*-1]))
    y_mid_pipes.append(sum(
        [data['Flux_surface_41_solute']*-1 + data['Flux_surface_45_solute']*-1 + \
            data['Flux_surface_47_solute']*-1]))
    y_rear_pipes.append(sum(
        [data['Flux_surface_42_solute']*-1 + data['Flux_surface_43_solute']*-1 + \
            data['Flux_surface_48_solute']*-1 + data['Flux_surface_49_solute']*-1]))
    # Outlet
    y_outlet.append(data['Total_solute_surface_21'])


# ##########
# Inventories
# ##########

plt.figure()
x_values = np.array(eta_values)

plt.plot(
    x_values, y_lipb,
    label='LiPb', color=green_lipb, marker="+")
plt.plot(
    x_values, y_pipes,
    label='BZ pipes', color=grey_eurofer, marker="+")
plt.plot(
    x_values, y_structure,
    label='Structure', color=grey_eurofer, marker="+")
plt.plot(
    x_values, y_first_wall,
    label='First wall', color=red_W, marker="+")

plt.annotate(
    "BZ pipes", (0.8, 3e19), color=grey_eurofer)
plt.annotate(
    "Structure", (0.8, 5e20), color=grey_eurofer)
plt.annotate(
    "First wall", (0.8, 5e17), color=red_W)
plt.annotate(
    "LiPb", (0.8, 2e22), color=green_lipb)

# plt.xscale('log')
plt.yscale('log')
plt.ylabel(r"Inventory (T m$^{-1}$)")
xlabel = "Proportion of T re-entering the BB"
plt.xlabel(xlabel)
plt.xlim(left=0)
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()

# ##########
# Fluxes
# ##########

plt.figure()
x_values = np.array(eta_values)

plt.plot(
    x_values, y_fw_flux,
    label='FW', color='black', marker="+")
# plt.plot(
#     x_values, y_pipes_flux,
#     label='BZ Pipes', color=green_lipb, marker="+")
plt.plot(
    x_values, y_front_pipes,
    label='Front BZ Pipes', color='forestgreen', marker="+")
plt.plot(
    x_values, y_mid_pipes,
    label='Middle BZ Pipes', color='purple', marker="+")
plt.plot(
    x_values, y_rear_pipes,
    label='Rear BZ Pipes', color='steelblue', marker="+")

plt.annotate(
    "FW Cooling Channels", (0.05, 5e15), color='black')
plt.annotate(
    "Front BZ Pipes", (0.05, 1.5e16), color='forestgreen')
plt.annotate(
    "Middle BZ Pipes", (0.05, 9e15), color='purple')
plt.annotate(
    "Rear BZ Pipes", (0.05, 1.8e15), color='steelblue')

# plt.legend()
plt.yscale('log')
plt.ylabel(r"Surface flux (T m$^{-1}$ s$^{-1}$)")
xlabel = "Proportion of T re-entering the BB"
plt.xlabel(xlabel)
plt.xlim(left=0)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()

# ##########
# outlet
# ##########

plt.figure()
x_values = np.array(eta_values)

plt.plot(
    x_values, y_outlet,
    label='FW', color='black', marker="+")
plt.annotate(
    "Outlet", (0.8, 2e22), color='black')

plt.yscale('log')

plt.ylabel(r"Solute (T m$^{-2}$)")
xlabel = "Proportion of T re-entering the BB"
plt.xlabel(xlabel)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()

plt.show()
