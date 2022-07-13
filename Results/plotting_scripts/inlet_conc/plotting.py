import matplotlib.pyplot as plt
import numpy as np

# data_inlet_av = [0.00E+00, 1.68E+20, 8.77E+20, 1.85E+21, 2.94E+21, 4.16E+21]
data_inlet_av = [100, 99, 95, 90, 85, 80]
data_outlet_av = [1.67E+22, 1.68E+22, 1.75E+22, 1.85E+22, 1.96E+22, 2.08E+22]
x = np.linspace(0,100,100)
m = -2.2e+20
c = 3.84e+22
a = 0.9892
b = 1.67+22
eta = np.linspace(0,1,100)

c_m = b/(1-(a*eta))
y = m*x + c

plt.figure()
# plt.plot(data_inlet_av, data_outlet_av)
# plt.plot(x, y)
plt.plot(c_m, eta)

# plt.xlabel(r"Average inlet conc (T m$^{-3}$)")
plt.xlabel(r"Tritium removed from system (%)")
plt.ylabel(r"Average outlet conc (T m$^{-3}$)")
plt.grid()
# plt.ylim(0, 2.5e22)
# plt.yscale('log')
plt.xlim(left=0)
plt.show()
