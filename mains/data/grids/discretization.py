# Importing necessary libraries to generate the mesh
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import sys, os

# Generating a simple model for the section based on the image, using depth in kilometers
# Assuming a horizontal section with varying layers
cwd = os.getcwd()
print("CWD:", cwd)
def read_interface_from_csv(file_path):
    df = pd.read_csv(file_path)
    x = df['x'].values
    y = df[' y'].values
    return x, y

# Paths to your CSV files for each interface
csv_files = {
    'interface_1': 'mains/data/grids/basamento_top_pts.csv',
    'interface_2': 'mains/data/grids/clavo_top_pts.csv',
    'interface_3': 'mains/data/grids/salaqui_top_pts.csv',
    'interface_4': 'mains/data/grids/uva_top_pts.csv',
    'interface_5': 'mains/data/grids/napipi_top_pts.csv',
    'interface_6': 'mains/data/grids/sierra_top_pts.csv',
}

interfaces = {}
for name, file_path in csv_files.items():
    x, y = read_interface_from_csv(file_path)
    interfaces[name] = (x, y)

def interpolate_interface(x_old, y_old, x_new):
    interpolator = interp1d(x_old, y_old, kind='linear', fill_value='extrapolate')
    return interpolator(x_new)

# Add the surface interface
x_surface = np.linspace(0, 130000, 40)
y_surface = np.zeros_like(x_surface)  # Surface with 0 depth
interfaces['surface'] = (x_surface, y_surface)

# Create a common x-grid for interpolation
x_new = np.linspace(min(interfaces['surface'][0]), max(interfaces['surface'][0]), 100) #Higher resolution
interpolated_interfaces = {key: (x_new, interpolate_interface(x, y, x_new)) for key, (x, y) in interfaces.items()}


"""
# Length of the section (in kilometers)
x = np.linspace(0, 110, 12)

# Layers (in kilometers, y-axis going downward for depth)!!!!!
layers = {
    'surface': np.zeros_like(x),            # Surface (0 depth)
    'layer_1': 0.5 + 0.2 * np.sin(x/15),    # Top layer
    'layer_2': 1.5 + 0.2 * np.sin(x/20),    # Second layer
    'layer_3': 3.0 + 0.3 * np.sin(x/25),    # Third layer
    'layer_4': 5.0 + 0.4 * np.sin(x/30),    # Bottom layer (Cretaceous)
    "capa2": np.array([3.5, 3.6, 3.7, 3.8, 3.9, 4, 4.2, 4.4, 4.6, 4.8, 5, 5])
} 


# Create the X and Y coordinates
X = np.concatenate([x, x, x, x, x, x])
Y = np.concatenate([layers['surface'], layers['layer_1'], layers['layer_2'], layers['layer_3'], layers['layer_4'], layers['capa2']])
"""
X=np.concatenate([interpolated_interfaces['surface'][0], interpolated_interfaces['interface_1'][0], interpolated_interfaces['interface_2'][0], interpolated_interfaces['interface_3'][0], interpolated_interfaces['interface_4'][0], interpolated_interfaces['interface_5'][0], interpolated_interfaces['interface_6'][0]])
Y=np.concatenate([interpolated_interfaces['surface'][1], interpolated_interfaces['interface_1'][1], interpolated_interfaces['interface_2'][1], interpolated_interfaces['interface_3'][1], interpolated_interfaces['interface_4'][1], interpolated_interfaces['interface_5'][1], interpolated_interfaces['interface_6'][1]])
# Define the triangulation of the mesh
triang = tri.Triangulation(X, Y)

# Plotting the triangulated mesh to visualize the finite elements
plt.figure(figsize=(10, 5))
plt.gca().invert_yaxis()  # Invert Y axis (depth increases downward)
plt.fill_between(x, interpolated_interfaces['surface'], interpolated_interfaces['interface_1'], color='skyblue', label='Layer 1')
plt.triplot(triang, color='black', lw=0.8)
plt.title('Triangular Mesh of Geologic Section')
plt.xlabel('Distance (km)')
plt.ylabel('Depth (km)')
plt.show()
