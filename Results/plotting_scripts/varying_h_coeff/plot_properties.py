import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append("../../../")
from h_evaluator import (
    rho_func,
    thermal_cond_func,
    mu_func,
    cp_func,
    heat_transfer_coefficient,
)

T = np.linspace(568, 602, num=100)


pipe_diameter_bz = 0.008
pipe_width_fw = 0.007

water_density = rho_func(T)

# bz flow
total_mass_flow_rate_bz = 0.85491
n_tubes_bz = 14
mass_flow_rate_bz = total_mass_flow_rate_bz / n_tubes_bz
A_bz = np.pi * (pipe_diameter_bz / 2) ** 2
u_bz = mass_flow_rate_bz / (water_density * A_bz)

# fw flow
total_mass_flow_rate_fw = 0.63189
n_tubes_fw = 4
mass_flow_rate_fw = total_mass_flow_rate_fw / n_tubes_fw
A_fw = pipe_width_fw**2
u_fw = mass_flow_rate_fw / (water_density * A_fw)


h_bz = heat_transfer_coefficient(
    d_w=np.pi * (pipe_diameter_bz),
    u=u_bz,
    L=pipe_diameter_bz,
    T=T,
)

h_fw = heat_transfer_coefficient(
    d_w=4 * pipe_width_fw,
    u=u_fw,
    L=pipe_width_fw,
    T=T,
)


rho_min = rho_func(T[0])
rho_max = rho_func(T[-1])
rho_diff = ((rho_max - rho_min) / rho_min) * 100

cp_min = cp_func(T[0])
cp_max = cp_func(T[-1])
cp_diff = ((cp_max - cp_min) / cp_min) * 100

k_min = thermal_cond_func(T[0])
k_max = thermal_cond_func(T[-1])
k_diff = ((k_max - k_min) / k_min) * 100

mu_min = mu_func(T[0])
mu_max = mu_func(T[-1])
mu_diff = ((mu_max - mu_min) / mu_min) * 100

h_bz_min = h_bz[0]
h_bz_max = h_bz[-1]
h_bz_diff = ((h_bz_max - h_bz_min) / h_bz_min) * 100

h_fw_min = h_fw[0]
h_fw_max = h_fw[-1]
h_fw_diff = ((h_fw_max - h_fw_min) / h_fw_min) * 100


print("Difference in density = {:.1f} %".format(np.abs(rho_diff)))
print("Difference in specific heat capacity = {:.1f} %".format(np.abs(cp_diff)))
print("Difference in thermal conductivity = {:.1f} %".format(np.abs(k_diff)))
print("Difference in viscosity = {:.1f} %".format(np.abs(mu_diff)))
print(
    "Difference in heat transfer coefficient in BZ system = {:.1f} %".format(
        np.abs(h_bz_diff)
    )
)
print(
    "Difference in heat transfer coefficient in FW system = {:.1f} %".format(
        np.abs(h_fw_diff)
    )
)


def plot_all_separate():
    # density plot
    plt.figure()
    plt.plot(T, rho_func(T), color="black")
    plt.xlabel(r"Temperature (K)")
    plt.ylabel(r"Density, $\rho$ (Kg m$^{-3}$)")
    plt.ylim(0, 800)
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()

    # specific heat capacity plot
    plt.figure()
    plt.plot(T, cp_func(T), color="black")
    plt.xlabel(r"Temperature (K)")
    plt.ylabel(r"Specific heat capacity, c$_p$ (J kg$^{-3}$ K$^{-1}$)")
    plt.ylim(0, 7000)
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()

    # Thermal conductivity plot
    plt.figure()
    plt.plot(T, thermal_cond_func(T), color="black")
    plt.xlabel(r"Temperature (K)")
    plt.ylabel(r"Thermal conductivity, k (W m$^{-1}$ K$^{-1}$)")
    plt.ylim(0, 0.6)
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()

    # Viscosity plot
    plt.figure()
    plt.plot(T, mu_func(T), color="black")
    plt.xlabel(r"Temperature (K)")
    plt.ylabel(r"Viscosity, $\mu$ (Pa s)")
    plt.ylim(0, 1e-04)
    plt.ticklabel_format(axis="y", scilimits=(0, 0))
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()

    # Heat transfer coefficient in BZ system
    plt.figure()
    plt.plot(T, h_bz, color="black")
    plt.xlabel(r"Temperature (K)")
    plt.ylabel(r"Heat transfer coefficient in BZ system (W m$^{-2}$ K$^{-1}$)")
    plt.ylim(0, 6000)
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()

    # Heat transfer coefficient in FW system
    plt.figure()
    plt.plot(T, h_fw, color="black")
    plt.xlabel(r"Temperature (K)")
    plt.ylabel(r"Heat transfer coefficient in FW system (W m$^{-2}$ K$^{-1}$)")
    plt.ylim(0, 10000)
    # plt.ticklabel_format(axis="y", scilimits=(0, 0))
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()

    plt.show()


def plot_all_in_one():
    # Properties plot
    fig, axs = plt.subplots(2, 2, sharex=True, figsize=[8, 6])
    axs[0, 0].plot(T, rho_func(T), color="black")
    axs[0, 0].set_ylabel("Density \n" + r"(Kg m$^{-3}$)")
    axs[0, 0].set_ylim(0, 800)
    axs[0, 0].spines["top"].set_visible(False)
    axs[0, 0].spines["right"].set_visible(False)

    axs[0, 1].plot(T, mu_func(T), color="black")
    axs[0, 1].set_ylabel("Viscosity \n" + r"(Pa s)")
    axs[0, 1].set_ylim(0, 1e-04)
    axs[0, 1].ticklabel_format(axis="y", scilimits=(0, 0))
    axs[0, 1].spines["top"].set_visible(False)
    axs[0, 1].spines["right"].set_visible(False)

    axs[1, 0].plot(T, cp_func(T), color="black")
    axs[1, 0].set_xlabel(r"Temperature (K)")
    axs[1, 0].set_ylabel("Specific heat capacity \n" + r"(J kg$^{-3}$ K$^{-1}$)")
    axs[1, 0].set_ylim(0, 7000)
    axs[1, 0].spines["top"].set_visible(False)
    axs[1, 0].spines["right"].set_visible(False)

    axs[1, 1].plot(T, thermal_cond_func(T), color="black")
    axs[1, 1].set_xlabel(r"Temperature (K)")
    axs[1, 1].set_ylabel("Thermal conductivity \n" + r"(W m$^{-1}$ K$^{-1}$)")
    axs[1, 1].set_ylim(0, 0.6)
    axs[1, 1].spines["top"].set_visible(False)
    axs[1, 1].spines["right"].set_visible(False)
    plt.tight_layout()

    # Heat transfer coefficients plot
    fig, axs = plt.subplots(2, 1, sharex=True, figsize=[4, 6])
    axs[0].plot(T, h_bz, color="black")
    axs[0].set_ylabel("Heat transfer coefficient BZ \n" + r"(W m$^{-2}$ K$^{-1}$)")
    axs[0].set_ylim(0, 6000)
    axs[0].spines["top"].set_visible(False)
    axs[0].spines["right"].set_visible(False)

    axs[1].plot(T, h_fw, color="black")
    axs[1].set_xlabel(r"Temperature (K)")
    axs[1].set_ylabel("Heat transfer coefficient FW \n" + r"(W m$^{-2}$ K$^{-1}$)")
    axs[1].set_ylim(0, 10000)
    axs[1].spines["top"].set_visible(False)
    axs[1].spines["right"].set_visible(False)
    plt.tight_layout()

    plt.show()


# ##### PLOTTING ##### #

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

# plot_all_separate()
plot_all_in_one()
