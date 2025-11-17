#!/usr/bin/env python3
"""
Gate Configuration Predictor for RRGM V4.1

This script models which-path interference visibility as a function of identity
resolution strength, demonstrating how the universal gate Ω controls wave-particle
behavior in RRGM.

Based on:
Rozon, D. "RRGM V4.1: Light as Gateway to Identity"
Section 4.1: Wave-particle behaviour as gate choice
Section 6.4: Which-path visibility at low identity resolution

In RRGM:
- Gates that preserve structural coherence and avoid resolving identity
  reveal interference patterns
- Gates that resolve identity suppress structural cross-terms and reveal
  localized detection events

Visibility: V(η) ≈ V_std(η) + O(εγ)
where η parametrizes identity resolution strength

Author: Generated for RRGM research
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from typing import Tuple, Callable, List
import math
import warnings
warnings.filterwarnings('ignore')


class RRGMGatePredictor:
    """
    Predictor for interference visibility under different gate configurations.

    Models how the universal protocol Ω determines whether identity (MI) or
    structure (ES) is resolved in measurements.
    """

    def __init__(self):
        """Initialize the gate configuration predictor."""
        pass

    def visibility_standard(self, eta: float, gamma: float = 1.0) -> float:
        """
        Standard decoherence visibility curve.

        V_std(η) = exp(-γ η²)

        This is the standard form from decoherence theory, where η parameterizes
        the strength of which-path information extraction.

        Args:
            eta: Identity resolution strength parameter (0 = no resolution,
                 1 = full resolution)
            gamma: Decoherence strength parameter

        Returns:
            Visibility V in [0, 1]
        """
        return np.exp(-gamma * eta**2)

    def visibility_rrgm(
        self,
        eta: float,
        epsilon_gamma: float,
        gamma: float = 1.0
    ) -> float:
        """
        RRGM-corrected visibility with identity seed correction.

        V(η) = V_std(η) + O(εγ)

        At very low identity resolution (η → 0), RRGM predicts a small offset
        proportional to εγ.

        Args:
            eta: Identity resolution strength
            epsilon_gamma: Photon identity seed εγ
            gamma: Decoherence strength

        Returns:
            RRGM visibility V
        """
        V_std = self.visibility_standard(eta, gamma)

        # Phenomenological correction: offset decays with eta
        # When eta → 0 (no identity resolution), offset ~ εγ
        # When eta → 1 (full identity resolution), correction → 0
        correction = epsilon_gamma * np.exp(-eta) * (1 - eta)

        return np.clip(V_std + correction, 0, 1)

    def gate_weight_structural(self, eta: float) -> float:
        """
        Gate weight for structural (interference) channel.

        When η → 0, gate preserves structure.
        When η → 1, gate suppresses structural coherence.

        Args:
            eta: Identity resolution strength

        Returns:
            Weight for structural channel w_S ∈ [0, 1]
        """
        return 1 - eta

    def gate_weight_identity(self, eta: float) -> float:
        """
        Gate weight for identity (particle-like) channel.

        When η → 0, identity remains unresolved.
        When η → 1, gate resolves identity to localized events.

        Args:
            eta: Identity resolution strength

        Returns:
            Weight for identity channel w_I ∈ [0, 1]
        """
        return eta

    def intensity_with_interference(
        self,
        x: np.ndarray,
        d: float,
        wavelength: float,
        L: float,
        eta: float
    ) -> np.ndarray:
        """
        Intensity pattern with partial which-path information.

        I(x) = I₁ + I₂ + 2√(I₁I₂) V(η) cos(phase)

        Args:
            x: Position array on screen
            d: Slit separation
            wavelength: Photon wavelength
            L: Distance to screen
            eta: Identity resolution strength

        Returns:
            Intensity I(x)
        """
        k = 2 * np.pi / wavelength
        phase = k * d * x / L

        I_1 = 1.0  # Intensity from path 1
        I_2 = 1.0  # Intensity from path 2

        V = self.visibility_standard(eta)

        I_total = I_1 + I_2 + 2 * np.sqrt(I_1 * I_2) * V * np.cos(phase)

        return I_total

    def generate_visibility_curves(
        self,
        save_path: str = "gate_visibility_predictions.png"
    ):
        """
        Generate comprehensive visibility prediction plots.

        Args:
            save_path: Path to save figure
        """
        fig = plt.figure(figsize=(16, 10))
        gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.35)

        eta_range = np.linspace(0, 1, 200)

        # --- Plot 1: Visibility curves for different εγ ---
        ax1 = fig.add_subplot(gs[0, 0])

        epsilon_values = [0, 1e-18, 1e-15, 1e-12]
        colors = ['blue', 'green', 'orange', 'red']
        labels = ['Standard (εγ = 0)', 'εγ = 10⁻¹⁸', 'εγ = 10⁻¹⁵', 'εγ = 10⁻¹²']

        for eps, color, label in zip(epsilon_values, colors, labels):
            if eps == 0:
                V_vals = [self.visibility_standard(eta) for eta in eta_range]
            else:
                V_vals = [self.visibility_rrgm(eta, eps) for eta in eta_range]

            ax1.plot(eta_range, V_vals, color=color, linewidth=2.5, label=label)

        ax1.set_xlabel('Identity Resolution Strength η', fontsize=11)
        ax1.set_ylabel('Fringe Visibility V', fontsize=11)
        ax1.set_title('Visibility vs. Which-Path Information', fontsize=12, fontweight='bold')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim([0, 1])
        ax1.set_ylim([0, 1.05])

        # --- Plot 2: Gate weight distribution ---
        ax2 = fig.add_subplot(gs[0, 1])

        w_structural = [self.gate_weight_structural(eta) for eta in eta_range]
        w_identity = [self.gate_weight_identity(eta) for eta in eta_range]

        ax2.fill_between(eta_range, 0, w_structural, alpha=0.4, color='blue',
                        label='Structural Channel (interference)')
        ax2.fill_between(eta_range, w_structural, 1, alpha=0.4, color='red',
                        label='Identity Channel (particle-like)')
        ax2.plot(eta_range, w_structural, 'b-', linewidth=2)
        ax2.plot(eta_range, w_identity, 'r-', linewidth=2)

        ax2.set_xlabel('Identity Resolution Strength η', fontsize=11)
        ax2.set_ylabel('Gate Weight', fontsize=11)
        ax2.set_title('RRGM Gate Ω: Channel Allocation', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=9, loc='center right')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim([0, 1])
        ax2.set_ylim([0, 1])

        # --- Plot 3: Low-η zoom showing εγ offset ---
        ax3 = fig.add_subplot(gs[0, 2])

        eta_low = np.linspace(0, 0.1, 200)

        V_std_low = [self.visibility_standard(eta) for eta in eta_low]
        V_rrgm_low = [self.visibility_rrgm(eta, 1e-12) for eta in eta_low]

        ax3.plot(eta_low, V_std_low, 'b-', linewidth=2.5, label='Standard')
        ax3.plot(eta_low, V_rrgm_low, 'r--', linewidth=2.5, label='RRGM (εγ = 10⁻¹²)')
        ax3.fill_between(eta_low, V_std_low, V_rrgm_low, alpha=0.3, color='yellow',
                        label='RRGM offset')

        ax3.set_xlabel('Identity Resolution Strength η', fontsize=11)
        ax3.set_ylabel('Fringe Visibility V', fontsize=11)
        ax3.set_title('Low-η Regime: Identity Seed Signature', fontsize=12, fontweight='bold')
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim([0, 0.1])

        # --- Plot 4: Interference patterns for different η ---
        ax4 = fig.add_subplot(gs[1, 0])

        x = np.linspace(-10, 10, 500)  # Position on screen (arbitrary units)
        d = 1.0  # Slit separation
        wavelength = 0.5  # Wavelength
        L = 100  # Distance to screen

        eta_values = [0, 0.3, 0.7, 1.0]
        alphas = [1.0, 0.8, 0.5, 0.3]

        for eta_val, alpha in zip(eta_values, alphas):
            I = self.intensity_with_interference(x, d, wavelength, L, eta_val)
            ax4.plot(x, I, linewidth=2, alpha=alpha,
                    label=f'η = {eta_val:.1f} (V = {self.visibility_standard(eta_val):.2f})')

        ax4.set_xlabel('Position x (a.u.)', fontsize=11)
        ax4.set_ylabel('Intensity', fontsize=11)
        ax4.set_title('Two-Slit Patterns: Gate-Controlled Visibility',
                     fontsize=12, fontweight='bold')
        ax4.legend(fontsize=9)
        ax4.grid(True, alpha=0.3)

        # --- Plot 5: Complementarity diagram ---
        ax5 = fig.add_subplot(gs[1, 1])

        # Complementarity: V² + D² ≤ 1, where D is distinguishability
        D_range = np.linspace(0, 1, 200)
        V_max = np.sqrt(1 - D_range**2)  # Maximum visibility for given distinguishability

        ax5.fill_between(D_range, 0, V_max, alpha=0.3, color='lightblue',
                        label='Allowed region (standard)')
        ax5.plot(D_range, V_max, 'b-', linewidth=2.5, label='V² + D² = 1')

        # RRGM with small εγ: slight modification
        epsilon_gamma = 1e-12
        V_max_rrgm = np.sqrt(1 - D_range**2) + epsilon_gamma * (1 - D_range)
        V_max_rrgm = np.clip(V_max_rrgm, 0, 1)

        ax5.plot(D_range, V_max_rrgm, 'r--', linewidth=2.5,
                label=f'RRGM (εγ = {epsilon_gamma:.0e})')

        # Plot example experimental points
        eta_points = [0, 0.25, 0.5, 0.75, 1.0]
        D_points = eta_points
        V_points = [self.visibility_standard(eta) for eta in eta_points]

        ax5.scatter(D_points, V_points, s=80, c='red', marker='o',
                   edgecolors='black', linewidths=1.5, zorder=5,
                   label='Measurement points')

        ax5.set_xlabel('Distinguishability D', fontsize=11)
        ax5.set_ylabel('Visibility V', fontsize=11)
        ax5.set_title('Wave-Particle Complementarity', fontsize=12, fontweight='bold')
        ax5.legend(fontsize=9)
        ax5.grid(True, alpha=0.3)
        ax5.set_xlim([0, 1])
        ax5.set_ylim([0, 1.05])

        # --- Plot 6: Summary table ---
        ax6 = fig.add_subplot(gs[1, 2])
        ax6.axis('tight')
        ax6.axis('off')

        table_data = [
            ['Gate\nConfig', 'η\n(which-path)', 'V\n(visibility)', 'Behavior'],
            ['Structure-\npreserving', '0', '1.0', 'Full interference\n(wave-like)'],
            ['Weak\nidentity\nresolution', '0.3', '0.91', 'High visibility\nwith partial info'],
            ['Moderate\nresolution', '0.7', '0.37', 'Reduced fringes\nmixed behavior'],
            ['Full\nidentity\nresolution', '1.0', '0', 'No interference\n(particle-like)']
        ]

        table = ax6.table(
            cellText=table_data,
            cellLoc='center',
            loc='center',
            colWidths=[0.25, 0.2, 0.2, 0.35]
        )
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 2.8)

        # Style header
        for i in range(4):
            cell = table[(0, i)]
            cell.set_facecolor('#5B9BD5')
            cell.set_text_props(weight='bold', color='white')

        # Color code rows by regime
        colors = ['#D6EAF8', '#A9D6F0', '#F8D7A8', '#F5B7B1']
        for i in range(1, len(table_data)):
            for j in range(4):
                cell = table[(i, j)]
                cell.set_facecolor(colors[i-1])

        ax6.set_title('RRGM Gate Configurations: From Waves to Particles',
                     fontsize=11, fontweight='bold', pad=15)

        plt.suptitle(
            'RRGM V4.1: Gate-Controlled Wave-Particle Behavior',
            fontsize=15, fontweight='bold', y=0.98
        )

        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Gate visibility plots saved to {save_path}")

        return fig

    def generate_experimental_setup_plots(
        self,
        save_path: str = "gate_experimental_setups.png"
    ):
        """
        Generate plots showing experimental setups for testing gate predictions.

        Args:
            save_path: Path to save figure
        """
        fig = plt.figure(figsize=(14, 10))
        gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

        # --- Plot 1: Mach-Zehnder with tunable which-path detector ---
        ax1 = fig.add_subplot(gs[0, 0])

        # Simulate MZ interferometer with variable coupling to which-path detector
        eta_vals = np.linspace(0, 1, 100)
        coupling_strengths = [0, 0.3, 0.6, 1.0]

        for coupling in coupling_strengths:
            V_vals = [self.visibility_standard(eta * coupling) for eta in eta_vals]
            ax1.plot(eta_vals, V_vals, linewidth=2,
                    label=f'Detector coupling = {coupling:.1f}')

        ax1.set_xlabel('Internal Path Marker Strength η', fontsize=11)
        ax1.set_ylabel('Output Port Visibility V', fontsize=11)
        ax1.set_title('Mach-Zehnder: Tunable Which-Path Detection',
                     fontsize=12, fontweight='bold')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3)

        # --- Plot 2: Photon number statistics at different η ---
        ax2 = fig.add_subplot(gs[0, 1])

        # Simulate photon counting statistics
        n_photons_range = np.arange(0, 20)

        # Coherent state at high visibility (η ≈ 0)
        alpha = 4  # Coherent state parameter
        factorials = np.array([math.factorial(n) for n in n_photons_range], dtype=float)
        P_coherent = (alpha**n_photons_range / factorials) * np.exp(-alpha)

        # More thermal-like at low visibility (η → 1)
        n_thermal = 4
        P_thermal = (n_photons_range / (n_thermal + 1)**(n_photons_range + 1))

        ax2.bar(n_photons_range - 0.2, P_coherent, width=0.4, alpha=0.7,
               label='η = 0 (structural channel)', color='blue')
        ax2.bar(n_photons_range + 0.2, P_thermal, width=0.4, alpha=0.7,
               label='η = 1 (identity channel)', color='red')

        ax2.set_xlabel('Photon Number n', fontsize=11)
        ax2.set_ylabel('Probability P(n)', fontsize=11)
        ax2.set_title('Photon Statistics: Gate-Dependent', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3, axis='y')

        # --- Plot 3: Delayed-choice quantum eraser scenario ---
        ax3 = fig.add_subplot(gs[1, 0])

        # Four possible post-selection outcomes
        phase = np.linspace(0, 4*np.pi, 500)

        # Outcomes when eraser is applied (which-path info erased)
        I_erased_constructive = 2 * (1 + np.cos(phase))
        I_erased_destructive = 2 * (1 - np.cos(phase))

        # Outcomes when which-path info retained
        I_which_path = np.ones_like(phase) * 2  # Flat, no interference

        ax3.plot(phase / np.pi, I_erased_constructive, 'b-', linewidth=2,
                label='Eraser: constructive (η → 0)')
        ax3.plot(phase / np.pi, I_erased_destructive, 'g-', linewidth=2,
                label='Eraser: destructive (η → 0)')
        ax3.plot(phase / np.pi, I_which_path, 'r--', linewidth=2.5,
                label='No eraser: which-path (η = 1)')

        ax3.set_xlabel('Phase / π', fontsize=11)
        ax3.set_ylabel('Intensity (coincidence rate)', fontsize=11)
        ax3.set_title('Delayed-Choice Quantum Eraser', fontsize=12, fontweight='bold')
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.3)

        # Add text explanation
        textstr = (
            'RRGM Interpretation:\n'
            'Post-selection chooses gate Ω configuration.\n'
            'Eraser → structural gate (interference)\n'
            'No eraser → identity gate (no interference)'
        )
        props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.8)
        ax3.text(0.98, 0.97, textstr, transform=ax3.transAxes, fontsize=8,
                verticalalignment='top', horizontalalignment='right', bbox=props)

        # --- Plot 4: Testable predictions table ---
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.axis('tight')
        ax4.axis('off')

        table_data = [
            ['Experiment', 'Control\nParameter', 'RRGM\nPrediction', 'Standard\nPrediction'],
            ['Weak which-path\nmarker',
             'Marker\nstrength η',
             'V(η) with\nsmall εγ offset',
             'V_std(η)\nno offset'],
            ['High-finesse\nMach-Zehnder',
             'Path length\nstability',
             'Residual V_min\n∝ εγ',
             'V_min = 0'],
            ['Entangled\nphoton pairs',
             'Local\nmeasurement',
             'Nonlocal gate Ω\nlocal MI',
             'Nonlocal\ncorrelations'],
            ['Single-photon\nsource purity',
             'g²(0)\nstatistic',
             'Bound on εγ\nfrom purity',
             'Ideal g²(0)=0']
        ]

        table = ax4.table(
            cellText=table_data,
            cellLoc='center',
            loc='center',
            colWidths=[0.28, 0.22, 0.26, 0.24]
        )
        table.auto_set_font_size(False)
        table.set_fontsize(7.5)
        table.scale(1, 3)

        # Style header
        for i in range(4):
            cell = table[(0, i)]
            cell.set_facecolor('#7030A0')
            cell.set_text_props(weight='bold', color='white')

        # Alternate rows
        for i in range(1, len(table_data)):
            for j in range(4):
                cell = table[(i, j)]
                if i % 2 == 0:
                    cell.set_facecolor('#E4DFEC')
                else:
                    cell.set_facecolor('#F2F2F2')

        ax4.set_title('Experimental Tests: Gate Predictions vs. Standard QED',
                     fontsize=11, fontweight='bold', pad=15)

        plt.suptitle(
            'RRGM V4.1: Experimental Setups for Gate Configuration Tests',
            fontsize=15, fontweight='bold', y=0.98
        )

        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Experimental setup plots saved to {save_path}")

        return fig


def main():
    """
    Main execution: generate all gate configuration prediction plots.
    """
    print("=" * 70)
    print("RRGM V4.1: Gate Configuration Predictor")
    print("=" * 70)
    print()

    predictor = RRGMGatePredictor()

    print("Generating visibility prediction curves...")
    predictor.generate_visibility_curves(
        save_path="rrgm_gate_visibility_predictions.png"
    )

    print("Generating experimental setup plots...")
    predictor.generate_experimental_setup_plots(
        save_path="rrgm_gate_experimental_setups.png"
    )

    print()
    print("=" * 70)
    print("Analysis complete!")
    print()
    print("Key Results:")
    print("  • Visibility V(η) depends on identity resolution strength η")
    print("  • RRGM predicts small offset ∝ εγ at low η")
    print("  • Gate Ω allocates weight between structural and identity channels")
    print("  • Wave-particle behavior is gate choice, not dual ontology")
    print()
    print("Falsifiability:")
    print("  If V(η) shows NO deviation from standard decoherence curve")
    print("  across all regimes and setups, εγ is constrained to vanish.")
    print("  Weak marker experiments can test the low-η offset.")
    print("=" * 70)


if __name__ == "__main__":
    main()
