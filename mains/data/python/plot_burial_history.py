import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
from scipy.interpolate import interp1d
cwd = os.getcwd()
print(f"Current working directory = {cwd}")
#region Individual
def plot_burial_onelayer(file_path, output_folder):
    """Individual file one by one.

    Args:
        file_path (_type_): _description_
        output_folder (_type_): _description_
    """
    # Read data from the file
    data = {"t_values": [], "Z_values": []}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            t, Z = map(float, line.strip().split())
            data["t_values"].append(t)
            data["Z_values"].append(Z)

    # Plot Z against t for each file
    plt.figure(figsize=(8, 5))
    plt.plot(data["t_values"], data["Z_values"])
    
    # Customize the plot
    plt.title(f"Historia de enterramiento para {os.path.basename(file_path)}")
    plt.xlabel("t (m.A.)")
    plt.ylabel("Profundidad (ft)")
    plt.grid(True)
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    
    # Move x-axis ticks and tick labels to the top
    ax = plt.gca()
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    
    # Save the plot as an image
    output_path = os.path.join(output_folder, f"{os.path.basename(file_path).replace('.txt', '.png')}")
    plt.savefig(output_path)
    #Show figure
    #plt.show()
    # Close the plot to free up resources
    plt.close()

def plot_burial_alllayers(folder_path, output_folder):
    """Individual files at once.

    Args:
        folder_path (_type_): _description_
        output_folder (_type_): _description_
    """
    # Get a list of all files in the folder that match the pattern
    file_list = [file for file in os.listdir(folder_path) if file.startswith("burial_history_layer_") and file.endswith(".txt")]

    for file_name in file_list:
        # Create a plot for each file
        file_path = os.path.join(folder_path, file_name)
        plot_burial_onelayer(file_path, output_folder)
#endregion
#region History
def plot_burial_history(folder_path, output_fig):
    """All histories in one figure.

    Args:
        folder_path (_type_): _description_
        output_folder (_type_): _description_
    """
    # Get a list of all files in the folder that match the pattern
    file_list = [file for file in os.listdir(folder_path) if file.startswith("burial_history_layer_") and file.endswith(".txt")]
    #print(file_list)
    # Sort the file list based on the layer number (xx)
    file_list.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))

    # Plotting
    plt.figure(figsize=(10, 6))
    for file_name in file_list:
        # Read data from the file
        file_path = os.path.join(folder_path, file_name)
        data = {"t_values": [], "Z_values": []}
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('#'):
                    continue
                t, Z = map(float, line.strip().split())
                data["t_values"].append(t)
                data["Z_values"].append(Z)

        # Plot Z against t for each file
        plt.plot(data["t_values"], data["Z_values"], label=f"Layer {file_name.split('_')[-1].split('.')[0]}")
        plt.scatter(data["t_values"], data["Z_values"])

    # Customize the plot
    plt.title("Historia de enterramiento")
    plt.xlabel("t (m.A.)")
    plt.ylabel("Profundidad (ft)")
    plt.legend()
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()

    # Move x-axis ticks and tick labels to the top
    ax = plt.gca()
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    
    plt.grid(True)
    #save the figure
    plt.savefig(output_fig, dpi=600)
    # Show the plot
    #plt.show()
#endregion
#region V_R (%)
def plot_burial_history_vr(folder_path1, folder_path2, output_fig):
    """All histories in one figure.

    Args:
        folder_path (_type_): _description_
        output_folder (_type_): _description_
    """
    # Get a list of all files in the folder that match the pattern
    """file_list = [file for file in os.listdir(folder_path1) if file.startswith("burial_history_layer_") and file.endswith(".txt")]
    print(file_list)
    # Sort the file list based on the layer number (xx)
    file_list.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))

    # Plotting
    for file_name in file_list:
        # Read data from the file
        file_path = os.path.join(folder_path1, file_name)
        data = {"t_values": [], "Z_values": []}
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('#'):
                    continue
                t, Z = map(float, line.strip().split())
                data["t_values"].append(t)
                data["Z_values"].append(Z)

        # Plot Z against t for each file
        plt.plot(data["t_values"], data["Z_values"], label=f"Layer {file_name.split('_')[-1].split('.')[0]}") """

    plt.figure(figsize=(10, 6))
    # Get a list of all files in the folder that match the pattern
    file_list2 = [file for file in os.listdir(folder_path2) if file.startswith("VR_") and file.endswith(".txt")]
    file_list2.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))
    print(file_list2)
    all_t = []
    all_Z = []
    for i, file_name in enumerate(file_list2):
        # Read data from the file
        file_path = os.path.join(folder_path2, file_name)
        data = {"t_values": [], "Z_values": []}
        t_vals = []
        Z_vals = []
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('#'):
                    continue
                t, Z = map(float, line.strip().split())
                data["t_values"].append(t)
                data["Z_values"].append(Z)
        all_t.append(np.array(t_vals))
        all_Z.append(np.array(Z_vals))
        # Plot Z against t for each file
        plt.scatter(data["t_values"], data["Z_values"], s=1.5)
        plt.plot(data["t_values"], data["Z_values"], linewidth = 0.5, label = f"VR {file_name.split('_')[-1].split('.')[0]}")
        print( f"{i}) VR {file_name.split('_')[-1].split('.')[0]}")
    # Customize the plot
    plt.title("R0 (%)")
    plt.xlabel("t (m.A.)")
    plt.ylabel("Profundidad (ft)")
    plt.legend()
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()

    # Move x-axis ticks and tick labels to the top
    ax = plt.gca()
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    
    plt.grid(True)
    #save the figure
    plt.savefig(output_fig, dpi=600)
    # Show the plot
    #plt.show()
def plot_burial_history_vr_fill(folder_path1, folder_path2, output_fig):  
    # Plot the Ro values filled
    file_list2 = [file for file in os.listdir(folder_path2) if file.startswith("VR_") and file.endswith(".txt")]
    t_common = None
    interpolated_Z = []
    #First pass: find global t-range and build a common grid
    t_all = []
    for file_name in file_list2:
        t_vals, Z_vals = [], []
        file_path = os.path.join(folder_path2, file_name)
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith("#"):
                    continue
                t, Z = map(float, line.strip().split())
                t_vals.append(t)
                Z_vals.append(Z)
        t_all.extend(t_vals)
    #Define common t-grid with high enough resolution
    t_common = np.linspace(min(t_all), max(t_all), 500)
    #Interpolate all curves onto the common grid
    for file_name in file_list2:
        t_vals, Z_vals = [], []
        file_path = os.path.join(folder_path2, file_name)
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith("#"):
                    continue
                t, Z = map(float, line.strip().split())
                t_vals.append(t)
                Z_vals.append(Z)
        f_interp = interp1d(t_vals, Z_vals, bounds_error=False, fill_value="extrapolate")
        interpolated_Z.append(f_interp(t_common))
    
    #Plot and fill between layers
    plt.figure(figsize=(10, 6))
    n_layers = len(interpolated_Z)
    print(f"Number of layers = {n_layers}")
    colors = [
    '#001f3f',  # 1. dark blue
    '#0057b7',  # 2. cobalt blue
    '#3399ff',  # 3. medium blue
    '#66ccff',  # 4. light blue
    '#006400',  # 5. dark green
    '#33cc33',  # 6. medium green
    '#99ff66',  # 7. light green
    '#ffff66',  # 8. yellow
    '#ffcc66',  # 9. light orange
    '#ffb347',  # 10. soft orange
    '#ffd699',  # 11. very light orange
    '#ff99cc',  # 12. pink
    '#ff9933',  # 13. orange
    '#ff6600',  # 14. strong orange
    '#ff3300',  # 15. red-orange
    '#cc0000',  # 16. deep red
    '#990000',  # 17. dark red
    '#660000',  # 18. very dark red
    ]
    # Corresponding ranges
    labels = [
    "(0.19–0.29)",
    "(0.29–0.38)",
    "(0.38–0.47)",
    "(0.47–0.57)",
    "(0.57–0.67)",
    "(0.67–0.76)",
    "(0.76–0.85)",
    "(0.85–0.95)",
    "(0.95–1.04)",
    "(1.04–1.14)",
    "(1.14–1.24)",
    "(1.24–1.33)",
    "(1.33–1.43)",
    "(1.43–1.52)",
    "(1.52–1.61)",
    "(1.61–1.71)",
    "(1.71–1.80)",
    "(1.80–1.90)"]

    #cmap = mcolors.LinearSegmentedColormap.from_list("BlueGreenRed", ["blue", "green", "red"], N= n_layers)
    #cmap = plt.cm.jet
    """ for i in range(0, len(interpolated_Z)):
        plt.plot(t_common, interpolated_Z[i], label = f"Interface {i}") """
    """ plt.plot(t_common, interpolated_Z[0], label = f'Interface [0]')
    plt.plot(t_common, interpolated_Z[1], label = f'Interface [1]')
    plt.plot(t_common, interpolated_Z[2], label = f'Interface [2]')
    plt.plot(t_common, interpolated_Z[3], label = f'Interface [3]')
    plt.plot(t_common, interpolated_Z[4], label = f'Interface [4]')
    plt.plot(t_common, interpolated_Z[5], label = f'Interface [5]')
    plt.plot(t_common, interpolated_Z[6], label = f'Interface [6]')
    plt.plot(t_common, interpolated_Z[7], label = f'Interface [7]')
    plt.plot(t_common, interpolated_Z[8], label = f'Interface [8]')
    plt.plot(t_common, interpolated_Z[9], label = f'Interface [9]')
    plt.plot(t_common, interpolated_Z[10], label = f'Interface [10]')
    plt.plot(t_common, interpolated_Z[11], label = f'Interface [11]')
    plt.plot(t_common, interpolated_Z[12], label = f'Interface [12]')
    plt.plot(t_common, interpolated_Z[13], label = f'Interface [13]')
    plt.plot(t_common, interpolated_Z[14], label = f'Interface [14]')
    plt.plot(t_common, interpolated_Z[15], label = f'Interface [15]')
    plt.plot(t_common, interpolated_Z[16], label = f'Interface [16]')
    plt.plot(t_common, interpolated_Z[17], label = f'Interface [17]')
    plt.plot(t_common, interpolated_Z[18], label = f'Interface [18]') """


    cmap = mcolors.ListedColormap(colors)
    plt.fill_between(t_common, interpolated_Z[9], interpolated_Z[0], color = colors[0], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[0], interpolated_Z[1], color = colors[1], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[1], interpolated_Z[2], color = colors[2], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[2], interpolated_Z[3], color = colors[3], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[3], interpolated_Z[4], color = colors[4], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[4], interpolated_Z[5], color = colors[5], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[5], interpolated_Z[6], color = colors[6], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[6], interpolated_Z[7], color = colors[7], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[7], interpolated_Z[8], color = colors[8], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[8], interpolated_Z[10], color = colors[9], alpha = 0.5)#cmap(0) colors[0]
    #plt.fill_between(t_common, interpolated_Z[9], interpolated_Z[10], color = colors[10], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[10], interpolated_Z[11], color = colors[11], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[11], interpolated_Z[12], color = colors[12], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[12], interpolated_Z[13], color = colors[13], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[13], interpolated_Z[14], color = colors[14], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[14], interpolated_Z[15], color = colors[15], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[15], interpolated_Z[16], color = colors[16], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[16], interpolated_Z[17], color = colors[17], alpha = 0.5)#cmap(0) colors[0]
    plt.fill_between(t_common, interpolated_Z[17], interpolated_Z[18], color = colors[17], alpha = 0.5)#cmap(0) colors[0]
    # Fill between each pair
    """ for i in range(1, len(interpolated_Z) - 1):
        plt.fill_between(t_common, interpolated_Z[i-1], interpolated_Z[i],
                     color= colors[i], alpha=0.5)#colors[i % len(colors)] cmap(i / (n_layers - 1)) """
    
    #Plot burial history
    file_list = [file for file in os.listdir(folder_path1) if file.startswith("burial_history_layer_") and file.endswith(".txt")]
    print(file_list)
    # Sort the file list based on the layer number
    file_list.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))
    for file_name in file_list:
        # Read data from the file
        file_path = os.path.join(folder_path1, file_name)
        data = {"t_values": [], "Z_values": []}
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('#'):
                    continue
                t, Z = map(float, line.strip().split())
                data["t_values"].append(t)
                data["Z_values"].append(Z)
        # Plot Z against t for each file
        plt.plot(data["t_values"], data["Z_values"], c = 'k', label=f"Layer {file_name.split('_')[-1].split('.')[0]}")
    # Customize the plot
    plt.title("Historia de enterramiento con R0")
    plt.xlabel("t (m.A.)")
    plt.ylabel("Profundidadsss (ft)")
    plt.legend(loc='lower center')
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    # Move x-axis ticks and tick labels to the top
    ax = plt.gca()
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    plt.grid(True)
    #Colorbar
    fig = plt.gcf()
    cbar_ax = fig.add_axes([0.15, 0.11, 0.025, 0.48])
    bounds = np.linspace(0, len(colors), len(colors) + 1)
    norm = mcolors.BoundaryNorm(boundaries=bounds, ncolors=len(colors))
    cb = plt.colorbar(
    plt.cm.ScalarMappable(cmap=cmap, norm=norm),
    cax=cbar_ax,
    ticks=np.arange(len(colors)) + 0.5,
    boundaries=bounds,
    spacing='proportional',
    orientation='vertical'
    )
    cb.ax.set_yticklabels(labels)
    cb.set_label("%R0", rotation=270, labelpad=15)
    #plt.tight_layout()
    plt.savefig(output_fig, dpi=600)
#endregion
# Specify the path to your folder containing the files
folder_path_bh = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layers/"
folder_path_vr = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_vr/"
output_folder = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layers_plots/"
output_fig = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layers_plots/burial_history.png"
output_fig_vr = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layers_plots/burial_history_vr.png"
output_fig_vr_fill = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layers_plots/burial_history_vr_fill.png"
plot_burial_alllayers(folder_path_bh, output_folder)
plot_burial_history(folder_path_bh, output_fig)
plot_burial_history_vr(folder_path_bh, folder_path_vr, output_fig_vr)
plot_burial_history_vr_fill(folder_path_bh, folder_path_vr, output_fig_vr_fill)