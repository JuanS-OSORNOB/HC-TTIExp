import os
import re
import matplotlib.pyplot as plt

def plot_individual_file(file_path, save_path):
    data = {'X': [], 'Y': []}
    
    # Extract layer number from the file name
    match = re.match(r'merged_properties_layer_(\d+)\.txt', os.path.basename(file_path))
    layer_number = match.group(1) if match else 'Unknown'

    with open(file_path, 'r') as file:
        next(file)  # Skip the header line
        for line in file:
            t_value, T_value, _, additional_t_value = map(float, line.split())
            data['X'].append(additional_t_value)
            data['Y'].append(T_value)

    plt.plot(data['X'], data['Y'], label=f'Layer {layer_number}')
    plt.title('Pseudo-palaeotemperature')
    plt.xlabel('Additional_t_values')
    plt.ylabel('T_values')
    plt.gca().invert_xaxis()  # Invert the X-axis
    plt.legend()
    
    # Save individual figure
    save_file = f'pseudo_palaeo_temperature_layer_{layer_number}.png'
    save_path = os.path.join(save_path, save_file)
    plt.savefig(save_path)
    
    plt.show()

def plot_combined(files, save_path):
    plt.figure(figsize=(10, 6))

    for file_path in files:
        data = {'X': [], 'Y': []}

        # Extract layer number from the file name
        match = re.match(r'merged_properties_layer_(\d+)\.txt', os.path.basename(file_path))
        layer_number = match.group(1) if match else 'Unknown'

        with open(file_path, 'r') as file:
            next(file)  # Skip the header line
            for line in file:
                t_value, T_value, Z_value, additional_t_value = map(float, line.split())
                data['X'].append(additional_t_value)
                data['Y'].append(T_value)

        plt.plot(data['X'], data['Y'], label=f'Layer {layer_number}')

    plt.title('Combined Plot')
    plt.xlabel('Additional_t_values')
    plt.ylabel('T_values')
    plt.gca().invert_xaxis()  # Invert the X-axis
    plt.legend()

    # Save combined figure
    save_path_combined = os.path.join(save_path, 'pseudo_palaeo_temperature_all_layers.png')
    plt.savefig(save_path_combined)

    plt.show()

def main(folder_path, save_path):
    files = [f for f in os.listdir(folder_path) if re.match(r'merged_properties_layer_\d+\.txt', f)]

    for file in files:
        file_path = os.path.join(folder_path, file)
        plot_individual_file(file_path, save_path)

    plot_combined([os.path.join(folder_path, file) for file in files], save_path)


if __name__ == "__main__":
    folder_path = '/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/litho_properties/'  # Change this to the path of your folder containing TXT files
    save_path = '/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/palaeo_temperature/'  # Change this to the path where you want to save the figures
    main(folder_path, save_path)
