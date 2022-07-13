import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=12)

folder = '../../parametric_studies/varying_buoyancy/transient'
data_buoyancy = np.genfromtxt(
    folder + '/with_buoyancy/derived_quantities.csv',
    delimiter=',', names=True)

t = data_buoyancy["ts"]
eurofer = data_buoyancy['Flux_surface_39_solute']*-1
pipe_1 = data_buoyancy['Flux_surface_40_solute']*-1
pipe_2 = data_buoyancy['Flux_surface_41_solute']*-1
pipe_3 = data_buoyancy['Flux_surface_42_solute']*-1
pipe_4 = data_buoyancy['Flux_surface_43_solute']*-1
pipe_5 = data_buoyancy['Flux_surface_44_solute']*-1
pipe_6 = data_buoyancy['Flux_surface_45_solute']*-1
pipe_7 = data_buoyancy['Flux_surface_46_solute']*-1
pipe_8 = data_buoyancy['Flux_surface_47_solute']*-1
pipe_9 = data_buoyancy['Flux_surface_48_solute']*-1
pipe_10 = data_buoyancy['Flux_surface_49_solute']*-1


data_no_buoyancy = np.genfromtxt(
    folder + '/without_buoyancy/derived_quantities.csv',
    delimiter=',', names=True)
t_no_buoyancy = data_no_buoyancy["ts"]
eurofer_no_buoyancy = data_no_buoyancy['Flux_surface_39_solute']*-1
pipe_1_no_buoyancy = data_no_buoyancy['Flux_surface_40_solute']*-1
pipe_2_no_buoyancy = data_no_buoyancy['Flux_surface_41_solute']*-1
pipe_3_no_buoyancy = data_no_buoyancy['Flux_surface_42_solute']*-1
pipe_4_no_buoyancy = data_no_buoyancy['Flux_surface_43_solute']*-1
pipe_5_no_buoyancy = data_no_buoyancy['Flux_surface_44_solute']*-1
pipe_6_no_buoyancy = data_no_buoyancy['Flux_surface_45_solute']*-1
pipe_7_no_buoyancy = data_no_buoyancy['Flux_surface_46_solute']*-1
pipe_8_no_buoyancy = data_no_buoyancy['Flux_surface_47_solute']*-1
pipe_9_no_buoyancy = data_no_buoyancy['Flux_surface_48_solute']*-1
pipe_10_no_buoyancy = data_no_buoyancy['Flux_surface_49_solute']*-1


# fig, axs = plt.subplots(1, 1, sharey=True, figsize=(9.6, 4.8))

plt.figure()

# plt.sca(axs[0])
x_annotation = t[-1]*1.15

colour = 'black'
plt.plot(t, eurofer, color=colour)
plt.plot(
    t_no_buoyancy, eurofer_no_buoyancy,
    color=colour, linestyle="dashed", alpha=0.5)
plt.annotate(
    "FW cooling", (x_annotation, eurofer[-1]), color=colour)

plt.ylabel(r"Surface flux (T m$^{-1}$ s$^{-1}$)")

colour = 'forestgreen'
front = pipe_1 + pipe_5 + pipe_7
front_no_buoyancy = pipe_1_no_buoyancy + pipe_5_no_buoyancy + pipe_7_no_buoyancy
plt.plot(t, front, color=colour)
plt.plot(
    t_no_buoyancy, front_no_buoyancy,
    color=colour, linestyle="dashed", alpha=0.5)
plt.annotate(
    "Front BZ pipes", (x_annotation, front[-1]*1.2), color=colour)


colour = 'purple'
middle_flux = pipe_2 + pipe_6 + pipe_8
middle_flux_no_buoyancy = pipe_2_no_buoyancy + pipe_6_no_buoyancy + pipe_8_no_buoyancy
plt.plot(t, middle_flux, color=colour)
plt.plot(
    t_no_buoyancy, middle_flux_no_buoyancy,
    color=colour, linestyle="dashed", alpha=0.5)
plt.annotate(
    "Middle BZ pipes", (x_annotation, middle_flux[-1]*0.8), color=colour)

colour = 'steelblue'
rear_flux = pipe_3 + pipe_4 + pipe_9 + pipe_10
rear_flux_no_buoyancy = pipe_3_no_buoyancy + pipe_4_no_buoyancy + pipe_9_no_buoyancy + \
     pipe_10_no_buoyancy
plt.plot(t, rear_flux, color=colour)
plt.plot(
    t_no_buoyancy, rear_flux_no_buoyancy,
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
plt.ylim(bottom=1e14, top=2e16)
custom_lines = (Line2D([0], [0], color='grey', linestyle='solid'),
                Line2D([0], [0], color='grey', linestyle='dashed'))
plt.legend(custom_lines, ['Buoyancy', 'No buoyancy'])
plt.tight_layout()
plt.show()
