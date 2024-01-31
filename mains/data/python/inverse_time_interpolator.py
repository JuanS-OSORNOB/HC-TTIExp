# inverse_time_interpolator.py

import numpy as np
import matplotlib.pyplot as plt

class TimeInterpolatorPlotter:
    def __init__(self, data_file_path):
        self.data = np.genfromtxt(data_file_path, names=True, comments='#')
        self.t_values = self.data['t_values']
        self.z_values = self.data['Z_values']
        self.results_inverse_t = None  # To store results from inverse interpolation of t_values
        self.results_inverse_z = None  # To store results from inverse interpolation of Z_values

    def inverse_interpolate_t(self, inverted_z_file):

        # Read inverted Z values from file
        inverted_z_values = np.loadtxt(inverted_z_file, usecols=1)

        self.results_inverse_t = []

        # Sort data points by Z values
        sorted_indices = np.argsort(self.z_values)
        sorted_t_values = self.t_values[sorted_indices]
        sorted_z_values = self.z_values[sorted_indices]

        for target_z in inverted_z_values:
            # Find the index where target_z would fit in the sorted array
            index = np.searchsorted(sorted_z_values, target_z)

            # Make sure the index is within bounds
            index = np.clip(index, 1, len(sorted_t_values) - 1)

            # Get the two closest points
            t1, t2 = sorted_t_values[index - 1], sorted_t_values[index]
            z1, z2 = sorted_z_values[index - 1], sorted_z_values[index]

            # Calculate the intersection point using the equation of the line
            slope = (t2 - t1) / (z2 - z1)
            inverse_interpolated_t = t1 + slope * (target_z - z1)

            # Ensure the result is within the range of the two closest points
            inverse_interpolated_t = np.clip(inverse_interpolated_t, min(t1, t2), max(t1, t2))

            self.results_inverse_t.append((target_z, inverse_interpolated_t))

            print(f"For inverted Z = {target_z}, closest datapoints are: ({z1}, {t1}) and ({z2}, {t2}), inverse interpolated t = {inverse_interpolated_t}")

    def save_results_inverse_t(self, output_file_path):
        with open(output_file_path, "w") as file:
            file.write("# Z_values t_values\n")

            for inverse_interpolated_z, inverse_interpolated_t in self.results_inverse_t:
                result_str = f"{inverse_interpolated_z} {inverse_interpolated_t}"
                file.write(result_str + "\n")

        print(f"Results saved to {output_file_path}")

    def plot_inverse_t(self, label=None, linecolor=None, scattercolor=None):
        #Plot Z vs t values
        plt.plot(self.t_values, self.z_values, marker='o', linestyle='-', color=linecolor, label=f'Layer {label}')
        #Plot inverted Z vs t values as scatter
        if self.results_inverse_t:
            inverted_t_values = [result[1] for result in self.results_inverse_t]
            inverted_z_values = [result[0] for result in self.results_inverse_t]
            plt.scatter(inverted_t_values, inverted_z_values, marker='x', color=scattercolor, label=f'Inverse Interpolated Values - Layer {label}')

        plt.xlabel('t')
        plt.ylabel('Z')
        plt.title('Depth vs Time - Inverse Interpolation of t')
        plt.legend()
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()

    def save_plot_inverse_t(self, save_path):
        plt.savefig(save_path)
        print(f"Figure saved to {save_path}\n")
    def show_plot_inverse_t(self):
        plt.show()