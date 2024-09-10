# Importing necessary libraries to generate the mesh
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import os

# Generating a simple model for the section based on the image, using depth in kilometers
# Assuming a horizontal section with varying layers
cwd = os.getcwd()
print("CWD:", cwd)
def read_interface_from_csv(file_path):
    df = pd.read_csv(file_path)
    x = df['x'].values
    y = df[' y'].values
    return x, y
def interpolate_interface(x_old, y_old, x_new):
    interpolator = interp1d(x_old, y_old, kind='linear', fill_value='extrapolate')
    return interpolator(x_new)

# Find the minimum and maximum across all x and y values
def find_min_max(interfaces_dict):
    all_x = []
    all_y = []
    for key, (x, y) in interfaces_dict.items():
        all_x.append(x)
        all_y.append(y)
    all_x = np.concatenate(all_x)
    all_y = np.concatenate(all_y)
    
    x_min, x_max = np.min(all_x), np.max(all_x)
    y_min, y_max = np.min(all_y), np.max(all_y)
    
    return x_min, x_max, y_min, y_max

# Paths to your CSV files for each interface
csv_files = {
    'interface_1': 'mains/data/grids/basamento_top_pts.csv',
    'interface_2': 'mains/data/grids/clavo_top_pts.csv',
    'interface_3': 'mains/data/grids/salaqui_top_pts.csv',
    'interface_4': 'mains/data/grids/uva_top_pts.csv',
    'interface_5': 'mains/data/grids/napipi_top_pts.csv',
    'interface_6': 'mains/data/grids/sierra_top_pts_3.csv',
}

interfaces = {}
for name, file_path in csv_files.items():
    x, y = read_interface_from_csv(file_path)
    interfaces[name] = (x, y)

x_min, x_max, y_min, y_max = find_min_max(interfaces)
print("Original interfaces ranges")
print(f"x_min: {x_min}, x_max: {x_max}")
print(f"y_min: {y_min}, y_max: {y_max}")

# Add the surface interface
x_surface = np.linspace(0, 130000, 40)
y_surface = np.zeros_like(x_surface)  # Surface with 0 depth
interfaces['surface'] = (x_surface, y_surface)

# Get the min and max values
x_min, x_max, y_min, y_max = find_min_max(interfaces)
print("Interfaces after adding the surface layer")
print(f"x_min: {x_min}, x_max: {x_max}")
print(f"y_min: {y_min}, y_max: {y_max}")
#Add the bottom interface
x_bottom = x_surface
y_bottom = np.full_like(x_bottom, y_max + 10)
interfaces['bottom'] = (x_bottom, y_bottom)

# Create a common x-grid for interpolation
x_new = np.linspace(min(interfaces['surface'][0]), max(interfaces['surface'][0]), 140) #Higher resolution
interpolated_interfaces = {key: (x_new, interpolate_interface(x, y, x_new)) for key, (x, y) in interfaces.items()}
#Concatenate to triangulate
X=np.concatenate([interpolated_interfaces['surface'][0], interpolated_interfaces['interface_1'][0], interpolated_interfaces['interface_2'][0], interpolated_interfaces['interface_3'][0], interpolated_interfaces['interface_4'][0], interpolated_interfaces['interface_5'][0], interpolated_interfaces['interface_6'][0], interpolated_interfaces['bottom'][0]])
Y=np.concatenate([interpolated_interfaces['surface'][1], interpolated_interfaces['interface_1'][1], interpolated_interfaces['interface_2'][1], interpolated_interfaces['interface_3'][1], interpolated_interfaces['interface_4'][1], interpolated_interfaces['interface_5'][1], interpolated_interfaces['interface_6'][1], interpolated_interfaces['bottom'][1]])
# Define the triangulation of the mesh
triang = tri.Triangulation(X, Y)

#Extract triangle vertices
X_triang = triang.x
Y_triang = triang.y
#Compute centroids of each triangle
triangles = triang.triangles
centroids_x = np.mean(X_triang[triangles], axis = 1)
centroids_y = np.mean(Y_triang[triangles], axis = 1)

# Plotting the triangulated mesh to visualize the finite elements
plt.figure(figsize=(10, 5))
plt.gca().invert_yaxis()  # Invert Y axis (depth increases downward)
plt.fill_between(x_new, interpolated_interfaces['interface_6'][1], interpolated_interfaces['surface'][1], color='lemonchiffon', label='Fm. Quibdó')
plt.fill_between(x_new, interpolated_interfaces['interface_5'][1], interpolated_interfaces['interface_6'][1], color='yellow', label='Fm. Sierra')
plt.fill_between(x_new, interpolated_interfaces['interface_4'][1], interpolated_interfaces['interface_5'][1], color='khaki', label='Fm. Napipí')
plt.fill_between(x_new, interpolated_interfaces['interface_3'][1], interpolated_interfaces['interface_4'][1], color='violet', label='Fm. Uva')
plt.fill_between(x_new, interpolated_interfaces['interface_2'][1], interpolated_interfaces['interface_3'][1], color='peachpuff', label='Fm. Salaquí')
plt.fill_between(x_new, interpolated_interfaces['interface_1'][1], interpolated_interfaces['interface_2'][1], color='lightsalmon', label='Fm. Clavo')
plt.fill_between(x_new, interpolated_interfaces['bottom'][1], interpolated_interfaces['interface_1'][1], color='yellowgreen', label='Basamento')
plt.triplot(triang, color='black', lw=0.5)
plt.scatter(centroids_x, centroids_y, color = 'red', marker = 'o', label = 'Centroides', s = 2)
plt.title('Discretización espacial subcuenca Atrato')
plt.xlabel('Distancia (m)')
plt.ylabel('Profundidad (m)')
plt.legend()
plt.savefig(os.path.join(cwd, 'mains/data/grids', 'discretization.png'))
#plt.show()
