import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

# plt.rc('text', usetex=True)
# plt.rc('font', family='serif', size=12)

folder = '../../parametric_studies/varying_eurofer_trap_florian/transient'
data_standard = np.genfromtxt(
    folder + '/standard/derived_quantities.csv',
    delimiter=',', names=True)
t = data_standard["ts"]
eurofer = data_standard['Flux_surface_39_solute']*-1
pipe_1 = data_standard['Flux_surface_40_solute']*-1
pipe_2 = data_standard['Flux_surface_41_solute']*-1
pipe_3 = data_standard['Flux_surface_42_solute']*-1
pipe_4 = data_standard['Flux_surface_43_solute']*-1
pipe_5 = data_standard['Flux_surface_44_solute']*-1
pipe_6 = data_standard['Flux_surface_45_solute']*-1
pipe_7 = data_standard['Flux_surface_46_solute']*-1
pipe_8 = data_standard['Flux_surface_47_solute']*-1
pipe_9 = data_standard['Flux_surface_48_solute']*-1
pipe_10 = data_standard['Flux_surface_49_solute']*-1


data_florian = np.genfromtxt(
    folder + '/florian/derived_quantities.csv',
    delimiter=',', names=True)
t_florian = data_florian["ts"]
eurofer_florian = data_florian['Flux_surface_39_solute']*-1
pipe_1_florian = data_florian['Flux_surface_40_solute']*-1
pipe_2_florian = data_florian['Flux_surface_41_solute']*-1
pipe_3_florian = data_florian['Flux_surface_42_solute']*-1
pipe_4_florian = data_florian['Flux_surface_43_solute']*-1
pipe_5_florian = data_florian['Flux_surface_44_solute']*-1
pipe_6_florian = data_florian['Flux_surface_45_solute']*-1
pipe_7_florian = data_florian['Flux_surface_46_solute']*-1
pipe_8_florian = data_florian['Flux_surface_47_solute']*-1
pipe_9_florian = data_florian['Flux_surface_48_solute']*-1
pipe_10_florian = data_florian['Flux_surface_49_solute']*-1


# fig, axs = plt.subplots(1, 1, sharey=True, figsize=(9.6, 4.8))

plt.figure()

# plt.sca(axs[0])
x_annotation = t[-1]*1.15

colour = 'black'
# plt.plot(t, eurofer, color=colour)
plt.plot(
    t_florian, eurofer_florian,
    color=colour, linestyle="dashed", alpha=0.5)
plt.annotate(
    "FW cooling", (x_annotation, eurofer[-1]), color=colour)

plt.ylabel(r"Surface flux (T m$^{-1}$ s$^{-1}$)")

colour = 'forestgreen'
front = pipe_1 + pipe_5 + pipe_7
front_florian = pipe_1_florian + pipe_5_florian + pipe_7_florian
# plt.plot(t, front, color=colour)
plt.plot(
    t_florian, front_florian,
    color=colour, linestyle="dashed", alpha=0.5)
plt.annotate(
    "Front BZ pipes", (x_annotation, front[-1]*1.2), color=colour)


colour = 'purple'
middle_flux = pipe_2 + pipe_6 + pipe_8
middle_flux_florian = pipe_2_florian + pipe_6_florian + pipe_8_florian
# plt.plot(t, middle_flux, color=colour)
plt.plot(
    t_florian, middle_flux_florian,
    color=colour, linestyle="dashed", alpha=0.5)
plt.annotate(
    "Middle BZ pipes", (x_annotation, middle_flux[-1]*0.8), color=colour)

colour = 'steelblue'
rear_flux = pipe_3 + pipe_4 + pipe_9 + pipe_10
rear_flux_florian = pipe_3_florian + pipe_4_florian + pipe_9_florian + \
     pipe_10_florian
# plt.plot(t, rear_flux, color=colour)
plt.plot(
    # t_florian, rear_flux_florian,
    color=colour, linestyle="dashed", alpha=0.5)
plt.annotate(
    "Rear BZ pipes", (x_annotation, rear_flux[-1]*0.9),
    color=colour)


# plt.annotate("BZ pipes", (x_annotation + 300, middle_flux[-1]*1.1))

plt.yscale("log")
plt.xlabel(r"Time (s)")
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xscale('log')
plt.xlim(right=5e6)
# plt.ylim(bottom=1e14, top=2e16)
custom_lines = (Line2D([0], [0], color='grey', linestyle='solid'),
                Line2D([0], [0], color='grey', linestyle='dashed'))
plt.legend(custom_lines, ['standard', 'No standard'])
# plt.tight_layout()
plt.show()
