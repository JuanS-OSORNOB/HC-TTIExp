# inverse_depth_interpolator.py

import numpy as np
import matplotlib.pyplot as plt

class DepthInterpolatorPlotter:
    def __init__(self, data_file_path):
        self.data = np.genfromtxt(data_file_path, names=True, comments='#')
        self.t_values = self.data['t_values']
        self.z_values = self.data['Z_values']
        self.results = None  # To store results from inverse interpolation

    def inverse_interpolate_depth(self, inverted_t_file):

        # Read inverted t values from file using pandas
        inverted_t_values = np.loadtxt(inverted_t_file, usecols=0)
        print(inverted_t_values)


        self.results = []

        # Sort data points by t values
        sorted_indices = np.argsort(self.t_values)
        sorted_t_values = self.t_values[sorted_indices]
        sorted_z_values = self.z_values[sorted_indices]

        for target_t in inverted_t_values:
            # Find the index where target_t would fit in the sorted array
            index = np.searchsorted(sorted_t_values, target_t)

            # Make sure the index is within bounds
            index = np.clip(index, 1, len(sorted_z_values) - 1)

            # Get the two closest points
            t1, t2 = sorted_t_values[index - 1], sorted_t_values[index]
            z1, z2 = sorted_z_values[index - 1], sorted_z_values[index]

            # Calculate the intersection point using the equation of the line
            slope = (z2 - z1) / (t2 - t1)
            inverse_interpolated_z = z1 + slope * (target_t - t1)

            # Ensure the result is within the range of the two closest points
            inverse_interpolated_z = np.clip(inverse_interpolated_z, min(z1, z2), max(z1, z2))

            self.results.append((target_t, inverse_interpolated_z))

            print(f"For inverted t = {target_t}, closest datapoints are: ({t1}, {z1}) and ({t2}, {z2}), inverse interpolated Z = {inverse_interpolated_z}")

    def save_results(self, output_file_path):
        with open(output_file_path, "w") as file:
            file.write("# t_values Z_values\n")

            for inverse_interpolated_t, inverse_interpolated_z in self.results:
                result_str = f"{inverse_interpolated_t} {inverse_interpolated_z}"
                file.write(result_str + "\n")

        print(f"\nResults saved to {output_file_path}")

    def plot_depth(self):
        plt.plot(self.t_values, self.z_values, marker='o', linestyle='-', color='b', label='Z vs t')
        plt.xlabel('t')
        plt.ylabel('Z')
        plt.title('Depth vs Time')

        if self.results:
            inverted_t_values = [result[0] for result in self.results]
            inverted_z_values = [result[1] for result in self.results]
            plt.scatter(inverted_t_values, inverted_z_values, marker='x', color='r', label='Inverse Interpolated Values')

        plt.legend()
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()

    def save_plot(self, save_path):
        plt.savefig(save_path)

    def show_plot(self):
        plt.show()