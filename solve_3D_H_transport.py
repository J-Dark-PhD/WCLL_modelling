from fenics import *
from context import FESTIM as F
from properties import S_0_lipb, E_S_lipb
from parameters_3D import my_model, id_lipb


def run_H_transport(S_0=S_0_lipb, E_S=E_S_lipb):
    # create a simulation with these normal parameters

    my_model.initialise()

    # read the u_full function written in solve_NS_submesh.py
    mesh = my_model.mesh.mesh
    V_ele = VectorElement("CG", mesh.ufl_cell(), 3)
    V_u = FunctionSpace(mesh, V_ele)

    mesh_cfd = "3D_Results/u_full.xdmf"
    u = Function(V_u)
    XDMFFile(mesh_cfd).read_checkpoint(u, "u", -1)

    # modify the form F
    id_flow = id_lipb
    test_function_solute = split(my_model.h_transport_problem.v)[0]
    solute = split(my_model.h_transport_problem.u)[0]
    dx = my_model.mesh.dx
    S = S_0 * exp(-E_S / F.k_B / my_model.T.T)
    my_model.h_transport_problem.F += inner(
        dot(grad(S * solute), u), test_function_solute
    ) * dx(id_flow)

    # run the simulation with the modified formulation
    my_model.run()


if __name__ == "__main__":
    run_H_transport()
