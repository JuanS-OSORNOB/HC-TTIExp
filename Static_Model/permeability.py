""" Monte Carlo simulation for permeability estimation and reservoir upscaling"""
import numpy as np
import matplotlib.pyplot as plt
import os

class ReservoirMonteCarloSimulation:
    def __init__(self, num_simulations, mean_porosity, std_dev_porosity, mean_water_saturation, std_dev_water_saturation):
        #Script dir
        self.script_dir = os.path.dirname(__file__)
        self.num_simulations = num_simulations
        self.mean_porosity = mean_porosity
        self.std_dev_porosity = std_dev_porosity
        self.mean_water_saturation = mean_water_saturation
        self.std_dev_water_saturation = std_dev_water_saturation
        self.permeability_values = np.zeros(num_simulations)
    """TImur's 1968 equation: https://petrophysicsequations.blogspot.com/p/permeability-timur-1968-timur-1968-also.html"""
    def timur_equation(self, porosity, water_saturation):
        return (0.93 * porosity**2.2 / water_saturation)**2
    """Compute permeability with Timur's equation"""
    def run_simulation(self, porosity_samples, water_saturation_samples):
        for i in range(self.num_simulations):
            self.permeability_values[i] = self.timur_equation(porosity_samples[i], water_saturation_samples[i])
    """Plot the histogram of the simulation"""
    def plot_histogram(self):
        hist_figname = f"hist_run_{run}.png"
        hist_filepath = os.path.join(simulation.script_dir, hist_figname)
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
    def sensitivity_analysis(self, parameter_values, sensitivity_parameter):
        sensitivity_results = []
        for value in parameter_values:
            # Create arrays of constant values for porosity and water saturation from initialized values of the class
            porosity_samples = np.random.normal(self.mean_porosity, self.std_dev_porosity, self.num_simulations)
            water_saturation_samples = np.random.normal(self.mean_water_saturation, self.std_dev_water_saturation, self.num_simulations)
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
        plt.plot([result[0] for result in sensitivity_results], [result[1] for result in sensitivity_results], label='Permeabilidad media') #Plot Mean Perm vs sensible value 
        plt.plot([result[0] for result in sensitivity_results], [result[2] for result in sensitivity_results], label='Desviación típica de Permeabilidad') #Plot Std Dev Perm vs sensible value
        plt.title(f'Analisis de sensibilidad de {sensitivity_parameter} - Cuenca Atrato')
        plt.xlabel('Porosidad')
        plt.legend()
        sensitivity_figname = f'sensitivity_analysis_{sensitivity_parameter}_run_{run}.png'
        plt.savefig(os.path.join(simulation.script_dir, sensitivity_figname))
        #plt.show()


if __name__ == "__main__":
    #OPOGADO
    num_simulations = 10000
    
    mean_porosity = 0.12
    std_dev_porosity = 0.02
    
    mean_water_saturation = 0.904
    std_dev_water_saturation = 0.05
    
    #Perform analysis over multiple runs
    for run in range(1, 11):
        simulation = ReservoirMonteCarloSimulation(num_simulations, mean_porosity, std_dev_porosity,
                                                   mean_water_saturation, std_dev_water_saturation)
        # Run the Monte Carlo simulation
        porosity_samples = np.random.normal(mean_porosity, std_dev_porosity, num_simulations)
        water_saturation_samples = np.random.normal(mean_water_saturation, std_dev_water_saturation, num_simulations)
        simulation.run_simulation(porosity_samples, water_saturation_samples)
        # Analyze and print the results of the Monte Carlo simulation
        mean_perm, std_dev_perm = simulation.analyze_results()
        print(f"RUN {run} - MONTE CARLO SIMULATION RESULTS\n    Mean Permeability: {mean_perm}, Standard Deviation of Permeability: {std_dev_perm}")
        # Plot the histogram of permeability values
        plt.figure(figsize=(10, 6))
        simulation.plot_histogram()
        plt.close()

        # Perform sensitivity analysis
        print(f"    SENSITIVITY ANALYSIS")
        parameter_values = np.linspace(0.10, 0.30, 10)
        sensitivity_parameter = "phi"
        sensitivity_results = simulation.sensitivity_analysis(parameter_values, sensitivity_parameter)
        for i, result in enumerate(sensitivity_results):
            print(f"    {i + 1} - For a value of {sensitivity_parameter}={result[0]}; Mean permeability={result[1]}, Std dev permeability={result[2]}")
        #Plot the sensitivity result
        plt.figure(figsize=(10, 6))
        simulation.plot_sensitivity(sensitivity_results)
        plt.close()
        
