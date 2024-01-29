from inverse_time_interpolator import TimeInterpolatorPlotter
import matplotlib.pyplot as plt

if __name__ == "__main__":
    def process_burial_history(layers_to_process):
        inverted_z_file = "/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/burial_history/inversion/burial_history_layer_5_with_inverse.txt"
        

        plt.figure(figsize=(12, 8))
        #Define a colormap for layers
        cmap = plt.cm.get_cmap('tab10', len(layers_to_process)+1) #One colormap for the line plot
        cmap2 = plt.cm.get_cmap('inferno', len(layers_to_process)+1) #Another colormap for the scatter
        for idx, layer_number in enumerate(layers_to_process):
            data_file_path = f"/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/burial_history/burial_history_layer_{layer_number}.txt"
            output_file_path = f"/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/burial_history/inversion/burial_history_layer_{layer_number}_with_inverse_time.txt"
            output_plot_path = f"/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/burial_history/inversion/burial_history_layer_{layer_number}_with_inverse_time.png"


            plotter = TimeInterpolatorPlotter(data_file_path)
            plotter.inverse_interpolate_t(inverted_z_file)

            # Save the results to a txt file
            plotter.save_results_inverse_t(output_file_path)
            # Plot, save and show the inverse t plot. 
            #COMMENT THE LAST TWO IF YOU WANT TO PLOT EVERYTHING IN A SINGLE FIGURE
            plotter.plot_inverse_t(label=layer_number, linecolor = cmap(idx), scattercolor=cmap2(idx))
            #plotter.save_plot_inverse_t(output_plot_path)
            #plotter.show_plot_inverse_t()

        #Customize the combined plot
        plt.xlabel('t')
        plt.ylabel('Z')
        plt.title('Burial history - Inverse interpolation of t')
        plt.legend()
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()

        #Save and show the combined plot
        combine_output_path = "/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/burial_history/inversion/burial_history_with_inverse_time.png"
        plt.savefig(combine_output_path)
        print(f"\nFigure saved to {combine_output_path}")
        plt.show()

    # Specify the layers you want to process
    layers_to_process = [0, 1, 2, 3, 4, 6]

    # Process each layer
    
    process_burial_history(layers_to_process)