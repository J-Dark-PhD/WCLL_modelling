import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LogNorm
import numpy as np
from scipy.interpolate import interp1d

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=12)

red_W = (171/255, 15/255, 26/255)

dark_factor = 0.8
grey_eurofer = (
    dark_factor*153/255,
    dark_factor*153/255,
    dark_factor*153/255)
green_lipb = (
    dark_factor*146/255,
    dark_factor*196/255,
    dark_factor*125/255)


# ##### Final values ##### #

S_0_values = [
    2.0e21, 3.9e21, 7.5e21, 1.5e22, 2.8e22, 5.5e22, 1.1e23, 2.1e23, 4.0e23]
S_0_ref = 1.427e23
k_B = 8.6e-5
solubilities = np.array(S_0_values)*np.exp(-0.133/k_B/600)
S_ref = S_0_ref*np.exp(-0.133/k_B/600)


y_first_wall, y_pipes, y_structure, y_lipb = [], [], [], []
folder = "../../parametric_studies/varying_lipb_S_0"
for S_0 in S_0_values:
    filename = folder + "/S_0={:.1e}/derived_quantities.csv".format(S_0)
    data = np.genfromtxt(filename, delimiter=",", names=True)
    y_first_wall.append(data['Total_retention_volume_7'])
    y_pipes.append(sum(
        [data['Total_retention_volume_{}'.format(i)]
         for i in range(10, 20)]))
    y_structure.append(
        data['Total_retention_volume_8'] + data['Total_retention_volume_9'])
    y_lipb.append(data['Total_solute_volume_6'])


# All in one plot version
plt.figure()
solubilities_normalised = solubilities/S_ref
total = np.array(y_pipes) + np.array(y_structure) + \
    np.array(y_first_wall) + np.array(y_lipb)
x_annotation = solubilities_normalised[-1]*1.15

plt.plot(
    solubilities_normalised, y_pipes,
    label='BZ pipes', color=grey_eurofer, marker="+")
plt.plot(
    solubilities_normalised, y_structure,
    label='Structure', color=grey_eurofer, marker="+")
plt.plot(
    solubilities_normalised, y_first_wall,
    label='First wall', color=red_W, marker="+")
plt.plot(
    solubilities_normalised, y_lipb,
    label='LiPb', color=green_lipb, marker="+")
# plt.plot(
#     solubilities_normalised, total,
#     label='Total', color='black', marker="+")

plt.annotate(
    "BZ pipes", (x_annotation, y_pipes[-1]*1), color=grey_eurofer)
plt.annotate(
    "Structure", (x_annotation, y_structure[-1]*0.9), color=grey_eurofer)
plt.annotate(
    "First wall", (x_annotation, y_first_wall[-1]*1.1), color=red_W)
# plt.annotate("Total", (x_annotation, total[-1]*1.05), color="black")
plt.annotate("LiPb", (x_annotation, y_lipb[-1]*1.1), color=green_lipb)

plt.vlines(1, 0, 1e22, color='black', linestyle='dashed')
plt.annotate('Standard \n case', (0.4, 1e21), color='black')

plt.xscale('log')
plt.yscale('log')
# plt.ylim(0, 2e19)
# plt.ylim(1e17, 2e19)
plt.ylabel(r"Inventory (T m$^{-1}$)")
xlabel = "Normalised LiPb solubility" + \
    r" $K_S$(600)/$K_{S-SC}$(600)"
plt.xlabel(xlabel)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.show()
