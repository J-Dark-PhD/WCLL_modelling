from parameters_2D import my_model, materials_eurofers
from solve_H_transport import run_H_transport
import FESTIM as F

test_2_1 = 4e23
test_2_2 = 2e21

test_3_1 = 2.82842712e22

test_5_1 = 7.52120619e21
test_5_2 = 1.06365918e23

test_9_1 = 3.87845489e21
test_9_2 = 1.45853295e22
test_9_3 = 5.48496351e22
test_9_4 = 2.06267708e23

test_values = [
    test_2_1,
    test_2_2,
    test_3_1,
    test_5_1,
    test_5_2,
    test_9_1,
    test_9_2,
    test_9_3,
    test_9_4,
]
folder = "Results/parametric_studies/varying_lipb_solubility/"
# E_S = 0.01399  # average value
E_S = 0.133

transient = True
if transient:
    my_model.dt = F.Stepsize(
        initial_value=1,
        stepsize_change_ratio=1.1,
        dt_min=1e-04,
        stepsize_stop_max=1 / 10,
    )
    my_model.settings = F.Settings(
        transient=True,
        final_time=86400 * 15,
        absolute_tolerance=1e12,
        relative_tolerance=1e-08,
        traps_element_type="DG",
        maximum_iterations=50,
        chemical_pot=True,
        linear_solver="mumps",
    )
    folder += "transient/"

for S_0 in test_values:
    for eurofer_vol in materials_eurofers:
        eurofer_vol.S_0 = S_0
        eurofer_vol.E_S = E_S

    results_folder = folder + "/S_0={:.1e}/".format(S_0)
    for export in my_model.exports.exports:
        if isinstance(export, F.DerivedQuantities):
            export.filename = results_folder + "derived_quantities.csv"
        elif isinstance(export, F.XDMFExport):
            export.folder = results_folder
            export.append = False
            export.define_xdmf_file()

    print("Current step is S_0 = {:.1e}".format(S_0))
    run_H_transport(my_model, S_0_lipb=S_0, E_S_lipb=E_S)
