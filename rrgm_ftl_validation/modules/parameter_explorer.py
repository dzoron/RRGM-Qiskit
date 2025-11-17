"""
RRGM FTL Validation Toolkit - Module 2: Parameter Space Explorer

Maps λ_int/λ_ext ratios needed for FTL-equivalent scenarios.
Calculates energy costs for maintaining different RPG strengths.
Shows collapse threshold boundaries.
Generates parameter space heatmaps and requirement tables.

Based on Section 5 and 7 of the RRGM FTL paper.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
import json
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import (
    PhysicalConstants,
    RRGMParameters,
    SimulationDefaults,
    effective_decay_rate,
    FTL_effective_velocity,
    get_default_config,
)
from utils.plotting import (
    plot_parameter_heatmap,
    plot_FTL_requirements,
    save_figure,
)


class ParameterSpaceExplorer:
    """
    Explore RRGM FTL parameter space

    Calculates:
    - FTL-equivalent velocity requirements
    - Energy costs for RIF maintenance
    - Collapse threshold boundaries
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize parameter space explorer

        Parameters:
        -----------
        config : dict, optional
            Configuration dictionary
        """
        self.config = config if config is not None else get_default_config()
        self.results = {}

    def calculate_FTL_requirements(self,
                                   distances: np.ndarray,
                                   transit_times: np.ndarray,
                                   λ_ext: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculate λ_int/λ_ext requirements for FTL-equivalent transit

        For endpoint-only realization between A and B:
        v_eff = L / t_external
        FTL requires v_eff > c

        Parameters:
        -----------
        distances : array
            Transit distances (meters)
        transit_times : array
            External transit times (seconds)
        λ_ext : float, optional
            External decay rate

        Returns:
        --------
        results : dict
            FTL requirement analysis
        """
        if λ_ext is None:
            λ_ext = self.config['rrgm']['λ_ext_default']

        c = PhysicalConstants.c

        # Create parameter grid
        λ_ratios = np.logspace(-4, 0, 50)  # λ_int/λ_ext from 0.0001 to 1
        dist_grid, ratio_grid = np.meshgrid(distances, λ_ratios)

        results = {
            'distances': distances,
            'transit_times': transit_times,
            'λ_ratios': λ_ratios,
            'λ_ext': λ_ext,
        }

        # For each (distance, λ_ratio), calculate v_eff
        v_eff_grid = np.zeros_like(dist_grid)
        v_ratio_grid = np.zeros_like(dist_grid)
        is_FTL_grid = np.zeros_like(dist_grid, dtype=bool)

        for i, ratio in enumerate(λ_ratios):
            λ_int = ratio * λ_ext

            # Recursive delay factor: how much "internal time" per "external time"
            # If λ_int << λ_ext, structure survives longer internally
            delay_factor = λ_ext / λ_int if λ_int > 0 else np.inf

            for j, (distance, t_ext) in enumerate(zip(distances, transit_times)):
                # Effective velocity for endpoint-only realization
                ftl_calc = FTL_effective_velocity(distance, t_ext, λ_int, λ_ext, c)

                v_eff_grid[i, j] = ftl_calc['v_effective']
                v_ratio_grid[i, j] = ftl_calc['v_ratio_to_c']
                is_FTL_grid[i, j] = ftl_calc['is_FTL_equivalent']

        results['v_effective_grid'] = v_eff_grid
        results['v_ratio_grid'] = v_ratio_grid
        results['is_FTL_grid'] = is_FTL_grid

        # Find minimum λ_ratio for FTL at each distance
        min_ratio_for_FTL = np.zeros(len(distances))
        for j in range(len(distances)):
            ftl_indices = np.where(is_FTL_grid[:, j])[0]
            if len(ftl_indices) > 0:
                min_ratio_for_FTL[j] = λ_ratios[ftl_indices[0]]
            else:
                min_ratio_for_FTL[j] = np.nan

        results['min_λ_ratio_for_FTL'] = min_ratio_for_FTL

        self.results['ftl_requirements'] = results
        return results

    def calculate_energy_costs(self,
                              χ_values: np.ndarray,
                              volumes: np.ndarray,
                              duration: float = 1.0,
                              energy_density_scale: float = 1e6) -> Dict[str, Any]:
        """
        Estimate energy costs for maintaining RIF with different χ strengths

        Simplified model: E_RIF ∝ χ² × V × t × ε₀

        Parameters:
        -----------
        χ_values : array
            RPG field strengths
        volumes : array
            RIF volumes (m³)
        duration : float
            Maintenance duration (seconds)
        energy_density_scale : float
            Energy density scale factor (J/m³/s)

        Returns:
        --------
        results : dict
            Energy cost analysis
        """
        # Create grid
        χ_grid, vol_grid = np.meshgrid(χ_values, volumes)

        # Energy cost model: E ∝ χ² × V × t
        # Higher χ requires more energy to suppress external coupling
        energy_grid = energy_density_scale * (χ_grid**2) * vol_grid * duration

        # Convert to practical units
        energy_kWh = energy_grid / 3.6e6  # Joules to kWh

        results = {
            'χ_values': χ_values,
            'volumes': volumes,
            'duration': duration,
            'energy_grid_joules': energy_grid,
            'energy_grid_kWh': energy_kWh,
            'energy_density_scale': energy_density_scale,
        }

        # Calculate specific scenarios
        scenarios = []
        for χ in [0.5, 0.9, 0.99]:
            for vol in [1e-9, 1e-6, 1e-3]:  # nm³, μm³, mm³
                E_J = energy_density_scale * (χ**2) * vol * duration
                E_kWh = E_J / 3.6e6
                scenarios.append({
                    'χ': χ,
                    'volume_m3': vol,
                    'duration_s': duration,
                    'energy_J': E_J,
                    'energy_kWh': E_kWh,
                })

        results['scenarios'] = scenarios

        self.results['energy_costs'] = results
        return results

    def map_collapse_boundaries(self,
                                λ_ratios: np.ndarray,
                                coherence_times: np.ndarray,
                                target_fidelity: float = 0.9) -> Dict[str, Any]:
        """
        Map boundaries where collapse becomes favorable vs unfavorable

        Parameters:
        -----------
        λ_ratios : array
            λ_int/λ_ext ratios
        coherence_times : array
            Required coherence times (seconds)
        target_fidelity : float
            Target final fidelity

        Returns:
        --------
        results : dict
            Collapse boundary analysis
        """
        λ_ext = self.config['rrgm']['λ_ext_default']

        # Create grid
        ratio_grid, time_grid = np.meshgrid(λ_ratios, coherence_times)

        # Survival probability model: P(survive) ~ exp(-λ_int × t)
        # Target: P > target_fidelity
        survival_prob = np.zeros_like(ratio_grid)

        for i, ratio in enumerate(λ_ratios):
            λ_int = ratio * λ_ext
            for j, t_coh in enumerate(coherence_times):
                # Exponential decay model
                survival_prob[j, i] = np.exp(-λ_int * t_coh)

        # Identify boundary where survival = target_fidelity
        boundary_mask = (survival_prob >= target_fidelity)

        results = {
            'λ_ratios': λ_ratios,
            'coherence_times': coherence_times,
            'survival_probability': survival_prob,
            'boundary_mask': boundary_mask,
            'target_fidelity': target_fidelity,
            'λ_ext': λ_ext,
        }

        self.results['collapse_boundaries'] = results
        return results

    def generate_requirement_table(self,
                                   scenario_configs: Optional[List[Dict]] = None) -> pd.DataFrame:
        """
        Generate table of FTL scenario requirements

        Parameters:
        -----------
        scenario_configs : list of dict, optional
            Scenario specifications

        Returns:
        --------
        df : pandas.DataFrame
            Requirement table
        """
        if scenario_configs is None:
            # Default scenarios
            scenario_configs = [
                {'name': 'Quantum chip (1 cm)', 'distance': 0.01, 'time': 1e-9},
                {'name': 'Lab bench (1 m)', 'distance': 1.0, 'time': 1e-8},
                {'name': 'Building (100 m)', 'distance': 100.0, 'time': 1e-7},
                {'name': 'Campus (1 km)', 'distance': 1000.0, 'time': 1e-6},
                {'name': 'City (10 km)', 'distance': 10000.0, 'time': 1e-5},
                {'name': 'Earth-Moon', 'distance': 3.84e8, 'time': 1.0},
                {'name': 'Earth-Mars (min)', 'distance': 5.5e10, 'time': 60.0},
            ]

        c = PhysicalConstants.c
        λ_ext = self.config['rrgm']['λ_ext_default']

        rows = []
        for scenario in scenario_configs:
            name = scenario['name']
            L = scenario['distance']
            t_ext = scenario['time']

            # Classical speed
            v_classical = L / t_ext
            v_ratio_classical = v_classical / c

            # Is FTL required?
            ftl_required = v_classical > c

            # Required λ_int/λ_ext for this scenario
            # Approximate: need delay_factor ~ v_classical / c
            if ftl_required:
                # Very rough estimate: need λ_int ~ λ_ext / (v/c)
                required_ratio = 1.0 / v_ratio_classical
            else:
                required_ratio = 1.0  # No RIF needed

            # Corresponding χ
            required_χ = 1.0 - required_ratio if required_ratio <= 1.0 else np.nan

            rows.append({
                'Scenario': name,
                'Distance (m)': L,
                'External Time (s)': t_ext,
                'v_eff (m/s)': v_classical,
                'v_eff / c': v_ratio_classical,
                'FTL Required?': 'Yes' if ftl_required else 'No',
                'Min λ_int/λ_ext': required_ratio,
                'Min χ': required_χ,
            })

        df = pd.DataFrame(rows)
        self.results['requirement_table'] = df
        return df

    def plot_results(self, output_dir: str = 'outputs/figures') -> List[str]:
        """
        Generate all plots for parameter exploration

        Parameters:
        -----------
        output_dir : str
            Output directory

        Returns:
        --------
        saved_files : list
            List of saved file paths
        """
        saved_files = []

        # FTL requirements heatmap
        if 'ftl_requirements' in self.results:
            ftl = self.results['ftl_requirements']
            fig = plot_FTL_requirements(
                ftl['λ_ratios'],
                ftl['distances'],
                ftl['transit_times'],
                ftl['v_ratio_grid'],
                save_path=None
            )
            filepath = os.path.join(output_dir, 'module2_ftl_requirements.png')
            save_figure(fig, 'module2_ftl_requirements.png', output_dir)
            saved_files.append(filepath)

        # Energy costs heatmap
        if 'energy_costs' in self.results:
            ec = self.results['energy_costs']
            fig = plot_parameter_heatmap(
                ec['χ_values'],
                ec['volumes'] * 1e9,  # Convert to nm³ for readability
                ec['energy_grid_kWh'].T,
                xlabel='RPG Field Strength χ',
                ylabel='Volume (nm³)',
                zlabel='Energy (kWh)',
                title='RIF Maintenance Energy Costs',
                log_scale=True,
                save_path=None
            )
            filepath = os.path.join(output_dir, 'module2_energy_costs.png')
            save_figure(fig, 'module2_energy_costs.png', output_dir)
            saved_files.append(filepath)

        # Collapse boundaries
        if 'collapse_boundaries' in self.results:
            cb = self.results['collapse_boundaries']
            fig = plot_parameter_heatmap(
                cb['λ_ratios'],
                cb['coherence_times'] * 1e9,  # Convert to ns
                cb['survival_probability'].T,
                xlabel='$\\lambda_{int}/\\lambda_{ext}$ Ratio',
                ylabel='Coherence Time (ns)',
                zlabel='Survival Probability',
                title='Collapse Threshold Boundaries',
                log_scale=False,
                contours=True,
                save_path=None
            )
            filepath = os.path.join(output_dir, 'module2_collapse_boundaries.png')
            save_figure(fig, 'module2_collapse_boundaries.png', output_dir)
            saved_files.append(filepath)

        return saved_files

    def save_results(self, output_dir: str = 'outputs/data',
                    filename: str = 'module2_results.json') -> str:
        """
        Save results to JSON and CSV

        Parameters:
        -----------
        output_dir : str
            Output directory
        filename : str
            JSON output filename

        Returns:
        --------
        filepath : str
            Path to saved JSON file
        """
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        # Convert numpy arrays to lists for JSON
        results_serializable = {}
        for key, value in self.results.items():
            if key == 'requirement_table':
                # Save DataFrame separately as CSV
                csv_path = os.path.join(output_dir, 'module2_requirement_table.csv')
                value.to_csv(csv_path, index=False)
                print(f"✓ Saved table: {csv_path}")
                continue

            if isinstance(value, dict):
                results_serializable[key] = {}
                for k, v in value.items():
                    if isinstance(v, np.ndarray):
                        results_serializable[key][k] = v.tolist()
                    elif isinstance(v, (list, tuple)) and len(v) > 0 and isinstance(v[0], dict):
                        results_serializable[key][k] = v
                    else:
                        try:
                            json.dumps(v)
                            results_serializable[key][k] = v
                        except:
                            results_serializable[key][k] = str(v)
            else:
                results_serializable[key] = value

        with open(filepath, 'w') as f:
            json.dump(results_serializable, f, indent=2)

        print(f"✓ Saved results: {filepath}")
        return filepath


def run_module2_demo():
    """
    Demo run of Module 2: Parameter Space Explorer
    """
    print("\n" + "="*70)
    print("MODULE 2: PARAMETER SPACE EXPLORER")
    print("="*70)
    print("\nMapping FTL requirements and energy costs...\n")

    explorer = ParameterSpaceExplorer()

    # FTL requirements
    print("Calculating FTL velocity requirements...")
    distances = np.logspace(0, 11, 50)  # 1 m to 10^11 m
    transit_times = distances / PhysicalConstants.c * 0.1  # 10% of light travel time
    ftl_results = explorer.calculate_FTL_requirements(distances, transit_times)
    print(f"  Analyzed {len(distances)} distance scales")

    # Energy costs
    print("\nCalculating RIF energy costs...")
    χ_values = np.linspace(0.1, 0.99, 30)
    volumes = np.logspace(-12, -3, 30)  # pm³ to mm³
    energy_results = explorer.calculate_energy_costs(χ_values, volumes)
    print(f"  Analyzed {len(energy_results['scenarios'])} energy scenarios")

    # Collapse boundaries
    print("\nMapping collapse boundaries...")
    λ_ratios = np.logspace(-3, 0, 50)
    coherence_times = np.logspace(-9, -6, 50)  # ns to μs
    boundary_results = explorer.map_collapse_boundaries(λ_ratios, coherence_times)

    # Generate requirement table
    print("\nGenerating FTL requirement table...")
    req_table = explorer.generate_requirement_table()
    print("\n" + "="*70)
    print("FTL Scenario Requirements:")
    print("="*70)
    print(req_table.to_string(index=False))

    # Generate plots
    print("\n" + "="*70)
    print("Generating plots...")
    saved = explorer.plot_results()

    # Save data
    filepath = explorer.save_results()

    print("\n" + "="*70)
    print("MODULE 2 COMPLETE")
    print("="*70)
    print(f"\nGenerated {len(saved)} figures")
    print(f"Saved data: {filepath}")

    return explorer


if __name__ == '__main__':
    explorer = run_module2_demo()
