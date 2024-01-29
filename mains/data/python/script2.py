# script2.py
from inverse_depth_interpolator import DepthInterpolatorPlotter

if __name__ == "__main__":
    inverted_t_file = '/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/palaeo_temperature/palaeo_temperature_layer_5_with_inverse.txt'
    depth_data_file_path = '/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layer_5.txt'
    output_file_path_depth = '/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/burial_history/inversion/burial_history_layer_5_with_inverse.txt'
    save_path_depth = '/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/burial_history/inversion/burial_history_layer_5_with_inverse.png'


    depth_interpolator_plotter = DepthInterpolatorPlotter(depth_data_file_path)
    depth_interpolator_plotter.inverse_interpolate_depth(inverted_t_file)
    depth_interpolator_plotter.save_results(output_file_path_depth)

    depth_interpolator_plotter.plot_depth()
    depth_interpolator_plotter.save_plot(save_path_depth)
    depth_interpolator_plotter.show_plot()
