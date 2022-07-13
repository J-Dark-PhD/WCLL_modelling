from parameters_2D import my_model, materials_eurofers
from solve_H_transport import run_H_transport
import FESTIM as F


S_0_eur_original = 2.4088e23

reduction_factors = [
    1,
    10,
    100,
    200,
    300,
    400,
    500,
    600,
    700,
    800,
    900,
    1000,
    1e4,
    1e5,
    1e6,
    1e7,
]

folder = "Results/parametric_studies/varying_perm_barrier/"
E_S_eurofer = 0.3026
for reduction_factor in reduction_factors:
    reduced_S_0_eurofer = S_0_eur_original / reduction_factor
    for eurofer in materials_eurofers:
        eurofer.S_0 = reduced_S_0_eurofer
        eurofer.E_S = E_S_eurofer

    results_folder = folder + "S_0_eur={:.1e}/".format(reduced_S_0_eurofer)

    for export in my_model.exports.exports:
        if isinstance(export, F.DerivedQuantities):
            export.filename = results_folder + "derived_quantities.csv"
        elif isinstance(export, F.XDMFExport):
            export.folder = results_folder
            export.append = False
            export.define_xdmf_file()

    print("Current step is S_0_eur = {:.1e}".format(reduced_S_0_eurofer))
    run_H_transport(my_model)
