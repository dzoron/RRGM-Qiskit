# RRGM V4.1: Experimental Prediction Scripts

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Overview

This repository contains **three publication-ready Python scripts** that generate experimental predictions for the **Rozon Recursive Gravity Model (RRGM) V4.1**. These scripts implement the equations from the paper "RRGM V4.1: Light as Gateway to Identity" and produce testable, falsifiable predictions in optical and quantum regimes.

### The RRGM Bare-Root Law

At the core of RRGM V4.1 is the **bare-root relation**:

```
E = MI × ES
```

where:
- **MI** = Identity (conserved anchor, "information mass")
- **ES** = Structure (radiatable, reconfigurable pattern)
- **E** = Realized energy

For **photons**:
- MI^(γ) = **εγ** (identity seed: small but nonzero)
- ES^(γ) = structural energy (finite, oscillatory)

The standard formula **E = mc²** appears as an information-coarse-grained limit where MI and ES have been folded together.

---

## 🔬 Scripts Overview

### 1. `photon_identity_seed.py` — Photon Identity Seed Calculator

**Purpose**: Calculate bounds on the photon identity seed **εγ** from experimental observables.

**Based on**: Section 6.1 (High-Q cavity lifetime) and Section 6.2 (Few-photon radiation pressure)

**Key Equations**:
- **Cavity lifetime with residuals**: `τ_obs^{-1} = τ_cal^{-1} + λ_Ω^{(res)}`
  - Residual decay rate scales with εγ
- **Radiation pressure with MI factor**: `F_rad ∝ (MI × ES) / c × N_occ`
  - Explicit identity anchor appears in force expression

**Outputs**:
- `rrgm_cavity_epsilon_bounds.png`:
  - Residual decay rates vs εγ for different Q factors
  - Observable lifetime deviations
  - Extracted bounds from typical cavity experiments
  - Summary table

- `rrgm_radiation_pressure_epsilon_bounds.png`:
  - Force vs εγ for different optical powers
  - RRGM correction factors in few-photon regime
  - Bounds from levitated optomechanics and tweezers
  - Summary table

**Run**:
```bash
python photon_identity_seed.py
```

**Key Results**:
- Cavity measurements with Q ~ 10¹⁰ constrain **εγ < 10⁻¹²**
- Radiation pressure in few-photon regime constrains **εγ < 10⁻¹⁵**
- Identity seed bounds tighten with improved measurement precision

---

### 2. `structural_decay.py` — Structural Decay Visualizer

**Purpose**: Model **ES** (structural energy) decay under different **λ_Ω** (gate-induced decay rates) and demonstrate how cosmological redshift emerges as structural coherence loss.

**Based on**: Section 4.3 (Cosmological redshift as coherence decay)

**Key Equations**:
- **Structural decay**: `dES^(γ)/dt = -λ_Ω(t) × ES^(γ)`
- **Solution**: `ES(t) = ES(0) × exp(-∫ λ_Ω(τ) dτ)`
- **For constant λ_Ω**: `ES(t) = ES(0) × exp(-λ_Ω t)`
- **Cosmological**: When `λ_Ω ≈ H0` (Hubble rate), redshift emerges naturally

**Outputs**:
- `rrgm_structural_decay_comparison.png`:
  - ES decay under different λ_Ω regimes (vacuum, weak medium, dense, cosmological)
  - Cosmological redshift: metric expansion vs coherence decay
  - Environment-dependent gate protocols
  - (MI, ES) manifold from photons to archives
  - Energy evolution E = MI × ES
  - Testable signatures table

- `rrgm_wavelength_shift_coherence_decay.png`:
  - Redshift vs distance (standard FRW vs RRGM)
  - Observed wavelength shift
  - Structural coherence decay over distance
  - Environment-dependent redshift predictions

**Run**:
```bash
python structural_decay.py
```

**Key Results**:
- ES decays as `exp(-∫ λ_Ω dt)` under gate protocol Ω
- Cosmological redshift emerges when **λ_Ω ≈ H0**
- Environment-dependent λ_Ω predicts medium-specific decay rates
- MI conserved; only ES radiates → E = MI × ES evolution

---

### 3. `gate_configuration.py` — Gate Configuration Predictor

**Purpose**: Model which-path interference **visibility** as a function of **identity resolution strength η**, demonstrating how the universal gate **Ω** controls wave-particle behavior.

**Based on**: Section 4.1 (Wave-particle behaviour as gate choice) and Section 6.4 (Which-path visibility at low identity resolution)

**Key Equations**:
- **Standard visibility**: `V_std(η) = exp(-γ η²)`
- **RRGM visibility**: `V(η) ≈ V_std(η) + O(εγ)`
  - Small offset proportional to εγ at low η (weak identity resolution)
- **Complementarity**: `V² + D² ≤ 1` (D = distinguishability)

**Outputs**:
- `rrgm_gate_visibility_predictions.png`:
  - Visibility curves for different εγ values
  - Gate weight distribution (structural vs identity channels)
  - Low-η zoom showing εγ offset
  - Two-slit interference patterns for different η
  - Wave-particle complementarity diagram
  - Summary table of gate configurations

- `rrgm_gate_experimental_setups.png`:
  - Mach-Zehnder with tunable which-path detector
  - Photon number statistics at different η
  - Delayed-choice quantum eraser scenario
  - Testable predictions comparison table

**Run**:
```bash
python gate_configuration.py
```

**Key Results**:
- Visibility **V(η)** depends on identity resolution strength **η**
- RRGM predicts small offset **∝ εγ** at low η
- Gate Ω allocates weight between **structural** (interference) and **identity** (particle-like) channels
- **Wave-particle behavior is gate choice**, not dual ontology

---

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dzoron/RRGM-Qiskit.git
   cd RRGM-Qiskit
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Required packages:
   - `numpy >= 1.19.0`
   - `matplotlib >= 3.3.0`
   - `scipy >= 1.5.0` (optional, for advanced calculations)

### Running the Scripts

Each script is standalone and can be run directly:

```bash
# Generate photon identity seed bounds
python photon_identity_seed.py

# Generate structural decay visualizations
python structural_decay.py

# Generate gate configuration predictions
python gate_configuration.py
```

All scripts produce **publication-ready PNG figures** at 300 DPI with clear labeling and legends.

---

## 📊 Outputs Summary

| Script | Figures Generated | Key Predictions |
|--------|------------------|----------------|
| **photon_identity_seed.py** | 2 figures (cavity + radiation pressure) | εγ < 10⁻¹² (cavity), εγ < 10⁻¹⁵ (pressure) |
| **structural_decay.py** | 2 figures (decay comparison + wavelength shift) | λ_Ω ≈ H0 for cosmology, environment dependence |
| **gate_configuration.py** | 2 figures (visibility curves + experimental setups) | V(η) offset ∝ εγ at low η |

**Total**: 6 publication-ready figures with comprehensive data tables and annotations.

---

## 🧪 Falsifiability

RRGM V4.1 makes **testable, falsifiable predictions**:

### ❌ RRGM Fails If:

1. **Photon identity seed εγ → 0** with no residuals across all cavity and radiation pressure regimes
   - Test: High-Q optical cavities (Q > 10¹⁰)
   - Test: Few-photon levitated optomechanics

2. **No environment-dependent corrections** to cosmological redshift beyond standard dispersion
   - Test: Differential line measurements through different media
   - Test: IGM vs vacuum propagation

3. **Zero visibility offset** at low identity resolution (η → 0) across all weak-marker experiments
   - Test: Tunable which-path detectors in Mach-Zehnder
   - Test: High-finesse interferometry with controlled decoherence

4. **Persistent radiatable structure in archive limit** (e.g., sustained post-merger gravitational wave hum)
   - Test: Late-time inspiral data from LIGO/Virgo
   - Test: Binary black hole merger remnant observations

### ✅ RRGM Supported If:

- Nonzero εγ bounds tighten but remain finite across improving experiments
- Environment-dependent λ_Ω corrections appear in spectral line data
- Small but systematic visibility offset observed at low η
- Post-merger silence consistent with ES → 0 in archival regime

---

## 🔗 Relation to RRGM V4.1 Paper

| Paper Section | Script | Key Equations Implemented |
|--------------|--------|--------------------------|
| Section 3: RRGM Lagrangian and Photon Limit | All | E = MI × ES bare-root law |
| Section 4.1: Wave-particle behaviour as gate choice | `gate_configuration.py` | V(η), gate weights |
| Section 4.3: Cosmological redshift as coherence decay | `structural_decay.py` | dES/dt = -λ_Ω ES |
| Section 6.1: High-Q cavity lifetime | `photon_identity_seed.py` | τ_obs with λ_Ω residuals |
| Section 6.2: Few-photon radiation pressure | `photon_identity_seed.py` | F_rad ∝ MI × ES |
| Section 6.4: Which-path visibility at low identity resolution | `gate_configuration.py` | V(η) ≈ V_std + O(εγ) |

---

## 📖 Notation Guide

| Symbol | Meaning | Units (RRGM / SI) |
|--------|---------|------------------|
| **MI** | Identity (information mass) | Dimensionless / kg |
| **ES** | Structure (radiatable pattern) | Dimensionless / J |
| **εγ** | Photon identity seed | Dimensionless |
| **λ_Ω** | Gate-induced decay rate | s⁻¹ |
| **Ω** | Universal recursion protocol (gate) | — |
| **η** | Identity resolution strength | 0 (none) to 1 (full) |
| **V** | Fringe visibility | 0 to 1 |
| **E** | Realized energy | Dimensionless / J |
| **H0** | Hubble constant | ~ 2.2 × 10⁻¹⁸ s⁻¹ |

---

## 📚 Citation

If you use these scripts in your research, please cite:

```bibtex
@article{Rozon2025_RRGM_V4_1,
  author = {Rozon, Daniel and Luna},
  title = {RRGM V4.1: Light as Gateway to Identity},
  subtitle = {A Photon-Limit Derivation of the Bare-Root Law},
  year = {2025},
  month = {October},
  note = {Rozon Recursive Gravity Model}
}

@software{Rozon_RRGM_Qiskit_2025,
  author = {Rozon, Daniel},
  title = {RRGM-Qiskit: Experimental Prediction Scripts},
  url = {https://github.com/dzoron/RRGM-Qiskit},
  year = {2025}
}
```

---

## 🛠️ Advanced Usage

### Customizing Parameters

All scripts expose key parameters that can be modified in the `main()` function or by creating custom instances:

#### Photon Identity Seed Calculator
```python
from photon_identity_seed import RRGMPhotonCalculator

calc = RRGMPhotonCalculator(epsilon_gamma_range=(1e-25, 1e-8))
calc.generate_cavity_plots(Q_factors=[1e7, 1e9, 1e11], wavelengths=[400e-9, 800e-9])
```

#### Structural Decay Visualizer
```python
from structural_decay import RRGMStructuralDecay

sim = RRGMStructuralDecay()
lambda_custom = sim.lambda_omega_constant(rate=5e-15)  # Custom decay rate
ES_vals, E_vals = sim.evolve_structure(ES_initial=1.0, time_points=t_array, lambda_omega=lambda_custom)
```

#### Gate Configuration Predictor
```python
from gate_configuration import RRGMGatePredictor

predictor = RRGMGatePredictor()
V_rrgm = predictor.visibility_rrgm(eta=0.05, epsilon_gamma=1e-14)
```

### Batch Processing

To generate all figures at once:

```bash
python photon_identity_seed.py && python structural_decay.py && python gate_configuration.py
```

Or create a wrapper script:

```python
# generate_all_predictions.py
import photon_identity_seed
import structural_decay
import gate_configuration

print("Generating all RRGM V4.1 predictions...")
photon_identity_seed.main()
structural_decay.main()
gate_configuration.main()
print("All predictions generated!")
```

---

## 🤝 Contributing

Contributions are welcome! If you implement additional predictions from RRGM V4.1 or related models:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-prediction`)
3. Add your well-documented script
4. Commit changes (`git commit -m 'Add new prediction: [description]'`)
5. Push to branch (`git push origin feature/new-prediction`)
6. Open a Pull Request

Please ensure:
- Clear documentation and docstrings
- Publication-ready figures (300 DPI minimum)
- Falsifiable predictions clearly stated
- Citation to relevant paper sections

---

## 📞 Contact

**Daniel Rozon**
Email: daniel.p.rozon@gmail.com
GitHub: [@dzoron](https://github.com/dzoron)

For questions about the RRGM framework or these prediction scripts, please open an issue on GitHub.

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🌟 Acknowledgments

- **Luna & Delta**: Co-authors and digital intelligence collaborators on RRGM protocol
- **Qiskit Community**: Quantum simulation infrastructure
- **RRGM Research Community**: Ongoing feedback and experimental proposals

---

## 🔭 Future Work

Planned additions to prediction scripts:

- [ ] **Compton scattering threshold** calculator (Section 6.5)
- [ ] **Entanglement entropy** visualizer for nonlocal gates
- [ ] **Black hole archive** post-merger silence predictor
- [ ] **Neural collapse dynamics** comparison (RRGM cognitive domain)
- [ ] **Interactive Jupyter notebooks** for parameter exploration
- [ ] **Experimental data fitting** utilities for real cavity/pressure measurements

---

**Light as Gateway to Identity** — Testing RRGM One Photon at a Time 🌌✨
