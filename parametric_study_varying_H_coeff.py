from solve_H_transport import run_H_transport
from parameters_3D import (
    my_model as my_model_3D,
    convective_flux_fw,
    convective_flux_bz,
)
from parameters_2D import my_model as my_model_2D
from temp_3D_slicer import slicer
from h_evaluator import para_h_bz, para_h_fw
from fenics import *
import FESTIM as F
import numpy as np

temp_range = np.linspace(569, 601, num=15)

folder_temperature_fields_3D = (
    "Results/parametric_studies/varying_h_coeff/preliminary_study/3D_temp_fields/"
)
folder_2D_slices = (
    "Results/parametric_studies/varying_h_coeff/preliminary_study/2D_slices/"
)
folder_h_transport = (
    "Results/parametric_studies/varying_h_coeff/preliminary_study/results/"
)

# ##### 3D Heat transfer ##### #

for temp in temp_range:
    """
    Can be run in parallel

    Runs heat transfer simualtions using the 3D geometry using the defined
    temp as a bulk coolant temp and is used to evaulate the heat transfer coefficient
    """
    print("Simulating at coolant T = {:.1f}K".format(temp))
    convective_flux_bz.h_coeff = para_h_bz(temp)
    convective_flux_fw.h_coeff = para_h_fw(temp) * 5

    convective_flux_bz.T_ext = temp
    convective_flux_fw.T_ext = temp

    my_model_3D.initialise()

    XDMFFile(
        folder_temperature_fields_3D + "{:.1f}K.xdmf".format(temp)
    ).write_checkpoint(my_model_3D.T.T, "T", 0, XDMFFile.Encoding.HDF5, append=False)

# ##### Slicer ##### #

for temp in temp_range:
    """
    needs to be run in serial

    takes a central slice from each 3D temperature field
    """
    print("Doing for temp = {:.1f}K".format(temp))
    filename = folder_temperature_fields_3D + "{:.1f}K.xdmf".format(temp)
    T_sl = slicer(filename)
    XDMFFile(folder_2D_slices + "{:.1f}K_slice.xdmf".format(temp)).write_checkpoint(
        T_sl, "T", 0, XDMFFile.Encoding.HDF5, append=False
    )

# ##### 2D FESTIM sim ##### #

for temp in temp_range:
    """
    Can be run in parallel

    Runs heat transfer simualtions using the 3D geometry using the defined
    temp as a bulk coolant temp and is used to evaulate the heat transfer coefficient
    """
    print("Running simulation for coolant temp = {:.1f}K".format(temp))
    T_file = folder_2D_slices + "{:.1f}K_slice.xdmf".format(temp)
    my_model_2D.T = F.TemperatureFromXDMF(filename=T_file, label="T")

    folder_results = folder_h_transport + "run_{:.1f}K/".format(temp)

    for export in my_model_2D.exports.exports:
        if isinstance(export, F.DerivedQuantities):
            export.filename = folder_results + "derived_quantities.csv"
        elif isinstance(export, F.XDMFExport):
            export.folder = folder_results
            export.append = False
            export.define_xdmf_file()

    run_H_transport(my_model_2D)
