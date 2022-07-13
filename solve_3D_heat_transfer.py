from fenics import *
from parameters_3D import my_model
import FESTIM as F


def standard_3D_case():
    my_model.initialise()

    T = my_model.T.T

    XDMFFile("Results/3D_results/T_3D.xdmf").write_checkpoint(
        T, "T", 0, XDMFFile.Encoding.HDF5, append=False
    )


def dense_3D_case():
    mesh_folder = "meshes/"
    my_model.mesh = F.MeshFromXDMF(
        volume_file=mesh_folder + "mesh_domains_3D_temp.xdmf",
        boundary_file=mesh_folder + "mesh_boundaries_3D_temp.xdmf",
    )

    # chemical potential doesnt work in parallel
    my_model.settings = F.Settings(
        absolute_tolerance=1e12,
        relative_tolerance=1e-08,
        chemical_pot=False,
    )

    my_model.initialise()

    T = my_model.T.T

    XDMFFile("Results/3D_results/T_3D_detailed.xdmf").write_checkpoint(
        T, "T", 0, XDMFFile.Encoding.HDF5, append=False
    )


if __name__ == "__main__":
    # standard case
    standard_3D_case()

    # More dense mesh, resulting in detailed temperature field
    # dense_3D_case()
