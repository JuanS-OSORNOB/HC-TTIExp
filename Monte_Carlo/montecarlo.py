""" Monte Carlo simulation for permeability estimation and reservoir upscaling"""
import numpy as np
import matplotlib.pyplot as plt
import os

class ReservoirMonteCarloSimulation:
    def __init__(self, config):
        self.script_dir = os.path.dirname(__file__) #Script dir
        self.config = config
        
        self.jobname = self.config['jobname']
        self.num_simulations = self.config['num_simulations']
        self.num_runs = self.config['num_runs']
        self.mean_porosity = self.config['mean_porosity']
        self.std_dev_porosity = self.config['std_dev_porosity']
        self.mean_water_saturation = self.config['mean_water_saturation']
        self.std_dev_water_saturation = self.config['std_dev_water_saturation']
        
        self.permeability_values = np.zeros(self.num_simulations)

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

    @property
    def get_simulationpath(self):
        return self.simulationpath

    #region Timur's equation
    """Timur's 1968 equation: https://petrophysicsequations.blogspot.com/p/permeability-timur-1968-timur-1968-also.html"""
    @staticmethod
    def timur_equation(porosity, water_saturation):
        if water_saturation == 0:
            water_saturation = 0.0001 #Small number to avoid division by zero
        return (93 * (porosity**2.2) / water_saturation)**2
    
    def generate_samples(self):
        porosity_samples = np.random.normal(self.config['mean_porosity'], self.config['std_dev_porosity'], self.config['num_simulations'])
        porosity_samples = np.clip(porosity_samples, 0, None) #Physical sense, values below zero are not accepted
        
        water_saturation_samples = np.random.normal(self.config['mean_water_saturation'], self.config['std_dev_water_saturation'], self.config['num_simulations'])
        water_saturation_samples = np.clip(water_saturation_samples, 0, None) #Physical sense, values below zero are not accepted
        
        return porosity_samples, water_saturation_samples
    
    """Compute permeability with Timur's equation"""
    def run_simulation(self, porosity_samples, water_saturation_samples):
        #porosity_samples, water_saturation_samples = self.generate_samples()
        for i in range(self.num_simulations):
            self.permeability_values[i] = self.timur_equation(porosity_samples[i], water_saturation_samples[i])

    """Plot the histogram of the simulation"""
    def plot_histogram(self, run):
        plt.figure(figsize=(10, 6))
        hist_figname = f"hist_run_{run}.png"
        hist_filepath = os.path.join(self.simulationpath, hist_figname)
        plt.hist(self.permeability_values, bins=50, color='blue', alpha=0.7)
        plt.title(f'Distribución de permeabilidad: {self.jobname} - Cuenca Atrato')
        plt.xlabel('Permeabilidad')
        plt.ylabel('Frecuencia')
        plt.savefig(hist_filepath)
        plt.close()
        #plt.show()

    """Extract mean and std from permeability simulated values"""
    def analyze_results(self):
        mean_perm = np.mean(self.permeability_values)
        std_dev_perm = np.std(self.permeability_values)
        return mean_perm, std_dev_perm
    #endregion Timur's equation

    #region Sensitivity
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
    
    def plot_sensitivity(self, sensitivity_parameter, run):
        sensitivity_results = self.sensitivity_analysis(sensitivity_parameter)
        # Plot sensitivity results
        plt.figure(figsize=(10, 6))
        plt.plot([result[0] for result in sensitivity_results], [result[1] for result in sensitivity_results], label='Permeabilidad media') #Plot: Mean Perm vs Sensitivity value 
        plt.plot([result[0] for result in sensitivity_results], [result[2] for result in sensitivity_results], label='Desviación típica de Permeabilidad') #Plot: Std Dev Perm vs Sensitivity value
        plt.title(f'Analisis de sensibilidad de {sensitivity_parameter}: {self.jobname} - Cuenca Atrato')
        plt.xlabel(f'{sensitivity_parameter}')
        plt.ylabel('Permeabilidad: Media y Desviacion tipica')
        plt.legend()
        figurepath = os.path.join(self.sensitivitypath, sensitivity_parameter)
        if not os.path.exists(figurepath):
            os.makedirs(figurepath)
        sensitivity_figname = f'sensitivity_analysis_{sensitivity_parameter}_run_{run}.png'
        plt.savefig(os.path.join(figurepath, sensitivity_figname))
        plt.close()
        #plt.show()
    #endregion Sensitivity

#region Results
class Simulationresults:
    def __init__(self):
        self.simu_lines_to_write = []
    
    def add_simulation_line(self, line):
        self.simu_lines_to_write.append(line)
    
    def write_samples(self, simulation_instance, variable, samples_list):
        simulation_path = simulation_instance.get_simulationpath()
        variable_samples = variable + '_samples'
        path = os.path.join(simulation_path, variable_samples)
        if not os.path.exists(path):
            os.makedirs(path)
        
        for i, samples in enumerate(samples_list):
            filename = os.path.join(path, f'{variable_samples}_{i + 1}.txt')
            with open(filename, 'w') as file:
                for value in samples:
                    file.write(str(value) + '\n')
        file.close()

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

    def perform_sensitivity(self, simulation_instance):
        config = simulation_instance.config
        parameter_values = np.linspace(config['sensitivity_min'], config['sensitivity_max'], config['sensitivity_freq']) #For Phi usually take between 5 and 40%. For Sw usually take between 40 and 80%.
        sensitivities = simulation_instance.sensitivity_analysis(config['sensitivity_parameter'], parameter_values)
        self.add_sensitivity_line(f"#Value Mean_Perm Std_dev_Perm")
        for i, sensitivity in enumerate(sensitivities):
            print(f"    {i + 1} - For a value of {config['sensitivity_parameter']}={sensitivity[0]}; Mean permeability={sensitivity[1]}, Std dev permeability={sensitivity[2]}")
            line = f"{sensitivity[0]}, {sensitivity[1]}, {sensitivity[2]}"
            self.add_sensitivity_line(line)
        return sensitivities
        
    def write_sensitivity_results(self, sensitivitypath, sensitivity_parameter):
        filename = f"sensitivity_results.txt"
        filepath = os.path.join(sensitivitypath, sensitivity_parameter, filename)
        with open(filepath, 'w') as file:
            for line in self.sens_lines_to_write:
                file.write(line + '\n')
#endregion results