from fenics import *
from parameters_3D import my_model
import festim as F


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
        transient=False,
        absolute_tolerance=1e12,
        relative_tolerance=1e-08,
        chemical_pot=False,
    )

    my_model.initialise()

    T = my_model.T.T

    XDMFFile("Results/3D_results/T_3D_detailed.xdmf").write_checkpoint(
        T, "T", 0, XDMFFile.Encoding.HDF5, append=False
    )

def standard_3D_case_submesh():
    my_model.initialise()

    T = my_model.T.T

    mesh_folder = "meshes/"
    mesh_full = F.MeshFromXDMF(
        volume_file=mesh_folder + "mesh_domains_3D.xdmf",
        boundary_file=mesh_folder + "mesh_boundaries_3D.xdmf",
    )
    id_lipb = 6
    mesh_sub = SubMesh(mesh_full.mesh, mesh_full.volume_markers, id_lipb)
    XDMFFile("meshes/submesh_3D.xdmf").write(mesh_sub)

    print("Projecting temperature field onto mesh")
    V_CG1_sub = FunctionSpace(mesh_sub, "CG", 1)
    T.set_allow_extrapolation(True)
    T_sub = project(T, V_CG1_sub)

    XDMFFile("Results/3D_results/T_3D_sub.xdmf").write_checkpoint(
        T_sub, "T", 0, XDMFFile.Encoding.HDF5, append=False
    )


if __name__ == "__main__":
    # standard case
    # standard_3D_case()

    # More dense mesh, resulting in detailed temperature field
    # dense_3D_case()

    standard_3D_case_submesh()
