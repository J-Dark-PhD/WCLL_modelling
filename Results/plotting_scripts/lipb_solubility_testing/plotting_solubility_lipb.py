import matplotlib.pyplot as plt
import numpy as np

k_B = 8.6e-5


def S(T, S_0, E_S):
    return S_0*np.exp(-E_S/k_B/T)


plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=12)

# Eurofer
# taken from (Chen, 2021)
S_0_eurofer_chen = 2.4088e23  # (at/m3 Pa^-0.5)
E_S_eurofer_chen = 0.3026  # (eV)


def S_eurofer_chen(T):
    return S(T, S_0_eurofer_chen, E_S_eurofer_chen)


# taken from (Esteban 2007)
S_0_eurofer_esteban = 5.5463e21  # (atom/m3 Pa^-0.5)
E_S_eurofer_esteban = 0.0434  # (eV)


def S_eurofer_esteban(T):
    return S(T, S_0_eurofer_esteban, E_S_eurofer_esteban)


# taken from (Leblond 2021)
S_0_eurofer_leblond = 1.059872e23  # (atom/m3 Pa^-0.5)
E_S_eurofer_leblond = 0.27  # (eV)


def S_eurofer_leblond(T):
    return S(T, S_0_eurofer_leblond, E_S_eurofer_leblond)


# ##### LiPb values ##### #
E_S_lipb_test = 0.133

S_0_values = np.logspace(np.log10(2e+21), np.log10(4e+23), num=0)

# taken from (Reiter, 1990)
T_reiter = np.arange(508, 700, step=1)

S_0_lipb_reiter_H = 4.4310e+20  # (atom/m3 Pa^-0.5)
E_S_lipb_reiter_H = 0.01399  # (eV)

S_0_lipb_reiter_D = 4.2857e+20  # (atom/m3 Pa^-0.5)
E_S_lipb_reiter_D = 0.01399     # (eV)

S_0_lipb_reiter_T = 4.2131e+20   # (atom/m3 Pa^-0.5)
E_S_lipb_reiter_T = 0.01399      # (eV)

S_lipb_reiter_H = S(T_reiter, S_0_lipb_reiter_D, E_S_lipb_reiter_D)
S_lipb_reiter_D = S(T_reiter, S_0_lipb_reiter_H, E_S_lipb_reiter_H)
S_lipb_reiter_T = S(T_reiter, S_0_lipb_reiter_T, E_S_lipb_reiter_T)


# taken from (Aiello, 2008)
S_0_lipb_aiello = 1.427214e23   # (atom/m3 Pa^-0.5)
E_S_lipb_aiello = 0.133     # (eV)
T_aiello = np.arange(600, 900, step=1)

S_lipb_aillo = S(T_aiello, S_0_lipb_aiello, E_S_lipb_aiello)

# taken from G.Alberro 2015
S_0_lipb_alberro = 5.203e21   # (atom/m3 Pa^-0.5)
E_S_lipb_alberro = 0.00938     # (eV)
T_alberro = np.arange(523, 922, step=1)
S_lipb_alberro = S(T_alberro, S_0_lipb_alberro, E_S_lipb_alberro)

# taken from Chan and Veleski 1984
S_0_lipb_chan = 8.535e21   # (atom/m3 Pa^-0.5)
E_S_lipb_chan = 0.0933     # (eV)
T_chan = np.arange(573, 773, step=1)
S_lipb_chan = S(T_chan, S_0_lipb_chan, E_S_lipb_chan)

# taken from Schumacher 1990
S_0_lipb_schumacher = 1.6131e22   # (atom/m3 Pa^-0.5)
E_S_lipb_schumacher = 0.0632     # (eV)
T_schumacher = np.arange(508, 1040, step=1)
S_lipb_schumacher = S(T_schumacher, S_0_lipb_schumacher, E_S_lipb_schumacher)


if __name__ == "__main__":
    def tick_function(X):
        V = 1000/(X)
        return ["%.0f" % z for z in V]

    T = np.arange(500, 1000, step=1)
    grey_W = (228/255, 146/255, 64/255)
    # orange_eurofer = (228/255, 146/255, 64/255)
    orange_eurofer = "grey"
    # yellow_lipb = (180/255, 95/255, 6/255)
    yellow_lipb = "green"

    fig = plt.figure(figsize=(5, 4))
    # plt.xlabel(r"1000/$T$ (K)")
    # plt.ylabel(r"Solubility (m$^{-3}$Pa$^{-0.5}$)")
    # plt.yscale("log")

    # # LiPb comparison
    plt.figure(1, figsize=(5, 4))
    plt.plot(
        1000/T_aiello, S_lipb_aillo,
        label="H (Aiello'08)", color='darkred')
    plt.annotate("H (Aiello'08)", (1.6, 1.5e22), color='darkred')

    plt.plot(
        1000/T_schumacher, S_lipb_schumacher,
        label="H (Schumacher'90)", color='peru')
    plt.annotate("H (Schumacher'90)", (1.2, 8e21), color='peru')

    plt.plot(
        1000/T_alberro, S_lipb_alberro,
        label="T (Alberro'15)", color='forestgreen')
    plt.annotate("T (Alberro'15))", (1.3, 3.5e21), color='forestgreen')

    plt.plot(
        1000/T_chan, S_lipb_chan,
        label="H (Chan'84)", color='teal')
    plt.annotate("H (Chan'84)", (1.35, 1.2e21), color='teal')

    plt.plot(
        1000/T_reiter, S_lipb_reiter_T,
        label="T (Reiter'90)", color='purple')
    plt.annotate("T (Reiter'91)", (1.6, 4e20), color='purple')

    plt.yscale("log")
    plt.minorticks_on()
    plt.grid(which='minor', alpha=0.3)
    plt.grid(which='major', alpha=0.7)
    plt.xlabel(r"1000/$T$ (K)")
    plt.ylabel(r"Solubility (m$^{-3}$Pa$^{-0.5}$)")
    plt.yscale("log")
    plt.xlim(0.95, 2.05)
    plt.tight_layout()

    # EUROFER vs LiPb values
    T_exps = [T_reiter, T_aiello, T_alberro, T_chan, T_schumacher]
    S_functions = [
        S_lipb_reiter_T, S_lipb_aillo, S_lipb_alberro,
        S_lipb_chan, S_lipb_schumacher]

    plt.figure(2, figsize=(5, 4))
    plt.plot(
        1000/T, S_eurofer_chen(T),
        label="Eurofer (Chen'21)", color='dimgrey', linestyle='dashed')
    plt.plot(
        1000/T, S_eurofer_esteban(T),
        label="Eurofer (Esteban'07)", color='dimgrey')
    plt.plot(
        1000/T, S_eurofer_leblond(T),
        label="Eurofer (Leblond'21)", color='black')

    for S_fun, T in zip(S_functions, T_exps):
        plt.plot(
            1000/T, S_fun, color='green', alpha=0.4)

    plt.plot(1000/T, S_eurofer_chen(T), label="Eurofer", color='dimgrey')

    plt.yscale("log")
    plt.minorticks_on()
    plt.grid(which='minor', alpha=0.3)
    plt.grid(which='major', alpha=0.7)
    plt.xlabel(r"1000/$T$ (K)")
    plt.ylabel(r"Solubility (m$^{-3}$Pa$^{-0.5}$)")
    plt.yscale("log")
    plt.xlim(0.9, 2.05)
    plt.tight_layout()


    # EUROFER vs LiPb values with test range
    plt.figure(3, figsize=(5, 4))
    plt.plot(
        1000/T, S_eurofer_chen(T),
        label="Eurofer (Chen'21)", color='dimgrey', linestyle='dashed')
    for S_fun, T in zip(S_functions, T_exps):
        plt.plot(
            1000/T, S_fun, color='green', alpha=0.4)
    plt.plot(1000/T, S_eurofer_chen(T), label="Eurofer", color='dimgrey')
    plt.yscale("log")

    # 9 values
    for S_0 in S_0_values:
        plt.plot(
            1000/T, S(T, S_0, E_S_lipb_test),
            color='red', label="Test values")

    plt.yscale("log")
    plt.minorticks_on()
    plt.grid(which='minor', alpha=0.3)
    plt.grid(which='major', alpha=0.7)
    plt.xlabel(r"1000/$T$ (K)")
    plt.ylabel(r"Solubility (m$^{-3}$Pa$^{-0.5}$)")
    plt.yscale("log")
    plt.xlim(0.9, 2.05)
    plt.ylim(8e19, 1.5e23)
    plt.tight_layout()

    plt.show()
