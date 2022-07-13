import matplotlib.pyplot as plt
import numpy as np

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=12)

red_W = (171/255, 15/255, 26/255)
grey_eurofer = (153/255, 153/255, 153/255)
green_lipb = (146/255, 196/255, 125/255)


# ## Read data
volumes_bz_pipes = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

folder = '../../parametric_studies/varying_source/transient'

# both_traps sources
data_both_traps = np.genfromtxt(
    folder + '/both_traps/derived_quantities.csv',
    delimiter=',', names=True)
t_both_traps = data_both_traps["ts"]/86400
lipb_both_traps = data_both_traps['Total_solute_volume_6']
structure_both_traps = data_both_traps['Total_retention_volume_8'] + \
    data_both_traps['Total_retention_volume_9']
first_wall_both_traps = data_both_traps['Total_retention_volume_7']
bz_pipes_both_traps = \
    sum([data_both_traps['Total_retention_volume_{}'.format(vol)]
        for vol in volumes_bz_pipes])

# breeder_traps source
data_breeder_traps = np.genfromtxt(
    folder + '/breeder_traps/derived_quantities.csv',
    delimiter=',', names=True)
t_breeder_traps = data_breeder_traps["ts"]/86400
lipb_breeder_traps = data_breeder_traps['Total_solute_volume_6']
structure_breeder_traps = data_breeder_traps['Total_retention_volume_8'] + \
    data_breeder_traps['Total_retention_volume_9']
first_wall_breeder_traps = data_breeder_traps['Total_retention_volume_7']
bz_pipe_breeder_traps = data_breeder_traps['Total_retention_volume_10']
bz_pipes_breeder_traps = \
    sum([data_breeder_traps['Total_retention_volume_{}'.format(vol)]
        for vol in volumes_bz_pipes])

# plasma_traps source
data_plasma_traps = np.genfromtxt(
    folder + '/plasma_traps/derived_quantities.csv',
    delimiter=',', names=True)
t_plasma_traps = data_plasma_traps["ts"]/86400
lipb_plasma_traps = data_plasma_traps['Total_solute_volume_6']
structure_plasma_traps = data_plasma_traps['Total_retention_volume_8'] + \
    data_plasma_traps['Total_retention_volume_9']
first_wall_plasma_traps = data_plasma_traps['Total_retention_volume_7']
bz_pipe_plasma_traps = data_plasma_traps['Total_retention_volume_10']
bz_pipes_plasma_traps = \
    sum([data_plasma_traps['Total_retention_volume_{}'.format(vol)]
        for vol in volumes_bz_pipes])


# ## Plot
fig = plt.figure(figsize=(4.5, 9))
linestyle_no_trap = "dashed"

# create one big plot to have a common y label
ax = fig.add_subplot(111)
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['right'].set_color('none')
ax.tick_params(
    labelcolor='w', top=False, bottom=False, left=False, right=False)
ax.set_ylabel(r"Inventory (T m$^{-1}$)")

# LiPb
ax1 = fig.add_subplot(411)
plt.sca(ax1)

plt.plot(
    t_both_traps, lipb_both_traps, color='black')
plt.plot(
    t_breeder_traps, lipb_breeder_traps, color=green_lipb)
plt.plot(
    t_plasma_traps, lipb_plasma_traps, color=red_W)
plt.annotate(
    "LiPb", (t_both_traps[-1], lipb_both_traps[-1]),
    xytext=(t_both_traps[-1]*1.1, lipb_both_traps[-1]), color= 'black')


# Structure
ax2 = fig.add_subplot(412)
plt.sca(ax2)
plt.plot(
    t_both_traps, structure_both_traps, color='black')
plt.plot(
    t_breeder_traps, structure_breeder_traps, color=green_lipb)
plt.plot(
    t_plasma_traps, structure_plasma_traps, color=red_W)
plt.annotate(
    "Structure", (t_both_traps[-1], structure_both_traps[-1]),
    xytext=(t_both_traps[-1]*1.1, structure_both_traps[-1]), color='black')

# Pipes
ax3 = fig.add_subplot(413)
plt.sca(ax3)
plt.plot(
    t_both_traps, bz_pipes_both_traps, color='black')
plt.plot(
    t_breeder_traps, bz_pipes_breeder_traps, color=green_lipb)
plt.plot(
    t_plasma_traps, bz_pipes_plasma_traps, color=red_W)
plt.annotate(
    "BZ pipes", (t_both_traps[-1], bz_pipes_both_traps[-1]),
    xytext=(t_both_traps[-1]*1.1, bz_pipes_both_traps[-1]), color='black')


# FW
ax4 = fig.add_subplot(414)
plt.sca(ax4)
plt.plot(
    t_both_traps, first_wall_both_traps, color='black')
plt.plot(
    t_breeder_traps, first_wall_breeder_traps, color=green_lipb)
plt.plot(
    t_plasma_traps, first_wall_plasma_traps, color=red_W)
plt.annotate(
    "First wall", (t_both_traps[-1], first_wall_both_traps[-1]),
    xytext=(t_both_traps[-1]*1.1, first_wall_both_traps[-1]), color='black')

# axs[-1].set_ylabel(r"Inventory (T m$^{-1}$)")

plt.xlabel(r"Time (days)")

for ax in [ax1, ax2, ax3, ax4]:
    plt.sca(ax)
    ax.get_shared_x_axes().join(ax, ax4)
    # plt.ylabel(r"Inventory (T m$^{-1}$)")  # "Inventory \n" + r"(T m$^{-1}$)"
    # plt.ylim(bottom=0)
    plt.yscale('log')
    # plt.xlim(left=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# remove the xticks for top plots
ax1.set_xticklabels([])
ax2.set_xticklabels([])
ax3.set_xticklabels([])

plt.tight_layout()

plt.show()
