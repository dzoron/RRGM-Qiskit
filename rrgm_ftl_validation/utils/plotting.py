"""
RRGM FTL Validation Toolkit - Plotting Utilities

Publication-quality visualization functions (300 DPI) with exact RRGM notation
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec
from typing import Dict, List, Tuple, Optional, Any
import os

from .constants import SimulationDefaults


def setup_publication_style():
    """Configure matplotlib for publication-quality figures"""
    rcParams['figure.dpi'] = SimulationDefaults.dpi
    rcParams['savefig.dpi'] = SimulationDefaults.dpi
    rcParams['font.size'] = 11
    rcParams['font.family'] = 'serif'
    rcParams['font.serif'] = ['Computer Modern Roman', 'Times New Roman', 'DejaVu Serif']
    rcParams['axes.labelsize'] = 12
    rcParams['axes.titlesize'] = 13
    rcParams['xtick.labelsize'] = 10
    rcParams['ytick.labelsize'] = 10
    rcParams['legend.fontsize'] = 10
    rcParams['figure.titlesize'] = 14
    rcParams['text.usetex'] = False  # Set to True if LaTeX is available
    rcParams['axes.grid'] = True
    rcParams['grid.alpha'] = 0.3
    rcParams['lines.linewidth'] = 2


def save_figure(fig, filename: str, output_dir: str = 'outputs/figures',
                tight: bool = True, transparent: bool = False):
    """
    Save figure with publication settings

    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        Figure to save
    filename : str
        Output filename (with extension)
    output_dir : str
        Output directory path
    tight : bool
        Use tight_layout
    transparent : bool
        Transparent background
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    if tight:
        fig.tight_layout()

    fig.savefig(filepath, dpi=SimulationDefaults.dpi,
                bbox_inches='tight', transparent=transparent)
    print(f"✓ Saved: {filepath}")


def plot_coherence_decay(times: np.ndarray,
                        coherence_data: Dict[str, np.ndarray],
                        title: str = "Qubit Coherence Decay: RIF-Protected vs Unprotected",
                        save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot coherence survival curves for different RIF configurations

    Parameters:
    -----------
    times : array
        Time points (seconds)
    coherence_data : dict
        Dictionary mapping labels to coherence arrays
    title : str
        Plot title
    save_path : str, optional
        If provided, save figure to this path

    Returns:
    --------
    fig : matplotlib.figure.Figure
    """
    setup_publication_style()

    fig, ax = plt.subplots(figsize=SimulationDefaults.figsize)

    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(coherence_data)))

    for (label, coherence), color in zip(coherence_data.items(), colors):
        ax.plot(times * 1e9, coherence, label=label, linewidth=2.5, color=color)

    ax.set_xlabel('Time (ns)', fontsize=12)
    ax.set_ylabel('Coherence $|\\rho_{01}|$', fontsize=12)
    ax.set_title(title, fontsize=13, pad=15)
    ax.legend(loc='best', framealpha=0.9)
    ax.set_ylim([0, 1.05])
    ax.grid(True, alpha=0.3)

    if save_path:
        save_figure(fig, save_path)

    return fig


def plot_RPG_profiles(x: np.ndarray,
                     profiles: Dict[str, np.ndarray],
                     title: str = "RPG Field Profiles $\\chi(x)$",
                     xlabel: str = "Position (arb. units)",
                     save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot RPG field spatial profiles

    Parameters:
    -----------
    x : array
        Spatial coordinate
    profiles : dict
        Dictionary mapping labels to χ(x) arrays
    title : str
        Plot title
    xlabel : str
        X-axis label
    save_path : str, optional
        Save path

    Returns:
    --------
    fig : matplotlib.figure.Figure
    """
    setup_publication_style()

    fig, ax = plt.subplots(figsize=SimulationDefaults.figsize)

    colors = plt.cm.plasma(np.linspace(0.2, 0.9, len(profiles)))

    for (label, profile), color in zip(profiles.items(), colors):
        ax.plot(x, profile, label=label, linewidth=2.5, color=color)

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel('RPG Field Strength $\\chi$', fontsize=12)
    ax.set_title(title, fontsize=13, pad=15)
    ax.legend(loc='best', framealpha=0.9)
    ax.set_ylim([0, 1.05])
    ax.grid(True, alpha=0.3)

    if save_path:
        save_figure(fig, save_path)

    return fig


def plot_parameter_heatmap(x: np.ndarray, y: np.ndarray, Z: np.ndarray,
                          xlabel: str, ylabel: str, zlabel: str,
                          title: str,
                          log_scale: bool = False,
                          contours: bool = True,
                          save_path: Optional[str] = None) -> plt.Figure:
    """
    Create parameter space heatmap

    Parameters:
    -----------
    x, y : array
        Parameter grid coordinates
    Z : 2D array
        Values to plot
    xlabel, ylabel, zlabel : str
        Axis labels
    title : str
        Plot title
    log_scale : bool
        Use log scale for color
    contours : bool
        Add contour lines
    save_path : str, optional
        Save path

    Returns:
    --------
    fig : matplotlib.figure.Figure
    """
    setup_publication_style()

    fig, ax = plt.subplots(figsize=(10, 8))

    if log_scale:
        Z_plot = np.log10(np.clip(Z, 1e-10, None))
        cbar_label = f'$\\log_{{10}}$({zlabel})'
    else:
        Z_plot = Z
        cbar_label = zlabel

    im = ax.pcolormesh(x, y, Z_plot, shading='auto', cmap='viridis')

    if contours:
        contour_levels = np.linspace(Z_plot.min(), Z_plot.max(), 8)
        cs = ax.contour(x, y, Z_plot, levels=contour_levels,
                       colors='white', alpha=0.4, linewidths=1)
        ax.clabel(cs, inline=True, fontsize=8)

    cbar = plt.colorbar(im, ax=ax, label=cbar_label)
    cbar.ax.tick_params(labelsize=10)

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=13, pad=15)

    if save_path:
        save_figure(fig, save_path)

    return fig


def plot_FTL_requirements(λ_ratios: np.ndarray,
                         distances: np.ndarray,
                         transit_times: np.ndarray,
                         v_ratio_grid: np.ndarray,
                         save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot FTL-equivalent velocity requirements

    Parameters:
    -----------
    λ_ratios : array
        λ_int/λ_ext ratios
    distances : array
        Transit distances (meters)
    transit_times : array
        External transit times (seconds)
    v_ratio_grid : 2D array
        v_eff/c ratios
    save_path : str, optional
        Save path

    Returns:
    --------
    fig : matplotlib.figure.Figure
    """
    setup_publication_style()

    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Main heatmap: v_eff/c vs λ_ratio and distance
    ax1 = fig.add_subplot(gs[0, :])
    im1 = ax1.pcolormesh(distances, λ_ratios, v_ratio_grid,
                         shading='auto', cmap='RdYlGn_r', vmin=0, vmax=2)
    contours = ax1.contour(distances, λ_ratios, v_ratio_grid,
                          levels=[0.5, 1.0, 1.5, 2.0],
                          colors='black', linewidths=1.5)
    ax1.clabel(contours, inline=True, fontsize=9, fmt='%.1f')

    # Mark FTL boundary (v_eff/c = 1)
    ax1.contour(distances, λ_ratios, v_ratio_grid,
               levels=[1.0], colors='red', linewidths=3,
               linestyles='--', label='FTL boundary')

    ax1.set_xlabel('Transit Distance (m)', fontsize=12)
    ax1.set_ylabel('$\\lambda_{int}/\\lambda_{ext}$ Ratio', fontsize=12)
    ax1.set_title('FTL-Equivalent Velocity Requirements ($v_{eff}/c$)',
                 fontsize=13, pad=15)
    ax1.set_yscale('log')
    cbar1 = plt.colorbar(im1, ax=ax1, label='$v_{eff}/c$')

    # Subplot 2: v_eff/c vs λ_ratio for fixed distance
    ax2 = fig.add_subplot(gs[1, 0])
    mid_dist_idx = len(distances) // 2
    ax2.plot(λ_ratios, v_ratio_grid[:, mid_dist_idx],
            linewidth=2.5, color='darkblue')
    ax2.axhline(y=1.0, color='red', linestyle='--', linewidth=2,
               label='$c$ boundary')
    ax2.set_xlabel('$\\lambda_{int}/\\lambda_{ext}$', fontsize=11)
    ax2.set_ylabel('$v_{eff}/c$', fontsize=11)
    ax2.set_title(f'Distance = {distances[mid_dist_idx]:.1e} m', fontsize=11)
    ax2.set_xscale('log')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Subplot 3: Required λ_ratio for FTL vs distance
    ax3 = fig.add_subplot(gs[1, 1])
    # Find minimum λ_ratio for v_eff/c > 1 at each distance
    ftl_threshold = []
    for i, d in enumerate(distances):
        ftl_indices = np.where(v_ratio_grid[:, i] > 1.0)[0]
        if len(ftl_indices) > 0:
            ftl_threshold.append(λ_ratios[ftl_indices[0]])
        else:
            ftl_threshold.append(np.nan)

    ax3.plot(distances, ftl_threshold, linewidth=2.5, color='darkred')
    ax3.set_xlabel('Transit Distance (m)', fontsize=11)
    ax3.set_ylabel('Minimum $\\lambda_{int}/\\lambda_{ext}$ for FTL',
                  fontsize=11)
    ax3.set_title('FTL Threshold Requirements', fontsize=11)
    ax3.set_yscale('log')
    ax3.grid(True, alpha=0.3)

    if save_path:
        save_figure(fig, save_path)

    return fig


def plot_falsification_comparison(experimental_data: Dict[str, Any],
                                  rrgm_predictions: Dict[str, Any],
                                  control_predictions: Dict[str, Any],
                                  title: str = "Falsification Test: RRGM vs Control",
                                  save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot experimental protocol comparison for falsification tests

    Parameters:
    -----------
    experimental_data : dict
        Experimental measurements (x, y, errors)
    rrgm_predictions : dict
        RRGM model predictions
    control_predictions : dict
        Standard physics predictions
    title : str
        Plot title
    save_path : str, optional
        Save path

    Returns:
    --------
    fig : matplotlib.figure.Figure
    """
    setup_publication_style()

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left panel: Direct comparison
    ax1 = axes[0]
    x_exp = experimental_data['x']
    y_exp = experimental_data['y']
    yerr_exp = experimental_data.get('yerr', None)

    ax1.errorbar(x_exp, y_exp, yerr=yerr_exp, fmt='o', markersize=8,
                label='Experimental Data', color='black', capsize=5)

    x_pred = rrgm_predictions['x']
    ax1.plot(x_pred, rrgm_predictions['y'], '--', linewidth=2.5,
            label='RRGM Prediction', color='blue')
    ax1.fill_between(x_pred,
                     rrgm_predictions['y'] - rrgm_predictions.get('uncertainty', 0),
                     rrgm_predictions['y'] + rrgm_predictions.get('uncertainty', 0),
                     alpha=0.3, color='blue')

    ax1.plot(control_predictions['x'], control_predictions['y'], '-.',
            linewidth=2.5, label='Standard Physics', color='red')
    ax1.fill_between(control_predictions['x'],
                     control_predictions['y'] - control_predictions.get('uncertainty', 0),
                     control_predictions['y'] + control_predictions.get('uncertainty', 0),
                     alpha=0.3, color='red')

    ax1.set_xlabel(experimental_data.get('xlabel', 'Parameter'), fontsize=12)
    ax1.set_ylabel(experimental_data.get('ylabel', 'Observable'), fontsize=12)
    ax1.set_title('Model Comparison', fontsize=12)
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)

    # Right panel: Residuals
    ax2 = axes[1]
    residuals_rrgm = y_exp - np.interp(x_exp, x_pred, rrgm_predictions['y'])
    residuals_control = y_exp - np.interp(x_exp, control_predictions['x'],
                                          control_predictions['y'])

    ax2.errorbar(x_exp, residuals_rrgm, yerr=yerr_exp, fmt='o', markersize=8,
                label='RRGM Residuals', color='blue', capsize=5)
    ax2.errorbar(x_exp, residuals_control, yerr=yerr_exp, fmt='s', markersize=8,
                label='Control Residuals', color='red', capsize=5, alpha=0.7)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)

    ax2.set_xlabel(experimental_data.get('xlabel', 'Parameter'), fontsize=12)
    ax2.set_ylabel('Residuals', fontsize=12)
    ax2.set_title('Residual Analysis', fontsize=12)
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)

    fig.suptitle(title, fontsize=14, y=1.02)

    if save_path:
        save_figure(fig, save_path)

    return fig


def plot_multi_panel_summary(results: Dict[str, Any],
                            save_path: Optional[str] = None) -> plt.Figure:
    """
    Create comprehensive multi-panel summary figure

    Parameters:
    -----------
    results : dict
        Complete results from all modules
    save_path : str, optional
        Save path

    Returns:
    --------
    fig : matplotlib.figure.Figure
    """
    setup_publication_style()

    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3)

    # Panel 1: Coherence decay
    ax1 = fig.add_subplot(gs[0, 0])
    if 'coherence' in results:
        times = results['coherence']['times']
        for label, data in results['coherence']['data'].items():
            ax1.plot(times * 1e9, data, label=label, linewidth=2)
    ax1.set_xlabel('Time (ns)', fontsize=11)
    ax1.set_ylabel('Coherence', fontsize=11)
    ax1.set_title('Module 1: RIF Coherence Protection', fontsize=12)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Panel 2: RPG profiles
    ax2 = fig.add_subplot(gs[0, 1])
    if 'rpg_profiles' in results:
        x = results['rpg_profiles']['x']
        for label, profile in results['rpg_profiles']['profiles'].items():
            ax2.plot(x, profile, label=label, linewidth=2)
    ax2.set_xlabel('Position', fontsize=11)
    ax2.set_ylabel('$\\chi(x)$', fontsize=11)
    ax2.set_title('RPG Field Profiles', fontsize=12)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    # Panel 3: Parameter space heatmap
    ax3 = fig.add_subplot(gs[1, :])
    if 'parameter_space' in results:
        ps = results['parameter_space']
        im = ax3.pcolormesh(ps['x'], ps['y'], ps['z'],
                           shading='auto', cmap='viridis')
        plt.colorbar(im, ax=ax3, label=ps.get('zlabel', 'Value'))
    ax3.set_xlabel(ps.get('xlabel', 'Parameter 1') if 'parameter_space' in results else '', fontsize=11)
    ax3.set_ylabel(ps.get('ylabel', 'Parameter 2') if 'parameter_space' in results else '', fontsize=11)
    ax3.set_title('Module 2: Parameter Space Exploration', fontsize=12)

    # Panel 4: FTL requirements
    ax4 = fig.add_subplot(gs[2, 0])
    if 'ftl_requirements' in results:
        ftl = results['ftl_requirements']
        ax4.plot(ftl['x'], ftl['y'], linewidth=2.5, color='darkred')
        ax4.axhline(y=1.0, color='black', linestyle='--', linewidth=1.5)
    ax4.set_xlabel('$\\lambda_{int}/\\lambda_{ext}$', fontsize=11)
    ax4.set_ylabel('$v_{eff}/c$', fontsize=11)
    ax4.set_title('FTL Velocity Requirements', fontsize=12)
    ax4.set_xscale('log')
    ax4.grid(True, alpha=0.3)

    # Panel 5: Falsification metrics
    ax5 = fig.add_subplot(gs[2, 1])
    if 'falsification' in results:
        fals = results['falsification']
        categories = list(fals.keys())
        values = list(fals.values())
        colors = ['green' if v > 0 else 'red' for v in values]
        ax5.barh(categories, values, color=colors, alpha=0.7)
        ax5.axvline(x=0, color='black', linewidth=1.5)
    ax5.set_xlabel('Deviation from Control (σ)', fontsize=11)
    ax5.set_title('Module 3: Falsification Metrics', fontsize=12)
    ax5.grid(True, alpha=0.3, axis='x')

    fig.suptitle('RRGM FTL Validation Toolkit - Comprehensive Summary',
                fontsize=15, y=0.995)

    if save_path:
        save_figure(fig, save_path)

    return fig


# Export all plotting functions
__all__ = [
    'setup_publication_style',
    'save_figure',
    'plot_coherence_decay',
    'plot_RPG_profiles',
    'plot_parameter_heatmap',
    'plot_FTL_requirements',
    'plot_falsification_comparison',
    'plot_multi_panel_summary',
]
