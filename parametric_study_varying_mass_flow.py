import numpy as np
from solve_H_transport import run_H_transport
from fenics import *
from parameters_3D import (
    my_model as my_model_3D,
    convective_flux_fw,
    convective_flux_bz,
)
from parameters_2D import my_model as my_model_2D
from h_evaluator import (
    para_h_bz,
    para_h_fw,
    para_flow_velocity_bz,
    para_flow_velocity_fw,
)
from temp_3D_slicer import slicer
import FESTIM as F

no_values = 11

temp_range = np.linspace(569, 601, num=no_values)

lower_bound = 0.1
upper_bound = 1.9
mass_flow_range_bz = 0.85491 * np.linspace(lower_bound, upper_bound, num=no_values)
mass_flow_range_fw = 0.63189 * np.linspace(lower_bound, upper_bound, num=no_values)


def heat_transfer_3D(T, mass_flow_bz, mass_flow_fw):
    """3D heat transfer simulation

    Args:
        T (float): bulk coolant temperature (K)
        mass_flow_bz (float): mass flow rate in breeding zone pipes (kg s-1)
        mass_flow_fw (float): mass flow rate in first wall channels (kg s-1)
    """
    print("Running 3D heat transfer simulation")
    print("BZ mass flow rate =  {} kg/s".format(mass_flow_bz))
    print("FW mass flow rate =  {} kg/s".format(mass_flow_fw))
    print("Bulk coolant temperature = {}K".format(T))

    u_bz = para_flow_velocity_bz(mass_flow_bz=mass_flow_bz)
    u_fw = para_flow_velocity_fw(mass_flow_fw=mass_flow_fw)

    convective_flux_bz.h_coeff = para_h_bz(T, u=u_bz)
    convective_flux_fw.h_coeff = para_h_fw(T, u=u_fw) * 5

    convective_flux_bz.T_ext = T
    convective_flux_fw.T_ext = T

    my_model_3D.initialise()

    XDMFFile(
        folder_temperature_fields_3D
        + "bz_mass_flow={:.3e}_fw_mass_flow={:.3e}_T={:.1f}K.xdmf".format(
            mass_flow_bz, mass_flow_fw, T
        )
    ).write_checkpoint(my_model_3D.T.T, "T", 0, XDMFFile.Encoding.HDF5, append=False)


def temperature_slicer(T, mass_flow_bz, mass_flow_fw):
    """3D temperature field slicer

    Args:
        T (float): bulk coolant temperature (K)
        mass_flow_bz (float): mass flow rate in breeding zone pipes (kg s-1)
        mass_flow_fw (float): mass flow rate in first wall channels (kg s-1)
    """
    print("Running 2D slicer")
    print("BZ mass flow rate = {} kg/s".format(mass_flow_bz))
    print("FW mass flow rate = {} kg/s".format(mass_flow_fw))
    print("Bulk coolant temperature = {}K".format(T))

    filename = (
        folder_temperature_fields_3D
        + "bz_mass_flow={:.3e}_fw_mass_flow={:.3e}_T={:.1f}K.xdmf".format(
            mass_flow_bz, mass_flow_fw, T
        )
    )
    T_sl = slicer(filename)

    XDMFFile(
        folder_2D_slices
        + "bz_mass_flow={:.3e}_fw_mass_flow={:.3e}_T={:.1f}K_slice.xdmf".format(
            mass_flow_bz, mass_flow_fw, T
        )
    ).write_checkpoint(T_sl, "T", 0, XDMFFile.Encoding.HDF5, append=False)


def h_transport_sim_FESTIM(T, mass_flow_bz, mass_flow_fw):
    """2D H transport simulation

    Args:
        T (float): bulk coolant temperature (K)
        mass_flow_bz (float): mass flow rate in breeding zone pipes (kg s-1)
        mass_flow_fw (float): mass flow rate in first wall channels (kg s-1)
    """
    print("Running FESTIM hydrogen simulation")
    print("BZ mass flow rate = {} kg/s".format(mass_flow_bz))
    print("FW mass flow rate = {} kg/s".format(mass_flow_fw))
    print("Bulk coolant temperature = {}K".format(T))

    T_file = (
        folder_2D_slices
        + "bz_mass_flow={:.3e}_fw_mass_flow={:.3e}_T={:.1f}K_slice.xdmf".format(
            mass_flow_bz, mass_flow_fw, T
        )
    )

    my_model_2D.T = F.TemperatureFromXDMF(filename=T_file, label="T")
    folder = (
        folder_results
        + "bz_mass_flow={:.3e}_fw_mass_flow={:.3e}_T={:.1f}K/".format(
            mass_flow_bz, mass_flow_fw, T
        )
    )
    for export in my_model_2D.exports.exports:
        if isinstance(export, F.DerivedQuantities):
            export.filename = folder + "derived_quantities.csv"
        elif isinstance(export, F.XDMFExport):
            export.folder = folder
            export.append = False
            export.define_xdmf_file()

    run_H_transport(my_model_2D)


if __name__ == "__main__":

    folder_temperature_fields_3D = (
        "Results/parametric_studies/varying_h_coeff/3D_temp_fields/"
    )
    folder_2D_slices = "Results/parametric_studies/varying_h_coeff/2D_slices/"
    folder_results = "Results/parametric_studies/varying_h_coeff/results/"

    # varying both mass flow rates by same value
    for mass_flow_bz, mass_flow_fw in zip(mass_flow_range_bz, mass_flow_range_fw):
        for T in temp_range:
            heat_transfer_3D(T, mass_flow_bz, mass_flow_fw)
            temperature_slicer(T, mass_flow_bz, mass_flow_fw)
            h_transport_sim_FESTIM(T, mass_flow_bz, mass_flow_fw)

    # varying mass flow rates individually
    # for mass_flow_bz in mass_flow_range_bz:
    #     mass_flow_fw = 0.63189
    #     for T in temp_range:
    #         heat_transfer_3D(T, mass_flow_bz, mass_flow_fw)
    #         temperature_slicer(T, mass_flow_bz, mass_flow_fw)
    #         h_transport_sim_FESTIM(T, mass_flow_bz, mass_flow_fw)

    # for mass_flow_fw in mass_flow_range_fw:
    #     mass_flow_bz = 0.85491
    #     for T in temp_range:
    #         heat_transfer_3D(T, mass_flow_bz, mass_flow_fw)
    #         temperature_slicer(T, mass_flow_bz, mass_flow_fw)
    #         h_transport_sim_FESTIM(T, mass_flow_bz, mass_flow_fw)
