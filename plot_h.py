from h_evaluator import para_h_bz, para_h_fw
import numpy as np
import matplotlib.pyplot as plt

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

# temp_range = np.linspace(569, 602, num=100)

temp = 569
print("bz = ", para_h_bz(temp), ". fw = ", para_h_fw(temp))

quit()
h_bz_values = []
h_fw_values = []
for temp in temp_range:
    h_bz = para_h_bz(temp)
    h_fw = para_h_fw(temp)
    h_bz_values.append(h_bz)
    h_fw_values.append(h_fw)

plt.figure()
plt.plot(temp_range, h_bz_values, label="bz pipes")
plt.plot(temp_range, h_fw_values, label="fw channels")
plt.ylabel(r"Heat transfer coefficient (T m$^{-2}$K$^{-1}$)")
plt.xlabel(r"Coolant temperature (K)")
plt.ylim(bottom=0)
plt.legend()
ax = plt.gca()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

bz_diff = ((h_bz_values[-1] - h_bz_values[0]) / h_bz_values[0]) * 100
fw_diff = ((h_fw_values[-1] - h_fw_values[0]) / h_fw_values[0]) * 100
print("Difference in bz pipes = {:.1f} %".format(bz_diff))
print("Difference in fw_channels = {:.1f} %".format(fw_diff))
plt.show()
