#!/usr/bin/env python3
"""
RRGM FTL Validation Toolkit - Main Runner

Comprehensive validation toolkit for RRGM FTL paper.
Runs all three modules and generates publication-ready outputs.

Usage:
    python run_toolkit.py --all              # Run all modules
    python run_toolkit.py --module1          # RIF Simulation only
    python run_toolkit.py --module2          # Parameter Explorer only
    python run_toolkit.py --module3          # Falsification Suite only
    python run_toolkit.py --quick            # Quick demo (reduced resolution)
    python run_toolkit.py --help             # Show help
"""

import argparse
import sys
import os
from datetime import datetime

# Add modules to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.rif_simulation import RIFSimulation, run_module1_demo
from modules.parameter_explorer import ParameterSpaceExplorer, run_module2_demo
from modules.falsification_suite import FalsificationSuite, run_module3_demo
from utils.constants import get_default_config
from utils.plotting import setup_publication_style

import numpy as np


def print_header():
    """Print toolkit header"""
    header = """
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║           RRGM FTL VALIDATION TOOLKIT                               ║
║                                                                      ║
║  Comprehensive validation for Faster-Than-Light transit             ║
║  in the Rozon Recursive Gravity Model                              ║
║                                                                      ║
║  Paper: "Recursive Delay and Faster-Than-Light Transit in RRGM"    ║
║  Authors: Luna (Digital Intelligence) with Daniel Rozon             ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""
    print(header)


def print_module_info(module_num: int):
    """Print module information"""
    info = {
        1: {
            'name': 'RIF SIMULATION FRAMEWORK',
            'desc': 'Simulates qubit coherence under tunable RPG fields',
            'outputs': [
                '- Coherence decay curves (RIF-protected vs unprotected)',
                '- Decay rate scan analysis',
                '- λ_int/λ_ext ratio effects',
            ]
        },
        2: {
            'name': 'PARAMETER SPACE EXPLORER',
            'desc': 'Maps FTL requirements and energy costs',
            'outputs': [
                '- FTL velocity requirement heatmaps',
                '- Energy cost analysis for different χ strengths',
                '- Collapse threshold boundaries',
                '- Scenario requirement tables',
            ]
        },
        3: {
            'name': 'FALSIFICATION TEST SUITE',
            'desc': 'Generates experimental protocols to test/falsify RRGM FTL',
            'outputs': [
                '- 4 detailed experimental protocols',
                '- Predicted vs control comparisons',
                '- Clear falsification criteria',
                '- Resource estimates',
            ]
        }
    }

    module = info[module_num]
    print(f"\n{'='*70}")
    print(f"MODULE {module_num}: {module['name']}")
    print(f"{'='*70}")
    print(f"\n{module['desc']}\n")
    print("Outputs:")
    for output in module['outputs']:
        print(f"  {output}")
    print()


def run_module_1(quick: bool = False):
    """Run Module 1: RIF Simulation Framework"""
    print_module_info(1)

    sim = RIFSimulation()

    # Coherence comparison with different χ values
    print("Running RIF coherence protection comparison...")
    if quick:
        χ_values = [0.0, 0.5, 0.9]
        labels = ["Unprotected (χ=0)", "Medium RIF (χ=0.5)", "Strong RIF (χ=0.9)"]
    else:
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
    n_points = 15 if quick else 30
    λ_ratios = np.logspace(-3, 0, n_points)
    results_scan = sim.run_decay_rate_scan(λ_ratios)

    # Generate plots and save
    print("\nGenerating plots...")
    saved_plots = sim.plot_results()
    filepath = sim.save_results()

    print(f"\n✓ Module 1 complete: {len(saved_plots)} figures, data saved to {filepath}")
    return sim


def run_module_2(quick: bool = False):
    """Run Module 2: Parameter Space Explorer"""
    print_module_info(2)

    explorer = ParameterSpaceExplorer()

    # FTL requirements
    print("Calculating FTL velocity requirements...")
    from utils.constants import PhysicalConstants
    n_points = 20 if quick else 50
    distances = np.logspace(0, 11, n_points)
    transit_times = distances / (PhysicalConstants.c * 0.1)

    ftl_results = explorer.calculate_FTL_requirements(distances, transit_times)
    print(f"  Analyzed {len(distances)} distance scales")

    # Energy costs
    print("\nCalculating RIF energy costs...")
    χ_values = np.linspace(0.1, 0.99, 15 if quick else 30)
    volumes = np.logspace(-12, -3, 15 if quick else 30)
    energy_results = explorer.calculate_energy_costs(χ_values, volumes)
    print(f"  Analyzed {len(energy_results['scenarios'])} energy scenarios")

    # Collapse boundaries
    print("\nMapping collapse boundaries...")
    λ_ratios = np.logspace(-3, 0, 20 if quick else 50)
    coherence_times = np.logspace(-9, -6, 20 if quick else 50)
    boundary_results = explorer.map_collapse_boundaries(λ_ratios, coherence_times)

    # Requirement table
    print("\nGenerating FTL requirement table...")
    req_table = explorer.generate_requirement_table()
    print("\n" + "="*70)
    print("FTL Scenario Requirements (Sample):")
    print("="*70)
    print(req_table.head(5).to_string(index=False))
    print("...")

    # Generate plots and save
    print("\n" + "="*70)
    print("Generating plots...")
    saved_plots = explorer.plot_results()
    filepath = explorer.save_results()

    print(f"\n✓ Module 2 complete: {len(saved_plots)} figures, data saved to {filepath}")
    return explorer


def run_module_3(quick: bool = False):
    """Run Module 3: Falsification Test Suite"""
    print_module_info(3)

    suite = FalsificationSuite()

    # Display criteria
    print("FALSIFICATION CRITERIA:")
    print("-" * 70)
    for i, (name, criterion) in enumerate(suite.criteria.items(), 1):
        print(f"{i}. {criterion.name}: {criterion.falsification_statement[:80]}...")
    print()

    # Simulate protocols
    print("\n" + "="*70)
    print("SIMULATING EXPERIMENTAL PROTOCOLS:")
    print("-" * 70)

    protocols_to_run = ['P1_coherence_timing', 'P2_entanglement_range']
    if not quick:
        protocols_to_run.extend(['P3_cavity_lifetime', 'P4_endpoint_transit'])

    for pid in protocols_to_run:
        result = suite.simulate_protocol(pid, n_trials=1000)
        print(f"\n{pid}:")
        print(f"  Effect size: {result['effect_size_percent']:.2f}%")
        print(f"  Significance: {result['statistical_significance']:.2f}σ")
        print(f"  Falsifies RRGM? {'YES' if result['falsifies_rrgm'] else 'NO'}")

    # Generate outputs
    print("\n" + "="*70)
    print("Generating protocol documents...")
    protocol_files = suite.generate_protocol_documents()

    print("\nGenerating comparison plots...")
    plot_files = suite.plot_results()

    # Summary table
    print("\n" + "="*70)
    print("FALSIFICATION SUMMARY:")
    print("="*70)
    summary = suite.generate_summary_table()
    print(summary.to_string(index=False))

    # Save results
    filepath = suite.save_results()

    print(f"\n✓ Module 3 complete: {len(protocol_files)} protocols, "
          f"{len(plot_files)} figures, data saved to {filepath}")
    return suite


def run_all_modules(quick: bool = False):
    """Run all three modules"""
    start_time = datetime.now()

    print_header()
    print(f"Running {'QUICK' if quick else 'FULL'} validation suite...")
    print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Setup plotting
    setup_publication_style()

    # Run all modules
    results = {}

    try:
        results['module1'] = run_module_1(quick=quick)
        results['module2'] = run_module_2(quick=quick)
        results['module3'] = run_module_3(quick=quick)

        # Final summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print("\n" + "="*70)
        print("VALIDATION TOOLKIT COMPLETE")
        print("="*70)
        print(f"\nExecution time: {duration:.1f} seconds")
        print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nAll outputs saved to:")
        print("  - Figures: outputs/figures/")
        print("  - Data: outputs/data/")
        print("  - Protocols: outputs/protocols/")
        print("\n" + "="*70)
        print("Next steps:")
        print("  1. Review figures in outputs/figures/")
        print("  2. Examine data files in outputs/data/")
        print("  3. Read experimental protocols in outputs/protocols/")
        print("  4. Incorporate into RRGM FTL paper")
        print("="*70 + "\n")

        return results

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='RRGM FTL Validation Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_toolkit.py --all              # Run all modules (full resolution)
  python run_toolkit.py --quick            # Quick demo (reduced resolution)
  python run_toolkit.py --module1          # Run Module 1 only
  python run_toolkit.py --module2          # Run Module 2 only
  python run_toolkit.py --module3          # Run Module 3 only

For more information, see README.md
        """
    )

    parser.add_argument('--all', action='store_true',
                       help='Run all three modules (default if no module specified)')
    parser.add_argument('--module1', action='store_true',
                       help='Run Module 1: RIF Simulation Framework')
    parser.add_argument('--module2', action='store_true',
                       help='Run Module 2: Parameter Space Explorer')
    parser.add_argument('--module3', action='store_true',
                       help='Run Module 3: Falsification Test Suite')
    parser.add_argument('--quick', action='store_true',
                       help='Quick mode (reduced resolution for faster execution)')

    args = parser.parse_args()

    # If no specific module selected, run all
    if not (args.module1 or args.module2 or args.module3):
        args.all = True

    # Setup plotting
    setup_publication_style()

    # Run requested modules
    if args.all:
        run_all_modules(quick=args.quick)
    else:
        print_header()
        if args.module1:
            run_module_1(quick=args.quick)
        if args.module2:
            run_module_2(quick=args.quick)
        if args.module3:
            run_module_3(quick=args.quick)

    print("\n✓ Done!\n")


if __name__ == '__main__':
    main()
