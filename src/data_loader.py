"""Data loader: generates the reproducible illustrative datasets used by the
QBR companion simulations.

The parent article is conceptual; these datasets are synthetic but seeded and
documented, serving as an illustrative testbed for the framework's logic
(Layers 2, 3, 5, 6). No empirical claims are attached to them.
"""
import numpy as np
import pandas as pd

SEED = 42

USE_CASE_NAMES = [
    "Portfolio rebalancing optimization", "Loan collateral optimization",
    "Derivative pricing simulation", "Fraud pattern detection",
    "UAV mission route planning", "GPS-denied navigation filtering",
    "Supply-chain network design", "Workforce shift scheduling",
    "Molecular property screening", "Cyber alert triage optimization",
    "Data-center energy dispatch", "Insurance risk aggregation",
]

def load_use_case_portfolio(seed: int = SEED) -> pd.DataFrame:
    """Layer 2 testbed: candidate use cases scored on decision-first criteria."""
    rng = np.random.default_rng(seed)
    n = len(USE_CASE_NAMES)
    df = pd.DataFrame({
        "use_case": USE_CASE_NAMES,
        "combinatorial_structure": rng.uniform(0.2, 1.0, n).round(2),
        "simulation_content": rng.uniform(0.0, 1.0, n).round(2),
        "optimization_criticality": rng.uniform(0.3, 1.0, n).round(2),
        "data_readiness": rng.uniform(0.2, 1.0, n).round(2),
        "near_term_feasibility": rng.uniform(0.1, 0.9, n).round(2),
        "decision_value_potential": rng.uniform(0.3, 1.0, n).round(2),
    })
    return df

def load_asset_universe(n_assets: int = 20, seed: int = SEED):
    """Layer 3 testbed: mean returns and covariance for QUBO portfolio selection."""
    rng = np.random.default_rng(seed)
    mu = rng.uniform(0.02, 0.15, n_assets)                    # expected returns
    A = rng.normal(0, 0.05, (n_assets, n_assets))
    cov = A @ A.T + np.diag(rng.uniform(0.01, 0.04, n_assets))  # PSD covariance
    names = [f"A{i:02d}" for i in range(n_assets)]
    return names, mu, cov

def load_crypto_inventory(seed: int = SEED) -> pd.DataFrame:
    """Layer 5 testbed: systems with data shelf-life and migration times (years)."""
    rng = np.random.default_rng(seed)
    systems = [
        "Customer PII vault", "Payment switch", "Archived contracts",
        "IoT firmware signing", "VPN gateway", "HR records",
        "R&D data lake", "Public web TLS", "Backup archive", "M&A data room",
    ]
    n = len(systems)
    return pd.DataFrame({
        "system": systems,
        "shelf_life_years": rng.integers(1, 25, n),       # x: years data must stay secret
        "migration_years": rng.uniform(0.5, 8.0, n).round(1),  # y: time to migrate to PQC
        "sensitivity": rng.uniform(0.2, 1.0, n).round(2),
    })

def load_initiative_scenarios(seed: int = SEED):
    """Layer 6 testbed: initiatives and technology scenarios for Equation (1)."""
    initiatives = ["Pilot quantum-inspired optimizer", "Cloud QPU experiment",
                   "PQC migration program", "Quantum talent program", "Wait and monitor"]
    scenarios = {"Slow progress": 0.4, "Steady NISQ growth": 0.45, "Breakthrough": 0.15}
    rng = np.random.default_rng(seed)
    rows = []
    for i, init in enumerate(initiatives):
        for s in scenarios:
            rows.append({
                "initiative": init, "scenario": s,
                "p_advantage": rng.uniform(0.05, 0.7),
                "delta_value": rng.uniform(0.5, 5.0),   # $M incremental decision value
                "cost": rng.uniform(0.2, 2.0),          # $M cost
                "learning_value": rng.uniform(0.1, 1.5) # $M option/learning value
            })
    return pd.DataFrame(rows).round(3), scenarios
