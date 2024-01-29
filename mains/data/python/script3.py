from inverse_time_interpolator import TimeInterpolatorPlotter

if __name__ == "__main__":
    def process_burial_history(layer_number):
        inverted_z_file = "/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/burial_history/inversion/burial_history_layer_5_with_inverse.txt"
        
        data_file_path = f"/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layer_{layer_number}.txt"
        output_file_path = f"/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/burial_history/inversion/burial_history_layer_{layer_number}_with_inverse_time.txt"
        output_plot_path = f"/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/burial_history/inversion/burial_history_layer_{layer_number}_with_inverse_time.png"


        plotter = TimeInterpolatorPlotter(data_file_path)
        plotter.inverse_interpolate_t(inverted_z_file)

        # Save the results to a txt file
        plotter.save_results_inverse_t(output_file_path)
        # Plot, save and show the inverse t plot
        plotter.plot_inverse_t()
        plotter.save_plot_inverse_t(output_plot_path)
        plotter.show_plot_inverse_t()

    # Specify the layers you want to process
    layers_to_process = [0, 1, 2, 3, 4, 6]

    # Process each layer
    for layer_number in layers_to_process:
        process_burial_history(layer_number)