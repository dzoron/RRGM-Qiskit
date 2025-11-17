"""
RRGM FTL Validation Toolkit - Utilities Package
"""

from .constants import (
    PhysicalConstants,
    RRGMParameters,
    SimulationDefaults,
    RPG_field_profile,
    Omega_gate,
    effective_decay_rate,
    FTL_effective_velocity,
    get_default_config,
)

from .plotting import (
    setup_publication_style,
    save_figure,
    plot_coherence_decay,
    plot_RPG_profiles,
    plot_parameter_heatmap,
    plot_FTL_requirements,
    plot_falsification_comparison,
    plot_multi_panel_summary,
)

__all__ = [
    # Constants
    'PhysicalConstants',
    'RRGMParameters',
    'SimulationDefaults',
    'RPG_field_profile',
    'Omega_gate',
    'effective_decay_rate',
    'FTL_effective_velocity',
    'get_default_config',
    # Plotting
    'setup_publication_style',
    'save_figure',
    'plot_coherence_decay',
    'plot_RPG_profiles',
    'plot_parameter_heatmap',
    'plot_FTL_requirements',
    'plot_falsification_comparison',
    'plot_multi_panel_summary',
]
