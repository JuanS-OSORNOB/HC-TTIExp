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
    print(f"VR file list:\n{file_list2}")
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
        #print( f"{i}) VR {file_name.split('_')[-1].split('.')[0]}")
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
    #First step: find global t-range and build a common grid
    file_list2 = [file for file in os.listdir(folder_path2) if file.startswith("VR_") and file.endswith(".txt")]
    t_common = None
    vr_interfaces = []
    geol_interfaces = []
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
    #Second step: Define common t-grid with high enough resolution
    t_common = np.linspace(min(t_all), max(t_all), 500)
    #Third step: Interpolate all curves onto the common grid
    file_list1_grid = [file for file in os.listdir(folder_path1) if file.startswith("grid_burial_history_layer_") and file.endswith(".txt")]
    for file_name in file_list1_grid:
        t_vals, Z_vals = [], []
        file_path = os.path.join(folder_path1, file_name)
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith("#"):
                    continue
                t, Z = map(float, line.strip().split())
                t_vals.append(t)
                Z_vals.append(Z)
        f_interp = interp1d(t_vals, Z_vals, bounds_error=False, fill_value="extrapolate")
        geol_interfaces.append(f_interp(t_common))

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
        vr_interfaces.append(f_interp(t_common))
    
    # Move vr_interfaces[9] to position 0
    item = vr_interfaces.pop(9)  # Remove item at index 9
    vr_interfaces.insert(0, item)  # Insert it at the beginning to fix re-ordering problem visually identified

    ########## Compute areas individually /begin/ ##########
    def compute_area(t, bottom_curve, top_curve):
        height = top_curve - bottom_curve
        area = np.trapz(height, t)
        return area
    # Step 1: compute VR areas
    vr_areas = []
    for j in range(len(vr_interfaces) - 1):
        area = compute_area(t_common, vr_interfaces[j], vr_interfaces[j + 1])
        vr_areas.append(area)
    print(f"VR areas=\n{vr_areas}")
    # Step 2: compute geological areas
    geol_areas = []
    for i in range(len(geol_interfaces) - 1):
        area = compute_area(t_common, geol_interfaces[i], geol_interfaces[i + 1])
        geol_areas.append(area)
    print(f"Geological areas=\n{geol_areas}")
    # Step 3: Compute intersection areas
    overlap_percentages = np.zeros((len(geol_areas), len(vr_areas)))
    for i in range(len(geol_interfaces) - 1):
        geo_bottom = geol_interfaces[i]
        geo_top = geol_interfaces[i + 1]
        for j in range(len(vr_interfaces) - 1):
            vr_bottom = vr_interfaces[j]
            vr_top = vr_interfaces[j + 1]
            bottom_overlap = np.maximum(geo_bottom, vr_bottom)
            top_overlap = np.minimum(geo_top, vr_top)
            #If no overlap (top < bottom), clip heights to zero
            overlap_height = np.clip(top_overlap - bottom_overlap, a_min=0, a_max=None)
            overlap_area = np.trapz(overlap_height, t_common)
            if geol_areas[i] > 0:
                overlap_percentages[i, j] = (overlap_area / geol_areas[i])
            else:
                overlap_percentages[i, j] = 0 #Avoid division by zero
    np.set_printoptions(suppress=True, precision=6)
    print(f"Overlap percentages (VR range inside each geological layer):\n{overlap_percentages}")
    col_sums = np.sum(overlap_percentages, axis = 1)
    print(f"Just checking column sums {col_sums}. Should be 100%")
    ########## Compute areas individually /end/ ##########
    
    #Plot and fill between layers
    plt.figure(figsize=(10, 6))
    """ for i in range(len(geol_interfaces)):
        plt.plot(t_common, geol_interfaces[i], label = f"Layer grid {i}") """
    """ for i in range(len(vr_interfaces)):
        plt.plot(t_common, vr_interfaces[i], label = f"Interface {i}") """
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
    cmap = mcolors.ListedColormap(colors)
    # Fill between each pair
    for i in range(1, len(vr_interfaces) - 1):
        plt.fill_between(t_common, vr_interfaces[i-1], vr_interfaces[i],
                     color= colors[i], alpha=0.5)#colors[i % len(colors)] cmap(i / (n_layers - 1))
    
    #Plot burial history
    labels_layers = ["Fm. Quibó", "Fm. Sierra", "Fm. Napipí", "Fm. Uva", "Fm. Salaquí", "Fm. Clavo"]
    file_list = [file for file in os.listdir(folder_path1) if file.startswith("burial_history_layer_") and file.endswith(".txt")]
    print(f"Burial history file list:\n{file_list}")
    # Sort the file list based on the layer number
    file_list.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))
    for i, file_name in enumerate(file_list):
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
        plt.plot(data["t_values"], data["Z_values"], label=labels_layers[i])#f"Layer {file_name.split('_')[-1].split('.')[0]}"
    
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

    return overlap_percentages, labels
#endregion
#region Exposure time
def plot_exposuretime(folder_path1, folder_path2, output_fig1, output_fig2):
    overlap_percentages, labels = plot_burial_history_vr_fill(folder_path1, folder_path2, output_fig1)
    last_times = [3.3939393939393936, 11.272727272727273, 14.787878787878789, 33.81818181818182, 38.06060606060606, 39.0]
    """ def compute_exposuretime(percentage, last_time):
        return percentage * last_time
    exposuretime = np.vectorize(compute_exposuretime)(overlap_percentages) """
    exposuretimes = []
    for i, layers in enumerate(overlap_percentages):
        exposuretime_layer = []
        for j, percentage in enumerate(layers):
            exposuretime = percentage * last_times[i]
            exposuretime_layer.append(exposuretime)
        exposuretimes.append(exposuretime_layer)
    print(f"Exposure time:\n{exposuretimes}")

    fig, axes = plt.subplots(2, 3, figsize =(18, 10), sharey = True, sharex = True)
    axes = axes.flatten()
    titles = ["Tiempo de exposición - Fm. Quibdó",
               "Tiempo de exposición - Fm. Sierra",
               "Tiempo de exposición - Fm. Napipí",
               "Tiempo de exposición - Fm. Uva",
               "Tiempo de exposición - Fm. Salaquí",
               "Tiempo de exposición - Fm. Clavo"]
    for i in range(6):
        axes[i].bar(labels, exposuretimes[i])
        axes[i].set_title(titles[i])
        axes[i].set_xlabel("Rango VR0 (%)")
        axes[i].set_ylabel("Tiempo (mA)")
        axes[i].tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.savefig(output_fig2, dpi = 600)
    #plt.show()

#endregion
# Specify the path to your folder containing the files
folder_path_bh = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layers/"
folder_path_vr = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_vr/"
output_folder = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layers_plots/"
output_fig = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layers_plots/burial_history.png"
output_fig_vr = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layers_plots/burial_history_vr.png"
output_fig_vr_fill = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layers_plots/burial_history_vr_fill.png"
output_fig_exposuretime = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layers_plots/exposuretime.png"
plot_burial_alllayers(folder_path_bh, output_folder)
plot_burial_history(folder_path_bh, output_fig)
plot_burial_history_vr(folder_path_bh, folder_path_vr, output_fig_vr)
#plot_burial_history_vr_fill(folder_path_bh, folder_path_vr, output_fig_vr_fill)
plot_exposuretime(folder_path_bh, folder_path_vr, output_fig_vr_fill, output_fig_exposuretime)