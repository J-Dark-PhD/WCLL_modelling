import matplotlib.pyplot as plt
import numpy as np

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)

# ## Read data
volumes_bz_pipes = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

folder = '../../parametric_studies/varying_eurofer_trap_florian/transient'

# standard data
data_standard = np.genfromtxt(
    folder + '/standard/derived_quantities.csv',
    delimiter=',', names=True)
t_standard = data_standard["ts"]/86400
lipb_standard = data_standard['Total_solute_volume_6']
structure_standard = data_standard['Total_retention_volume_8'] + \
    data_standard['Total_retention_volume_9']
first_wall_standard = data_standard['Total_retention_volume_7']
bz_pipes_standard = \
    sum([data_standard['Total_retention_volume_{}'.format(vol)]
        for vol in volumes_bz_pipes])

# Breeder source
data_florian = np.genfromtxt(
    folder + '/florian/derived_quantities.csv',
    delimiter=',', names=True)
t_florian = data_florian["ts"]/86400
lipb_florian = data_florian['Total_solute_volume_6']
structure_florian = data_florian['Total_retention_volume_8'] + \
    data_florian['Total_retention_volume_9']
first_wall_florian = data_florian['Total_retention_volume_7']
bz_pipe_florian = data_florian['Total_retention_volume_10']
bz_pipes_florian = \
    sum([data_florian['Total_retention_volume_{}'.format(vol)]
        for vol in volumes_bz_pipes])

# LiPb
plt.figure()
plt.plot(
    t_standard, lipb_standard, color='black')
plt.plot(
    t_florian, lipb_florian, color='blue')
plt.xlabel(r"Time (days)")
plt.ylabel(r"Inventory (T m$^{-1}$)")
plt.title(label="Inventories in LiPb breeder")
plt.tight_layout()

# Structure
plt.figure()
plt.plot(
    t_standard, structure_standard, color='black')
plt.plot(
    t_florian, structure_florian, color='blue')
plt.xlabel(r"Time (days)")
plt.ylabel(r"Inventory (T m$^{-1}$)")
plt.title(label="Inventories in Eurofer outer structure")
plt.yscale('log')
plt.tight_layout()

# Pipes
plt.figure()
plt.plot(
    t_standard, bz_pipes_standard, color='black')
plt.plot(
    t_florian, bz_pipes_florian, color='blue')
plt.xlabel(r"Time (days)")
plt.ylabel(r"Inventory (T m$^{-1}$)")
plt.title(label="Inventories in Eurofer pipes")
plt.yscale('log')
plt.tight_layout()

# FW
plt.figure()
plt.plot(
    t_standard, first_wall_standard, color='black')
plt.plot(
    t_florian, first_wall_florian, color='blue')
plt.xlabel(r"Time (days)")
plt.ylabel(r"Inventory (T m$^{-1}$)")
plt.title(label="Inventories in first wall")
plt.tight_layout()

plt.show()
