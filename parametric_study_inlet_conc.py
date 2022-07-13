from parameters_2D import my_model, inlet_h_concentration
from solve_H_transport import run_H_transport
import numpy as np
import FESTIM as F


test_values = np.linspace(0, 1, num=11)

folder = "Results/parametric_studies/varying_inlet_conc/"
for eta in test_values:
    results_folder = folder + "eta={:.1f}/".format(eta)
    for export in my_model.exports.exports:
        if isinstance(export, F.DerivedQuantities):
            export.filename = results_folder + "derived_quantities.csv"
        elif isinstance(export, F.XDMFExport):
            export.folder = results_folder
            export.append = False
            export.define_xdmf_file()

    print("Current step is eta = {:.1f}".format(eta))
    relative_error = 1  # initialise relative error
    average_concentration_outlet_old = (
        1.01741917005023e21 / 0.061
    )  # initialise average concentration outlet old to smth
    while relative_error > 0.01:
        # run FESTIM
        derived_quantities = run_H_transport(my_model)

        # compute what the average conc at the outlet is
        index = np.where(
            np.array(derived_quantities.data[0]) == "Total solute surface 21"
        )
        average_concentration_outlet = derived_quantities.data[1][index[0][0]] / 0.061

        # modify the BC accordingly
        inlet_h_concentration.value = eta * average_concentration_outlet

        # compute the relative error
        relative_error = (
            average_concentration_outlet - average_concentration_outlet_old
        ) / average_concentration_outlet_old

        # store the old value of conc outlet
        average_concentration_outlet_old = average_concentration_outlet
        print("relative error = ", relative_error)
        print("refining")
