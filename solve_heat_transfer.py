from fenics import *
from parameters_2D import my_model

my_model.initialise()

T = my_model.T.T
XDMFFile("Results/temperature.xdmf").write(T)
