# RRGM FTL Validation Toolkit - Quick Start Guide

## Installation (2 minutes)

```bash
cd rrgm_ftl_validation

# Install dependencies
pip install -r requirements.txt
```

## Run the Toolkit (30 seconds - 5 minutes)

### Quick Demo (30 seconds)
```bash
python run_toolkit.py --quick
```

### Full Validation Suite (2-5 minutes)
```bash
python run_toolkit.py --all
```

### Run Individual Modules
```bash
python run_toolkit.py --module1  # RIF Simulation Framework
python run_toolkit.py --module2  # Parameter Space Explorer
python run_toolkit.py --module3  # Falsification Test Suite
```

## View Results

After running, check these directories:

```
outputs/
├── figures/              # 7 publication-quality PNG figures (300 DPI)
├── data/                 # 5 JSON/CSV data files
└── protocols/            # 4 detailed experimental protocols (Markdown)
```

## What You'll Get

### Module 1: RIF Simulation Framework
- **Figures**:
  - `module1_coherence_comparison.png` - Coherence decay with different χ values
  - `module1_decay_scan.png` - Final coherence vs λ_int/λ_ext ratio
- **Data**: `module1_results.json` - Complete simulation results

### Module 2: Parameter Space Explorer
- **Figures**:
  - `module2_ftl_requirements.png` - Multi-panel FTL velocity requirements
  - `module2_energy_costs.png` - RIF maintenance energy heatmap
  - `module2_collapse_boundaries.png` - Survival probability boundaries
- **Data**:
  - `module2_results.json` - Complete analysis results
  - `module2_requirement_table.csv` - FTL scenario requirements table

### Module 3: Falsification Test Suite
- **Figures**:
  - `module3_P1_coherence_timing_comparison.png` - Protocol 1 predictions
  - `module3_P2_entanglement_range_comparison.png` - Protocol 2 predictions
  - (+ 2 more in full mode)
- **Data**:
  - `module3_results.json` - Simulation results for all protocols
  - `module3_summary.csv` - Falsification summary table
- **Protocols**: 4 detailed experimental protocol documents

## Example Output

```
VALIDATION TOOLKIT COMPLETE
======================================================================

Execution time: 5.4 seconds
End time: 2025-11-17 18:36:48

All outputs saved to:
  - Figures: outputs/figures/
  - Data: outputs/data/
  - Protocols: outputs/protocols/

======================================================================
Next steps:
  1. Review figures in outputs/figures/
  2. Examine data files in outputs/data/
  3. Read experimental protocols in outputs/protocols/
  4. Incorporate into RRGM FTL paper
======================================================================
```

## Customization

See `README.md` for advanced usage, including:
- Custom parameter configurations
- Modifying simulation parameters
- Creating new experimental protocols
- Extending the toolkit

## Need Help?

- Full documentation: `README.md`
- Module documentation: See docstrings in `modules/*.py`
- Contact: Daniel Rozon

---

**Ready in 2 minutes. Publication-ready outputs in 5 minutes.**
