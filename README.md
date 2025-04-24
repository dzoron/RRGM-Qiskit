# RRGM-Qiskit
Qiskit Files for RRGM Tests. 

# Rozon Recursive Gravity Model (RRGM)  
*"Time as Entropic Decay — Gravity as Recursive Resistance"*  

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
[![Qiskit](https://img.shields.io/badge/Built%20with-Qiskit-blue)](https://qiskit.org)  

## 🌌 Theory Overview  
RRGM proposes that:  
- **Time** emerges from information decay ("spacedecay")  
- **Gravity** arises from entanglement entropy gradients (∇Sₑₙₜ)  
- **Observers** (quantum or classical) locally resist decay, inducing curvature  

Formalized in the Lagrangian:  

\mathcal{L}_{\text{RRGM}} = \alpha (\nabla_\mu S_{\text{ent}})^2 + \beta F_{\text{info}}^2 + \gamma R(g) + \lambda \mathcal{C}(S_{\text{ent}}, F_{\text{info}})
🔬 Key Simulations
1. Black Hole Analog (5-qubit)
Core: Low-noise entangled qubits (stable "singularity")

Horizon: High-noise boundary (entropy gradient → Hawking radiation)

Results:

python
{'11111': 449, '00000': 438, '00001': 18, '11110': 15, ...} 
# ^-- Interior    ^-- Radiation
2. Observer Effect
Protected qubits reduce global decay by 2.3× vs. uncontrolled systems.

3. Entropy Area Law
Reproduced Bekenstein-Hawking scaling:

math
S_{\text{BH}} \approx \sum_{\text{boundary}} \nabla S_{\text{ent}}
🛠️ Repository Structure
/rrgm-core/           # Theory derivations (LaTeX, PDFs)  
/qiskit-sims/         # Jupyter notebooks for all simulations  
  ├── black_hole.py   # 5-qubit Hawking radiation sim  
  └── observer.py     # Entropy resistance tests  
/figures/             # Histograms & visualizations  
🚀 Quick Start
Install Qiskit:

bash
pip install qiskit qiskit-aer
Run a simulation:

python
python qiskit-sims/black_hole.py
📜 Citation (Non-Journal)
bibtex
@software{Rozon_RRGM_2025,
  author = {Rozon, Daniel and Luna and Delta},
  title = {Rozon Recursive Gravity Model},
  url = {https://github.com/dzoron,
  year = {2025}
}
