import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# Load and sort line files
line_files = sorted(glob.glob("lines/*.txt"))
region_files = sorted(glob.glob("regions/*.txt"))

# Define fill colors (one less than number of region lines)
fill_colors = ['blue', 'skyblue', 'lightgreen', 'orange', 'red']

# Load all region lines (for fill_between)
region_lines = [np.loadtxt(f) for f in region_files]

# Plotting
plt.figure(figsize=(8, 6))

# Fill between regions
for i in range(len(region_lines) - 1):
    x = region_lines[i][:, 0]
    y1 = region_lines[i][:, 1]
    y2 = region_lines[i+1][:, 1]
    plt.fill_betweenx(x, y1, y2, color=fill_colors[i % len(fill_colors)], alpha=0.6)

# Plot all lines (from line_files folder)
for f in line_files:
    data = np.loadtxt(f)
    x, y = data[:, 0], data[:, 1]
    plt.plot(y, x, label=os.path.basename(f))

# Axes and legend
plt.xlabel("Y")
plt.ylabel("X")
plt.title("Inverted Axes with Colored Regions")
plt.legend()
plt.grid(True)
plt.gca().invert_xaxis()  # Optional, if you want to invert x visually
plt.gca().invert_yaxis()  # Optional, if you want to invert y visually
plt.tight_layout()
plt.show()
