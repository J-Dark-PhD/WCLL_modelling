import sympy as sp
import festim as F
import properties

# IDs for volumes and surfaces (must be the same as in xdmf files)
id_lipb = 6
id_W = 7
id_structure = 8
id_baffle = 9
id_pipe_1 = 10
id_pipe_2 = 11
id_pipe_3 = 12
id_pipe_4 = 13
id_pipe_5 = 14
id_pipe_6 = 15
id_pipe_7 = 16
id_pipe_8 = 17
id_pipe_9 = 18
id_channel_pipe_top = 19
id_channel_pipe_bot = 20
id_eurofers = [
    id_structure,
    id_baffle,
    id_pipe_1,
    id_pipe_2,
    id_pipe_3,
    id_pipe_4,
    id_pipe_5,
    id_pipe_6,
    id_pipe_7,
    id_pipe_8,
    id_pipe_9,
    id_channel_pipe_top,
    id_channel_pipe_bot,
]


id_fw_coolant_interface = 21
id_pipe_1_coolant_interface = 22
id_pipe_2_coolant_interface = 23
id_pipe_3_coolant_interface = 24
id_pipe_4_coolant_interface = 25
id_pipe_5_coolant_interface = 26
id_pipe_6_coolant_interface = 27
id_pipe_7_coolant_interface = 28
id_pipe_8_coolant_interface = 29
id_pipe_9_coolant_interface = 30
id_channel_pipe_top_coolant_interface = 31
id_channel_pipe_bot_coolant_interface = 32
ids_pipe_coolant_interface = [
    id_pipe_1_coolant_interface,
    id_pipe_2_coolant_interface,
    id_pipe_3_coolant_interface,
    id_pipe_4_coolant_interface,
    id_pipe_5_coolant_interface,
    id_pipe_6_coolant_interface,
    id_pipe_7_coolant_interface,
    id_pipe_8_coolant_interface,
    id_pipe_9_coolant_interface,
    id_channel_pipe_top_coolant_interface,
    id_channel_pipe_bot_coolant_interface,
]

id_plasma_facing_surface = 33
id_inlet = 34
id_outlet = 35

my_model = F.Simulation(log_level=20)

# define mesh
mesh_folder = "meshes/"
my_model.mesh = F.MeshFromXDMF(
    volume_file=mesh_folder + "mesh_domains_3D.xdmf",
    boundary_file=mesh_folder + "mesh_boundaries_3D.xdmf",
)

# define materials
tungsten = F.Material(
    id=id_W,
    D_0=properties.D_0_W,
    E_D=properties.E_D_W,
    S_0=properties.S_0_W,
    E_S=properties.E_S_W,
    thermal_cond=properties.thermal_cond_W,
    heat_capacity=properties.Cp_W,
    rho=properties.rho_W,
)
materials_eurofers = [
    F.Material(
        id=id_vol,
        D_0=properties.D_0_eurofer,
        E_D=properties.E_D_eurofer,
        S_0=properties.S_0_eurofer,
        E_S=properties.E_S_eurofer,
        thermal_cond=properties.thermal_cond_eurofer,
        heat_capacity=properties.Cp_eurofer,
        rho=properties.rho_eurofer,
    )
    for id_vol in id_eurofers
]
lipb = F.Material(
    id=id_lipb,
    D_0=properties.D_0_lipb,
    E_D=properties.E_D_lipb,
    S_0=properties.S_0_lipb,
    E_S=properties.E_S_lipb,
    thermal_cond=properties.thermal_cond_lipb,
    heat_capacity=properties.Cp_lipb,
    rho=properties.rho_lipb,
)
my_model.materials = F.Materials([tungsten, *materials_eurofers, lipb])

# define traps
trap_W_1 = F.Trap(
    k_0=properties.D_0_W / (1.1e-10**2 * 6 * properties.atom_density_W),
    E_k=properties.E_D_W,
    p_0=1e13,
    E_p=0.87,
    density=1.3e-3 * properties.atom_density_W,
    materials=tungsten,
)
trap_W_2 = F.Trap(
    k_0=4.1e-7 / (1.1e-10**2 * 6 * properties.atom_density_W),
    E_k=properties.E_D_W,
    p_0=1e13,
    E_p=1.00,
    density=4e-4 * properties.atom_density_W,
    materials=tungsten,
)

trap_eurofer_1 = F.Trap(
    k_0=properties.D_0_eurofer
    / (1.1e-10**2)
    * 0.8165
    / properties.atom_density_eurofer,
    E_k=properties.E_D_eurofer,
    p_0=1e13,
    E_p=properties.trap_energy_eurofer,
    density=properties.trap_density_eurofer,
    materials=materials_eurofers,
)
my_model.traps = F.Traps(
    [
        trap_eurofer_1,
        trap_W_1,
        trap_W_2,
    ]
)

# define sources
my_model.T = F.HeatTransferProblem(transient=False, linear_solver="mumps")
my_model.sources = [
    F.Source(
        value=23.2e06 * sp.exp(-71.74 * F.x),
        volume=id_W,
        field="T",
    ),
    F.Source(
        value=(
            (9.6209e06 * sp.exp(-12.02 * F.x)) * (F.x < 0.15)
            + (4.7109e06 * sp.exp(-7.773 * F.x)) * (F.x >= 0.15)
        ),
        volume=id_eurofers,
        field="T",
    ),
    F.Source(
        value=
        # mine
        # (3.9108e05 * F.x ** (-1.213)) * (F.x < 0.15)
        # + 8.4629e06 * sp.exp(-5.485 * F.x) * (F.x >= 0.15)
        # alt
        (6.3034e05 * F.x ** (-0.789)) * (F.x < 0.15)
        + 3.4588e06 * sp.exp(-3.993 * F.x) * (F.x >= 0.15),
        # candido
        # (
        #     25.53 * sp.exp(-0.5089 * F.x * 1e2)
        #     + 5.443 * sp.exp(-0.0879 * F.x * 1e2)
        # )
        # * 1e6,
        volume=id_lipb,
        field="T",
    ),
    F.Source(
        value=6.022e23
        * 1e6
        * (
            1.044e-11 * sp.exp(-0.2182 * F.x * 1e2)
            + 6.514e-12 * sp.exp(-0.04106 * F.x * 1e2)
        ),
        volume=id_lipb,
        field="solute",
    ),
]

# define boundary conditions
plasma_heat_flux = F.FluxBC(surfaces=id_plasma_facing_surface, value=0.5e06, field="T")
convective_flux_bz = F.ConvectiveFlux(
    h_coeff=5.025e03, T_ext=584.65, surfaces=ids_pipe_coolant_interface
)
convective_flux_fw = F.ConvectiveFlux(
    h_coeff=8.876e03 * 5, T_ext=584.65, surfaces=id_fw_coolant_interface
)
inlet_temp = F.DirichletBC(surfaces=id_inlet, value=598.15, field="T")
inlet_conc = F.DirichletBC(surfaces=id_inlet, value=0, field=0)
recomb_flux = F.RecombinationFlux(
    Kr_0=properties.Kr_0_eurofer,
    E_Kr=properties.E_Kr_eurofer,
    order=2,
    surfaces=[*ids_pipe_coolant_interface, id_fw_coolant_interface],
)
implantation_flux = F.ImplantationDirichlet(
    surfaces=id_plasma_facing_surface,
    phi=1e20,
    R_p=3e-09,
    D_0=properties.D_0_W,
    E_D=properties.E_D_W,
)
my_model.boundary_conditions = [
    plasma_heat_flux,
    convective_flux_bz,
    convective_flux_fw,
    inlet_temp,
    inlet_conc,
    recomb_flux,
    implantation_flux,
]

folder = "Results/3D_results/"
my_derived_quantities = F.DerivedQuantities(
    filename=folder + "derived_quantities.csv",
    nb_iterations_between_exports=1,
)
my_derived_quantities.derived_quantities = [
    F.TotalVolume("solute", volume=id_W),
    *[F.TotalVolume("solute", volume=id_vol) for id_vol in id_eurofers],
    F.TotalVolume("solute", volume=id_lipb),
    F.TotalVolume("retention", volume=id_W),
    *[F.TotalVolume("retention", volume=id_vol) for id_vol in id_eurofers],
    F.TotalVolume("retention", volume=id_lipb),
    *[
        F.SurfaceFlux("solute", surface=id_surf)
        for id_surf in ids_pipe_coolant_interface
    ],
    F.SurfaceFlux("solute", surface=id_fw_coolant_interface),
    F.SurfaceFlux("solute", surface=id_plasma_facing_surface),
]
my_model.exports = F.Exports(
    [
        F.XDMFExport("solute", folder=folder, mode=1),
        # F.XDMFExport("retention", folder=folder, mode=1),
        # F.XDMFExport("1", folder=folder, label="trap_W_1", mode=1),
        # F.XDMFExport("2", folder=folder, label="trap_W_2", mode=1),
        # F.XDMFExport("3", folder=folder, label="trap_eurofer_1", mode=1),
        F.XDMFExport("T", folder=folder, mode=1),
        # my_derived_quantities,
    ]
)

# define solving parameters
my_model.settings = F.Settings(
    transient=False,
    absolute_tolerance=1e12,
    relative_tolerance=1e-08,
    traps_element_type="DG",
    maximum_iterations=50,
    chemical_pot=True,
    linear_solver="mumps",
)

if __name__ == "__main__":
    my_model.initialise()
    my_model.run()
