from parameters_2D import my_model, tungsten, id_eurofers, id_W, id_lipb
from solve_H_transport import run_H_transport
import festim as F
import properties


mesh_folder = "meshes/"
my_model.mesh = F.MeshFromXDMF(
    volume_file=mesh_folder + "mesh_domains_floriane.xdmf",
    boundary_file=mesh_folder + "mesh_boundaries_floriane.xdmf",
    # volume_file=mesh_folder + "mesh_domains_2D.xdmf",
    # boundary_file=mesh_folder + "mesh_boundaries_2D.xdmf",
)

materials_eurofers = [
    F.Material(
        id=id_vol,
        D_0=(2.52e-07) / (3**0.5),
        E_D=0.16,
        S_0=1.06e23,
        E_S=0.27,
    )
    for id_vol in id_eurofers
]

trap_W_1 = F.Trap(
    k_0=properties.D_0_W / (1.1e-10**2 * 6 * properties.atom_density_W),
    E_k=properties.E_D_W,
    p_0=1e13,
    E_p=0.87,
    density=1.3e-3 * properties.atom_density_W,
    materials=tungsten,
)
trap_W_2 = F.Trap(
    k_0=properties.D_0_W / (1.1e-10**2 * 6 * properties.atom_density_W),
    E_k=properties.E_D_W,
    p_0=1e13,
    E_p=1.00,
    density=4e-4 * properties.atom_density_W,
    materials=tungsten,
)
trap_eurofer_1 = F.Trap(
    k_0=1.94e-17,
    E_k=0.16,
    p_0=1e13,
    E_p=0.51,
    density=1.71e26,
    materials=materials_eurofers,
)
trap_eurofer_2 = F.Trap(
    k_0=1.94e-17,
    E_k=0.16,
    p_0=1e13,
    E_p=1.27,
    density=2.11e22,
    materials=materials_eurofers,
)
trap_eurofer_3 = F.Trap(
    k_0=1.94e-17,
    E_k=0.16,
    p_0=1e13,
    E_p=1.65,
    density=3.88e23,
    materials=materials_eurofers,
)
my_model.traps = F.Traps(
    [
        trap_W_1,
        trap_W_2,
        trap_eurofer_1,
        trap_eurofer_2,
        trap_eurofer_3,
    ],
)

results_folder = "Results/parametric_studies/floriane_traps/"
my_derived_quantities = F.DerivedQuantities(
    filename=results_folder + "derived_quantities.csv",
    nb_iterations_between_exports=1,
)
my_derived_quantities.derived_quantities = [
    F.TotalVolume("solute", volume=id_W),
    *[F.TotalVolume("solute", volume=id_vol) for id_vol in id_eurofers],
    F.TotalVolume("solute", volume=id_lipb),
    F.TotalVolume("retention", volume=id_W),
    *[F.TotalVolume("retention", volume=id_vol) for id_vol in id_eurofers],
    F.TotalVolume("retention", volume=id_lipb),
    # *[
    #     F.SurfaceFlux("solute", surface=id_surf)
    #     for id_surf in ids_bz_coolant_interfaces
    # ],
    # *[
    #     F.SurfaceFlux("solute", surface=id_surf)
    #     for id_surf in ids_fw_coolant_interfaces
    # ],
    # F.SurfaceFlux("solute", surface=id_plasma_facing_wall),
]
my_model.exports = F.Exports(
    [
        # F.XDMFExport("solute", folder=results_folder, mode=1),
        # F.XDMFExport("retention", folder=results_folder, mode=1),
        # F.XDMFExport("1", folder=results_folder, label="trap_W_1", mode=1),
        # F.XDMFExport("2", folder=results_folder, label="trap_W_2", mode=1),
        # F.XDMFExport("3", folder=results_folder, label="trap_eurofer", mode=1),
        # F.XDMFExport("3", folder=results_folder, label="trap_eurofer_1", mode=1),
        # F.XDMFExport("4", folder=results_folder, label="trap_eurofer_2", mode=1),
        # F.XDMFExport("5", folder=results_folder, label="trap_eurofer_3", mode=1),
        # F.XDMFExport("T", folder=results_folder, mode=1),
        my_derived_quantities,
    ]
)

my_model.initialise()
run_H_transport(model=my_model)
