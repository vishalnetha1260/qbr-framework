"""Layer 6: Strategic Decision Intelligence.

Implements Equation (1) of the article:
    E[V_i] = sum_s  pi_s * ( p_{i,s} * dV_{i,s} - C_{i,s} + L_{i,s} )
plus Monte Carlo sensitivity over scenario probabilities and a decomposition
showing when learning/option value L dominates the near-term case.
"""
import numpy as np
import pandas as pd

def expected_strategic_value(df: pd.DataFrame, scenarios: dict) -> pd.DataFrame:
    """Compute E[V_i] per initiative and the L-share of total value."""
    rows = []
    for init, g in df.groupby("initiative", sort=False):
        ev, ev_learning = 0.0, 0.0
        for _, r in g.iterrows():
            pi = scenarios[r.scenario]
            ev += pi * (r.p_advantage * r.delta_value - r.cost + r.learning_value)
            ev_learning += pi * r.learning_value
        rows.append(dict(initiative=init, expected_value=round(ev, 3),
                         learning_component=round(ev_learning, 3),
                         learning_share_pct=round(100 * ev_learning / ev, 1) if ev > 0 else np.nan))
    out = pd.DataFrame(rows).sort_values("expected_value", ascending=False).reset_index(drop=True)
    out["rank"] = out.index + 1
    def rec(v):
        if v >= 1.0: return "SCALE / commit"
        if v >= 0.3: return "PILOT (staged option)"
        if v >= 0.0: return "PARTNER or WAIT"
        return "DIVEST / defer"
    out["recommendation"] = out.expected_value.map(rec)
    return out

def scenario_sensitivity(df: pd.DataFrame, scenarios: dict, n_draws=2000, seed=7):
    """Monte Carlo over Dirichlet-perturbed scenario probabilities:
    how robust is each initiative's ranking to scenario uncertainty?"""
    rng = np.random.default_rng(seed)
    names = list(scenarios)
    base = np.array([scenarios[s] for s in names])
    inits = df.initiative.unique()
    evs = {i: [] for i in inits}
    for _ in range(n_draws):
        probs = rng.dirichlet(base * 30)  # concentration around base beliefs
        sdict = dict(zip(names, probs))
        res = expected_strategic_value(df, sdict)
        for _, r in res.iterrows():
            evs[r.initiative].append(r.expected_value)
    return pd.DataFrame({
        "initiative": inits,
        "ev_mean": [np.mean(evs[i]) for i in inits],
        "ev_p05": [np.percentile(evs[i], 5) for i in inits],
        "ev_p95": [np.percentile(evs[i], 95) for i in inits],
        "prob_positive": [np.mean(np.array(evs[i]) > 0) for i in inits],
    }).round(3).sort_values("ev_mean", ascending=False).reset_index(drop=True)
