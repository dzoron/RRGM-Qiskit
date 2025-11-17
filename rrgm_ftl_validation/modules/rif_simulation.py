"""
RRGM FTL Validation Toolkit - Module 1: RIF Simulation Framework

Simulates qubit coherence under tunable χ(RPG) field profiles.
Compares RIF-protected vs unprotected systems.
Generates publication-ready coherence survival graphs.

Based on Section 7.1 of the RRGM FTL paper: "Qubit survivability under collapse noise"
"""

import numpy as np
from scipy.linalg import expm
from typing import Dict, List, Tuple, Optional, Any
import json
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import (
    PhysicalConstants,
    RRGMParameters,
    SimulationDefaults,
    RPG_field_profile,
    effective_decay_rate,
    get_default_config,
)
from utils.plotting import (
    plot_coherence_decay,
    plot_RPG_profiles,
    save_figure,
)


class QubitSystem:
    """
    Qubit system under RRGM dynamics with RIF protection

    Models coherence decay under:
    - Default Ω behavior (λ_ext)
    - RIF-protected behavior (λ_int < λ_ext via χ field)
    """

    def __init__(self, n_qubits: int = 1,
                 λ_ext: float = RRGMParameters.λ_ext_default,
                 initial_state: Optional[np.ndarray] = None):
        """
        Initialize qubit system

        Parameters:
        -----------
        n_qubits : int
            Number of qubits
        λ_ext : float
            External decay rate (1/s)
        initial_state : array, optional
            Initial density matrix (default: |+⟩ state)
        """
        self.n_qubits = n_qubits
        self.dim = 2**n_qubits
        self.λ_ext = λ_ext

        # Initialize to |+⟩ state (equal superposition) if not specified
        if initial_state is None:
            psi = np.ones(self.dim, dtype=complex) / np.sqrt(self.dim)
            self.ρ = np.outer(psi, psi.conj())
        else:
            self.ρ = initial_state.copy()

        # Ensure density matrix is complex
        self.ρ = self.ρ.astype(complex)

        # Store initial state for reset
        self.ρ_initial = self.ρ.copy()

    def reset(self):
        """Reset to initial state"""
        self.ρ = self.ρ_initial.copy()

    def coherence(self) -> float:
        """
        Calculate coherence as max off-diagonal element magnitude

        Returns:
        --------
        coherence : float
            |ρ_01| for single qubit, generalized for multi-qubit
        """
        if self.n_qubits == 1:
            return np.abs(self.ρ[0, 1])
        else:
            # For multi-qubit: average off-diagonal magnitude
            mask = ~np.eye(self.dim, dtype=bool)
            return np.mean(np.abs(self.ρ[mask]))

    def purity(self) -> float:
        """
        Calculate purity Tr(ρ²)

        Returns:
        --------
        purity : float
            Purity measure (1 = pure, 1/dim = maximally mixed)
        """
        return np.real(np.trace(self.ρ @ self.ρ))

    def evolve_lindblad(self, dt: float, λ_eff: float,
                       dephasing: bool = True,
                       relaxation: bool = True) -> None:
        """
        Evolve density matrix under Lindblad master equation

        dρ/dt = -i[H,ρ] + Σ_k (L_k ρ L_k† - 1/2{L_k†L_k, ρ})

        Parameters:
        -----------
        dt : float
            Time step (seconds)
        λ_eff : float
            Effective decay rate (λ_int or λ_ext)
        dephasing : bool
            Include dephasing channel
        relaxation : bool
            Include amplitude damping
        """
        # Pauli matrices for single qubit
        if self.n_qubits == 1:
            σ_x = np.array([[0, 1], [1, 0]], dtype=complex)
            σ_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
            σ_z = np.array([[1, 0], [0, -1]], dtype=complex)
            σ_minus = np.array([[0, 0], [1, 0]], dtype=complex)

            # Hamiltonian (free evolution, can be set to zero for pure decoherence)
            H = np.zeros((2, 2), dtype=complex)

            # Lindblad operators
            L_ops = []
            if dephasing:
                # Dephasing: σ_z with rate λ_eff
                L_ops.append(np.sqrt(λ_eff) * σ_z)
            if relaxation:
                # Amplitude damping: σ_- with rate λ_eff/2
                L_ops.append(np.sqrt(λ_eff / 2) * σ_minus)

            # Compute Lindbladian superoperator effect
            dρ = -1j * (H @ self.ρ - self.ρ @ H)

            for L in L_ops:
                L_dag = L.conj().T
                dρ += L @ self.ρ @ L_dag - 0.5 * (L_dag @ L @ self.ρ + self.ρ @ L_dag @ L)

            # Euler step
            self.ρ += dt * dρ

            # Ensure Hermiticity and trace preservation (numerical stability)
            self.ρ = 0.5 * (self.ρ + self.ρ.conj().T)
            self.ρ /= np.trace(self.ρ)

        else:
            # Multi-qubit: simplified depolarizing channel
            γ = λ_eff * dt
            identity = np.eye(self.dim)
            self.ρ = (1 - γ) * self.ρ + (γ / self.dim) * identity

    def simulate_decay(self, t_max: float, n_steps: int,
                      χ: float = 0.0,
                      coupling_strength: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simulate coherence decay over time

        Parameters:
        -----------
        t_max : float
            Maximum simulation time (seconds)
        n_steps : int
            Number of time steps
        χ : float
            RPG field strength (0 = no protection, 1 = max protection)
        coupling_strength : float
            RPG coupling strength

        Returns:
        --------
        times : array
            Time points
        coherence : array
            Coherence at each time point
        """
        self.reset()

        times = np.linspace(0, t_max, n_steps)
        dt = times[1] - times[0]
        coherence = np.zeros(n_steps)

        # Calculate effective decay rate from RPG field
        λ_eff = effective_decay_rate(self.λ_ext, χ, coupling_strength)

        for i, t in enumerate(times):
            coherence[i] = self.coherence()
            if i < n_steps - 1:
                self.evolve_lindblad(dt, λ_eff)

        return times, coherence


class RIFSimulation:
    """
    Complete RIF simulation framework

    Manages multiple qubit systems with different RPG configurations
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize RIF simulation

        Parameters:
        -----------
        config : dict, optional
            Configuration dictionary (default: get_default_config())
        """
        self.config = config if config is not None else get_default_config()
        self.results = {}

    def run_comparison(self,
                      χ_values: List[float],
                      labels: Optional[List[str]] = None,
                      n_qubits: int = 1,
                      t_max: Optional[float] = None,
                      n_steps: Optional[int] = None,
                      λ_ext: Optional[float] = None) -> Dict[str, Any]:
        """
        Run coherence decay comparison for multiple χ values

        Parameters:
        -----------
        χ_values : list of float
            RPG field strengths to compare
        labels : list of str, optional
            Labels for each configuration
        n_qubits : int
            Number of qubits
        t_max : float, optional
            Maximum time (default from config)
        n_steps : int, optional
            Number of steps (default from config)
        λ_ext : float, optional
            External decay rate (default from config)

        Returns:
        --------
        results : dict
            Dictionary with times and coherence data
        """
        # Use defaults from config if not specified
        if t_max is None:
            t_max = self.config['simulation']['t_max']
        if n_steps is None:
            n_steps = self.config['simulation']['n_timesteps']
        if λ_ext is None:
            λ_ext = self.config['rrgm']['λ_ext_default']

        # Generate labels if not provided
        if labels is None:
            labels = [f"χ = {χ:.2f}" for χ in χ_values]

        # Initialize system
        system = QubitSystem(n_qubits=n_qubits, λ_ext=λ_ext)

        # Run simulations
        results = {
            'times': None,
            'coherence_data': {},
            'parameters': {
                'χ_values': χ_values,
                'n_qubits': n_qubits,
                't_max': t_max,
                'n_steps': n_steps,
                'λ_ext': λ_ext,
            }
        }

        for χ, label in zip(χ_values, labels):
            times, coherence = system.simulate_decay(t_max, n_steps, χ=χ)
            if results['times'] is None:
                results['times'] = times
            results['coherence_data'][label] = coherence

            # Calculate λ_int/λ_ext ratio
            λ_int = effective_decay_rate(λ_ext, χ)
            ratio = λ_int / λ_ext if λ_ext > 0 else 0
            print(f"  {label}: λ_int/λ_ext = {ratio:.4f}, "
                  f"final coherence = {coherence[-1]:.4f}")

        self.results['comparison'] = results
        return results

    def run_decay_rate_scan(self,
                           λ_ratios: np.ndarray,
                           t_max: Optional[float] = None,
                           n_steps: Optional[int] = None) -> Dict[str, Any]:
        """
        Scan decay rate ratios λ_int/λ_ext

        Parameters:
        -----------
        λ_ratios : array
            Array of λ_int/λ_ext ratios to scan
        t_max : float, optional
            Maximum time
        n_steps : int, optional
            Number of steps

        Returns:
        --------
        results : dict
            Scan results
        """
        if t_max is None:
            t_max = self.config['simulation']['t_max']
        if n_steps is None:
            n_steps = self.config['simulation']['n_timesteps']

        λ_ext = self.config['rrgm']['λ_ext_default']
        system = QubitSystem(n_qubits=1, λ_ext=λ_ext)

        results = {
            'λ_ratios': λ_ratios,
            'final_coherence': np.zeros_like(λ_ratios),
            'coherence_half_time': np.zeros_like(λ_ratios),
        }

        for i, ratio in enumerate(λ_ratios):
            # Calculate χ needed for this ratio
            # λ_int = λ_ext * (1 - χ) => χ = 1 - λ_int/λ_ext
            χ = 1.0 - ratio if ratio <= 1.0 else 0.0

            times, coherence = system.simulate_decay(t_max, n_steps, χ=χ)

            results['final_coherence'][i] = coherence[-1]

            # Find half-coherence time
            half_idx = np.argmin(np.abs(coherence - 0.5))
            results['coherence_half_time'][i] = times[half_idx]

        self.results['decay_scan'] = results
        return results

    def plot_results(self, output_dir: str = 'outputs/figures') -> List[str]:
        """
        Generate all plots for RIF simulation

        Parameters:
        -----------
        output_dir : str
            Output directory for figures

        Returns:
        --------
        saved_files : list
            List of saved file paths
        """
        saved_files = []

        if 'comparison' in self.results:
            comp = self.results['comparison']
            fig = plot_coherence_decay(
                comp['times'],
                comp['coherence_data'],
                title="RIF Coherence Protection: χ Dependence",
                save_path=None
            )
            filepath = os.path.join(output_dir, 'module1_coherence_comparison.png')
            save_figure(fig, 'module1_coherence_comparison.png', output_dir)
            saved_files.append(filepath)

        if 'decay_scan' in self.results:
            scan = self.results['decay_scan']
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(scan['λ_ratios'], scan['final_coherence'],
                   linewidth=2.5, color='darkblue')
            ax.set_xlabel('$\\lambda_{int}/\\lambda_{ext}$ Ratio', fontsize=12)
            ax.set_ylabel('Final Coherence', fontsize=12)
            ax.set_title('Coherence vs Decay Rate Ratio', fontsize=13)
            ax.set_xscale('log')
            ax.grid(True, alpha=0.3)

            filepath = os.path.join(output_dir, 'module1_decay_scan.png')
            save_figure(fig, 'module1_decay_scan.png', output_dir)
            saved_files.append(filepath)

        return saved_files

    def save_results(self, output_dir: str = 'outputs/data',
                    filename: str = 'module1_results.json') -> str:
        """
        Save results to JSON

        Parameters:
        -----------
        output_dir : str
            Output directory
        filename : str
            Output filename

        Returns:
        --------
        filepath : str
            Path to saved file
        """
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        # Convert numpy arrays to lists for JSON serialization
        results_serializable = {}
        for key, value in self.results.items():
            if isinstance(value, dict):
                results_serializable[key] = {}
                for k, v in value.items():
                    if isinstance(v, np.ndarray):
                        results_serializable[key][k] = v.tolist()
                    elif isinstance(v, dict):
                        results_serializable[key][k] = {
                            kk: vv.tolist() if isinstance(vv, np.ndarray) else vv
                            for kk, vv in v.items()
                        }
                    else:
                        results_serializable[key][k] = v
            else:
                results_serializable[key] = value

        with open(filepath, 'w') as f:
            json.dump(results_serializable, f, indent=2)

        print(f"✓ Saved results: {filepath}")
        return filepath


def run_module1_demo():
    """
    Demo run of Module 1: RIF Simulation Framework
    """
    print("\n" + "="*70)
    print("MODULE 1: RIF SIMULATION FRAMEWORK")
    print("="*70)
    print("\nSimulating qubit coherence under RIF protection...\n")

    sim = RIFSimulation()

    # Comparison: different χ values
    print("Running RIF protection comparison...")
    χ_values = [0.0, 0.3, 0.6, 0.9, 0.99]
    labels = [
        "Unprotected (χ=0)",
        "Weak RIF (χ=0.3)",
        "Medium RIF (χ=0.6)",
        "Strong RIF (χ=0.9)",
        "Ultra-strong RIF (χ=0.99)"
    ]
    results_comp = sim.run_comparison(χ_values, labels=labels)

    # Decay rate scan
    print("\nScanning λ_int/λ_ext ratios...")
    λ_ratios = np.logspace(-3, 0, 30)
    results_scan = sim.run_decay_rate_scan(λ_ratios)

    # Generate plots
    print("\nGenerating plots...")
    saved = sim.plot_results()

    # Save data
    filepath = sim.save_results()

    print("\n" + "="*70)
    print("MODULE 1 COMPLETE")
    print("="*70)
    print(f"\nGenerated {len(saved)} figures")
    print(f"Saved data: {filepath}")

    return sim


if __name__ == '__main__':
    sim = run_module1_demo()
