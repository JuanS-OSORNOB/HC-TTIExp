import os, re
import pandas as pd

# Define paths to use
basepath = '/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/'
palaeopath = 'palaeo_temperature/'
lithopath = 'litho_properties/'
burialhistorypath = 'burial_history/inversion/'

###############################################################################################
## STEP 1: Create the litho properties for layer 5
temp_vs_t_layer5_path = basepath+palaeopath+'palaeo_temperature_layer_5_with_inverse.txt'
temp_vs_t_layer5 = pd.read_csv(temp_vs_t_layer5_path, sep=' ', names=['t_values', 'T_values'], skiprows=1, dtype={'t_values': float, 'T_values': float})
print("\nTemperature vs time layer 5:\n", temp_vs_t_layer5)

litho_properties_5 = pd.DataFrame({
    'Tn' : temp_vs_t_layer5['T_values'].iloc[:-1].values,#exclude the last element
    'Tn+1' : temp_vs_t_layer5['T_values'].iloc[1:].values,#exclude the first element
    'tn' : 40 -temp_vs_t_layer5['t_values'].iloc[:-1].values, #Assume basin evolution since 40 m.A.
    'tn+1' : 40 -temp_vs_t_layer5['t_values'].iloc[1:].values

})

outfile_path = basepath+lithopath+'litho_properties_layer_5.txt'
litho_properties_5.to_csv(outfile_path, sep=' ', index=False) # Save to a text file (space-separated values)
print("\nLitho properties layer 5:\n", litho_properties_5) # Print the resulting DataFrame
###############################################################################################
## STEP 2: Create the merged properties for layer 5
temperature_data = {}
with open(temp_vs_t_layer5_path, 'r') as temperature_file: # Read data from palaeo_temperature_layer5.txt
    next(temperature_file)  # Skip the header
    for line in temperature_file:
        t_value, T_value = map(float, line.split())
        temperature_data[t_value] = T_value

# Read data from burial_history_layer5.txt and merge with temperature_data
depth_vs_time_layer5_path = basepath + burialhistorypath + 'burial_history_layer_5_with_inverse.txt'
merged_data = []
with open(depth_vs_time_layer5_path, 'r') as burial_file:
    next(burial_file)  # Skip the header
    for line in burial_file:
        t_value, Z_value = map(float, line.split())
        if t_value in temperature_data:
            merged_data.append((t_value, temperature_data[t_value], Z_value))

# Write the merged data to a new file
mergedfilepath = basepath+lithopath+'time_temp_Z_merged_layer_5.txt' 
with open(mergedfilepath, 'w') as merged_file:
    merged_file.write('# t_values T_values Z_values\n')
    for data_point in merged_data:
        merged_file.write(f"{data_point[0]} {data_point[1]} {data_point[2]}\n")
        print(f"{data_point[0]} {data_point[1]} {data_point[2]}\n")
print("Find the file at: ", mergedfilepath)
print("Number of rows in the merged data:", len(merged_data)) # Print the number of rows in the merged data
###############################################################################################
## STEP 3: Create the merged properties for other layers and create litho files from these properties
# Function to extract the layer information from the filename
def extract_layer_info(file_name):
    match = re.search(r'layer_\d+', file_name)
    return match.group() if match else None

# Read data from the merged file
merged_data = []
with open(mergedfilepath, 'r') as merged_file:
    next(merged_file)  # Skip the header
    for line in merged_file:
        t_value, T_value, Z_value = map(float, line.split())
        merged_data.append((t_value, T_value, Z_value))

# List of additional burial history files
additional_files = [
    basepath+burialhistorypath+'/burial_history_layer_0_with_inverse_time.txt',
    basepath+burialhistorypath+'/burial_history_layer_1_with_inverse_time.txt',
    basepath+burialhistorypath+'/burial_history_layer_2_with_inverse_time.txt',
    basepath+burialhistorypath+'/burial_history_layer_3_with_inverse_time.txt',
    basepath+burialhistorypath+'/burial_history_layer_4_with_inverse_time.txt',
    basepath+burialhistorypath+'/burial_history_layer_6_with_inverse_time.txt'
]

# Process each additional burial history file separately
for file_path in additional_files:
    # Extract the filename without the path
    file_name_without_path = os.path.basename(file_path)

    # Extract the layer information from the filename
    layer_info = extract_layer_info(file_name_without_path)

    # Create a list to store the updated merged data for the current additional file
    updated_merged_data = []

    # Read data from the current additional burial history file
    additional_burial_data = {}
    with open(file_path, 'r') as additional_burial_file:
        next(additional_burial_file)  # Skip the header
        for line in additional_burial_file:
            Z_value, t_value = map(float, line.split())
            additional_burial_data[Z_value] = t_value

    # Associate additional burial history data with the merged data based on Z_values
    for i in range(len(merged_data)):
        Z_value = merged_data[i][2]
        if Z_value in additional_burial_data:
            updated_merged_data.append((*merged_data[i], additional_burial_data[Z_value]))
        else:
            updated_merged_data.append((*merged_data[i], None))
    ## STEP 3.1: Write the updated merged data to a new file for the current additional file
    updated_merged_data_path = basepath+lithopath+f'merged_properties_{layer_info}.txt'
    with open(updated_merged_data_path, 'w') as updated_merged_file:
        updated_merged_file.write('# t_values T_values Z_values Additional_t_values\n')
        for data_point in updated_merged_data:
            updated_merged_file.write(f"{data_point[0]} {data_point[1]} {data_point[2]} {data_point[3]}\n")

    ## STEP 3.2: Create the litho properties for the current layer
    # Read the updated merged data for the current layer
    updated_merged_data = pd.read_csv(updated_merged_data_path, sep=' ', names=['t_values', 'T_values', 'Z_values', 'Additional_t_values'], skiprows=1, dtype={'t_values': float, 'T_values': float, 'Z_values': float, 'Additional_t_values': float})

    litho_properties = pd.DataFrame({
        'Tn': updated_merged_data['T_values'].iloc[:-1].values,
        'Tn+1': updated_merged_data['T_values'].iloc[1:].values,
        'tn': 40 - updated_merged_data['Additional_t_values'].iloc[:-1].values,
        'tn+1': 40 - updated_merged_data['Additional_t_values'].iloc[1:].values
    })

    # Save litho properties to a text file
    outfile_path = basepath+lithopath+f'litho_properties_{layer_info}.txt'
    litho_properties.to_csv(outfile_path, sep=' ', index=False)

    # Print the resulting DataFrame for the current layer
    print(f"\nLitho properties {layer_info}:\n", litho_properties)
###############################################################################################