import pandas as pd

# Read the data from the text file
basepath = '/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/'
palaeopath = 'palaeo_temperature/'
lithopath = 'litho_properties/'
burialhistorypath = 'burial_history/inversion/'

temp_vs_t_layer5_path = basepath+palaeopath+'palaeo_temperature_layer_5_with_inverse.txt'
temp_vs_t_layer5 = pd.read_csv(temp_vs_t_layer5_path, sep=' ', names=['t_values', 'T_values'], skiprows=1, dtype={'t_values': float, 'T_values': float})
print("\nTemperature vs time layer 5:\n", temp_vs_t_layer5)

#result_dict = dict(zip(temp_vs_t_layer5['T_values'], temp_vs_t_layer5['t_values']))
#print("\nDictionary: ", result_dict, "\n")
#.map(result_dict).values
###############################################################################################
#Create the litho properties for layer 5
litho_properties_5 = pd.DataFrame({
    'Tn' : temp_vs_t_layer5['T_values'].iloc[:-1].values,#exclude the last element
    'Tn+1' : temp_vs_t_layer5['T_values'].iloc[1:].values,#exclude the first element
    'tn' : 40 -temp_vs_t_layer5['t_values'].iloc[:-1].values, #Assume basin evolution since 40 m.A.
    'tn+1' : 40 -temp_vs_t_layer5['t_values'].iloc[1:].values

})

# Save to a text file (space-separated values)
outfile_path = basepath+lithopath+'litho_properties_layer_5.txt'
litho_properties_5.to_csv(outfile_path, sep=' ', index=False)
# Print the resulting DataFrame
print("\nLitho properties layer 5:\n", litho_properties_5)
###############################################################################################
#ASSOCIATING FILES
#Associating layer 5
depth_vs_time_layer5_path = basepath + burialhistorypath + 'burial_history_layer_5_with_inverse.txt'
depth_vs_time_layer5 = pd.read_csv(depth_vs_time_layer5_path, sep=' ', names=['t_values', 'Z_values'], skiprows=1, dtype={'t_values': float, 'Z_values' : float})

TandZ_vs_time_layer5 = pd.merge(temp_vs_t_layer5, depth_vs_time_layer5, on='t_values')
TandZ_vs_time_layer5_path = basepath + lithopath + 'merged_properties_5.txt'
TandZ_vs_time_layer5.to_csv(TandZ_vs_time_layer5_path, sep=' ', index=False)
print("\nMerged data for layer 5\n", TandZ_vs_time_layer5)

#Associating other layers
layers = [0, 1, 2, 3, 4, 6]
merged_data_by_layer = {}
for layer in layers:
    filename = f'{basepath}{burialhistorypath}burial_history_layer_{layer}_with_inverse_time.txt'
    outfile_path = f'{basepath}{lithopath}merged_properties_{layer}.txt'

    # Read the additional data from the file
    additional_data = pd.read_csv(filename, sep=' ', names=['Z_values', f't_values_{layer}'], skiprows=1, dtype={'Z_values': float, f't_values_{layer}': float})

    # Merge with the existing dataframe for the current layer
    if layer not in merged_data_by_layer:
        merged_data_by_layer[layer] = additional_data
    else:
        merged_data_by_layer[layer] = pd.merge(merged_data_by_layer[layer], additional_data, on='Z_values', suffixes=('', f'_{layer}'))

    # Save the merged data to a separate text file for the current layer
    selected_columns = ['Z_values'] + ([f'T_values'] if 'T_values' in merged_data_by_layer[layer].columns else []) + [f't_values_{layer}']
    merged_data_layer = merged_data_by_layer[layer][selected_columns]
    merged_data_layer.to_csv(outfile_path, index=False, sep=' ')