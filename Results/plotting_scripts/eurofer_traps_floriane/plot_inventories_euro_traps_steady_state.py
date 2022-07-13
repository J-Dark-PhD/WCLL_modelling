import matplotlib.pyplot as plt
import numpy as np

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)

# ## Read data
volumes_bz_pipes = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
x_values = ["Standard case", "floriane"]

folder = '../../parametric_studies/varying_eurofer_trap_floriane/steady_state'

# standard data
data_standard = np.genfromtxt(
    folder + '/standard/derived_quantities.csv',
    delimiter=',', names=True)
lipb_standard = data_standard['Total_solute_volume_6']
structure_standard = data_standard['Total_retention_volume_8'] + \
    data_standard['Total_retention_volume_9']
first_wall_standard = data_standard['Total_retention_volume_7']
bz_pipes_standard = \
    sum([data_standard['Total_retention_volume_{}'.format(vol)]
        for vol in volumes_bz_pipes])

# floriane data
data_floriane = np.genfromtxt(
    folder + '/floriane/derived_quantities.csv',
    delimiter=',', names=True)
lipb_floriane = data_floriane['Total_solute_volume_6']
structure_floriane = data_floriane['Total_retention_volume_8'] + \
    data_floriane['Total_retention_volume_9']
first_wall_floriane = data_floriane['Total_retention_volume_7']
bz_pipe_floriane = data_floriane['Total_retention_volume_10']
bz_pipes_floriane = \
    sum([data_floriane['Total_retention_volume_{}'.format(vol)]
        for vol in volumes_bz_pipes])


print("Inventory in standard LiPb = {:.2e}".format(lipb_standard))
print("Inventory in floriane LiPb = {:.2e}".format(lipb_floriane))
print("Difference in LiPb = {:.1f}".format(((lipb_floriane-lipb_standard)/lipb_standard)*100), " %")
print("Inventory in standard structure = {:.2e}".format(structure_standard))
print("Inventory in floriane structure = {:.2e}".format(structure_floriane))
print("Difference in structure = {:.1f}".format(((structure_floriane-structure_standard)/structure_standard)*100), " %")
print("Inventory in standard BZ Pipes = {:.2e}".format(bz_pipes_standard))
print("Inventory in floriane BZ Pipes = {:.2e}".format(bz_pipes_floriane))
print("Difference in BZ Pipes = {:.1f}".format(((bz_pipes_floriane-bz_pipes_standard)/bz_pipes_standard)*100), " %")
print("Inventory in standard FW = {:.2e}".format(first_wall_standard))
print("Inventory in floriane FW = {:.2e}".format(first_wall_floriane))
print("Difference in FW = {:.1f}".format(((first_wall_floriane-first_wall_standard)/first_wall_standard)*100), " %")

# # LiPb
# plt.figure()
# plt.bar(
#     x_values[0], lipb_standard, width=0.5, color='black')
# plt.bar(
#     x_values[1], lipb_floriane, width=0.5, color='blue')
# plt.ylabel(r"Inventory (T m$^{-1}$)")
# plt.title(label="Inventories in LiPb breeder")
# plt.tight_layout()

# # Structure
# plt.figure()
# plt.bar(
#     x_values[0], structure_standard, width=0.5, color='black')
# plt.bar(
#     x_values[1], structure_floriane, width=0.5, color='blue')
# plt.ylabel(r"Inventory (T m$^{-1}$)")
# plt.title(label="Inventories in eurofer structure")
# plt.tight_layout()

# # Pipes
# plt.figure()
# plt.bar(
#     x_values[0], bz_pipes_standard, width=0.5, color='black')
# plt.bar(
#     x_values[1], bz_pipe_floriane, width=0.5, color='blue')
# plt.ylabel(r"Inventory (T m$^{-1}$)")
# plt.title(label="Inventories in eurofer pipes")
# plt.tight_layout()

# # FW
# plt.figure()
# plt.bar(
#     x_values[0], first_wall_standard, width=0.5, color='black')
# plt.bar(
#     x_values[1], first_wall_floriane, width=0.5, color='blue')
# plt.ylabel(r"Inventory (T m$^{-1}$)")
# plt.title(label="Inventories in LiPb breeder")
# plt.tight_layout()

# plt.show()
