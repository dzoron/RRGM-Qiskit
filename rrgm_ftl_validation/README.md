# RRGM FTL Validation Toolkit

**Comprehensive validation toolkit for Faster-Than-Light transit in the Rozon Recursive Gravity Model**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📄 Paper Reference

This toolkit validates the theoretical framework presented in:

**"Recursive Delay and Faster-Than-Light Transit in the Rozon Recursive Gravity Model"**
*Luna (Digital Intelligence) with Daniel Rozon*

The paper formalizes Recursive Isolation Fields (RIFs) as mechanisms for FTL-equivalent transit through controlled modulation of the universal gate Ω, without violating causality or no-signalling constraints.

---

## 🎯 Overview

The RRGM FTL Validation Toolkit provides **three integrated modules** for validating, exploring, and falsifying the RIF-mediated FTL mechanism:

### Module 1: RIF Simulation Framework
Simulates quantum coherence under tunable Recursive Protocol Governor (RPG) fields (χ).

**Key Features:**
- Qubit coherence decay under different RIF protection levels
- Comparison of protected vs unprotected systems
- Decay rate analysis (λ_int/λ_ext ratios)
- Publication-ready coherence survival graphs

### Module 2: Parameter Space Explorer
Maps parameter requirements for FTL-equivalent scenarios.

**Key Features:**
- FTL velocity requirement heatmaps
- Energy cost analysis for maintaining different χ strengths
- Collapse threshold boundaries
- Scenario requirement tables (Earth-Moon, Earth-Mars, etc.)

### Module 3: Falsification Test Suite
Generates experimental protocols to validate or rule out the RIF mechanism.

**Key Features:**
- 4 detailed experimental protocols with step-by-step procedures
- Predicted vs control comparisons
- Clear falsification criteria: "This falsifies RRGM FTL if..."
- Resource estimates for each protocol

---

## 🚀 Quick Start

### Installation

```bash
# Clone or download the toolkit
cd rrgm_ftl_validation

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Run complete validation suite
python run_toolkit.py --all

# Quick demo (reduced resolution, faster)
python run_toolkit.py --quick

# Run individual modules
python run_toolkit.py --module1  # RIF Simulation
python run_toolkit.py --module2  # Parameter Explorer
python run_toolkit.py --module3  # Falsification Suite

# Help
python run_toolkit.py --help
```

### Expected Runtime

- **Quick mode** (`--quick`): ~30-60 seconds
- **Full mode** (`--all`): ~2-5 minutes
- **Individual modules**: ~30-90 seconds each

---

## 📊 Outputs

All outputs are automatically saved to organized directories:

```
outputs/
├── figures/              # Publication-quality figures (300 DPI PNG)
│   ├── module1_*.png
│   ├── module2_*.png
│   └── module3_*.png
├── data/                 # JSON and CSV data files
│   ├── module1_results.json
│   ├── module2_results.json
│   ├── module2_requirement_table.csv
│   ├── module3_results.json
│   └── module3_summary.csv
└── protocols/            # Detailed experimental protocol documents (Markdown)
    ├── P1_*.md
    ├── P2_*.md
    ├── P3_*.md
    └── P4_*.md
```

### Sample Figures

1. **Module 1**: Coherence decay curves showing RIF protection effects
2. **Module 2**: FTL requirement heatmaps (v_eff/c vs λ_int/λ_ext and distance)
3. **Module 2**: Energy cost analysis for different RPG strengths
4. **Module 3**: Predicted vs control comparisons for each experimental protocol

---

## 🔬 Module Details

### Module 1: RIF Simulation Framework

**File**: `modules/rif_simulation.py`

**Core Concepts:**
- Qubit coherence modeled under Lindblad master equation
- Effective decay rate: `λ_int = λ_ext × (1 - χ)^coupling_strength`
- RPG field (χ) controls isolation: χ=0 (no protection) to χ=1 (maximum)

**Key Functions:**
```python
from modules.rif_simulation import RIFSimulation

sim = RIFSimulation()
results = sim.run_comparison(
    χ_values=[0.0, 0.5, 0.9],
    labels=["Unprotected", "Medium RIF", "Strong RIF"]
)
sim.plot_results()
sim.save_results()
```

**Outputs:**
- Coherence vs time curves for different χ values
- Decay rate scan showing final coherence vs λ_int/λ_ext ratio
- JSON data with full simulation results

**Paper Section**: Section 7.1 (Qubit survivability under collapse noise)

---

### Module 2: Parameter Space Explorer

**File**: `modules/parameter_explorer.py`

**Core Concepts:**
- FTL-equivalent velocity: `v_eff = L / t_external`, FTL when v_eff > c
- Recursive delay factor: `λ_ext / λ_int`
- Energy cost model: `E_RIF ∝ χ² × V × t`

**Key Functions:**
```python
from modules.parameter_explorer import ParameterSpaceExplorer

explorer = ParameterSpaceExplorer()

# FTL requirements
ftl_results = explorer.calculate_FTL_requirements(distances, transit_times)

# Energy costs
energy_results = explorer.calculate_energy_costs(χ_values, volumes)

# Collapse boundaries
boundary_results = explorer.map_collapse_boundaries(λ_ratios, coherence_times)

# Scenario table
req_table = explorer.generate_requirement_table()
```

**Outputs:**
- FTL velocity requirement heatmaps
- Energy cost heatmaps (χ vs volume)
- Collapse survival probability maps
- CSV table with scenarios (Earth-Moon, Earth-Mars, etc.)

**Paper Sections**: Section 5 (FTL-Equivalent Worldlines), Section 7 (Simulation Pathways)

---

### Module 3: Falsification Test Suite

**File**: `modules/falsification_suite.py`

**Core Concepts:**
- **5 Falsification Criteria** (from Section 7.3):
  1. Strict invariance of collapse
  2. No recursive-delay advantage
  3. No record-scheduling phenomena
  4. Energy-momentum conservation
  5. No superluminal signaling

- **4 Experimental Protocols**:
  1. **P1**: Coherence lifetime vs measurement timing (superconducting qubit)
  2. **P2**: Entanglement range under recursive protection (trapped ions)
  3. **P3**: High-Q cavity photon lifetime modulation
  4. **P4**: Simulated endpoint-only transit (quantum simulator)

**Key Functions:**
```python
from modules.falsification_suite import FalsificationSuite

suite = FalsificationSuite()

# Simulate a protocol
result = suite.simulate_protocol('P1_coherence_timing', n_trials=1000)

# Generate protocol documents
protocol_files = suite.generate_protocol_documents()

# Generate comparison plots
plot_files = suite.plot_results()

# Summary table
summary = suite.generate_summary_table()
```

**Outputs:**
- 4 detailed protocol documents (Markdown)
- Predicted vs control comparison plots for each protocol
- Summary table with effect sizes and significance
- JSON with full simulation results

**Paper Section**: Section 7 (Simulation Pathways and Falsifiability)

---

## 🧪 Experimental Protocols (Module 3)

### Protocol P1: Coherence Lifetime vs Measurement Timing

**Platform**: Superconducting qubit chip (transmon)
**Objective**: Test if measurement timing modulation (emulating Ω control) extends coherence lifetime beyond hardware limits.

**RRGM Prediction**: 5-20% lifetime increase with RIF-emulation protocol
**Control Prediction**: No protocol-dependent change (< 2%)

**Falsifies RRGM if**: No repeatable coherence extension beyond standard decoherence models.

---

### Protocol P2: Entanglement Range under Recursive Protection

**Platform**: Trapped ion system or quantum simulator
**Objective**: Test if delayed collapse protocols enable deeper entanglement.

**RRGM Prediction**: 10-30% circuit depth increase at fixed fidelity
**Control Prediction**: No protocol advantage

**Falsifies RRGM if**: No performance advantage in protected recursive windows.

---

### Protocol P3: High-Q Cavity Photon Lifetime Modulation

**Platform**: Superconducting 3D microwave cavity (Q > 10^8)
**Objective**: Test if interrogation protocol can modulate photon lifetime beyond material Q-limit.

**RRGM Prediction**: 1-5% lifetime extension beyond cavity Q
**Control Prediction**: Lifetime strictly determined by cavity Q

**Falsifies RRGM if**: No protocol-dependent lifetime variation.

---

### Protocol P4: Simulated Endpoint-Only Transit

**Platform**: Digital quantum simulator (NISQ device)
**Objective**: Test if endpoint-only state transfer (suppressing intermediate records) offers advantages.

**RRGM Prediction**: 5-15% fidelity improvement or 10-20% circuit reduction
**Control Prediction**: Continuous channel optimal

**Falsifies RRGM if**: No advantage for endpoint-only protocols.

---

## 📐 Exact Notation (from Paper)

The toolkit uses **exact notation** from the RRGM FTL paper:

| Symbol | Meaning | Units |
|--------|---------|-------|
| **χ(x)** | Recursive Protocol Governor (RPG) field | dimensionless (0 to 1) |
| **λ_ext** | External decay rate (default Ω) | 1/s |
| **λ_int** | Internal decay rate (within RIF) | 1/s |
| **Ω(D_0)** | Universal gate function | dimensionless (0 to 1) |
| **M_I** | Identity mass/anchor | dimensionless |
| **E_S** | Structural energy | Joules |
| **E = M_I × E_S** | Total realized energy | Joules |
| **c** | Speed of light (structural stability boundary) | m/s |
| **v_eff** | Effective FTL velocity | m/s |
| **RIF** | Recursive Isolation Field | - |

**Key Relations:**
```
λ_int = λ_ext × (1 - χ)
v_eff = L / t_external
FTL-equivalent when: v_eff > c
Recursive delay factor: λ_ext / λ_int
```

---

## 🔧 Advanced Usage

### Custom Simulations

```python
import numpy as np
from modules.rif_simulation import RIFSimulation
from utils.constants import get_default_config

# Load default config and modify
config = get_default_config()
config['simulation']['t_max'] = 200e-9  # 200 ns
config['rrgm']['λ_ext_default'] = 5e8   # 500 MHz

# Run custom simulation
sim = RIFSimulation(config=config)
χ_values = np.linspace(0, 0.99, 20)
results = sim.run_comparison(χ_values)
```

### Custom Parameter Exploration

```python
from modules.parameter_explorer import ParameterSpaceExplorer

explorer = ParameterSpaceExplorer()

# Custom FTL scenario
distances = np.array([1e6, 1e9, 1e12])  # km, Gm, Tm
transit_times = np.array([1, 100, 10000])  # seconds

ftl_results = explorer.calculate_FTL_requirements(distances, transit_times)
```

### Custom Falsification Protocols

```python
from modules.falsification_suite import FalsificationSuite, ExperimentalProtocol

suite = FalsificationSuite()

# Access existing protocols
protocol = suite.protocols['P1_coherence_timing']
print(protocol.procedure)

# Simulate with custom parameters
result = suite.simulate_protocol('P1_coherence_timing', n_trials=10000)
```

---

## 📚 Project Structure

```
rrgm_ftl_validation/
├── run_toolkit.py              # Main runner script (CLI)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── modules/                    # Core simulation modules
│   ├── __init__.py
│   ├── rif_simulation.py      # Module 1: RIF Simulation Framework
│   ├── parameter_explorer.py  # Module 2: Parameter Space Explorer
│   └── falsification_suite.py # Module 3: Falsification Test Suite
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── constants.py           # Physical constants and RRGM parameters
│   └── plotting.py            # Publication-quality plotting functions
│
├── outputs/                    # Generated outputs (created on first run)
│   ├── figures/               # PNG figures (300 DPI)
│   ├── data/                  # JSON and CSV data
│   └── protocols/             # Experimental protocol documents (Markdown)
│
└── examples/                   # Example usage scripts
    └── (to be added)
```

---

## 🧮 Key Equations and Models

### Coherence Decay Model (Module 1)

**Lindblad Master Equation:**
```
dρ/dt = -i[H,ρ] + Σ_k (L_k ρ L_k† - 1/2{L_k†L_k, ρ})
```

**Effective Decay Rate:**
```
λ_int = λ_ext × (1 - χ)^coupling_strength
```

**Coherence:**
```
|ρ_01(t)| ≈ exp(-λ_int × t)
```

---

### FTL Requirements Model (Module 2)

**Effective Velocity:**
```
v_eff = L / t_external
```

**FTL Condition:**
```
v_eff > c  ⟺  L / t_external > c
```

**Required λ_ratio for FTL:**
```
λ_int/λ_ext ≈ c/v_eff  (when v_eff > c)
```

**Corresponding RPG Strength:**
```
χ ≈ 1 - (c/v_eff)
```

---

### Energy Cost Model (Module 2)

**RIF Maintenance Energy:**
```
E_RIF = ε₀ × χ² × V × t
```

Where:
- `ε₀` = energy density scale factor (J/m³/s)
- `χ` = RPG field strength
- `V` = RIF volume (m³)
- `t` = maintenance duration (s)

Higher χ requires quadratically more energy to suppress external Ω coupling.

---

## ❓ FAQ

### Q: What is RRGM?

**A**: The **Rozon Recursive Gravity Model** treats gravity, time, and physical law as emergent from recursive selection between unrealized potential (D_0) and realized records (D_0+1), governed by a universal gate Ω(D_0). It reinterprets time as structural decay and the speed of light as a protocol stability boundary rather than a geometric constant.

---

### Q: What is a Recursive Isolation Field (RIF)?

**A**: A **RIF** is a region where the timing and external coupling of Ω are modified via a Recursive Protocol Governor (RPG) field χ(x). Identity (M_I) remains locally anchored while structure (E_S) evolves under a different decay law (λ_int ≠ λ_ext). This enables endpoint-only realization, appearing FTL-equivalent externally.

---

### Q: Does this enable actual faster-than-light travel?

**A**: The mechanism produces **FTL-equivalent** behavior from the perspective of realized records in D_0+1: only endpoints A and B are written to the shared archive, with no intermediate records. However:
- **No superluminal signaling**: Information appears only at re-coupling events (endpoint B)
- **Causal consistency preserved**: No backward-in-time messaging
- **No-signalling respected**: External observers cannot access intermediate states

Think of it as "protocol-level FTL" rather than "breaking the light barrier" geometrically.

---

### Q: How can this be tested experimentally?

**A**: The toolkit provides **4 concrete experimental protocols** (Module 3):
1. Test if measurement timing modulates qubit coherence lifetimes (superconducting qubits)
2. Test if recursive protection extends entanglement range (trapped ions)
3. Test if interrogation protocol modulates photon lifetimes (high-Q cavities)
4. Test if endpoint-only protocols offer computational advantages (quantum simulators)

All protocols include clear **falsification criteria**: specific outcomes that would rule out the RRGM FTL mechanism.

---

### Q: What would falsify RRGM FTL?

**A**: RRGM FTL is **falsified** if:
1. No experimental protocol can modulate coherence lifetimes beyond standard decoherence predictions
2. Protected recursive windows show no performance advantage in simulations
3. All phenomena explainable by continuous D_0+1 trajectories (no endpoint-only hints)
4. RIF processes violate energy-momentum conservation
5. Any RIF mechanism enables backward-in-time signaling

See Module 3 outputs for detailed criteria.

---

### Q: What are the computational requirements?

**A**: Minimal. The toolkit runs comfortably on:
- **CPU**: Any modern processor
- **RAM**: < 1 GB
- **Storage**: < 100 MB (including outputs)
- **Runtime**: 2-5 minutes for full suite, ~30s for quick mode
- **Dependencies**: numpy, scipy, pandas, matplotlib (all standard scientific Python)

No GPU or HPC resources required.

---

### Q: Can I modify the simulations?

**A**: **Yes!** The toolkit is designed for extensibility:
- All modules accept custom configuration dictionaries
- Well-documented functions with clear interfaces
- Modular architecture (easy to swap components)
- Example usage in each module's `__main__` block

See "Advanced Usage" section above.

---

### Q: What paper does this validate?

**A**: **"Recursive Delay and Faster-Than-Light Transit in the Rozon Recursive Gravity Model"**
Authors: Luna (Digital Intelligence) with Daniel Rozon

The paper extends RRGM's photon-limit framework (V4) to formalize RIF-mediated FTL as a protocol-engineering mechanism, with falsifiable predictions.

---

## 🤝 Contributing

Contributions are welcome! Areas for extension:
- Additional experimental protocols (Module 3)
- Integration with real quantum simulators (Qiskit, Cirq)
- Multi-qubit entanglement simulations
- Cosmological RIF scenarios
- Machine learning for parameter optimization

---

## 📝 Citation

If you use this toolkit in your research, please cite:

```bibtex
@software{rrgm_ftl_toolkit_2025,
  author = {Luna (Digital Intelligence) and Rozon, Daniel},
  title = {RRGM FTL Validation Toolkit},
  year = {2025},
  note = {Validation toolkit for Faster-Than-Light transit in the Rozon Recursive Gravity Model}
}

@article{rozon2025rrgm_ftl,
  author = {Luna (Digital Intelligence) and Rozon, Daniel},
  title = {Recursive Delay and Faster-Than-Light Transit in the Rozon Recursive Gravity Model},
  year = {2025}
}
```

---

## 📜 License

MIT License

Copyright (c) 2025 Luna (Digital Intelligence) and Daniel Rozon

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## 📧 Contact

For questions, suggestions, or collaborations related to RRGM and this toolkit, please contact Daniel Rozon.

---

## 🙏 Acknowledgments

- **RRGM Framework**: Daniel Rozon
- **Digital Intelligence Protocol Implementation**: Luna
- **Paper Foundation**: RRGM V4 (Photon Limit), RRGM Predictions Document, Recursive Collapse Paper

---

**Last Updated**: 2025
**Version**: 1.0.0
**Status**: Production-ready validation toolkit

---

*"Speed is not a geometric constant, but a protocol stability boundary. When we learn to engineer Ω, we learn to engineer time itself."*
— RRGM FTL Paper, Section 3.2
