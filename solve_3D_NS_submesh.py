"""
Needs to be run in serial
"""

from fenics import *
import properties
import tqdm.autonotebook
import numpy as np
import festim as F

# IDs for volumes and surfaces (must be the same as in xdmf files)

parameters["std_out_all_processes"] = False

id_lipb = 6

id_inlet = 34
id_outlet = 35

mesh_folder = "meshes/"

mesh_sub = Mesh()
XDMFFile("meshes/submesh_3D.xdmf").read(mesh_sub)

volume_markers_sub = MeshFunction("size_t", mesh_sub, mesh_sub.topology().dim(), 1)
surface_markers_sub = MeshFunction("size_t", mesh_sub, mesh_sub.topology().dim() - 1, 0)

sub_cells = str(len(volume_markers_sub))
begin("Succesfully loaded submesh with {} cells".format(sub_cells))
end()

boundary = CompiledSubDomain("on_boundary")
boundary_inlet = CompiledSubDomain(
    "on_boundary && near(x[0], L, tol) && x[1] <= h - DOLFIN_EPS",
    tol=1e-14,
    L=0.567,
    h=0.066,
)
boundary_oulet = CompiledSubDomain(
    "on_boundary && near(x[0], L, tol) && x[1] > h + DOLFIN_EPS",
    tol=1e-14,
    L=0.567,
    h=0.066,
)
boundary_symmetry = CompiledSubDomain(
    "on_boundary && near(x[2], 0, tol)",
    tol=1e-14,
)

id_walls = 5
id_sym = 4
boundary.mark(surface_markers_sub, id_walls)
boundary_inlet.mark(surface_markers_sub, id_inlet)
boundary_oulet.mark(surface_markers_sub, id_outlet)
boundary_symmetry.mark(surface_markers_sub, id_sym)


# XDMFFile("sm_sub.xdmf").write(surface_markers_sub)

# ##### Define Function Spaces ##### #

V = VectorFunctionSpace(mesh_sub, "CG", 2)
Q = FunctionSpace(mesh_sub, "CG", 1)

# ##### CFD --> Boundary conditions ##### #

# User defined boundary conditions
inlet_temperature = 598.15  # units: K
inlet_velocity = 2e-04  # units: ms-1

# Simulation boundary conditions
non_slip = Constant((0.0, 0.0, 0.0))

inflow = DirichletBC(
    V, Constant((-inlet_velocity, 0.0, 0.0)), surface_markers_sub, id_inlet
)

walls = DirichletBC(V, non_slip, surface_markers_sub, id_walls)

pressure_outlet = DirichletBC(Q, Constant(0.0), surface_markers_sub, id_outlet)

sym_boundary = DirichletBC(V.sub(2), Constant(0.0), surface_markers_sub, id_sym)

bcu = [inflow, walls, sym_boundary]
bcp = [pressure_outlet]

g = Constant((0.0, -9.81, 0.0))
T_0 = inlet_temperature

# ##### CFD --> Define Variational Parameters ##### #

u = TrialFunction(V)
p = TrialFunction(Q)
v = TestFunction(V)
q = TestFunction(Q)

u_n = Function(V)
u_ = Function(V)
p_n = Function(Q)
p_ = Function(Q)

begin("Projecting temperature field onto mesh")
end()
V_T = FunctionSpace(mesh_sub, "CG", 1)
T = Function(V_T)
XDMFFile("Results/3D_results/T_3D_sub.xdmf").read_checkpoint(T, "T", -1)

t = 0
total_time = 20
dt = 2e-01  # Time step size
num_steps = int(total_time / dt)

k = Constant(dt)
n = FacetNormal(mesh_sub)
U = 0.5 * (u_n + u)

# LiPb
mu = properties.visc_lipb(T)
rho = properties.rho_lipb(T)

def epsilon(u):
    return sym(nabla_grad(u))

def sigma(u, p):
    return 2 * mu * epsilon(u) - p * Identity(len(u))

# ##### Solver ##### #
dx = Measure("dx", subdomain_data=volume_markers_sub)
ds = Measure("ds", subdomain_data=surface_markers_sub)

# Tentative velocity step
F1 = rho * dot((u-u_n)/k, v) * dx
F1 += rho * dot(dot(u_n, nabla_grad(u_n)), v) * dx
F1 += inner(sigma(U, p_n), epsilon(v)) * dx
F1 += dot(p_n * n, v) * ds
F1 -= dot(mu * nabla_grad(U) * n, v) * ds

a1 = lhs(F1)
L1 = rhs(F1)

solver1 = KrylovSolver('bicgstab', "hypre_amg")
solver1.parameters['absolute_tolerance'] = 1e-08
solver1.parameters['relative_tolerance'] = 1e-08
solver1.parameters['maximum_iterations'] = 1000
solver1.parameters['report'] = False
solver1.parameters['monitor_convergence'] = False

# Pressure update
a2 = dot(nabla_grad(p), nabla_grad(q)) * dx
L2 = dot(nabla_grad(p_n), nabla_grad(q)) * dx
L2 -= (1/k) * div(u_) * q * dx

solver2 = KrylovSolver('bicgstab', "hypre_amg")
solver2.parameters['absolute_tolerance'] = 1e-08
solver2.parameters['relative_tolerance'] = 1e-08
solver2.parameters['maximum_iterations'] = 1000
solver2.parameters['report'] = False
solver2.parameters['monitor_convergence'] = False

# Velocity update
a3 = dot(u, v) * dx
L3 = dot(u_, v) * dx 
L3 -= k*dot(nabla_grad(p_ - p_n), v) * dx

solver3 = KrylovSolver('cg', "sor")
solver3.parameters['absolute_tolerance'] = 1e-08
solver3.parameters['relative_tolerance'] = 1e-08
solver3.parameters['maximum_iterations'] = 1000
solver3.parameters['report'] = False
solver3.parameters['monitor_convergence'] = False

# Assemble matrices
A1 = assemble(a1)
A2 = assemble(a2)
A3 = assemble(a3)

[bc.apply(A1) for bc in bcu]
[bc.apply(A2) for bc in bcp]

results_folder = "Results/velocity_fields/"
velocity_file = XDMFFile(results_folder + "u_3D_sub.xdmf")
pressure_file = XDMFFile("Results/3D_results/p_3D_sub.xdmf")

max_u = []

# Time-stepping
progress = tqdm.autonotebook.tqdm(desc="Solving Navier-Stokes", total=num_steps)
for i in range(num_steps):
    progress.update(1)
    # Update current time step
    t += dt

    # Compute tentative velocity step
    b1 = assemble(L1)
    [bc.apply(A1, b1) for bc in bcu]
    solver1.solve(A1, u_.vector(), b1)

    # Pressure correction
    b2 = assemble(L2)
    [bc.apply(A2, b2) for bc in bcp]
    solver2.solve(A2, p_.vector(), b2)

    # Velocity correction
    b3 = assemble(L3)
    [bc.apply(A3, b3) for bc in bcu]
    solver3.solve(A3, u_.vector(), b3)

    # Move to next time step
    u_n.assign(u_)
    p_n.assign(p_)

    velocity_file.write(u_, t)
    # pressure_file.write(p_, t)

    max_u.append(u_.vector().max())
    np.savetxt(results_folder + "3D_case_max_u.txt", np.array(max_u))

# # ### extend from subdomain to full mesh

# print("Extending the function")
# ele_full = VectorElement("CG", mesh_full.mesh.ufl_cell(), 2)
# V = FunctionSpace(mesh_full.mesh, ele_full)
# u_full = Function(V)
# v_full = TestFunction(V)

# mesh_full.define_markers()
# mesh_full.define_measures()

# F = inner(u_full, v_full) * mesh_full.dx
# F += -inner(u_out, v_full) * mesh_full.dx(id_lipb)
# print("Projecting onto full mesh")
# solve(
#     F == 0,
#     u_full,
#     bcs=[],
#     solver_parameters={"newton_solver": {"linear_solver": "gmres"}},
# )

# print("Exporting velocity map")
# XDMFFile("Results/3D_results/u_full_3D.xdmf").write_checkpoint(
#     u_full, "u", 0, XDMFFile.Encoding.HDF5, append=False
# )
