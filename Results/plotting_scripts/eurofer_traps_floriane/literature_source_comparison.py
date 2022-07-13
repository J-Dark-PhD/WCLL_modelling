import matplotlib.pyplot as plt
import numpy as np

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=12)

k_B = 8.6e-5

# Eurofer
# taken from (Chen, 2021)
D_0_eurofer_chen = 3.15e-08  # (m2/s)
E_D_eurofer_chen = 0.0622  # (eV)
S_0_eurofer_chen = 2.4088e23  # (m-3 Pa^-0.5)
E_S_eurofer_chen = 0.3026  # (eV)

# taken from (Esteban 2007)
D_0_eurofer_esteban = 1.33e-06  # (m2/s)
E_D_eurofer_esteban = 0.315  # (eV)
S_0_eurofer_esteban = 5.5463e21  # (atom/m3 Pa^-0.5)
E_S_eurofer_esteban = 0.0434  # (eV)

# taken from (Leblond 2021)
D_0_eurofer_leblond = 2.52e-07  # (m2/s)
E_D_eurofer_leblond = 0.16  # (eV)
S_0_eurofer_leblond = 1.059872e23  # (atom/m3 Pa^-0.5)
E_S_eurofer_leblond = 0.27  # (eV)


def S(T, S_0, E_S):
    return S_0*np.exp(-E_S/k_B/T)


def D(T, D_0, E_D):
    return D_0*np.exp(-E_D/k_B/T)


def D_eurofer_chen(T):
    return D(T, D_0_eurofer_chen, E_D_eurofer_chen)


def S_eurofer_chen(T):
    return S(T, S_0_eurofer_chen, E_S_eurofer_chen)


def D_eurofer_esteban(T):
    return D(T, D_0_eurofer_esteban, E_D_eurofer_esteban)


def S_eurofer_esteban(T):
    return S(T, S_0_eurofer_esteban, E_S_eurofer_esteban)


def D_eurofer_leblond(T):
    return D(T, D_0_eurofer_leblond, E_D_eurofer_leblond)


def S_eurofer_leblond(T):
    return S(T, S_0_eurofer_leblond, E_S_eurofer_leblond)


if __name__ == "__main__":
    def tick_function(X):
        V = 1000/(X)
        return ["%.0f" % z for z in V]

    T = np.arange(500, 1000, step=1)

    # #### Diffusion comparison ##### #
    plt.figure(1, figsize=(5, 4))
    plt.plot(
        1000/T, D_eurofer_chen(T),
        label="Chen'21", color='darkred')
    plt.annotate("Chen'21", (1.5, 7.5e-09), color='darkred')

    plt.plot(
        1000/T, D_eurofer_esteban(T),
        label="Esteban'07", color='peru')
    plt.annotate("Esteban'07", (1.6, 1.4e-09), color='peru')

    plt.plot(
        1000/T, D_eurofer_leblond(T),
        label="Montupet-Leblond'21", color='forestgreen')
    plt.annotate("Montupet-Leblond'21", (1.4, 2e-08), color='forestgreen')

    plt.yscale("log")
    plt.minorticks_on()
    plt.grid(which='minor', alpha=0.3)
    plt.grid(which='major', alpha=0.7)
    plt.xlabel(r"1000/$T$ (K)")
    plt.ylabel(r"Diffusivity (m$^{2}$s$^{-1}$)")
    plt.yscale("log")
    plt.xlim(0.95, 2.05)
    plt.ylim(5e-10, 1e-07)
    plt.tight_layout()

    # #### Solubility comparison ##### #
    plt.figure(2, figsize=(5, 4))
    plt.plot(
        1000/T, S_eurofer_chen(T),
        label="Chen'21", color='darkred')
    plt.annotate("Chen'21", (1.8, 5e20), color='darkred')

    plt.plot(
        1000/T, S_eurofer_esteban(T),
        label="Esteban'07", color='peru')
    plt.annotate("Esteban'07", (1.7, 2.5e21), color='peru')

    plt.plot(
        1000/T, S_eurofer_leblond(T),
        label="Montupet-Leblond'21", color='forestgreen')
    plt.annotate("Montupet-Leblond'21", (1.4, 2.5e20), color='forestgreen')

    plt.yscale("log")
    plt.minorticks_on()
    plt.grid(which='minor', alpha=0.3)
    plt.grid(which='major', alpha=0.7)
    plt.xlabel(r"1000/$T$ (K)")
    plt.ylabel(r"Solubility (m$^{-3}$Pa$^{-0.5}$)")
    plt.yscale("log")
    plt.ylim(1e20, 1e22)
    plt.xlim(0.95, 2.05)
    plt.tight_layout()

    plt.show()
