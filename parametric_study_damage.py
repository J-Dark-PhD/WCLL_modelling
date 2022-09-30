from parameters_2D import my_model, tungsten, materials_eurofers, id_lipb
from solve_H_transport import run_H_transport
import numpy as np
import festim as F
import fenics as f
import properties


def trap_conc_steady(A_0, E_A, phi, K, n_max):
    """
    Evaluates the trap concentration at steady state
    """
    A = A_0 * f.exp(E_A / (F.k_B * my_model.T.T))
    n_t = 1 / ((A / (phi * K) + (1 / (n_max))))
    return n_t


def damage_testing(dpa):

    trap_W_1 = F.Trap(
        k_0=properties.D_0_W / (1.1e-10**2 * 6 * properties.atom_density_W),
        E_k=properties.E_D_W,
        p_0=1e13,
        E_p=0.87,
        density=1.3e-3 * properties.atom_density_W,
        materials=tungsten,
    )
    trap_W_2 = F.Trap(
        k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
        E_k=properties.E_D_W,
        p_0=1e13,
        E_p=1.00,
        density=4e-4 * properties.atom_density_W,
        materials=tungsten,
    )
    trap_W_damage_1 = F.Trap(
        k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
        E_k=properties.E_D_W,
        p_0=1e13,
        E_p=1.15,
        density=1,
        materials=tungsten,
    )
    trap_W_damage_2 = F.Trap(
        k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
        E_k=properties.E_D_W,
        p_0=1e13,
        E_p=1.30,
        density=1,
        materials=tungsten,
    )
    trap_W_damage_3 = F.Trap(
        k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
        E_k=properties.E_D_W,
        p_0=1e13,
        E_p=1.50,
        density=1,
        materials=tungsten,
    )
    trap_W_damage_4 = F.Trap(
        k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
        E_k=properties.E_D_W,
        p_0=1e13,
        E_p=1.85,
        density=1,
        materials=tungsten,
    )

    trap_eurofer_1 = F.Trap(
        k_0=properties.D_0_eurofer
        / (1.1e-10**2)
        * 0.8165
        / properties.atom_density_eurofer,
        E_k=properties.E_D_eurofer,
        p_0=1e13,
        E_p=properties.trap_energy_eurofer,
        density=properties.trap_density_eurofer,
        materials=materials_eurofers,
    )
    my_model.traps = F.Traps(
        [
            trap_W_1,
            trap_W_2,
            trap_W_damage_1,
            trap_W_damage_2,
            trap_W_damage_3,
            trap_W_damage_4,
            trap_eurofer_1,
        ],
    )

    folder = "Results/parametric_studies/varying_damage/"
    results_folder = folder + "{:.1f}_dpa/".format(dpa)
    for export in my_model.exports.exports:
        if isinstance(export, F.DerivedQuantities):
            export.filename = results_folder + "derived_quantities.csv"
        elif isinstance(export, F.XDMFExport):
            export.folder = results_folder
            export.append = False
            export.define_xdmf_file()

    print("Current step is dpa = {:.1f}".format(dpa))

    my_model.initialise()

    fpy = 3600 * 24 * 365.25

    trap_W_damage_1.density = (
        trap_conc_steady(
            A_0=6.1838e-03,
            E_A=0.2792,
            phi=dpa / fpy,
            K=6.0e26,
            n_max=4.5e25,
        ),
    )
    trap_W_damage_2.density = (
        trap_conc_steady(
            A_0=6.1838e-03,
            E_A=0.2792,
            phi=dpa / fpy,
            K=3.5e26,
            n_max=3.1e25,
        ),
    )
    trap_W_damage_3.density = (
        trap_conc_steady(
            A_0=6.1838e-03,
            E_A=0.2792,
            phi=dpa / fpy,
            K=2.9e26,
            n_max=2.4e25,
        ),
    )
    trap_W_damage_4.density = (
        trap_conc_steady(
            A_0=6.1838e-03,
            E_A=0.2792,
            phi=dpa / fpy,
            K=8.0e26,
            n_max=5.8e25,
        ),
    )

    run_H_transport(model=my_model)


if __name__ == "__main__":
    dpa_values = np.linspace(2, 19, num=18)
    for dpa in dpa_values:
        damage_testing(dpa)
