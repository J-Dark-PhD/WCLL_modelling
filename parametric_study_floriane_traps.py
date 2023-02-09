from parameters_2D import my_model, tungsten, materials_eurofers
from solve_H_transport import run_H_transport
import numpy as np
import festim as F
import properties


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
trap_eurofer_1 = F.Trap(
    k_0=2.52e-07 / (1.1e-10**2) * 0.8165 / properties.atom_density_eurofer,
    E_k=0.16,
    p_0=1e13,
    E_p=0.51,
    density=6.01e25,
    materials=materials_eurofers,
)
trap_eurofer_2 = F.Trap(
    k_0=2.52e-07 / (1.1e-10**2) * 0.8165 / properties.atom_density_eurofer,
    E_k=0.16,
    p_0=1e13,
    E_p=1.27,
    density=6.44e22,
    materials=materials_eurofers,
)
trap_eurofer_3 = F.Trap(
    k_0=2.52e-07 / (1.1e-10**2) * 0.8165 / properties.atom_density_eurofer,
    E_k=0.16,
    p_0=1e13,
    E_p=1.65,
    density=3.88e23,
    materials=materials_eurofers,
)
my_model.traps = F.Traps(
    [
        trap_W_1,
        trap_W_2,
        trap_eurofer_1,
        trap_eurofer_2,
        trap_eurofer_3,
    ],
)

results_folder = "Results/parametric_studies/floriane_traps/"
for export in my_model.exports.exports:
    if isinstance(export, F.DerivedQuantities):
        export.filename = results_folder + "derived_quantities.csv"
    elif isinstance(export, F.XDMFExport):
        export.folder = results_folder
        export.append = False
        export.define_xdmf_file()

my_model.initialise()
run_H_transport(model=my_model)
