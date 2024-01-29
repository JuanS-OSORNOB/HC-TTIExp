# inverse_temperature_interpolator.py

#This script helps find the corresponding Z (depth value in feet) from a given t (m.A.) 
# extracted from a palaeo-temperature plot of ONE lithology;
# after linear interpolation from its basal burial history curve.

# This is done for the purpose of using the found Z to do the inverse process on the burial
# history curves of other lithologies to obtain their corresponding t and with this the input data for the TTI calculation
import numpy as np
import matplotlib.pyplot as plt

class TemperatureInterpolatorPlotter:
    def __init__(self, data_file_path):
        self.data = np.genfromtxt(data_file_path, names=True, comments='#')
        self.t_values = self.data['t_values']
        self.temperature_values = self.data['T_values']
        self.results = None  # To store results from inverse interpolation

    def inverse_interpolate(self, target_temperature_values_file):
        # Read target_temperature_values from file
        target_temperature_values = np.loadtxt(target_temperature_values_file)

        self.results = []

        # Sort data points by temperature values
        sorted_indices = np.argsort(self.temperature_values)
        sorted_t_values = self.t_values[sorted_indices]
        sorted_temperature_values = self.temperature_values[sorted_indices]

        for target_temperature in target_temperature_values:
            # Find the index where target_temperature would fit in the sorted array
            index = np.searchsorted(sorted_temperature_values, target_temperature)

            # Make sure the index is within bounds
            index = np.clip(index, 1, len(sorted_t_values) - 1)

            # Get the two closest points
            t1, t2 = sorted_t_values[index - 1], sorted_t_values[index]
            temperature1, temperature2 = sorted_temperature_values[index - 1], sorted_temperature_values[index]

            # Calculate the intersection point using the equation of the line
            slope = (t2 - t1) / (temperature2 - temperature1)
            inverse_interpolated_t = t1 + slope * (target_temperature - temperature1)

            # Ensure the result is within the range of the two closest points
            inverse_interpolated_t = np.clip(inverse_interpolated_t, min(t1, t2), max(t1, t2))

            self.results.append((target_temperature, inverse_interpolated_t))

            print(f"For Temperature = {target_temperature}, closest datapoints are: ({t1}, {temperature1}) and ({t2}, {temperature2}), inverse interpolated t = {inverse_interpolated_t}")

    def save_results(self, output_file_path):
        with open(output_file_path, "w") as file:
            file.write("# t_values T_values\n")

            for inverse_interpolated_temperature, t_value in self.results:
                result_str = f"{t_value} {inverse_interpolated_temperature}"
                file.write(result_str + "\n")

        print(f"\nResults saved to {output_file_path}")

    def plot_temperature(self):
        plt.plot(self.t_values, self.temperature_values, marker='o', linestyle='-', color='b', label='T vs t')
        plt.xlabel('t')
        plt.ylabel('T')
        plt.title('Temperature vs Time')
        plt.gca().invert_xaxis()
        # Move x-axis ticks and tick labels to the top
        ax = plt.gca()
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')

        if self.results:
            inverted_t_values = [result[1] for result in self.results]
            inverted_temperature_values = [result[0] for result in self.results]
            plt.scatter(inverted_t_values, inverted_temperature_values, marker='x', color='r', label='Inverse Interpolated Values')

        plt.legend()

    def save_plot(self, save_path):
        plt.savefig(save_path)

    def show_plot(self):
        plt.show()