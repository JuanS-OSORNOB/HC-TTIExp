# script1.py
from inverse_temperature_interpolator import TemperatureInterpolatorPlotter

if __name__ == "__main__":
    data_file_path = '/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/palaeo_temperature/palaeo_temperature_layer_5.txt'
    target_temperature_file = '/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/palaeo_temperature/target_temperatures.txt'
    output_file_path = '/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/palaeo_temperature/palaeo_temperature_layer_5_with_inverse.txt'
    save_path = '/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/palaeo_temperature/palaeo_temperature_layer_5_with_inverse.png'

    temp_interpolator_plotter = TemperatureInterpolatorPlotter(data_file_path)
    temp_interpolator_plotter.inverse_interpolate(target_temperature_file)
    temp_interpolator_plotter.save_results(output_file_path)

    temp_interpolator_plotter.plot_temperature()
    temp_interpolator_plotter.save_plot(save_path)
    temp_interpolator_plotter.show_plot()
