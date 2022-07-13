import matplotlib.pyplot as plt
import numpy as np

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=12)
folder = '../../reference_case/transient'
data = np.genfromtxt(
    folder + '/without_traps/derived_quantities.csv',
    delimiter=',', names=True)
data_2 = np.genfromtxt(
    folder + '/with_traps/derived_quantities.csv',
    delimiter=',', names=True)

# print(data.dtype.names)
# exit()

t = data["ts"]
eurofer_coolant_interface = data['Flux_surface_39_solute']*-1
pipe_1_coolant_interface = data['Flux_surface_40_solute']*-1
pipe_2_coolant_interface = data['Flux_surface_41_solute']*-1
pipe_3_coolant_interface = data['Flux_surface_42_solute']*-1
pipe_4_coolant_interface = data['Flux_surface_43_solute']*-1
pipe_5_coolant_interface = data['Flux_surface_44_solute']*-1
pipe_6_coolant_interface = data['Flux_surface_45_solute']*-1
pipe_7_coolant_interface = data['Flux_surface_46_solute']*-1
pipe_8_coolant_interface = data['Flux_surface_47_solute']*-1
pipe_9_coolant_interface = data['Flux_surface_48_solute']*-1
pipe_10_coolant_interface = data['Flux_surface_49_solute']*-1

t_2 = data_2["ts"]
eurofer_coolant_interface_2 = data_2['Flux_surface_39_solute']*-1
pipe_1_coolant_interface_2 = data_2['Flux_surface_40_solute']*-1
pipe_2_coolant_interface_2 = data_2['Flux_surface_41_solute']*-1
pipe_3_coolant_interface_2 = data_2['Flux_surface_42_solute']*-1
pipe_4_coolant_interface_2 = data_2['Flux_surface_43_solute']*-1
pipe_5_coolant_interface_2 = data_2['Flux_surface_44_solute']*-1
pipe_6_coolant_interface_2 = data_2['Flux_surface_45_solute']*-1
pipe_7_coolant_interface_2 = data_2['Flux_surface_46_solute']*-1
pipe_8_coolant_interface_2 = data_2['Flux_surface_47_solute']*-1
pipe_9_coolant_interface_2 = data_2['Flux_surface_48_solute']*-1
pipe_10_coolant_interface_2 = data_2['Flux_surface_49_solute']*-1

# plot
fig, axs = plt.subplots(3, 4, sharex=True, sharey=True, figsize=(12, 9))
plt.sca(axs[0, 0])
plt.plot(
    t, pipe_1_coolant_interface,
    label='Pipe 1,1', color='darkseagreen', linestyle='dashed')
plt.plot(t_2, pipe_1_coolant_interface_2, label='traps', color='darkseagreen')
plt.ylabel(r"Surface flux (H m$^{-1}$s$^{-1}$)")
plt.legend()

plt.sca(axs[0, 1])
plt.plot(
    t, pipe_2_coolant_interface,
    label='Pipe 1,2', color='hotpink', linestyle='dashed')
plt.plot(t_2, pipe_2_coolant_interface_2, label='traps', color='hotpink')
plt.legend()

plt.sca(axs[0, 2])
plt.plot(
    t, pipe_3_coolant_interface,
    label='Pipe 1,3', color='dodgerblue', linestyle='dashed')
plt.plot(t_2, pipe_3_coolant_interface_2, label='traps', color='dodgerblue')
plt.legend()

plt.sca(axs[0, 3])
plt.plot(
    t, pipe_4_coolant_interface,
    label='Pipe 1,4', color='teal', linestyle='dashed')
plt.plot(t_2, pipe_4_coolant_interface_2, label='traps', color='teal')
plt.legend()

plt.sca(axs[1, 0])
plt.plot(
    t, pipe_5_coolant_interface,
    label='Pipe 2,1', color='forestgreen', linestyle='dashed')
plt.plot(t_2, pipe_5_coolant_interface_2, label='traps', color='forestgreen')
plt.ylabel(r"Surface flux (H m$^{-1}$s$^{-1}$)")
plt.legend()

plt.sca(axs[1, 1])
plt.plot(
    t, pipe_6_coolant_interface,
    label='Pipe 2,2', color='purple', linestyle='dashed')
plt.plot(t_2, pipe_6_coolant_interface_2, label='traps', color='purple')
plt.legend()

plt.sca(axs[1, 2])
plt.axis('off')
plt.sca(axs[1, 3])
plt.axis('off')

plt.sca(axs[2, 0])
plt.plot(
    t, pipe_7_coolant_interface,
    label='Pipe 3,1', color='limegreen', linestyle='dashed')
plt.plot(t_2, pipe_7_coolant_interface_2, label='traps', color='limegreen')
plt.ylabel(r"Surface flux (H m$^{-1}$s$^{-1}$)")
plt.xlabel(r"Time (s)")
plt.legend()

plt.sca(axs[2, 1])
plt.plot(
    t, pipe_8_coolant_interface,
    label='Pipe 3,2', color='fuchsia', linestyle='dashed')
plt.plot(t_2, pipe_8_coolant_interface_2, label='traps', color='fuchsia')
plt.xlabel(r"Time (s)")
plt.legend()

plt.sca(axs[2, 2])
plt.plot(
    t, pipe_9_coolant_interface,
    label='Pipe 3,3', color='steelblue', linestyle='dashed')
plt.plot(t_2, pipe_9_coolant_interface_2, label='traps', color='steelblue')
plt.xlabel(r"Time (s)")
plt.legend()

plt.sca(axs[2, 3])
plt.plot(
    t, pipe_10_coolant_interface,
    label='Pipe 3,4', color='skyblue', linestyle='dashed')
plt.plot(t_2, pipe_10_coolant_interface_2, label='traps', color='skyblue')
plt.xlabel(r"Time (s)")
plt.legend()

for ax_row in axs:
    for ax in ax_row:
        plt.sca(ax)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

plt.ylim(bottom=1e13, top=1e16)
plt.xscale("log")
plt.yscale("log")
plt.tight_layout()
plt.show()
