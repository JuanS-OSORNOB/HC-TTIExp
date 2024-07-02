""" Monte Carlo simulation for permeability estimation and reservoir upscaling"""
import numpy as np
import matplotlib.pyplot as plt
import os, sys

cwd = os.getcwd()
sys.path.append(cwd)

from utils.foldermanagement import Foldermanagement
foldermanagement = Foldermanagement()

#region Simulation
class ReservoirMC:
    def __init__(self, config):
        self.script_dir = os.path.dirname(__file__)
        self.config = config

        self.folder = self.config['folder']
        self.jobname = self.config['jobname']
        self.num_simulations = self.config['num_simulations']
        self.num_runs = self.config['num_runs']
        self.mean_porosity = self.config['mean_porosity']
        self.std_dev_porosity = self.config['std_dev_porosity']
        self.mean_water_saturation = self.config['mean_water_saturation']
        self.std_dev_water_saturation = self.config['std_dev_water_saturation']

        self.permeability_values = np.zeros(self.num_simulations) #Begin predicted parameter with zero
        self.setup_directories()
    
    def setup_directories(self):
        self.filepath = foldermanagement._create_directory(os.path.join(cwd, 'Static_Model', self.folder))

    @staticmethod
    def timur_equation(porosity, water_saturation):
        """Timur's 1968 equation: https://petrophysicsequations.blogspot.com/p/permeability-timur-1968-timur-1968-also.html
        """
    
        """ if water_saturation == 0:
            water_saturation = 0.0001 #Small number to avoid division by zero """
        if water_saturation == 0:
            water_saturation = 0.1
        permeability = ((93 * (porosity**2.2))/ water_saturation)**2
        return permeability

    def generate_samples(self):
        porosity_samples = np.random.normal(self.mean_porosity, self.std_dev_porosity, self.num_simulations)
        porosity_samples = np.clip(porosity_samples, 0, None) #Physical sense, values below zero are not accepted
        
        water_saturation_samples = np.random.normal(self.mean_water_saturation, self.std_dev_water_saturation, self.num_simulations)
        water_saturation_samples = np.clip(water_saturation_samples, 0.1, None) #Physical sense, values below zero are not accepted
        
        return porosity_samples, water_saturation_samples

    #NOTE I'm not using the generated samples from before because this will also be used for sensitivity analysis.
    def run_simulation(self, porosity_samples, water_saturation_samples):
        for i in range(self.num_simulations):
            self.permeability_values[i] = self.timur_equation(porosity_samples[i], water_saturation_samples[i])
    
    def analyze_results(self):
        mean_perm = np.mean(self.permeability_values)
        std_dev_perm = np.std(self.permeability_values)
        return mean_perm, std_dev_perm

class WritingFilesMC:
    def __init__(self, simulation):
        self.simulation = simulation
        self.simu_lines_to_write = []
        self.setup_directories()
    
    def setup_directories(self):
        self.simulationpath = foldermanagement._create_directory(os.path.join(self.simulation.filepath, self.simulation.jobname, 'Simulation_results'))
    
    def add_simulation_line(self, line):
        self.simu_lines_to_write.append(line)
    
    def print_simulation(self, run):
        mean_perm, std_dev_perm = self.simulation.analyze_results()
        print(f"RUN {run + 1} - MONTE CARLO SIMULATION RESULTS\n    Mean Permeability: {mean_perm}, Standard Deviation of Permeability: {std_dev_perm}")
        
    def write_samples(self, parameter, samples_list):
        parameter_samples = parameter + '_samples'
        path = os.path.join(self.simulationpath, parameter_samples)
        foldermanagement._create_directory(path)

        for i, samples in enumerate(samples_list):
            filename = os.path.join(path, f'{parameter_samples}_{i + 1}.txt')
            with open(filename, 'w') as file:
                for value in samples:
                    file.write(str(value) + '\n')
            file.close()

    def write_simulation_results(self, mean_perm_list, std_dev_perm_list):
        self.add_simulation_line(f"Mean_Perm, Std_dev_Perm")
        for mean_perm, std_dev_perm in zip(mean_perm_list, std_dev_perm_list):
            line = f"{mean_perm}, {std_dev_perm}"
            self.add_simulation_line(line)
        
        filename = f'simulation_results.csv'
        filepath = os.path.join(self.simulationpath, filename)
        with open(filepath, 'w') as file:
            for line in self.simu_lines_to_write:
                file.write(line + '\n')

class PlottingFilesMC:
    def __init__(self, simulation, writtermc):
        """Initializer for plotter class.

        Args:
            simulation (_type_): Instance of class *ReservoirMC*
            writtermc (_type_): Instance of class *WritingFilesMC*
        """
        self.simulation = simulation
        self.writtermc = writtermc
    
    def plot_histogram(self, run):
        plt.figure(figsize=(10, 6))
        hist_figname = f"hist_run_{run + 1}.png"
        hist_filepath = os.path.join(self.writtermc.simulationpath, hist_figname)
        print("10 first permeability values to plot:", self.simulation.permeability_values[:10])
        plt.hist(self.simulation.permeability_values, bins=1000, color='blue', alpha=0.7, density = True)
        plt.title(f'Distribución de permeabilidad: {self.simulation.jobname} - Cuenca Atrato')
        plt.xlabel('Permeabilidad')
        plt.ylabel('Frecuencia')
        plt.savefig(hist_filepath)
        plt.close()
        #plt.show()

#endregion
#region Sensitivity
class SensitivityMC:
    def __init__(self):
        pass
    
    @staticmethod
    def sensitivity_analysis(simulation):
        config = simulation.config
        parameter_values = np.linspace(config['sensitivity_min'], config['sensitivity_max'], config['sensitivity_freq'])
        sensitivity_results = []
        for value in parameter_values:
            # Create arrays of constant values for porosity and water saturation from initialized values of the class
            porosity_samples = np.random.normal(simulation.mean_porosity, simulation.std_dev_porosity, simulation.num_simulations)
            porosity_samples = np.clip(porosity_samples, 0, None) #Physical sense, values below zero are not accepted

            water_saturation_samples = np.random.normal(simulation.mean_water_saturation, simulation.std_dev_water_saturation, simulation.num_simulations)
            water_saturation_samples = np.clip(water_saturation_samples, 0, None) #Physical sense, values below zero are not accepted

            #Update parameter being analyzed
            if config['sensitivity_parameter'] == 'phi':
                porosity_samples = np.full(simulation.num_simulations, value)
            elif config['sensitivity_parameter'] == 'sw':
                water_saturation_samples = np.full(simulation.num_simulations, value)
            
            #Run simulation with updated parameter
            simulation.run_simulation(porosity_samples, water_saturation_samples)

            #Analyze the results and store them
            mean_perm, std_dev_perm = simulation.analyze_results()

            sensitivity_results.append((value, mean_perm, std_dev_perm))
        
        return sensitivity_results

class WritingFileSens:
    def __init__(self, simulation, sensitivitymc):
        """_summary_

        Args:
            simulation (_type_): Instance of class *ReservoirMC*
            sensitivitymc (_type_): Instance of class *SensitivityMC*
        """
        self.simulation = simulation
        self.config = self.simulation.config
        self.sensitivitymc = sensitivitymc
        self.sens_lines_to_write = []
        self.setup_directories()
    
    def setup_directories(self):
        self.sensitivitypath = foldermanagement._create_directory(os.path.join(self.simulation.filepath, self.simulation.jobname, 'Sensitivity_results'))
    
    def add_sensitivity_line(self, line):
        self.sens_lines_to_write.append(line)
    
    def print_sensitivity(self):
        sensitivity_results = self.sensitivitymc.sensitivity_analysis(self.simulation)
        for i, sensitivity_result in enumerate(sensitivity_results):
            print(f"    {i + 1} - For a value of {self.config['sensitivity_parameter']}={sensitivity_result[0]}; Mean permeability={sensitivity_result[1]}, Std dev permeability={sensitivity_result[2]}")

    def write_sensitivity_results(self):
        sensitivity_results = self.sensitivitymc.sensitivity_analysis(self.simulation)
        self.add_sensitivity_line(f"{self.config['sensitivity_parameter']}, Mean_Perm, Std_dev_Perm")
        for sensitivity_result in sensitivity_results:
            line = f"{sensitivity_result[0]}, {sensitivity_result[1]}, {sensitivity_result[2]}"
            self.add_sensitivity_line(line)
        
        directory_path = os.path.join(self.sensitivitypath, self.config['sensitivity_parameter'])
        foldermanagement._create_directory(directory_path)

        filename = f"sensitivity_results.csv"
        filepath = os.path.join(directory_path, filename)
        with open(filepath, 'w') as file:
            for line in self.sens_lines_to_write:
                file.write(line + '\n')
        file.close()

class PlottingFileSens:
    def __init__(self, simulation, sensitivitymc, writersens):
        self.simulation = simulation
        self.sensitivitymc = sensitivitymc
        self.config = self.simulation.config
        self.writersens = writersens
    
    def plot_sensitivity(self, run):
            sensitivity_results = self.sensitivitymc.sensitivity_analysis(self.simulation)
            # Plot sensitivity results
            plt.figure(figsize=(10, 6))
            plt.plot([result[0] for result in sensitivity_results], [result[1] for result in sensitivity_results], label='Permeabilidad media') #Plot: Mean Perm VS Sensitivity value 
            plt.plot([result[0] for result in sensitivity_results], [result[2] for result in sensitivity_results], label='Desviación típica de Permeabilidad') #Plot: Std Dev Perm VS Sensitivity value
            plt.title(f"Analisis de sensibilidad de {self.config['sensitivity_parameter']}: {self.simulation.jobname} - Cuenca Atrato")
            plt.xlabel(f"{self.config['sensitivity_parameter']}")
            plt.ylabel('Permeabilidad: Media y Desviacion tipica')
            plt.legend()
            figurepath = os.path.join(self.writersens.sensitivitypath, self.config['sensitivity_parameter'])
            foldermanagement._create_directory(figurepath)
            sensitivity_figname = f"sensitivity_analysis_{self.config['sensitivity_parameter']}_run_{run + 1}.png"
            plt.savefig(os.path.join(figurepath, sensitivity_figname))
            plt.close()
            #plt.show()
#endregion