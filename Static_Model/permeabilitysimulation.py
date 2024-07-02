import sys, os
cwd = os.getcwd()
print(f"cwd: {cwd}")
sys.path.append(str(cwd))
from utils.config import Config
from montecarlosimulation import ReservoirMC, WritingFilesMC, PlottingFilesMC, SensitivityMC, WritingFileSens, PlottingFileSens


def main():
    config_path = os.path.join(cwd, 'config.json')
    config = Config.load_config(config_path)

    porosity_samples_list, water_saturation_samples_list = [], []
    timur_output_list = []
    mean_perm_list, std_dev_perm_list = [], []
    for run in range(config['num_runs']):
        simulation = ReservoirMC(config)  # Create a new instance for each run
        porosity_samples, water_saturation_samples = simulation.generate_samples()
        porosity_samples_list.append(porosity_samples)
        water_saturation_samples_list.append(water_saturation_samples)

        #Run simulation
        simulation.run_simulation(porosity_samples, water_saturation_samples)
        timur_output_list.append(simulation.permeability_values.copy())
        
        #Print simulation results
        mcfilewriter = WritingFilesMC(simulation)
        mcfilewriter.print_simulation(run)
        print("\nPorosity samples: ", porosity_samples[:10])
        print("Water saturation samples: ", water_saturation_samples[:10])
        print("Permeability values: ", simulation.permeability_values[:10], "\n")

        #Append to list to write on a file 
        mean_perm, std_dev_perm = simulation.analyze_results()
        mean_perm_list.append(mean_perm)
        std_dev_perm_list.append(std_dev_perm)
        #Plot histogram
        mcplotter = PlottingFilesMC(simulation, mcfilewriter)
        
        mcplotter.plot_histogram(run)
        

        #Sensitivity
        sensitivitymc = SensitivityMC()
        mcsenswriter = WritingFileSens(simulation, sensitivitymc)
        mcfilewriter.simulation.reset_permeability_values()
        mcsenswriter.print_sensitivity()
        print("\n")
        #Plotting sensitivity
        mcsensplotter = PlottingFileSens(simulation, sensitivitymc, mcsenswriter)
        mcsensplotter.plot_sensitivity(run)

    #Write samples        
    mcfilewriter.write_samples('phi', porosity_samples_list)
    mcfilewriter.write_samples('sw', water_saturation_samples_list)
    #Writing a file of samples and computed permeability
    mcfilewriter.write_timur_in_out(porosity_samples_list, water_saturation_samples_list, timur_output_list)
    #Write results to file"""  """
    mcfilewriter.write_simulation_results(mean_perm_list, std_dev_perm_list)
    #Write sensitivity to file
    mcsenswriter.write_samples_sens()
    mcsenswriter.write_sensitivity_results()


if __name__ == '__main__':
    main()