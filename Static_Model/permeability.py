""" Monte Carlo simulation for permeability estimation and reservoir upscaling"""
import numpy as np
import matplotlib.pyplot as plt
import os

class ReservoirMonteCarloSimulation:
    def __init__(self, jobname, num_simulations, mean_porosity, std_dev_porosity, mean_water_saturation, std_dev_water_saturation):
        #Script dir
        self.script_dir = os.path.dirname(__file__)
        self.jobname = jobname
        self.num_simulations = num_simulations
        self.mean_porosity = mean_porosity
        self.std_dev_porosity = std_dev_porosity
        self.mean_water_saturation = mean_water_saturation
        self.std_dev_water_saturation = std_dev_water_saturation
        self.permeability_values = np.zeros(num_simulations)

        #Output file path
        self.filepath = os.path.join(self.script_dir, 'Monte Carlo')
        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)
        #Output figure path for Simulation Results
        self.simulationpath = os.path.join(self.filepath, self.jobname, 'Simulation_results')
        if not os.path.exists(self.simulationpath):
            os.makedirs(self.simulationpath)
        #Output figure path for Sensitivity results
        self.sensitivitypath = os.path.join(self.filepath, self.jobname, 'Sensitivity_results')
        if not os.path.exists(self.sensitivitypath):
            os.makedirs(self.sensitivitypath)
        
    """Timur's 1968 equation: https://petrophysicsequations.blogspot.com/p/permeability-timur-1968-timur-1968-also.html"""
    def timur_equation(self, porosity, water_saturation):
        return (93 * (porosity**2.2) / water_saturation)**2
    
    """Compute permeability with Timur's equation"""
    def run_simulation(self, porosity_samples, water_saturation_samples):
        for i in range(self.num_simulations):
            self.permeability_values[i] = self.timur_equation(porosity_samples[i], water_saturation_samples[i])

    """Plot the histogram of the simulation"""
    def plot_histogram(self):
        hist_figname = f"hist_run_{run}.png"
        hist_filepath = os.path.join(self.simulationpath, hist_figname)
        plt.hist(self.permeability_values, bins=50, color='blue', alpha=0.7)
        plt.title('Distribución de permeabilidad - Cuenca Atrato')
        plt.xlabel('Permeabilidad')
        plt.ylabel('Frecuencia')
        plt.savefig(hist_filepath)
        #plt.show()

    """Extract mean and std from permeability simulated values"""
    def analyze_results(self):
        mean_perm = np.mean(self.permeability_values)
        std_dev_perm = np.std(self.permeability_values)
        return mean_perm, std_dev_perm
    
    """Sensitivity analysis: Run the simulation with updated parameter (either Phi or Sw), store and compare"""
    """@parameter_value: Linear space from min to max with step"""
    """@parameter_name: Either phi or sw"""
    def sensitivity_analysis(self, sensitivity_parameter, parameter_values):
        sensitivity_results = []
        for value in parameter_values:
            # Create arrays of constant values for porosity and water saturation from initialized values of the class
            porosity_samples = np.random.normal(self.mean_porosity, self.std_dev_porosity, self.num_simulations)
            porosity_samples = np.clip(porosity_samples, 0, None) #Physical sense, values below zero are not accepted
            water_saturation_samples = np.random.normal(self.mean_water_saturation, self.std_dev_water_saturation, self.num_simulations)
            water_saturation_samples = np.clip(water_saturation_samples, 0, None) #Physical sense, values below zero are not accepted
            # Update the parameter being analyzed
            if sensitivity_parameter.lower() == 'phi':
                porosity_samples = np.full(self.num_simulations, value)
            elif sensitivity_parameter.lower() == 'sw':
                water_saturation_samples = np.full(self.num_simulations, value)
            # Run the simulation with the updated parameter
            self.run_simulation(porosity_samples, water_saturation_samples)
            # Analyze the results and store them
            mean_perm, std_dev_perm = self.analyze_results()
            sensitivity_results.append((value, mean_perm, std_dev_perm))
        return sensitivity_results
    
    def plot_sensitivity(self, sensitivity_results):
        # Plot sensitivity results
        plt.plot([result[0] for result in sensitivity_results], [result[1] for result in sensitivity_results], label='Permeabilidad media') #Plot Mean Perm vs Sensitivity value 
        plt.plot([result[0] for result in sensitivity_results], [result[2] for result in sensitivity_results], label='Desviación típica de Permeabilidad') #Plot Std Dev Perm vs Sensitivity value
        plt.title(f'Analisis de sensibilidad de {sensitivity_parameter} - Cuenca Atrato')
        plt.xlabel(f'{sensitivity_parameter}')
        plt.ylabel('Permeabilidad: Media y Desviacion tipica')
        plt.legend()
        figurepath = os.path.join(self.sensitivitypath, sensitivity_parameter)
        if not os.path.exists(figurepath):
            os.makedirs(figurepath)
        sensitivity_figname = f'sensitivity_analysis_{sensitivity_parameter}_run_{run}.png'
        plt.savefig(os.path.join(figurepath, sensitivity_figname))
        #plt.show()

class Simulationresults:
    def __init__(self):
        self.simu_lines_to_write = []
    
    def add_simulation_line(self, line):
        self.simu_lines_to_write.append(line)
    
    def write_simulation_results(self, simulationpath):
            filename = f"simulation_results.txt"
            filepath = os.path.join(simulationpath, filename)
            with open(filepath, 'w') as file:
                for line in self.simu_lines_to_write:
                    file.write(line + '\n')

class Sensitivityresults:
    def __init__(self):
        self.sens_lines_to_write = []

    def add_sensitivity_line(self, line):
        self.sens_lines_to_write.append(line)
        
    def write_sensitivity_results(self, sensitivitypath):
        filename = f"sensitivity_results.txt"
        filepath = os.path.join(sensitivitypath, sensitivity_parameter, filename)
        with open(filepath, 'w') as file:
            for line in self.sens_lines_to_write:
                file.write(line + '\n')

##############################################################################
#region Main
if __name__ == "__main__":
    #JOB --CHANGE PARAMETERS
    jobname = 'fm_clavo'
    num_simulations = 10000

    mean_porosity = 0.12 #No more than 30% for every section
    std_dev_porosity = 0.02#0.07
    
    mean_water_saturation = 0.9
    std_dev_water_saturation = 0.03#0.08
    ##############################
    montecarloresults = Simulationresults()
    montecarloresults.add_simulation_line(f"#Mean_Perm Std_dev_Perm")
    
    sensitivityresults = Sensitivityresults()
    sensitivityresults.add_sensitivity_line(f"#Value Mean_Perm Std_dev_Perm")
    ##############################
    porosity_samples_list = []
    water_saturation_samples_list = []
    for run in range(1, 26):#--CHANGE NUMBER OF RUNS
        simulation = ReservoirMonteCarloSimulation(jobname, num_simulations, mean_porosity, std_dev_porosity,
                                                   mean_water_saturation, std_dev_water_saturation)
        # Run the Monte Carlo simulation
        porosity_samples = np.random.normal(mean_porosity, std_dev_porosity, num_simulations)
        porosity_samples = np.clip(porosity_samples, 0, None) #Physical sense, values below zero are not accepted
        porosity_samples_list.append(porosity_samples)
        water_saturation_samples = np.random.normal(mean_water_saturation, std_dev_water_saturation, num_simulations)
        water_saturation_samples = np.clip(water_saturation_samples, 0, None) #Physical sense, values below zero are not accepted
        water_saturation_samples_list.append(water_saturation_samples)
        simulation.run_simulation(porosity_samples, water_saturation_samples)
        # Analyze, print and write the results of the Monte Carlo simulation
        mean_perm, std_dev_perm = simulation.analyze_results()
        print(f"RUN {run} - MONTE CARLO SIMULATION RESULTS\n    Mean Permeability: {mean_perm}, Standard Deviation of Permeability: {std_dev_perm}")
        line = f"{mean_perm} {std_dev_perm}"
        montecarloresults.add_simulation_line(line)
        # Plot the histogram of permeability values
        plt.figure(figsize=(10, 6))
        simulation.plot_histogram()
        plt.close()

        # Perform sensitivity analysis -- CHANGE PARAMETERS
        print(f"    SENSITIVITY ANALYSIS")
        sensitivity_parameter = 'phi'
        parameter_values = np.linspace(0.06, 0.3, 6) #For Phi usually take between 5 and 40%. For Sw usually take between 40 and 80%.
        sensitivity_results = simulation.sensitivity_analysis(sensitivity_parameter, parameter_values)
        for i, result in enumerate(sensitivity_results):
            print(f"    {i + 1} - For a value of {sensitivity_parameter}={result[0]}; Mean permeability={result[1]}, Std dev permeability={result[2]}")
            line = f"{result[0]}, {result[1]}, {result[2]}"
            sensitivityresults.add_sensitivity_line(line)
        #Plot the sensitivity result
        plt.figure(figsize=(10, 6))
        simulation.plot_sensitivity(sensitivity_results)
        plt.close()
    

    ########## Writing the Phi ans Sw samples to files ##########
    path1 = os.path.join(simulation.simulationpath, 'phi_samples')
    #Phi samples
    if not os.path.exists(path1):
        os.makedirs(path1)
    for i, porosity_samples in enumerate(porosity_samples_list):
        filename = os.path.join(path1, f'porosity_samples_{i + 1}.txt')
        with open(filename, 'w') as file:
            for value in porosity_samples:
                #porosity = np.array2string(porosity_samples)
                file.write(str(value) + '\n')
    file.close()
    #Sw samples
    path2 = os.path.join(simulation.simulationpath, 'sw_samples')
    if not os.path.exists(path2):
        os.makedirs(path2)
    for i, water_saturation_samples in enumerate(water_saturation_samples_list):
        filename = os.path.join(path2, f'water_saturation_samples_{i + 1}.txt')
        with open(filename, 'w') as file:
            for value in water_saturation_samples:
                #porosity = np.array2string(porosity_samples)
                file.write(str(value) + '\n')
    file.close()

    montecarloresults.write_simulation_results(simulation.simulationpath)
    sensitivityresults.write_sensitivity_results(simulation.sensitivitypath)
    #endregion