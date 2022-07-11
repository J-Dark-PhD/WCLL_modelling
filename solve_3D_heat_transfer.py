from fenics import *
from parameters_3D import my_model
from context import FESTIM as F


my_model.initialise()

T = my_model.T.T

XDMFFile("3D_Results/T.xdmf").write_checkpoint(
    T, "T", 0, XDMFFile.Encoding.HDF5, append=False
)


# def run_heat_transfer():
#     print("Running Heat transfer calculations")

#     my_model.initialise()

#     T = my_model.T.T

#     XDMFFile("3D_Results/T.xdmf").write_checkpoint(
#         T, "T", 0, XDMFFile.Encoding.HDF5, append=False
#     )
#     return T


# if __name__ == "__main__":
#     # run_heat_transfer()
