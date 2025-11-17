"""
RRGM FTL Validation Toolkit - Physical and Simulation Constants

This module defines the exact notation and constants from the RRGM FTL paper:
- χ(x): Recursive Protocol Governor (RPG) field
- λ_int: Internal decay rate within RIF
- λ_ext: External decay rate (default Ω)
- Ω: Universal gate function
- M_I: Identity mass/anchor
- E_S: Structural energy
"""

import numpy as np
from typing import Dict, Any

# Physical Constants (SI units where applicable)
class PhysicalConstants:
    """Physical constants for RRGM FTL calculations"""

    # Speed of light (m/s) - interpreted as structural propagation stability boundary
    c = 299792458.0

    # Planck constant (J⋅s)
    h = 6.62607015e-34
    hbar = h / (2 * np.pi)

    # Boltzmann constant (J/K)
    k_B = 1.380649e-23

    # Default time units (seconds)
    DEFAULT_TIME_UNIT = 1e-9  # nanoseconds

    # Default energy units (eV)
    DEFAULT_ENERGY_UNIT = 1.602176634e-19  # Joules per eV


class RRGMParameters:
    """Default RRGM-specific parameters for simulations"""

    # Default external decay rate (1/s) - represents default Ω behavior
    λ_ext_default = 1e9  # 1 GHz - typical quantum decoherence rate

    # RPG field strength range
    χ_min = 0.0  # No isolation
    χ_max = 1.0  # Maximum isolation

    # Internal-to-external decay ratio ranges for exploration
    λ_ratio_min = 1e-4  # Strong RIF protection
    λ_ratio_max = 1.0   # No protection

    # Identity-structure coupling coefficient (dimensionless)
    # E = M_I × E_S relationship
    coupling_coefficient = 1.0

    # Minimum identity seed (dimensionless) - photon limit
    ε_γ = 1e-6

    # Omega gate saturation (sigmoid parameters)
    Ω_midpoint = 0.5
    Ω_steepness = 10.0


class SimulationDefaults:
    """Default simulation parameters"""

    # Time parameters
    n_timesteps = 1000
    t_max = 100e-9  # 100 nanoseconds

    # Qubit simulation
    n_qubits_default = 5
    initial_coherence = 1.0

    # Parameter space resolution
    param_grid_resolution = 50

    # Figure output settings
    dpi = 300
    figsize = (10, 6)
    style = 'seaborn-v0_8-paper'

    # Random seed for reproducibility
    random_seed = 42


def RPG_field_profile(x: np.ndarray, center: float, width: float,
                      strength: float) -> np.ndarray:
    """
    Gaussian RPG field profile χ(x)

    Parameters:
    -----------
    x : array-like
        Spatial or parameter coordinate
    center : float
        Center of RPG field
    width : float
        Width of RPG field (standard deviation)
    strength : float
        Maximum χ value (0 to 1)

    Returns:
    --------
    χ : array-like
        RPG field values
    """
    return strength * np.exp(-0.5 * ((x - center) / width)**2)


def Omega_gate(recursive_flux: np.ndarray,
               midpoint: float = RRGMParameters.Ω_midpoint,
               steepness: float = RRGMParameters.Ω_steepness) -> np.ndarray:
    """
    Universal gate function Ω(D_0) - sigmoidal implementation

    Parameters:
    -----------
    recursive_flux : array-like
        Integrated recursive flux or activity measure
    midpoint : float
        Midpoint of sigmoid (default 0.5)
    steepness : float
        Steepness of sigmoid transition (default 10.0)

    Returns:
    --------
    Ω : array-like
        Gate values between 0 and 1
    """
    return 1.0 / (1.0 + np.exp(-steepness * (recursive_flux - midpoint)))


def effective_decay_rate(λ_ext: float, χ: float,
                         coupling_strength: float = 1.0) -> float:
    """
    Calculate effective internal decay rate given RPG field

    λ_int = λ_ext × (1 - χ)^coupling_strength

    Parameters:
    -----------
    λ_ext : float
        External decay rate
    χ : float
        RPG field strength (0 to 1)
    coupling_strength : float
        How strongly RPG suppresses decay (default 1.0)

    Returns:
    --------
    λ_int : float
        Effective internal decay rate
    """
    return λ_ext * (1 - χ)**coupling_strength


def FTL_effective_velocity(L: float, t_external: float,
                          λ_int: float, λ_ext: float,
                          c: float = PhysicalConstants.c) -> Dict[str, float]:
    """
    Calculate effective FTL velocity for RIF-mediated transit

    Parameters:
    -----------
    L : float
        Spatial separation (meters)
    t_external : float
        External time elapsed (seconds)
    λ_int : float
        Internal decay rate
    λ_ext : float
        External decay rate
    c : float
        Speed of light (default: PhysicalConstants.c)

    Returns:
    --------
    results : dict
        Dictionary with v_eff, v_eff/c ratio, and FTL indicator
    """
    v_eff = L / t_external
    v_ratio = v_eff / c
    is_FTL = v_eff > c

    # Recursive delay factor
    delay_factor = λ_ext / λ_int if λ_int > 0 else np.inf

    return {
        'v_effective': v_eff,
        'v_ratio_to_c': v_ratio,
        'is_FTL_equivalent': is_FTL,
        'recursive_delay_factor': delay_factor
    }


def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration for all simulations

    Returns:
    --------
    config : dict
        Complete configuration dictionary
    """
    return {
        'physical': {
            'c': PhysicalConstants.c,
            'hbar': PhysicalConstants.hbar,
            'k_B': PhysicalConstants.k_B,
        },
        'rrgm': {
            'λ_ext_default': RRGMParameters.λ_ext_default,
            'χ_range': (RRGMParameters.χ_min, RRGMParameters.χ_max),
            'λ_ratio_range': (RRGMParameters.λ_ratio_min, RRGMParameters.λ_ratio_max),
            'ε_γ': RRGMParameters.ε_γ,
        },
        'simulation': {
            'n_timesteps': SimulationDefaults.n_timesteps,
            't_max': SimulationDefaults.t_max,
            'n_qubits': SimulationDefaults.n_qubits_default,
            'dpi': SimulationDefaults.dpi,
            'figsize': SimulationDefaults.figsize,
            'random_seed': SimulationDefaults.random_seed,
        }
    }


# Export main components
__all__ = [
    'PhysicalConstants',
    'RRGMParameters',
    'SimulationDefaults',
    'RPG_field_profile',
    'Omega_gate',
    'effective_decay_rate',
    'FTL_effective_velocity',
    'get_default_config',
]
