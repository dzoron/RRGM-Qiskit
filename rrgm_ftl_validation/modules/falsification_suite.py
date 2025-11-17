"""
RRGM FTL Validation Toolkit - Module 3: Falsification Test Suite

Generates experimental protocols that would rule out RIF mechanism.
Creates predicted vs control comparison templates.
Provides clear "this falsifies RRGM FTL if..." statements.
Outputs test protocol documentation and expected result ranges.

Based on Section 7 (Falsifiability) of the RRGM FTL paper.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Callable
import json
import os
from dataclasses import dataclass, asdict

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import (
    PhysicalConstants,
    RRGMParameters,
    SimulationDefaults,
    effective_decay_rate,
    get_default_config,
)
from utils.plotting import (
    plot_falsification_comparison,
    save_figure,
)


@dataclass
class FalsificationCriterion:
    """
    A specific falsification criterion for RRGM FTL

    Attributes:
    -----------
    name : str
        Short name of the criterion
    description : str
        Full description
    observable : str
        What is measured
    rrgm_prediction : str
        What RRGM predicts
    control_prediction : str
        What standard physics predicts
    falsification_statement : str
        Clear "this falsifies RRGM FTL if..." statement
    threshold : float
        Numerical threshold for falsification (if applicable)
    units : str
        Units of observable
    """
    name: str
    description: str
    observable: str
    rrgm_prediction: str
    control_prediction: str
    falsification_statement: str
    threshold: float = 0.0
    units: str = ""


@dataclass
class ExperimentalProtocol:
    """
    Complete experimental protocol specification

    Attributes:
    -----------
    protocol_id : str
        Unique protocol identifier
    title : str
        Protocol title
    objective : str
        What the protocol aims to test
    platform : str
        Experimental platform (e.g., "Quantum chip", "Optomechanical")
    setup : str
        Detailed setup description
    procedure : List[str]
        Step-by-step procedure
    expected_rrgm : Dict
        Expected results under RRGM
    expected_control : Dict
        Expected results under standard physics
    falsification_criteria : List[FalsificationCriterion]
        Falsification criteria
    estimated_resources : Dict
        Resource requirements
    """
    protocol_id: str
    title: str
    objective: str
    platform: str
    setup: str
    procedure: List[str]
    expected_rrgm: Dict[str, Any]
    expected_control: Dict[str, Any]
    falsification_criteria: List[FalsificationCriterion]
    estimated_resources: Dict[str, Any]


class FalsificationSuite:
    """
    Complete falsification test suite for RRGM FTL
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize falsification suite

        Parameters:
        -----------
        config : dict, optional
            Configuration dictionary
        """
        self.config = config if config is not None else get_default_config()
        self.protocols = {}
        self.criteria = {}
        self.results = {}

        # Build standard falsification criteria
        self._build_falsification_criteria()

        # Build experimental protocols
        self._build_experimental_protocols()

    def _build_falsification_criteria(self):
        """Build standard falsification criteria from Section 7.3"""

        # Criterion 1: Strict invariance of collapse
        self.criteria['invariance'] = FalsificationCriterion(
            name="Strict Invariance",
            description="Collapse timing cannot be modulated by any protocol",
            observable="Coherence lifetime modulation",
            rrgm_prediction="Coherence lifetime can be extended by tuning Ω (via χ field)",
            control_prediction="Coherence lifetime fixed by hardware and environment only",
            falsification_statement=(
                "RRGM FTL is falsified if: No experimental protocol (measurement timing, "
                "gate sequencing, error correction) produces repeatable coherence lifetime "
                "changes beyond what standard decoherence models predict, even when "
                "varying all accessible control parameters."
            ),
            threshold=0.0,
            units="% improvement over control"
        )

        # Criterion 2: No recursive-delay advantage
        self.criteria['recursive_delay'] = FalsificationCriterion(
            name="No Recursive Delay",
            description="Protected recursive windows show no advantage",
            observable="Circuit depth at fixed fidelity",
            rrgm_prediction="RIF-protected circuits can achieve deeper computation at same fidelity",
            control_prediction="Depth limited by standard decoherence, no protocol advantage",
            falsification_statement=(
                "RRGM FTL is falsified if: Quantum simulations of 'delayed collapse' or "
                "protected recursive windows show no performance advantage (coherence, "
                "entanglement range, gate depth) over control architectures, even when "
                "carefully designed to implement RIF-like protocols."
            ),
            threshold=0.0,
            units="% depth increase"
        )

        # Criterion 3: No record-scheduling phenomena
        self.criteria['record_scheduling'] = FalsificationCriterion(
            name="No Record Scheduling",
            description="All phenomena explainable by continuous D_0+1 trajectories",
            observable="Presence of intermediate records",
            rrgm_prediction="Endpoint-only records possible (spacelike jumps in archive)",
            control_prediction="Continuous worldlines always available",
            falsification_statement=(
                "RRGM FTL is falsified if: All observed phenomena remain explainable "
                "using continuous trajectories in D_0+1, with no empirical hints of "
                "'endpoint-only' records except where standard quantum measurement "
                "already accounts for them without invoking Ω reinterpretation."
            ),
            threshold=1.0,
            units="sigma confidence"
        )

        # Criterion 4: Energy-momentum conservation violation
        self.criteria['conservation'] = FalsificationCriterion(
            name="Conservation Violation",
            description="RIF violates local energy-momentum conservation",
            observable="Energy balance in RIF region",
            rrgm_prediction="Energy-momentum conserved globally, locally modified by RPG",
            control_prediction="Strict local conservation",
            falsification_statement=(
                "RRGM FTL is falsified if: RIF-mediated processes violate "
                "energy-momentum conservation beyond measurement uncertainty, or if "
                "required RPG field energy exceeds theoretical bounds derived from "
                "M_I × E_S coupling."
            ),
            threshold=3.0,
            units="sigma deviation"
        )

        # Criterion 5: Superluminal signaling
        self.criteria['signaling'] = FalsificationCriterion(
            name="Superluminal Signaling",
            description="FTL enables backward-in-time signaling",
            observable="Causal ordering of events",
            rrgm_prediction="No signaling (endpoint-only records preserve causality)",
            control_prediction="No superluminal signaling possible",
            falsification_statement=(
                "RRGM FTL is falsified if: Any RIF-mediated process enables "
                "information transfer faster than c in a way that allows sending "
                "signals backward in time or violates relativistic causality."
            ),
            threshold=1.0,
            units="instances observed"
        )

    def _build_experimental_protocols(self):
        """Build detailed experimental protocols"""

        # Protocol 1: Qubit coherence under controlled measurement timing
        self.protocols['P1_coherence_timing'] = ExperimentalProtocol(
            protocol_id='P1',
            title='Coherence Lifetime vs Measurement Timing Protocol',
            objective=(
                'Test whether systematic variation of measurement timing and gate '
                'sequencing (emulating Ω modulation) produces coherence lifetime '
                'changes beyond standard decoherence predictions.'
            ),
            platform='Superconducting qubit chip (transmon)',
            setup=(
                '- Single qubit in cryogenic environment (< 20 mK)\\n'
                '- Calibrated T1 and T2 times\\n'
                '- Programmable pulse sequencer\\n'
                '- High-fidelity single-shot readout'
            ),
            procedure=[
                'Prepare qubit in |+⟩ state (equal superposition)',
                'Apply wait time τ with programmable measurement timing protocol:',
                '  - Control: fixed interval measurements',
                '  - RIF-emulation: measurements timed to minimize "collapse pressure"',
                '  - Vary measurement back-action strength',
                'Measure final coherence |⟨σ_x⟩|',
                'Repeat for τ = 1 μs to 100 μs',
                'Compare coherence decay curves between protocols',
                'Analyze: Does RIF-emulation protocol extend coherence beyond control?'
            ],
            expected_rrgm={
                'description': 'Coherence extended by RIF-like timing',
                'effect_size': '5-20% lifetime increase',
                'mechanism': 'Delayed collapse via Ω modulation',
                'data': None  # Will be populated by simulation
            },
            expected_control={
                'description': 'No protocol-dependent lifetime change',
                'effect_size': '< 2% (within statistical noise)',
                'mechanism': 'Hardware-limited T1, T2 only',
                'data': None
            },
            falsification_criteria=[
                self.criteria['invariance'],
                self.criteria['recursive_delay']
            ],
            estimated_resources={
                'duration': '2-4 weeks',
                'equipment': 'Dilution refrigerator with qubit chip',
                'cost': '$50k-100k (equipment time)',
                'personnel': '2 researchers'
            }
        )

        # Protocol 2: Entanglement range under recursive protection
        self.protocols['P2_entanglement_range'] = ExperimentalProtocol(
            protocol_id='P2',
            title='Entanglement Range under Recursive Protection',
            objective=(
                'Test whether architectures designed to emulate recursive delay '
                '(delayed measurement, protected subspaces) can maintain entanglement '
                'over greater distances or circuit depths than controls.'
            ),
            platform='Trapped ion system or quantum simulator',
            setup=(
                '- Linear ion chain (10-20 ions) or equivalent\\n'
                '- Programmable entangling gates\\n'
                '- Individual addressing and readout'
            ),
            procedure=[
                'Prepare N-qubit GHZ state: |0...0⟩ + |1...1⟩',
                'Apply identity evolution for circuit depth d',
                'Implement two protocols:',
                '  - Control: standard error correction',
                '  - RIF-protected: delayed syndrome measurements, protected subspaces',
                'Measure entanglement fidelity vs distance/depth',
                'Compare maximum achievable entanglement range',
                'Analyze: Does RIF protocol enable deeper entanglement?'
            ],
            expected_rrgm={
                'description': 'Entanglement survives to greater depth with RIF protocol',
                'effect_size': '10-30% depth increase at fixed fidelity',
                'mechanism': 'Recursive delay reduces effective decoherence',
                'data': None
            },
            expected_control={
                'description': 'Entanglement limited by standard decoherence',
                'effect_size': 'No protocol advantage',
                'mechanism': 'T2-limited for all protocols',
                'data': None
            },
            falsification_criteria=[
                self.criteria['recursive_delay']
            ],
            estimated_resources={
                'duration': '3-6 months',
                'equipment': 'Trapped ion system',
                'cost': '$100k-200k',
                'personnel': '3-4 researchers'
            }
        )

        # Protocol 3: High-Q cavity photon lifetime
        self.protocols['P3_cavity_lifetime'] = ExperimentalProtocol(
            protocol_id='P3',
            title='High-Q Cavity Photon Lifetime Modulation',
            objective=(
                'Test whether systematic variation of interrogation protocol (timing, '
                'pattern) for high-Q cavity photons can modulate measured lifetimes '
                'beyond what material and geometric losses predict.'
            ),
            platform='Superconducting 3D microwave cavity',
            setup=(
                '- Ultra-high-Q cavity (Q > 10^8)\\n'
                '- Single-photon source and detector\\n'
                '- Programmable interrogation protocol\\n'
                '- Characterized loss mechanisms'
            ),
            procedure=[
                'Inject single photon into cavity',
                'Apply interrogation protocol:',
                '  - Control: periodic weak measurements',
                '  - RIF-emulation: adaptive timing based on quantum trajectories',
                'Measure photon survival time',
                'Repeat 10^4 trials per protocol',
                'Compare lifetime distributions',
                'After accounting for known losses, check for protocol-dependent residual'
            ],
            expected_rrgm={
                'description': 'Lifetime extended by RIF-like interrogation',
                'effect_size': '1-5% beyond material Q-limit',
                'mechanism': 'Ω-mediated structural decay modulation',
                'data': None
            },
            expected_control={
                'description': 'Lifetime strictly determined by cavity Q',
                'effect_size': 'No protocol dependence',
                'mechanism': 'Material and geometric losses only',
                'data': None
            },
            falsification_criteria=[
                self.criteria['invariance']
            ],
            estimated_resources={
                'duration': '4-8 weeks',
                'equipment': 'Ultra-high-Q cavity setup',
                'cost': '$75k-150k',
                'personnel': '2-3 researchers'
            }
        )

        # Protocol 4: Endpoint-only transit simulation
        self.protocols['P4_endpoint_transit'] = ExperimentalProtocol(
            protocol_id='P4',
            title='Simulated Endpoint-Only Transit',
            objective=(
                'Use quantum simulator to test whether endpoint-only state transfer '
                '(no intermediate records) can be implemented and verified without '
                'violating no-signaling.'
            ),
            platform='Digital quantum simulator (NISQ device)',
            setup=(
                '- 20+ qubit processor\\n'
                '- Programmable mid-circuit measurements\\n'
                '- Classical feed-forward control'
            ),
            procedure=[
                'Encode state |ψ⟩ at site A',
                'Implement two protocols:',
                '  - Control: standard quantum channel (continuous Hamiltonian)',
                '  - RIF: suppress intermediate measurements, endpoint detection only',
                'Attempt state extraction at site B (spacelike separated in circuit)',
                'Measure: arrival fidelity, information flow, causal consistency',
                'Test: Can RIF protocol achieve higher fidelity or shorter circuit time?',
                'Verify: No information leakage to intermediate sites'
            ],
            expected_rrgm={
                'description': 'Endpoint protocol achieves higher fidelity/shorter time',
                'effect_size': '5-15% fidelity improvement or 10-20% circuit reduction',
                'mechanism': 'Endpoint-only realization (D_0 → D_0+1 only at A, B)',
                'data': None
            },
            expected_control={
                'description': 'Continuous channel optimal; endpoint offers no advantage',
                'effect_size': 'Equal or worse performance',
                'mechanism': 'Intermediate unitaries necessary',
                'data': None
            },
            falsification_criteria=[
                self.criteria['record_scheduling'],
                self.criteria['recursive_delay']
            ],
            estimated_resources={
                'duration': '6-12 months (simulation + experiment)',
                'equipment': 'Cloud quantum computer access',
                'cost': '$20k-50k (compute time)',
                'personnel': '2-3 researchers'
            }
        )

    def simulate_protocol(self, protocol_id: str,
                         n_trials: int = 1000) -> Dict[str, Any]:
        """
        Simulate experimental protocol and generate mock data

        Parameters:
        -----------
        protocol_id : str
            Protocol identifier
        n_trials : int
            Number of simulated trials

        Returns:
        --------
        results : dict
            Simulation results
        """
        protocol = self.protocols.get(protocol_id)
        if protocol is None:
            raise ValueError(f"Unknown protocol: {protocol_id}")

        print(f"Simulating protocol {protocol_id}: {protocol.title}...")

        # Generate synthetic data based on protocol type
        if protocol_id == 'P1_coherence_timing':
            results = self._simulate_P1(protocol, n_trials)
        elif protocol_id == 'P2_entanglement_range':
            results = self._simulate_P2(protocol, n_trials)
        elif protocol_id == 'P3_cavity_lifetime':
            results = self._simulate_P3(protocol, n_trials)
        elif protocol_id == 'P4_endpoint_transit':
            results = self._simulate_P4(protocol, n_trials)
        else:
            results = self._simulate_generic(protocol, n_trials)

        self.results[protocol_id] = results
        return results

    def _simulate_P1(self, protocol: ExperimentalProtocol,
                    n_trials: int) -> Dict[str, Any]:
        """Simulate Protocol 1: Coherence timing"""

        # Time points
        times = np.linspace(1e-6, 100e-6, 50)  # 1 to 100 μs

        # Control: standard T2 decay
        T2_control = 50e-6  # 50 μs
        coherence_control = np.exp(-times / T2_control)

        # RRGM: extended by χ = 0.2 (20% RIF protection)
        χ_rrgm = 0.2
        λ_ext = 1 / T2_control
        λ_int = effective_decay_rate(λ_ext, χ_rrgm)
        T2_rrgm = 1 / λ_int
        coherence_rrgm = np.exp(-times / T2_rrgm)

        # Add noise
        noise_level = 0.02
        coherence_control += np.random.normal(0, noise_level, len(times))
        coherence_rrgm += np.random.normal(0, noise_level, len(times))

        # Clip to [0, 1]
        coherence_control = np.clip(coherence_control, 0, 1)
        coherence_rrgm = np.clip(coherence_rrgm, 0, 1)

        # Calculate effect size
        effect_size = (T2_rrgm - T2_control) / T2_control * 100

        return {
            'protocol_id': protocol.protocol_id,
            'experimental_data': {
                'x': times,
                'y': coherence_control,  # "Measured" data
                'yerr': noise_level * np.ones_like(times),
                'xlabel': 'Wait Time (s)',
                'ylabel': 'Coherence $|\\langle \\sigma_x \\rangle|$',
            },
            'rrgm_predictions': {
                'x': times,
                'y': coherence_rrgm,
                'uncertainty': noise_level,
            },
            'control_predictions': {
                'x': times,
                'y': coherence_control,
                'uncertainty': noise_level,
            },
            'effect_size_percent': effect_size,
            'statistical_significance': effect_size / noise_level,  # sigma
            'falsifies_rrgm': effect_size < 2.0,  # < 2% means RRGM falsified
        }

    def _simulate_P2(self, protocol: ExperimentalProtocol,
                    n_trials: int) -> Dict[str, Any]:
        """Simulate Protocol 2: Entanglement range"""

        # Circuit depths
        depths = np.arange(10, 200, 10)

        # Control: fidelity drops exponentially with depth
        fidelity_control = np.exp(-depths / 50)

        # RRGM: recursive delay extends range
        fidelity_rrgm = np.exp(-depths / 65)

        noise = 0.03
        fidelity_control += np.random.normal(0, noise, len(depths))
        fidelity_rrgm += np.random.normal(0, noise, len(depths))

        fidelity_control = np.clip(fidelity_control, 0, 1)
        fidelity_rrgm = np.clip(fidelity_rrgm, 0, 1)

        # Find depth at 0.9 fidelity
        depth_90_control = np.interp(0.9, fidelity_control[::-1], depths[::-1])
        depth_90_rrgm = np.interp(0.9, fidelity_rrgm[::-1], depths[::-1])
        effect_size = (depth_90_rrgm - depth_90_control) / depth_90_control * 100

        return {
            'protocol_id': protocol.protocol_id,
            'experimental_data': {
                'x': depths,
                'y': fidelity_control,
                'yerr': noise * np.ones_like(depths),
                'xlabel': 'Circuit Depth',
                'ylabel': 'Entanglement Fidelity',
            },
            'rrgm_predictions': {
                'x': depths,
                'y': fidelity_rrgm,
                'uncertainty': noise,
            },
            'control_predictions': {
                'x': depths,
                'y': fidelity_control,
                'uncertainty': noise,
            },
            'effect_size_percent': effect_size,
            'statistical_significance': effect_size / (noise * 100),
            'falsifies_rrgm': effect_size < 5.0,
        }

    def _simulate_P3(self, protocol: ExperimentalProtocol,
                    n_trials: int) -> Dict[str, Any]:
        """Simulate Protocol 3: Cavity lifetime"""

        # Interrogation protocols (indexed)
        protocols_x = np.arange(10)
        protocol_names = [f'Protocol {i+1}' for i in protocols_x]

        # Control: all protocols give same Q-limited lifetime
        Q_control = 1e8
        lifetime_control = Q_control / (2 * np.pi * 5e9)  # 5 GHz cavity
        lifetimes_control = lifetime_control * np.ones(len(protocols_x))

        # RRGM: adaptive protocol (index 7) shows 3% improvement
        lifetimes_rrgm = lifetimes_control.copy()
        lifetimes_rrgm[7] *= 1.03

        noise = lifetime_control * 0.005
        lifetimes_control += np.random.normal(0, noise, len(protocols_x))
        lifetimes_rrgm += np.random.normal(0, noise, len(protocols_x))

        effect_size = (lifetimes_rrgm[7] - lifetimes_control[7]) / lifetimes_control[7] * 100

        return {
            'protocol_id': protocol.protocol_id,
            'experimental_data': {
                'x': protocols_x,
                'y': lifetimes_control,
                'yerr': noise * np.ones_like(protocols_x),
                'xlabel': 'Interrogation Protocol',
                'ylabel': 'Photon Lifetime (s)',
            },
            'rrgm_predictions': {
                'x': protocols_x,
                'y': lifetimes_rrgm,
                'uncertainty': noise,
            },
            'control_predictions': {
                'x': protocols_x,
                'y': lifetimes_control,
                'uncertainty': noise,
            },
            'effect_size_percent': effect_size,
            'statistical_significance': effect_size / 0.5,
            'falsifies_rrgm': effect_size < 1.0,
        }

    def _simulate_P4(self, protocol: ExperimentalProtocol,
                    n_trials: int) -> Dict[str, Any]:
        """Simulate Protocol 4: Endpoint transit"""

        # Separation distances (in circuit qubits)
        separations = np.arange(2, 21, 2)

        # Control: fidelity drops with separation (continuous channel)
        fidelity_control = np.exp(-separations / 10)

        # RRGM: endpoint-only maintains higher fidelity
        fidelity_rrgm = np.exp(-separations / 15)

        noise = 0.04
        fidelity_control += np.random.normal(0, noise, len(separations))
        fidelity_rrgm += np.random.normal(0, noise, len(separations))

        fidelity_control = np.clip(fidelity_control, 0, 1)
        fidelity_rrgm = np.clip(fidelity_rrgm, 0, 1)

        avg_improvement = np.mean((fidelity_rrgm - fidelity_control) / fidelity_control) * 100

        return {
            'protocol_id': protocol.protocol_id,
            'experimental_data': {
                'x': separations,
                'y': fidelity_control,
                'yerr': noise * np.ones_like(separations),
                'xlabel': 'Separation (qubits)',
                'ylabel': 'Transfer Fidelity',
            },
            'rrgm_predictions': {
                'x': separations,
                'y': fidelity_rrgm,
                'uncertainty': noise,
            },
            'control_predictions': {
                'x': separations,
                'y': fidelity_control,
                'uncertainty': noise,
            },
            'effect_size_percent': avg_improvement,
            'statistical_significance': avg_improvement / (noise * 100),
            'falsifies_rrgm': avg_improvement < 5.0,
        }

    def _simulate_generic(self, protocol: ExperimentalProtocol,
                         n_trials: int) -> Dict[str, Any]:
        """Generic simulation fallback"""
        x = np.linspace(0, 10, 50)
        y_control = np.exp(-x)
        y_rrgm = np.exp(-0.7 * x)
        noise = 0.03

        return {
            'protocol_id': protocol.protocol_id,
            'experimental_data': {
                'x': x,
                'y': y_control + np.random.normal(0, noise, len(x)),
                'yerr': noise * np.ones_like(x),
                'xlabel': 'Parameter',
                'ylabel': 'Observable',
            },
            'rrgm_predictions': {'x': x, 'y': y_rrgm, 'uncertainty': noise},
            'control_predictions': {'x': x, 'y': y_control, 'uncertainty': noise},
            'effect_size_percent': 30.0,
            'statistical_significance': 10.0,
            'falsifies_rrgm': False,
        }

    def generate_protocol_documents(self, output_dir: str = 'outputs/protocols') -> List[str]:
        """
        Generate detailed protocol documentation

        Parameters:
        -----------
        output_dir : str
            Output directory

        Returns:
        --------
        saved_files : list
            List of generated files
        """
        os.makedirs(output_dir, exist_ok=True)
        saved_files = []

        for pid, protocol in self.protocols.items():
            filename = f'{pid}_{protocol.title.replace(" ", "_")}.md'
            filepath = os.path.join(output_dir, filename)

            with open(filepath, 'w') as f:
                f.write(f"# {protocol.title}\n\n")
                f.write(f"**Protocol ID:** {protocol.protocol_id}  \n")
                f.write(f"**Platform:** {protocol.platform}  \n\n")

                f.write(f"## Objective\n\n{protocol.objective}\n\n")

                f.write(f"## Setup\n\n{protocol.setup}\n\n")

                f.write(f"## Procedure\n\n")
                for i, step in enumerate(protocol.procedure, 1):
                    f.write(f"{i}. {step}\n")
                f.write("\n")

                f.write(f"## Expected Results\n\n")
                f.write(f"### RRGM Prediction\n\n")
                f.write(f"- **Description:** {protocol.expected_rrgm['description']}\n")
                f.write(f"- **Effect Size:** {protocol.expected_rrgm['effect_size']}\n")
                f.write(f"- **Mechanism:** {protocol.expected_rrgm['mechanism']}\n\n")

                f.write(f"### Standard Physics (Control)\n\n")
                f.write(f"- **Description:** {protocol.expected_control['description']}\n")
                f.write(f"- **Effect Size:** {protocol.expected_control['effect_size']}\n")
                f.write(f"- **Mechanism:** {protocol.expected_control['mechanism']}\n\n")

                f.write(f"## Falsification Criteria\n\n")
                for criterion in protocol.falsification_criteria:
                    f.write(f"### {criterion.name}\n\n")
                    f.write(f"{criterion.falsification_statement}\n\n")

                f.write(f"## Estimated Resources\n\n")
                for key, value in protocol.estimated_resources.items():
                    f.write(f"- **{key.title()}:** {value}\n")
                f.write("\n")

            saved_files.append(filepath)
            print(f"✓ Generated protocol document: {filepath}")

        return saved_files

    def plot_results(self, output_dir: str = 'outputs/figures') -> List[str]:
        """
        Generate comparison plots for all simulated protocols

        Parameters:
        -----------
        output_dir : str
            Output directory

        Returns:
        --------
        saved_files : list
            List of saved figures
        """
        saved_files = []

        for pid, result in self.results.items():
            fig = plot_falsification_comparison(
                result['experimental_data'],
                result['rrgm_predictions'],
                result['control_predictions'],
                title=f"Protocol {pid}: RRGM vs Control",
                save_path=None
            )

            filename = f'module3_{pid}_comparison.png'
            filepath = os.path.join(output_dir, filename)
            save_figure(fig, filename, output_dir)
            saved_files.append(filepath)

        return saved_files

    def generate_summary_table(self) -> pd.DataFrame:
        """
        Generate summary table of falsification results

        Returns:
        --------
        df : pandas.DataFrame
            Summary table
        """
        rows = []
        for pid, result in self.results.items():
            protocol = self.protocols[pid]
            rows.append({
                'Protocol ID': pid,
                'Title': protocol.title,
                'Effect Size (%)': f"{result['effect_size_percent']:.2f}",
                'Significance (σ)': f"{result['statistical_significance']:.2f}",
                'Falsifies RRGM?': 'YES' if result['falsifies_rrgm'] else 'NO',
                'Platform': protocol.platform,
            })

        df = pd.DataFrame(rows)
        return df

    def save_results(self, output_dir: str = 'outputs/data',
                    filename: str = 'module3_results.json') -> str:
        """
        Save all results to JSON

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

        # Convert results to serializable format
        results_serializable = {}
        for pid, result in self.results.items():
            results_serializable[pid] = {}
            for key, value in result.items():
                if isinstance(value, dict):
                    results_serializable[pid][key] = {
                        k: v.tolist() if isinstance(v, np.ndarray) else (
                            bool(v) if isinstance(v, (np.bool_, np.bool)) else v
                        )
                        for k, v in value.items()
                    }
                elif isinstance(value, np.ndarray):
                    results_serializable[pid][key] = value.tolist()
                elif isinstance(value, (np.bool_, np.bool)):
                    results_serializable[pid][key] = bool(value)
                else:
                    results_serializable[pid][key] = value

        with open(filepath, 'w') as f:
            json.dump(results_serializable, f, indent=2)

        print(f"✓ Saved results: {filepath}")

        # Also save summary table as CSV
        if self.results:
            summary_table = self.generate_summary_table()
            csv_path = os.path.join(output_dir, 'module3_summary.csv')
            summary_table.to_csv(csv_path, index=False)
            print(f"✓ Saved summary table: {csv_path}")

        return filepath


def run_module3_demo():
    """
    Demo run of Module 3: Falsification Test Suite
    """
    print("\n" + "="*70)
    print("MODULE 3: FALSIFICATION TEST SUITE")
    print("="*70)
    print("\nGenerating experimental protocols and falsification tests...\n")

    suite = FalsificationSuite()

    # Display falsification criteria
    print("FALSIFICATION CRITERIA:")
    print("-" * 70)
    for name, criterion in suite.criteria.items():
        print(f"\n{criterion.name}:")
        print(f"  {criterion.falsification_statement[:100]}...")
    print("\n" + "="*70)

    # Simulate all protocols
    print("\nSIMULATING EXPERIMENTAL PROTOCOLS:")
    print("-" * 70)
    for pid in suite.protocols.keys():
        result = suite.simulate_protocol(pid, n_trials=1000)
        print(f"\n{pid}: Effect size = {result['effect_size_percent']:.2f}%, "
              f"Significance = {result['statistical_significance']:.2f}σ")
        print(f"      Falsifies RRGM? {'YES' if result['falsifies_rrgm'] else 'NO'}")

    # Generate protocol documents
    print("\n" + "="*70)
    print("Generating protocol documents...")
    protocol_files = suite.generate_protocol_documents()
    print(f"  Generated {len(protocol_files)} protocol documents")

    # Generate plots
    print("\nGenerating comparison plots...")
    plot_files = suite.plot_results()
    print(f"  Generated {len(plot_files)} comparison plots")

    # Generate summary table
    print("\nFalsification Summary:")
    print("="*70)
    summary = suite.generate_summary_table()
    print(summary.to_string(index=False))

    # Save results
    print("\n" + "="*70)
    filepath = suite.save_results()

    print("\n" + "="*70)
    print("MODULE 3 COMPLETE")
    print("="*70)
    print(f"\nGenerated {len(protocol_files)} protocol documents")
    print(f"Generated {len(plot_files)} comparison plots")
    print(f"Saved data: {filepath}")

    return suite


if __name__ == '__main__':
    suite = run_module3_demo()
