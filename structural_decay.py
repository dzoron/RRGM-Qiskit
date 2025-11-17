#!/usr/bin/env python3
"""
Structural Decay Visualizer for RRGM V4.1

This script models ES (structural energy) decay under different λ_Ω (gate-induced
decay rates) and demonstrates how cosmological redshift emerges as structural
coherence loss in RRGM.

Based on:
Rozon, D. "RRGM V4.1: Light as Gateway to Identity"
Section 4.3: Cosmological redshift as coherence decay

In RRGM:
    dES^(γ)/dt = -λ_Ω(t) × ES^(γ)
    Solution: ES(t) = ES(0) × exp(-∫λ_Ω(τ)dτ)

For photons: E = MI × ES, with MI conserved
Therefore: E(t) = MI × ES(0) × exp(-∫λ_Ω(τ)dτ)

Author: Generated for RRGM research
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from typing import Callable, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Physical constants
C_LIGHT = 2.998e8  # m/s
H_PLANCK = 6.626e-34  # J·s
H0_SI = 2.2e-18  # Hubble constant in SI (s^-1), approximately 70 km/s/Mpc


class RRGMStructuralDecay:
    """
    Simulator for structural energy decay in RRGM framework.

    Models the evolution of ES (radiatable structure) under various
    gate protocols Ω and environmental conditions.
    """

    def __init__(self):
        """Initialize the structural decay simulator."""
        self.c = C_LIGHT
        self.H0 = H0_SI

    def lambda_omega_constant(self, rate: float) -> Callable:
        """
        Constant decay rate λ_Ω.

        Args:
            rate: Constant decay rate (s^-1)

        Returns:
            Callable that returns constant rate
        """
        return lambda t: rate

    def lambda_omega_cosmological(self) -> Callable:
        """
        Cosmological decay rate matching Hubble expansion.

        In standard cosmology: z = (λ_obs - λ_emit) / λ_emit = H0 × t
        In RRGM: redshift emerges from structural coherence decay

        Returns:
            Callable for cosmological λ_Ω(t)
        """
        return lambda t: self.H0

    def lambda_omega_environment_dependent(
        self,
        base_rate: float,
        environment_factor: float
    ) -> Callable:
        """
        Environment-dependent decay rate.

        Models scenario where λ_Ω depends on local conditions
        (medium, field strength, etc.)

        Args:
            base_rate: Baseline decay rate
            environment_factor: Multiplicative environment contribution

        Returns:
            Callable for environment-dependent λ_Ω(t)
        """
        return lambda t: base_rate * (1 + environment_factor * np.sin(2 * np.pi * t / 1e8))

    def evolve_structure(
        self,
        ES_initial: float,
        time_points: np.ndarray,
        lambda_omega: Callable,
        MI: float = 1.0
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Evolve structural energy ES over time under given λ_Ω.

        Solves: dES/dt = -λ_Ω(t) × ES

        Args:
            ES_initial: Initial structural energy
            time_points: Array of time points
            lambda_omega: Decay rate function λ_Ω(t)
            MI: Identity anchor (conserved)

        Returns:
            (ES_values, E_total_values) arrays
        """
        ES_values = np.zeros_like(time_points)
        ES_values[0] = ES_initial

        # Integrate using simple Euler method for clarity
        dt = time_points[1] - time_points[0] if len(time_points) > 1 else 1

        for i in range(1, len(time_points)):
            t = time_points[i-1]
            ES_values[i] = ES_values[i-1] * (1 - lambda_omega(t) * dt)

        # Total energy E = MI × ES
        E_total = MI * ES_values

        return ES_values, E_total

    def redshift_from_decay(
        self,
        ES_initial: float,
        ES_final: float
    ) -> float:
        """
        Calculate effective redshift from structural decay.

        In RRGM: z = (E_initial - E_final) / E_final = (ES_i - ES_f) / ES_f

        Args:
            ES_initial: Initial structural energy
            ES_final: Final structural energy

        Returns:
            Effective redshift z
        """
        return (ES_initial - ES_final) / ES_final

    def generate_decay_comparison_plots(
        self,
        save_path: str = "structural_decay_comparison.png"
    ):
        """
        Generate comprehensive plots comparing different decay scenarios.

        Args:
            save_path: Path to save figure
        """
        fig = plt.figure(figsize=(16, 10))
        gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.35)

        # Time arrays for different scenarios
        t_short = np.linspace(0, 1e10, 500)  # Short timescale (seconds)
        t_cosmo = np.linspace(0, 4e17, 500)  # Cosmological timescale (~13 Gyr)

        ES_0 = 1.0  # Initial structural energy (normalized)
        MI = 1e-15  # Small identity seed for photon

        # --- Plot 1: Decay rates comparison ---
        ax1 = fig.add_subplot(gs[0, 0])

        decay_scenarios = {
            'Vacuum (λ_Ω→0)': self.lambda_omega_constant(1e-20),
            'Weak Medium': self.lambda_omega_constant(1e-15),
            'Dense Medium': self.lambda_omega_constant(1e-12),
            'Cosmological': self.lambda_omega_cosmological()
        }

        colors = ['blue', 'green', 'orange', 'red']

        for (name, lambda_func), color in zip(decay_scenarios.items(), colors):
            ES_vals, E_vals = self.evolve_structure(ES_0, t_short, lambda_func, MI)
            ax1.semilogy(t_short / 1e9, ES_vals, label=name, linewidth=2, color=color)

        ax1.set_xlabel('Time (s) ×10⁹', fontsize=11)
        ax1.set_ylabel('Structural Energy ES (normalized)', fontsize=11)
        ax1.set_title('ES Decay Under Different λ_Ω Regimes', fontsize=12, fontweight='bold')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim([1e-10, 2])

        # --- Plot 2: Cosmological redshift as coherence decay ---
        ax2 = fig.add_subplot(gs[0, 1])

        # Standard FRW redshift
        z_standard = self.H0 * t_cosmo

        # RRGM structural decay
        lambda_cosmo = self.lambda_omega_cosmological()
        ES_cosmo, E_cosmo = self.evolve_structure(ES_0, t_cosmo, lambda_cosmo, MI)
        z_rrgm = (ES_0 - ES_cosmo) / ES_cosmo

        ax2.plot(t_cosmo / (3.15e7 * 1e9), z_standard, 'b--',
                label='Standard FRW', linewidth=2)
        ax2.plot(t_cosmo / (3.15e7 * 1e9), z_rrgm, 'r-',
                label='RRGM Coherence Decay', linewidth=2)

        ax2.set_xlabel('Time (Gyr)', fontsize=11)
        ax2.set_ylabel('Redshift z', fontsize=11)
        ax2.set_title('Cosmological Redshift:\nMetric vs. Coherence Decay',
                     fontsize=12, fontweight='bold')
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim([0, 13])
        ax2.set_ylim([0, 4])

        # --- Plot 3: Environment-dependent λ_Ω ---
        ax3 = fig.add_subplot(gs[0, 2])

        lambda_env = self.lambda_omega_environment_dependent(1e-14, 0.5)
        lambda_values = [lambda_env(t) for t in t_short]

        ax3_twin = ax3.twinx()
        ax3.plot(t_short / 1e9, lambda_values, 'purple', linewidth=2, label='λ_Ω(t)')
        ES_env, _ = self.evolve_structure(ES_0, t_short, lambda_env, MI)
        ax3_twin.semilogy(t_short / 1e9, ES_env, 'darkorange',
                         linewidth=2, linestyle='--', label='ES(t)')

        ax3.set_xlabel('Time (s) ×10⁹', fontsize=11)
        ax3.set_ylabel('Decay Rate λ_Ω (s⁻¹)', fontsize=11, color='purple')
        ax3_twin.set_ylabel('Structural Energy ES', fontsize=11, color='darkorange')
        ax3.tick_params(axis='y', labelcolor='purple')
        ax3_twin.tick_params(axis='y', labelcolor='darkorange')
        ax3.set_title('Environment-Dependent Gate Protocol', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)

        lines1, labels1 = ax3.get_legend_handles_labels()
        lines2, labels2 = ax3_twin.get_legend_handles_labels()
        ax3.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc='upper right')

        # --- Plot 4: MI-ES manifold across regimes ---
        ax4 = fig.add_subplot(gs[1, 0])

        # Define three regimes: photon, matter, archive
        MI_photon = np.logspace(-20, -10, 50)
        ES_photon = np.logspace(-2, 2, 50)

        MI_matter = np.logspace(-5, 5, 50)
        ES_matter = np.logspace(-2, 2, 50)

        MI_archive = np.logspace(5, 15, 50)
        ES_archive = np.logspace(-10, -1, 50)

        # Plot as scatter in MI-ES space
        ax4.scatter(MI_photon, ES_photon, alpha=0.3, s=20, c='blue', label='Photon Regime')
        ax4.scatter(MI_matter, ES_matter, alpha=0.3, s=20, c='green', label='Matter Band')
        ax4.scatter(MI_archive, ES_archive, alpha=0.3, s=20, c='red', label='Archive Limit')

        # Add trajectory arrows
        ax4.annotate('', xy=(1e10, 1e-5), xytext=(1e0, 1e0),
                    arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        ax4.text(1e5, 1e-2, 'Irreversible\nAggregation', fontsize=9,
                ha='center', bbox=dict(boxstyle='round', facecolor='wheat'))

        ax4.set_xscale('log')
        ax4.set_yscale('log')
        ax4.set_xlabel('Identity MI', fontsize=11)
        ax4.set_ylabel('Structure ES', fontsize=11)
        ax4.set_title('(MI, ES) Manifold: Photons to Archives', fontsize=12, fontweight='bold')
        ax4.legend(fontsize=9)
        ax4.grid(True, alpha=0.3)

        # --- Plot 5: Energy evolution E = MI × ES ---
        ax5 = fig.add_subplot(gs[1, 1])

        # Three cases with different MI values
        MI_values = [1e-18, 1e-12, 1e-6]
        labels_MI = ['εγ = 10⁻¹⁸ (tight bound)', 'εγ = 10⁻¹² (loose bound)', 'MI = 10⁻⁶ (matter)']

        lambda_weak = self.lambda_omega_constant(1e-14)

        for MI_val, label, color in zip(MI_values, labels_MI, ['blue', 'green', 'red']):
            ES_vals, E_vals = self.evolve_structure(ES_0, t_short, lambda_weak, MI_val)
            ax5.semilogy(t_short / 1e9, E_vals, label=label, linewidth=2, color=color)

        ax5.set_xlabel('Time (s) ×10⁹', fontsize=11)
        ax5.set_ylabel('Total Energy E = MI × ES', fontsize=11)
        ax5.set_title('Energy Evolution: Bare-Root Law E = MI × ES',
                     fontsize=12, fontweight='bold')
        ax5.legend(fontsize=9)
        ax5.grid(True, alpha=0.3)

        # --- Plot 6: Testable signatures table ---
        ax6 = fig.add_subplot(gs[1, 2])
        ax6.axis('tight')
        ax6.axis('off')

        table_data = [
            ['Observable', 'RRGM Prediction', 'Falsifiable Test'],
            ['High-Q cavity\nlifetime',
             'Residual decay\n∝ εγ',
             'No residual →\nεγ bound'],
            ['Cosmological\nredshift',
             'Coherence loss\nλ_Ω ≈ H0',
             'Environment\ncorrelations'],
            ['Line-dependent\ncoherence',
             'Medium-dependent\nλ_Ω(medium)',
             'Differential\ndecay rates'],
            ['Archive merger\nwaves',
             'ES → 0\n(silence)',
             'Persistent GW\nhum → fails']
        ]

        table = ax6.table(
            cellText=table_data,
            cellLoc='left',
            loc='center',
            colWidths=[0.28, 0.36, 0.36]
        )
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 2.5)

        # Style header
        for i in range(3):
            cell = table[(0, i)]
            cell.set_facecolor('#C55A11')
            cell.set_text_props(weight='bold', color='white')

        # Alternate rows
        for i in range(1, len(table_data)):
            for j in range(3):
                cell = table[(i, j)]
                if i % 2 == 0:
                    cell.set_facecolor('#F4B183')
                else:
                    cell.set_facecolor('#FFF2CC')

        ax6.set_title('RRGM Structural Decay: Testable Signatures',
                     fontsize=12, fontweight='bold', pad=15)

        plt.suptitle(
            'RRGM V4.1: Structural Energy Decay and Cosmological Coherence Loss',
            fontsize=15, fontweight='bold', y=0.98
        )

        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Structural decay plots saved to {save_path}")

        return fig

    def generate_wavelength_shift_plot(
        self,
        save_path: str = "wavelength_shift_coherence_decay.png"
    ):
        """
        Generate plot showing wavelength shift due to structural coherence decay.

        Args:
            save_path: Path to save figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('RRGM: Wavelength Shift as Structural Coherence Decay',
                    fontsize=15, fontweight='bold')

        # Parameters
        lambda_0 = 500e-9  # Initial wavelength (m)
        distances = np.linspace(0, 3e26, 500)  # Up to ~10 Gpc

        # --- Plot 1: Redshift vs distance ---
        ax1 = axes[0, 0]

        # Standard cosmological redshift
        z_standard = (self.H0 / self.c) * distances

        # RRGM coherence decay (matches cosmological for λ_Ω = H0)
        lambda_cosmo = self.lambda_omega_cosmological()
        times = distances / self.c
        ES_vals, _ = self.evolve_structure(1.0, times, lambda_cosmo)
        z_rrgm = (1.0 - ES_vals) / ES_vals

        ax1.plot(distances / 3.086e25, z_standard, 'b-',
                label='Standard (metric expansion)', linewidth=2)
        ax1.plot(distances / 3.086e25, z_rrgm, 'r--',
                label='RRGM (coherence decay)', linewidth=2)

        ax1.set_xlabel('Distance (Gpc)', fontsize=11)
        ax1.set_ylabel('Redshift z', fontsize=11)
        ax1.set_title('Redshift vs. Distance', fontsize=12, fontweight='bold')
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        # --- Plot 2: Observed wavelength ---
        ax2 = axes[0, 1]

        lambda_obs_standard = lambda_0 * (1 + z_standard)
        lambda_obs_rrgm = lambda_0 * (1 + z_rrgm)

        ax2.plot(distances / 3.086e25, lambda_obs_standard * 1e9, 'b-',
                label='Standard', linewidth=2)
        ax2.plot(distances / 3.086e25, lambda_obs_rrgm * 1e9, 'r--',
                label='RRGM', linewidth=2)

        ax2.set_xlabel('Distance (Gpc)', fontsize=11)
        ax2.set_ylabel('Observed Wavelength (nm)', fontsize=11)
        ax2.set_title(f'Wavelength Shift (λ₀ = {lambda_0*1e9:.0f} nm)',
                     fontsize=12, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)

        # --- Plot 3: ES structural decay ---
        ax3 = axes[1, 0]

        ax3.semilogy(distances / 3.086e25, ES_vals, 'purple', linewidth=2.5)
        ax3.axhline(y=0.5, color='red', linestyle='--', linewidth=1.5,
                   label='ES = 0.5 (z = 1)')
        ax3.axhline(y=0.1, color='orange', linestyle='--', linewidth=1.5,
                   label='ES = 0.1 (z = 9)')

        ax3.set_xlabel('Distance (Gpc)', fontsize=11)
        ax3.set_ylabel('Structural Energy ES (normalized)', fontsize=11)
        ax3.set_title('Structural Coherence Decay Over Distance', fontsize=12, fontweight='bold')
        ax3.legend(fontsize=10)
        ax3.grid(True, alpha=0.3)

        # --- Plot 4: Differential decay for different media ---
        ax4 = axes[1, 1]

        # Three scenarios: vacuum, intergalactic medium, dense medium
        lambda_vacuum = self.lambda_omega_constant(self.H0)
        lambda_igm = self.lambda_omega_constant(self.H0 * 1.05)  # 5% enhancement
        lambda_dense = self.lambda_omega_constant(self.H0 * 1.2)  # 20% enhancement

        ES_vacuum, _ = self.evolve_structure(1.0, times, lambda_vacuum)
        ES_igm, _ = self.evolve_structure(1.0, times, lambda_igm)
        ES_dense, _ = self.evolve_structure(1.0, times, lambda_dense)

        z_vacuum = (1.0 - ES_vacuum) / ES_vacuum
        z_igm = (1.0 - ES_igm) / ES_igm
        z_dense = (1.0 - ES_dense) / ES_dense

        ax4.plot(distances / 3.086e25, z_vacuum, 'b-',
                label='Vacuum (λ_Ω = H0)', linewidth=2)
        ax4.plot(distances / 3.086e25, z_igm, 'g--',
                label='IGM (λ_Ω = 1.05 H0)', linewidth=2)
        ax4.plot(distances / 3.086e25, z_dense, 'r:',
                label='Dense (λ_Ω = 1.2 H0)', linewidth=2)

        ax4.set_xlabel('Distance (Gpc)', fontsize=11)
        ax4.set_ylabel('Redshift z', fontsize=11)
        ax4.set_title('Environment-Dependent Redshift', fontsize=12, fontweight='bold')
        ax4.legend(fontsize=10)
        ax4.grid(True, alpha=0.3)

        # Add text box with key insight
        textstr = (
            'RRGM Insight:\n'
            '• Standard: z from metric stretch\n'
            '• RRGM: z from ES coherence loss\n'
            '• Same z, different ontology\n'
            '• Testable via medium dependence'
        )
        props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.8)
        ax4.text(0.95, 0.05, textstr, transform=ax4.transAxes, fontsize=8,
                verticalalignment='bottom', horizontalalignment='right', bbox=props)

        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Wavelength shift plots saved to {save_path}")

        return fig


def main():
    """
    Main execution: generate all structural decay visualizations.
    """
    print("=" * 70)
    print("RRGM V4.1: Structural Energy Decay Visualizer")
    print("=" * 70)
    print()

    decay_sim = RRGMStructuralDecay()

    print("Generating structural decay comparison plots...")
    decay_sim.generate_decay_comparison_plots(
        save_path="rrgm_structural_decay_comparison.png"
    )

    print("Generating wavelength shift and coherence decay plots...")
    decay_sim.generate_wavelength_shift_plot(
        save_path="rrgm_wavelength_shift_coherence_decay.png"
    )

    print()
    print("=" * 70)
    print("Analysis complete!")
    print()
    print("Key Results:")
    print("  • ES decays as exp(-∫λ_Ω dt) under gate protocol Ω")
    print("  • Cosmological redshift emerges when λ_Ω ≈ H0")
    print("  • Environment-dependent λ_Ω predicts medium-specific decay")
    print("  • MI conserved; only ES radiates → E = MI × ES evolution")
    print()
    print("Falsifiability:")
    print("  If redshift shows NO environment dependence beyond standard")
    print("  dispersion, the RRGM coherence-decay interpretation is strongly")
    print("  constrained. Differential line measurements can test this.")
    print("=" * 70)


if __name__ == "__main__":
    main()
