import sys, os
from pathlib import Path
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from utils.config import Config
from montecarlo import ReservoirMonteCarloSimulation, Simulationresults, Sensitivityresults
import matplotlib.pyplot as plt

def main():
    #JOB --CHANGE PARAMETERS
    cwd = os.getcwd()
    config_path = os.path.join(cwd, 'config.json')
    config = Config.load_config(config_path)

    simulation = ReservoirMonteCarloSimulation(config)
    
    montecarloresults = Simulationresults()
    montecarloresults.add_simulation_line(f"#Mean_Perm Std_dev_Perm")
    
    sensitivityresults = Sensitivityresults()
    ##############################
    porosity_samples_list = []
    water_saturation_samples_list = []
    
    for run in range(1, config['num_runs']):
        #region Run simulation
        porosity_samples, water_saturation_samples = simulation.generate_samples()
        porosity_samples_list.append(porosity_samples)
        water_saturation_samples_list.append(water_saturation_samples)
        
        simulation.run_simulation()
        #endregion
        
        #region Analyze results
        mean_perm, std_dev_perm = simulation.analyze_results()
        print(f"RUN {run} - MONTE CARLO SIMULATION RESULTS\n    Mean Permeability: {mean_perm}, Standard Deviation of Permeability: {std_dev_perm}")
        line = f"{mean_perm} {std_dev_perm}"
        montecarloresults.add_simulation_line(line)
        
        # Plot the histogram of permeability values
        #plt.figure(figsize=(10, 6))
        simulation.plot_histogram(run)
        #plt.close()

        # Perform sensitivity analysis -- CHANGE PARAMETERS
        print(f"    SENSITIVITY ANALYSIS")
        #sensitivity_parameter = 'sw'#Choose = phi, sw
        
        sensitivites = sensitivityresults.perform_sensitivity(simulation)
        
        #Plot the sensitivity result
        plt.figure(figsize=(10, 6))
        simulation.plot_sensitivity(sensitivites)
        plt.close()
    

    ########## Writing the Phi ans Sw samples to files ##########

    montecarloresults.write_samples(simulation, 'phi', porosity_samples_list)
    montecarloresults.write_samples(simulation, 'sw', water_saturation_samples_list)
    montecarloresults.write_simulation_results(simulation.simulationpath)

    sensitivityresults.write_sensitivity_results(simulation.sensitivitypath)
    #endregion

if __name__ == "__main__":
    main()