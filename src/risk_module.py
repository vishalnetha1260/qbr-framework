"""Layer 5: Risk and Quantum-Safe Resilience.

Mosca timing analysis: a system is exposed if
    shelf_life (x) + migration_time (y)  >  time_to_CRQC (z),
under harvest-now-decrypt-later logic. Produces a prioritized migration
queue and exposure analysis across z assumptions.
"""
import numpy as np
import pandas as pd

def mosca_analysis(inv: pd.DataFrame, z_years: float = 12.0) -> pd.DataFrame:
    out = inv.copy()
    out["mosca_lhs_years"] = out.shelf_life_years + out.migration_years
    out["exposed"] = out.mosca_lhs_years > z_years
    out["margin_years"] = (z_years - out.mosca_lhs_years).round(1)
    out["priority_score"] = (out.sensitivity * np.maximum(0, -out.margin_years)).round(2)
    return out.sort_values("priority_score", ascending=False).reset_index(drop=True)

def exposure_curve(inv: pd.DataFrame, z_grid=None) -> pd.DataFrame:
    """Share of systems (and sensitivity-weighted share) exposed vs z."""
    if z_grid is None:
        z_grid = np.arange(2, 31)
    rows = []
    for z in z_grid:
        lhs = inv.shelf_life_years + inv.migration_years
        exp_mask = lhs > z
        rows.append(dict(
            z_years=int(z),
            pct_exposed=round(100 * exp_mask.mean(), 1),
            weighted_pct_exposed=round(100 * inv.sensitivity[exp_mask].sum() / inv.sensitivity.sum(), 1),
        ))
    return pd.DataFrame(rows)
