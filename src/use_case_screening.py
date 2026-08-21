"""Layer 2: Use-Case and Value Analytics.

Prescriptive screening: ranks candidate problems by quantum amenability vs
near-term feasibility, producing a scored portfolio with explicit go / pilot /
no-go rationales (decision-first, technology-second).
"""
import pandas as pd

WEIGHTS = {
    "combinatorial_structure": 0.25, "simulation_content": 0.10,
    "optimization_criticality": 0.20, "data_readiness": 0.15,
    "near_term_feasibility": 0.10, "decision_value_potential": 0.20,
}

def screen_use_cases(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["amenability_score"] = sum(out[k] * w for k, w in WEIGHTS.items()).round(3)
    def decide(r):
        if r.amenability_score >= 0.65 and r.near_term_feasibility >= 0.5:
            return "GO (pilot now)"
        if r.amenability_score >= 0.55:
            return "PILOT (quantum-inspired first)"
        return "NO-GO (harden classical pipeline)"
    out["recommendation"] = out.apply(decide, axis=1)
    out["rationale"] = out.apply(
        lambda r: f"score={r.amenability_score:.2f}, feasibility={r.near_term_feasibility:.2f}", axis=1)
    return out.sort_values("amenability_score", ascending=False).reset_index(drop=True)
