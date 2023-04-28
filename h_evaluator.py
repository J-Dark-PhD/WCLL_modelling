import numpy as np
from pyXSteam.XSteam import XSteam


def rho_func(T):
    """Evaluates density of fluid according to temperature T,
    sourced from: https://doi.org/10.1016/j.fusengdes.2020.111956

    Args:
        T (float): temperature of water (K)

    Returns:
        float: density of fluid (kg/m3)
    """
    rho = -1.4226e-2 * T**2 + 14.122 * T - 2693
    return rho


def thermal_cond_func(T):
    """Evaluates thermal conductivity of fluid according to temperature T,
    sourced from: https://doi.org/10.1016/j.fusengdes.2020.111956

    Args:
        T (float): temperature of water (K)

    Returns:
        float: thermal conductivity of fluid (W/m K)
    """
    k = -1.2024e-05 * T**2 + 1.1846e-02 * T - 2.2804
    return k


def mu_func(T):
    """Evaluates viscosity of fluid according to temperature T,
    sourced from: https://doi.org/10.1016/j.fusengdes.2020.111956

    Args:
        T (float): temperature of water (K)

    Returns:
        float: viscosity of fluid (Pa s)
    """
    mu = (-8.095238e-04 * T**2 + 0.5722429 * T + 29.67213) * 1e-06
    return mu


def cp_func(T):
    """Evaluates specific heat capacity of fluid according to temperature T,
    sourced from: https://doi.org/10.1016/j.fusengdes.2020.111956

    Args:
        T (float): temperature of water (K)

    Returns:
        float: specific heat capacity of fluid (J kg-1 K-1)
    """
    cp = 9.8485e-03 * T**3 - 16.39861 * T**2 + 9118.681 * T - 1.6882247 * 1e06
    return cp


def Pr_number_func(mu, k, cp):
    """Evaluates Prandtle Number of fluid

    Args:
        mu (float): viscosity of fluid (Pa s)
        k (float): thermal conducivity of fluid (W/ m K)
        cp (float): specific heat capacity of fluid (J kg-1 K-1)

    Returns:
        float: prandtl number
    """
    pr = (cp * mu) / k
    return pr


def Pr_number_steam_tables(P, T):
    """Evaluates a Pr number for water with a pressure between 150 and 175 bar
    and temperature between 250 and 300 C by interpolation

    Args:
        P (float): pressure of water (bar)
        T (float): temperture of water (C)

    Returns:
        float: Prandle number
    """
    pr_150bar_250c = 0.810
    pr_150bar_300c = 0.860
    pr_175bar_250c = 0.806
    pr_175bar_300c = 0.848

    if not 150 < pressure < 175:
        print("Pressure value out of range")
    elif not 250 < temp < 300:
        print("Temperature value out of range")
    else:
        # 150 bar interpolation
        pr_150bar_temp_interval = (pr_150bar_300c - pr_150bar_250c) / 50
        pr_150 = pr_150bar_250c + (T - 250) * pr_150bar_temp_interval
        # 175 bar interpolation
        pr_175bar_temp_interval = (pr_175bar_300c - pr_175bar_250c) / 50
        pr_175 = pr_175bar_250c + (T - 250) * pr_175bar_temp_interval
        # pressure interpolation
        pressure_temp_interval = (pr_175 - pr_150) / 25
        pr = pr_150 + (P - 150) * pressure_temp_interval
    return pr


def Re_number(rho, u, L, mu):
    """Evaluates Reynolds number

    Args:
        rho (float): density of fluid (kg/m3)
        u (float): velocity of fluid (m/s)
        length (float): characteristic length (m), diameter for pipe
        viscosity (float): viscosity of fluid (Pa s)

    Returns:
        float: Reynolds number
    """
    re = (rho * u * L) / mu
    return re


def friction_factor(Re):
    """Evaluates Darcy friction factor according to Reynolds number

    Args:
        Re (float): Reynolds number

    Returns:
        float: Darcy friction factor
    """
    xi = (0.790 * np.log(Re) - 1.64) ** -2
    return xi


def Nu_number(Re, Pr, xi):
    """Evaluates the nusselt number according to the Gnielinski correlation

    Args:
        Re (float): reynolds number
        Pr (float): prandtl number
        xi (float): darcy fricion factor

    Returns:
        float: nusselt number
    """
    nu = (
        (xi / 8)
        * (Re - 1000)
        * Pr
        / (1 + (12.7 * (xi / 8) ** 0.5) * ((Pr ** (2 / 3)) - 1))
    )
    return nu


def heat_transfer_coefficient(d_w, u, L, T, P=1):
    """_summary_

    Args:
        d_w (float): wetted perimeter (m)
        u (float): fluid velocity (m/s)
        L (float): characteristi length (m)
        P (float, optional): pressure of fluid (bar), only needed if steam table Pr evaluation is used
        T (float): Temperature of fluid (K)

    Returns:
        float: heat transfer coefficient (W/m2 K)
    """
    rho = rho_func(T)
    k = thermal_cond_func(T)
    mu = mu_func(T)
    cp = cp_func(T)

    # print("Density = {}".format(rho))
    # print("Thermal conductivity = {}".format(k))
    # print("Viscosity = {}".format(mu))
    # print("Specific heat capacity = {}".format(cp))

    Reynolds = Re_number(rho=rho, u=u, L=L, mu=mu)
    xi = friction_factor(Re=Reynolds)
    Prandtl = Pr_number_func(mu=mu, k=k, cp=cp)
    Nu = Nu_number(Re=Reynolds, Pr=Prandtl, xi=xi)

    # print("Reynolds number = {}".format(Reynolds))
    # print("Prandtl number = {}".format(Prandtl))
    # print("Nusselt number = {}".format(Nu))

    h = (Nu * k) / d_w
    return h


def heat_transfer_coefficient_alt(d_w, u, L, T, P=1):
    """_summary_

    Args:
        d_w (float): wetted perimeter (m)
        u (float): fluid velocity (m/s)
        L (float): characteristi length (m)
        P (float, optional): pressure of fluid (bar), only needed if steam table Pr evaluation is used
        T (float): Temperature of fluid (K)

    Returns:
        float: heat transfer coefficient (W/m2 K)
    """
    steamTable = XSteam(XSteam.UNIT_SYSTEM_BARE)
    P = 15.5
    rho = steamTable.rho_pt(P, T)
    k = steamTable.tc_pt(P, T)
    cp = steamTable.Cp_pt(P, T) * 1000
    mu = steamTable.my_pt(P, T)
    mu_w = steamTable.my_pt(P, T + 10)

    # print("Density alt = {}".format(rho))
    # print("Thermal conductivity alt = {}".format(k))
    # print("Viscosity alt = {}".format(mu))
    # print("Specific heat capacity alt = {}".format(cp))

    Reynolds = Re_number(rho=rho, u=u, L=L, mu=mu)
    xi = friction_factor(Re=Reynolds)
    Prandtl = Pr_number_func(mu=mu, k=k, cp=cp)
    # Nu = Nu_number(Re=Reynolds, Pr=Prandtl, xi=xi)
    Nu = 0.027 * (Reynolds ** (4 / 5)) * (Prandtl ** (1 / 3)) * ((mu / mu_w) ** 0.14)

    # print("Reynolds number alt = {}".format(Reynolds))
    # print("Prandtl number alt = {}".format(Prandtl))
    # print("Nusselt number alt = {}".format(Nu))

    h = (Nu * k) / d_w
    return h


def heat_transfer_coefficient_alt_2(d_w, u, L, T, P=1):
    """_summary_

    Args:
        d_w (float): wetted perimeter (m)
        u (float): fluid velocity (m/s)
        L (float): characteristi length (m)
        P (float, optional): pressure of fluid (bar), only needed if steam table Pr evaluation is used
        T (float): Temperature of fluid (K)

    Returns:
        float: heat transfer coefficient (W/m2 K)
    """
    steamTable = XSteam(XSteam.UNIT_SYSTEM_BARE)
    P = 15.5
    rho = steamTable.rho_pt(P, T)
    k = steamTable.tc_pt(P, T)
    cp = steamTable.Cp_pt(P, T) * 1000
    mu = steamTable.my_pt(P, T)
    mu_w = steamTable.my_pt(P, T + 10)

    # print("Density alt = {}".format(rho))
    # print("Thermal conductivity alt = {}".format(k))
    # print("Viscosity alt = {}".format(mu))
    # print("Specific heat capacity alt = {}".format(cp))

    Reynolds = Re_number(rho=rho, u=u, L=L, mu=mu)
    xi = friction_factor(Re=Reynolds)
    Prandtl = Pr_number_func(mu=mu, k=k, cp=cp)
    Nu = Nu_number(Re=Reynolds, Pr=Prandtl, xi=xi)

    # print("Reynolds number alt = {}".format(Reynolds))
    # print("Prandtl number alt = {}".format(Prandtl))
    # print("Nusselt number alt = {}".format(Nu))

    h = (Nu * k) / d_w
    return h


pressure = 155
T = 584.65  # average temp
# T = 568.15  # initial temp
pipe_diameter_bz = 0.008
pipe_width_fw = 0.007

water_density = rho_func(T)

# bz flow
total_mass_flow_rate_bz = 0.85491
n_tubes_bz = 14
mass_flow_rate_bz = total_mass_flow_rate_bz / n_tubes_bz
A_bz = np.pi * (pipe_diameter_bz / 2) ** 2
# mass flow rate m = rho*u*A
u_bz = mass_flow_rate_bz / (water_density * A_bz)

# fw flow
total_mass_flow_rate_fw = 0.63189
n_tubes_fw = 4
mass_flow_rate_fw = total_mass_flow_rate_fw / n_tubes_fw
A_fw = pipe_width_fw**2
# mass flow rate m = rho*u*A
u_fw = mass_flow_rate_fw / (water_density * A_fw)

# h_bz = heat_transfer_coefficient(
#     d_w=np.pi * (pipe_diameter_bz),
#     u=u_bz,
#     L=pipe_diameter_bz,
#     T=T,
# )

# h_fw = heat_transfer_coefficient(
#     d_w=4 * pipe_width_fw,
#     u=u_fw,
#     L=pipe_width_fw,
#     T=T,
# )

# print("h_bz = {:.3e}".format(h_bz))
# print("h_fw = {:.3e}".format(h_fw))


def para_flow_velocity_bz(mass_flow_bz=0.85491):
    total_mass_flow_rate_bz = mass_flow_bz
    n_tubes_bz = 14
    mass_flow_rate_bz = total_mass_flow_rate_bz / n_tubes_bz
    A_bz = np.pi * (pipe_diameter_bz / 2) ** 2
    u_bz = mass_flow_rate_bz / (water_density * A_bz)

    return u_bz


def para_flow_velocity_fw(mass_flow_fw=0.63189):
    total_mass_flow_rate_fw = mass_flow_fw
    n_tubes_fw = 4
    mass_flow_rate_fw = total_mass_flow_rate_fw / n_tubes_fw
    A_fw = pipe_width_fw**2
    # mass flow rate m = rho*u*A
    u_fw = mass_flow_rate_fw / (water_density * A_fw)

    return u_fw


def para_h_bz(T, d_w=np.pi * (pipe_diameter_bz), u=u_bz, L=pipe_diameter_bz):
    """_summary_

    Args:
        d_w (float): wetted perimeter (m)
        u (float): fluid velocity (m/s)
        L (float): characteristi length (m)
        P (float, optional): pressure of fluid (bar), only needed if steam table Pr evaluation is used
        T (float): Temperature of fluid (K)

    Returns:
        float: heat transfer coefficient (W/m2 K)
    """
    rho = rho_func(T)
    k = thermal_cond_func(T)
    mu = mu_func(T)
    cp = cp_func(T)
    Reynolds = Re_number(rho=rho, u=u, L=L, mu=mu)
    xi = friction_factor(Re=Reynolds)
    Prandtl = Pr_number_func(mu=mu, k=k, cp=cp)
    Nu = Nu_number(Re=Reynolds, Pr=Prandtl, xi=xi)

    h = (Nu * k) / d_w
    return h


def para_h_fw(T, d_w=4 * pipe_width_fw, u=u_fw, L=pipe_width_fw):
    """_summary_

    Args:
        d_w (float): wetted perimeter (m)
        u (float): fluid velocity (m/s)
        L (float): characteristi length (m)
        P (float, optional): pressure of fluid (bar), only needed if steam table Pr evaluation is used
        T (float): Temperature of fluid (K)

    Returns:
        float: heat transfer coefficient (W/m2 K)
    """
    rho = rho_func(T)
    k = thermal_cond_func(T)
    mu = mu_func(T)
    cp = cp_func(T)
    Reynolds = Re_number(rho=rho, u=u, L=L, mu=mu)
    xi = friction_factor(Re=Reynolds)
    Prandtl = Pr_number_func(mu=mu, k=k, cp=cp)
    Nu = Nu_number(Re=Reynolds, Pr=Prandtl, xi=xi)

    h = (Nu * k) / d_w
    return h
