"""
Needs to be run in serial
"""

from fenics import *
import FESTIM as F
import properties
import solve_3D_heat_transfer

# IDs for volumes and surfaces (must be the same as in xdmf files)

id_lipb = 6

id_inlet = 34
id_outlet = 35

mesh_folder = "meshes/"

# ##### Create SubMesh ##### #
mesh_full = F.MeshFromXDMF(
    volume_file=mesh_folder + "mesh_domains_3D.xdmf",
    boundary_file=mesh_folder + "mesh_boundaries_3D.xdmf",
)

mesh_sub = SubMesh(mesh_full.mesh, mesh_full.volume_markers, id_lipb)

volume_markers_sub = MeshFunction("size_t", mesh_sub, mesh_sub.topology().dim(), 1)
surface_markers_sub = MeshFunction("size_t", mesh_sub, mesh_sub.topology().dim() - 1, 0)

boundary = CompiledSubDomain("on_boundary")
boundary_inlet = CompiledSubDomain(
    "on_boundary && near(x[0], \
                                   L, tol) && x[1] <= h",
    tol=1e-14,
    L=0.567,
    h=0.066,
)
boundary_oulet = CompiledSubDomain(
    "on_boundary && near(x[0], \
                                   L, tol) && x[1] > h + DOLFIN_EPS",
    tol=1e-14,
    L=0.567,
    h=0.066,
)
boundary_symmetry = CompiledSubDomain(
    "on_boundary && near(x[2], \
                                      0, tol) && x[1] >= 0",
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

V_ele = VectorElement("CG", mesh_sub.ufl_cell(), 3)
Q_ele = FiniteElement("CG", mesh_sub.ufl_cell(), 1)
W = FunctionSpace(mesh_sub, MixedElement([V_ele, Q_ele]))

# ##### CFD --> Boundary conditions ##### #

# User defined boundary conditions
inlet_temperature = 598.15  # units: K
inlet_velocity = 1.27e-04  # units: ms-1

# Simulation boundary conditions
non_slip = Constant((0.0, 0.0, 0.0))

inflow = DirichletBC(
    W.sub(0), Constant((-inlet_velocity, 0.0, 0.0)), surface_markers_sub, id_inlet
)

walls = DirichletBC(W.sub(0), non_slip, surface_markers_sub, id_walls)

pressure_outlet = DirichletBC(W.sub(1), Constant(0), surface_markers_sub, id_outlet)

sym_boundary = DirichletBC(W.sub(0).sub(2), Constant(0.0), surface_markers_sub, id_sym)

bcu = [inflow, pressure_outlet, walls, sym_boundary]

g = Constant((0.0, -9.81, 0.0))
T_0 = inlet_temperature

# ##### CFD --> Define Variational Parameters ##### #

v, q = TestFunctions(W)
up = Function(W)
u, p = split(up)

# ##### CFD --> Fluid Materials properties ##### #
V_CG1 = FunctionSpace(mesh_sub, "CG", 1)
# T = 300
# T.set_allow_extrapolation(True)
T = project(solve_3D_heat_transfer.T, V_CG1, solver_type="mumps")

# LiPb
Cp_lipb = properties.Cp_lipb(T)
rho_lipb = properties.rho_lipb(T)
rho_0_lipb = properties.rho_0_lipb
thermal_cond_lipb = properties.thermal_cond_lipb(T)
visc_lipb = properties.visc_lipb(T)
beta_lipb = properties.beta_lipb(T)

# Fluid properties
rho_0 = rho_0_lipb
mu = visc_lipb
beta = beta_lipb

# ##### Solver ##### #
dx = Measure("dx", subdomain_data=volume_markers_sub)
ds = Measure("ds", subdomain_data=surface_markers_sub)

F = (
    #           momentum
    rho_0 * inner(grad(u), grad(v)) * dx
    - inner(p, div(v)) * dx
    + mu * inner(dot(grad(u), u), v) * dx
    - (beta * rho_0) * inner((T - T_0) * g, v) * dx
    #           continuity
    + inner(div(u), q) * dx
)

print("Solving Navier-Stokes")
solve(F == 0, up, bcu, solver_parameters={"newton_solver": {"linear_solver": "mumps"}})

u_export = Function(W)
u_export.assign(up)
u_out, p_out = u_export.split()
print("Exporting submesh velocity map")
XDMFFile("Results/3D_results/u_sub_3D.xdmf").write_checkpoint(
    u_out, "u", 0, XDMFFile.Encoding.HDF5, append=False
)

# ### extend from subdomain to full mesh

print("Extending the function")


ele_full = VectorElement("CG", mesh_full.mesh.ufl_cell(), 3)
V = FunctionSpace(mesh_full.mesh, ele_full)
u_full = Function(V)
v_full = TestFunction(V)

mesh_full.define_markers()
mesh_full.define_measures()

F = inner(u_full, v_full) * mesh_full.dx
F += -inner(u_out, v_full) * mesh_full.dx(id_lipb)
print("Projecting onto full mesh")
solve(
    F == 0,
    u_full,
    bcs=[],
    solver_parameters={"newton_solver": {"linear_solver": "gmres"}},
)

print("Exporting velocity map")
XDMFFile("Results/3D_results/u_full.xdmf").write_checkpoint(
    u_full, "u", 0, XDMFFile.Encoding.HDF5, append=False
)
