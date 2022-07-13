from fenics import *
from parameters_3D import my_model

my_model.initialise()

T = my_model.T.T

XDMFFile("Results/3D_results/T_3D.xdmf").write_checkpoint(
    T, "T", 0, XDMFFile.Encoding.HDF5, append=False
)
