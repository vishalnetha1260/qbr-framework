"""Layer 3: Quantum and Hybrid Computation (quantum-inspired mode).

Portfolio selection as a QUBO solved by simulated annealing (the canonical
quantum-inspired/annealing formulation), benchmarked against classical
baselines: random search, greedy, and exhaustive (exact) for small n.
This operationalizes the paper's claim that formulation skill (QUBO/penalty
design) is the transferable asset of the exercise layer.
"""
import itertools
import time
import numpy as np

def build_qubo(mu, cov, k, risk_aversion=2.0, penalty=4.0):
    """QUBO: maximize mu'x - q x'Cov x  s.t. sum(x)=k  (penalty-encoded)."""
    n = len(mu)
    Q = np.zeros((n, n))
    for i in range(n):
        Q[i, i] += -mu[i] + risk_aversion * cov[i, i] + penalty * (1 - 2 * k)
        for j in range(i + 1, n):
            Q[i, j] += 2 * risk_aversion * cov[i, j] + 2 * penalty
    return Q, penalty * k * k  # constant offset

def qubo_energy(Q, x):
    return float(x @ np.triu(Q) @ x)

def objective(mu, cov, x, risk_aversion=2.0):
    """True (unpenalized) objective: return - risk."""
    return float(mu @ x - risk_aversion * x @ cov @ x)

def simulated_annealing(Q, n, k, seed=0, n_sweeps=300, T0=0.05, Tf=1e-4):
    """Anneal on the QUBO energy using constraint-preserving swap moves
    (one selected asset out, one unselected in), the standard neighborhood
    for cardinality-constrained QUBO problems."""
    rng = np.random.default_rng(seed)
    x = np.zeros(n, dtype=int)
    x[rng.choice(n, k, replace=False)] = 1
    e = qubo_energy(Q, x)
    best_x, best_e = x.copy(), e
    for T in np.geomspace(T0, Tf, n_sweeps):
        for _ in range(n):
            ones = np.flatnonzero(x == 1); zeros = np.flatnonzero(x == 0)
            i, j = rng.choice(ones), rng.choice(zeros)
            x2 = x.copy(); x2[i], x2[j] = 0, 1
            e2 = qubo_energy(Q, x2)
            if e2 < e or rng.random() < np.exp(-(e2 - e) / T):
                x, e = x2, e2
                if e < best_e:
                    best_x, best_e = x.copy(), e
    return best_x, best_e

def greedy_select(mu, cov, k, risk_aversion=2.0):
    n = len(mu); x = np.zeros(n, dtype=int)
    for _ in range(k):
        best_gain, best_i = -np.inf, -1
        for i in range(n):
            if x[i]: continue
            x[i] = 1
            g = objective(mu, cov, x, risk_aversion)
            x[i] = 0
            if g > best_gain: best_gain, best_i = g, i
        x[best_i] = 1
    return x

def random_search(mu, cov, k, risk_aversion=2.0, iters=2000, seed=0):
    rng = np.random.default_rng(seed)
    n = len(mu); best_x, best_v = None, -np.inf
    for _ in range(iters):
        x = np.zeros(n, dtype=int)
        x[rng.choice(n, k, replace=False)] = 1
        v = objective(mu, cov, x, risk_aversion)
        if v > best_v: best_v, best_x = v, x
    return best_x

def exhaustive(mu, cov, k, risk_aversion=2.0):
    n = len(mu); best_x, best_v = None, -np.inf
    for comb in itertools.combinations(range(n), k):
        x = np.zeros(n, dtype=int); x[list(comb)] = 1
        v = objective(mu, cov, x, risk_aversion)
        if v > best_v: best_v, best_x = v, x
    return best_x

def run_benchmark(mu, cov, k=6, risk_aversion=2.0, n_seeds=10):
    """Compare methods; returns per-method rows with mean objective and runtime."""
    n = len(mu)
    Q, _ = build_qubo(mu, cov, k, risk_aversion)
    rows = []
    t0 = time.perf_counter(); x_ex = exhaustive(mu, cov, k, risk_aversion)
    rows.append(dict(method="Exhaustive (exact)", objective=objective(mu, cov, x_ex, risk_aversion),
                     std=0.0, runtime_s=time.perf_counter() - t0))
    t0 = time.perf_counter(); x_g = greedy_select(mu, cov, k, risk_aversion)
    rows.append(dict(method="Greedy (classical)", objective=objective(mu, cov, x_g, risk_aversion),
                     std=0.0, runtime_s=time.perf_counter() - t0))
    vals, t0 = [], time.perf_counter()
    for s in range(n_seeds):
        xr = random_search(mu, cov, k, risk_aversion, seed=s)
        vals.append(objective(mu, cov, xr, risk_aversion))
    rows.append(dict(method="Random search (classical)", objective=float(np.mean(vals)),
                     std=float(np.std(vals)), runtime_s=(time.perf_counter() - t0) / n_seeds))
    vals, t0 = [], time.perf_counter()
    for s in range(n_seeds):
        xs, _ = simulated_annealing(Q, n, k, seed=s)
        vals.append(objective(mu, cov, xs, risk_aversion))
    rows.append(dict(method="Simulated annealing (quantum-inspired)", objective=float(np.mean(vals)),
                     std=float(np.std(vals)), runtime_s=(time.perf_counter() - t0) / n_seeds))
    optimal = rows[0]["objective"]
    for r in rows:
        r["optimality_gap_pct"] = 100.0 * (optimal - r["objective"]) / abs(optimal)
    return rows
