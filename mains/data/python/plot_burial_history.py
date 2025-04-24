import os
import matplotlib.pyplot as plt
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
    plt.savefig(output_fig)
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
    file_list = [file for file in os.listdir(folder_path1) if file.startswith("burial_history_layer_") and file.endswith(".txt")]
    print(file_list)
    # Sort the file list based on the layer number (xx)
    file_list.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))

    # Plotting
    plt.figure(figsize=(10, 6))
    """ for file_name in file_list:
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

    # Get a list of all files in the folder that match the pattern
    file_list2 = [file for file in os.listdir(folder_path2) if file.startswith("VR_") and file.endswith(".txt")]
    print(file_list2)
    for file_name in file_list2:
        # Read data from the file
        file_path = os.path.join(folder_path2, file_name)
        data = {"t_values": [], "Z_values": []}
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith('#'):
                    continue
                t, Z = map(float, line.strip().split())
                data["t_values"].append(t)
                data["Z_values"].append(Z)

        # Plot Z against t for each file
        plt.scatter(data["t_values"], data["Z_values"])
        plt.plot(data["t_values"], data["Z_values"])
    
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
    plt.savefig(output_fig)
    # Show the plot
    #plt.show()
#endregion
# Specify the path to your folder containing the files
folder_path_bh = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layers/"
folder_path_vr = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_vr/"
output_folder = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layers_plots/"
output_fig = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layers_plots/burial_history.png"
output_fig_vr = "C:/Users/ecanc/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layers_plots/burial_history_vr.png"
plot_burial_alllayers(folder_path_bh, output_folder)
plot_burial_history(folder_path_bh, output_fig)
plot_burial_history_vr(folder_path_bh, folder_path_vr, output_fig_vr)