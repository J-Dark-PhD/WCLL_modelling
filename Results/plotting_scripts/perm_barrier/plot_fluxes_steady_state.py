import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LogNorm
import numpy as np
from scipy.interpolate import interp1d

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=12)

red_W = (171/255, 15/255, 26/255)
grey_eurofer = (153/255, 153/255, 153/255)
green_lipb = (146/255, 196/255, 125/255)

# ##### reduction factor 1e2 - 1e7 ##### #

S_0_log_values = [
    2.4e23, 2.4e22, 2.4e21, 2.4e20, 2.4e19, 2.4e18, 2.4e17, 2.4e16]
S_0_log_ref = 2.4088e23
k_B = 8.6e-5
solubilities_log = np.array(S_0_log_values)*np.exp(-0.3026/k_B/600)
S_log_ref = S_0_log_ref*np.exp(-0.3026/k_B/600)


y_fw_cooling_log, y_BZ_cooling_log = [], []
folder = "../../parametric_studies/varying_perm_barrier"
for S_0_log in S_0_log_values:
    filename = folder + \
         "/S_0_eur={:.1e}/derived_quantities.csv".format(S_0_log)
    data = np.genfromtxt(filename, delimiter=",", names=True)
    y_fw_cooling_log.append(data['Flux_surface_39_solute']*-1)
    y_BZ_cooling_log.append(sum(
        [data['Flux_surface_{}_solute'.format(i)]*-1
         for i in range(40, 49)]))


plt.figure(figsize=[6.4, 3.8])
solubilities_log_normalised = S_log_ref/solubilities_log
x_annotation = solubilities_log_normalised[-1]*1.5

plt.plot(
    solubilities_log_normalised, y_fw_cooling_log/y_fw_cooling_log[0],
    label='FW cooling channel', color=grey_eurofer, marker="+")
plt.plot(
    solubilities_log_normalised, y_BZ_cooling_log/y_BZ_cooling_log[0],
    label='BZ Cooling', color=green_lipb, marker="+")

plt.annotate(
    "FW cooling \n channel", (x_annotation, (y_fw_cooling_log/y_fw_cooling_log[0])[-1]*0.6), color=grey_eurofer)
plt.annotate(
    "BZ Cooling", (x_annotation, (y_BZ_cooling_log/y_BZ_cooling_log[0])[-1]*0.6), color=green_lipb)

plt.xscale('log')
plt.yscale('log')
plt.xlim(1e0, 5e8)
plt.ylabel(r"Relative Surface Flux")
xlabel = "Reduction Factor"
plt.xlabel(xlabel)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()


# ##### Reduction factor 1 - 1000 (linear) ##### #

S_0_values = [
    2.4e23, 2.4e21, 1.2e21, 8.0e20, 6.0e20, 4.8e20,
    4.0e20, 3.4e20, 3.0e20, 2.7e20, 2.4e20]
S_0_ref = 2.4088e23
k_B = 8.6e-5
solubilities = np.array(S_0_values)*np.exp(-0.3026/k_B/600)
S_ref = S_0_ref*np.exp(-0.3026/k_B/600)


y_fw_cooling, y_BZ_cooling = [], []
folder = "../../parametric_studies/varying_perm_barrier"
for S_0 in S_0_values:
    filename = folder + "/S_0_eur={:.1e}/derived_quantities.csv".format(S_0)
    data = np.genfromtxt(filename, delimiter=",", names=True)
    y_fw_cooling.append(data['Flux_surface_39_solute'])
    y_BZ_cooling.append(sum(
        [data['Flux_surface_{}_solute'.format(i)]*-1
         for i in range(40, 49)]))


plt.figure(figsize=[6.4, 3.8])
solubilities_normalised = S_ref/solubilities

x_annotation = solubilities_normalised[-1]*1.02

plt.plot(
    solubilities_normalised, y_fw_cooling/y_fw_cooling[0],
    label='BZ pipes', color=grey_eurofer, marker="+")
plt.plot(
    solubilities_normalised, y_BZ_cooling/y_BZ_cooling[0],
    label='First wall', color=green_lipb, marker="+")


plt.annotate(
    "FW cooling \n channel", (x_annotation, (y_fw_cooling/y_fw_cooling[0])[-1]), color=grey_eurofer)
plt.annotate(
    "BZ Cooling", (x_annotation, (y_BZ_cooling/y_BZ_cooling[0])[-1]*0.8), color=green_lipb)

plt.yscale('log')
plt.xlim(0, 1150)
plt.ylabel(r"Relative Surface Flux")
xlabel = "Reduction Factor"
plt.xlabel(xlabel)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()

plt.show()
