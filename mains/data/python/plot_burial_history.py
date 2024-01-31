import os
import matplotlib.pyplot as plt

def plot_file(file_path, output_folder):
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
    plt.title(f"Burial History for {os.path.basename(file_path)}")
    plt.xlabel("t (m.A.)")
    plt.ylabel("Depth (ft)")
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

def plot_burial_histories(folder_path, output_folder):
    # Get a list of all files in the folder that match the pattern
    file_list = [file for file in os.listdir(folder_path) if file.startswith("burial_history_layer_") and file.endswith(".txt")]

    for file_name in file_list:
        # Create a plot for each file
        file_path = os.path.join(folder_path, file_name)
        plot_file(file_path, output_folder)

# Specify the path to your folder containing the files
folder_path = "/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/burial_history/"
output_folder = "/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/burial_history/"
plot_burial_histories(folder_path, output_folder)



def plot_burial_history(folder_path, filename):
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

    # Customize the plot
    plt.title("Burial History")
    plt.xlabel("t (m.A.)")
    plt.ylabel("Depth (ft)")
    plt.legend()
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()

    # Move x-axis ticks and tick labels to the top
    ax = plt.gca()
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    
    plt.grid(True)
    #save the figure
    plt.savefig(folder_path + filename)
    # Show the plot
    #plt.show()

# Specify the path to your folder containing the files
folder_path = "/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/burial_history/"
filename = "burial_history.png"
plot_burial_history(folder_path, filename)

