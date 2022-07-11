from fenics import *
from context import FESTIM as F

# IDs for volumes and surfaces (must be the same as in xdmf files)

import solve_3D_heat_transfer

id_lipb = 6

# mesh_folder = "meshes/3D/wcll_ver_4/sym/"
mesh_folder = "../data/meshes/3D_test_meshes/"

# ##### Create SubMesh ##### #

mesh_full = F.MeshFromXDMF(
    volume_file=mesh_folder + "/mesh_domains_3D.xdmf",
    boundary_file=mesh_folder + "/mesh_boundaries_3D.xdmf",
)
mesh_sub = SubMesh(mesh_full.mesh, mesh_full.volume_markers, id_lipb)
XDMFFile("3D_Results/sub_mesh.xdmf").write(mesh_sub)

# project T onto submesh

V_CG1 = FunctionSpace(mesh_sub, "CG", 1)
T = project(solve_3D_heat_transfer.T, V_CG1, solver_type="mumps")
XDMFFile("3D_Results/T_sub_mesh.xdmf").write(T)
XDMFFile("3D_Results/T_sub_mesh.xdmf").write_checkpoint(
    T, "T", 0, XDMFFile.Encoding.HDF5, append=False
)
