import matplotlib.pyplot as plt
import numpy as np

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)

temp_range = np.linspace(569, 601, num=11)

T_pipes, T_structure, T_baffle = [], [], []
T_lipb, T_W = [], []
folder = "../../../../data/parametric_studies/varying_h_coeff/results/"
for temp in temp_range:
    filename = folder + "run_{:.1f}K/derived_quantities.csv".format(temp)
    data = np.genfromtxt(filename, delimiter=",", names=True)
    T_pipes_data = np.mean(
        [data["Maximum_T_volume_{}".format(i)] for i in range(10, 21)]
    )
    T_pipes.append(T_pipes_data)
    T_structure.append(data["Maximum_T_volume_7"])
    T_baffle.append(data["Maximum_T_volume_8"])
    T_lipb.append(data["Maximum_T_volume_6"])
    T_W.append(data["Maximum_T_volume_9"])

plt.figure()
plt.plot(temp_range, T_pipes, label="BZ Pipes")
plt.plot(temp_range, T_structure, label="Structure")
plt.plot(temp_range, T_baffle, label="Baffle plate")
plt.plot(temp_range, T_lipb, label="Breeding Zone")
plt.plot(temp_range, T_W, label="First Wall")
# plt.xscale("log")
# plt.yscale("log")
# plt.ylim(0, 2e19)
# plt.ylim(bottom=0)
plt.ylabel(r"Maximum temperture (K)")
plt.xlabel(r"Bulk coolant temperature (K)")
plt.legend()
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()


plt.show()
