# Configuration Guide
This guide helps the user properly set parameters for the Monte Carlo simulation of permeability values (that depend on water saturation and porosity of the rock - Timur's equation) necessary for the mapping of properties into a static model.

## Simulation Parameters

- **num_runs**: Number of simulation runs to perform. Typical values range from 10 to 1000 depending on the required precision.
- **num_simulations**: Number of samples per run. A higher number provides better statistical significance. Typical values range from 1000 to 10000.
- **mean_porosity**: Mean value of porosity. Typically between 0.10 and 0.30 (fraction).
- **std_dev_porosity**: Standard deviation of porosity. Typically between 0.02 and 0.05 (fraction).
- **mean_water_saturation**: Mean value of water saturation. Typically between 0.20 and 0.70 (fraction).
- **std_dev_water_saturation**: Standard deviation of water saturation. Typically between 0.05 and 0.15 (fraction).

## Sensitivity Analysis Parameters

- **sensitivity_parameter**: Parameter to analyze for sensitivity. Values are either 'phi' (porosity) or 'sw' (water saturation).
- **sensitivity_min**: Minimum value for the sensitivity analysis. Should be within the realistic range for the parameter.
- **sensitivity_max**: Maximum value for the sensitivity analysis. Should be within the realistic range for the parameter.
- **sensitivity_freq**: Number of steps between the minimum and maximum values for the sensitivity analysis. Typical values range from 5 to 20.

## Examples

### Example Configuration

```json
{
  "simulation": {
    "folder":"Permeability_Timur",
    "jobname":"Geologic_Formation",
    "num_runs": 100,
    "num_simulations": 10000,
    "mean_porosity": 0.15,
    "std_dev_porosity": 0.03,
    "mean_water_saturation": 0.35,
    "std_dev_water_saturation": 0.10
  },
  "sensitivity_analysis": {
    "sensitivity_parameter": "phi",
    "sensitivity_min": 0.05,
    "sensitivity_max": 0.30,
    "sensitivity_freq": 10
  }
}
