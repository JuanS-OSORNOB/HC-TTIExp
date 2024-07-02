import sys, os
cwd = os.getcwd()
print(f"cwd: {cwd}")
sys.path.append(str(cwd))

from utils.config import Config
from montecarlosimulation import ReservoirMC, WritingFilesMC, PlottingFilesMC, SensitivityMC, WritingFileSens, PlottingFileSens

def main():
    config_path = os.path.join(cwd, 'config.json')
    config = Config.load_config(config_path)

    simulation = ReservoirMC(config)


    porosity_samples_list, water_saturation_samples_list = [], []
    mean_perm_list, std_dev_perm_list = [], []
    for run in range(config['num_runs']):
        porosity_samples, water_saturation_samples = simulation.generate_samples()
        porosity_samples_list.append(porosity_samples)
        water_saturation_samples_list.append(water_saturation_samples)

        simulation.run_simulation(porosity_samples, water_saturation_samples)

        mcfilewriter = WritingFilesMC(simulation)
        mcfilewriter.print_simulation(run)

        mean_perm, std_dev_perm = simulation.analyze_results()
        mean_perm_list.append(mean_perm)
        std_dev_perm_list.append(std_dev_perm)

        mcplotter = PlottingFilesMC(simulation)
        mcplotter.plot_histogram(run)
        
    mcfilewriter.write_simulation_results(mean_perm_list, std_dev_perm_list)

    mcfilewriter.write_samples('phi', porosity_samples_list)
    mcfilewriter.write_samples('sw', water_saturation_samples_list)
    

        

if __name__ == '__main__':
    main()