# Quantum Business Readiness (QBR) Framework — Companion Simulations

Companion repository for the research article:

> **Quantum Computing and Business Readiness: A Human-Centered Framework for
> Risk-Aware Strategic Adoption of Quantum Technologies**
> (conceptual, critical literature-based research article — `paper/QBR_Research_Article.docx`)

The article is conceptual and reports no new empirical results. This repository
provides a **reproducible illustrative testbed** that operationalizes the
framework's logic layer by layer, and regenerates every figure and table with a
single command.

## What `run_experiment.py` produces

| Layer / concept | Module | Outputs |
|---|---|---|
| Layer 2 — use-case & value analytics | `src/use_case_screening.py` | Table 4, Fig. 8 (decision-first screening, go/pilot/no-go) |
| Layer 3 — quantum & hybrid computation | `src/quantum_inspired.py` | Table 5, Fig. 4 (QUBO portfolio selection: simulated annealing vs classical baselines vs exact) |
| Layer 5 — quantum-safe resilience | `src/risk_module.py` | Table 6, Fig. 6 (Mosca timing analysis, harvest-now-decrypt-later exposure, migration queue) |
| Layer 6 — Equation (1) | `src/decision_intelligence.py` | Tables 7–8, Fig. 5 (scenario-weighted E[V], Monte Carlo sensitivity) |
| Layer 4 / Proposition P3 | `src/explainability.py` | Table 9, Fig. 7 + narrative explanation (tornado sensitivity) |
| Article Figures 1–3 | `src/figures.py` | Publication-quality conceptual diagrams |

All datasets are synthetic, seeded, and documented (`src/data_loader.py`);
no empirical claims are attached to them.

## Quick start (local or RunPod)

```bash
git clone https://github.com/<YOUR_USERNAME>/qbr-framework.git
cd qbr-framework
pip install -r requirements.txt
python run_experiment.py        # ~10 s on CPU; no GPU required
```

Outputs land in `results/figures/` (PNG, 300 dpi) and `results/tables/`
(CSV + LaTeX booktabs, ready to `\input{}` into the manuscript).

On RunPod: any CPU or GPU pod works. `nvidia-smi` will confirm a GPU is
present, but the experiment is CPU-only by design (quantum-inspired =
classical hardware, per the article's Layer 3).

## Repository layout

```
qbr-framework/
├── run_experiment.py         # single entry point — regenerates everything
├── requirements.txt
├── paper/                    # the research article
├── src/                      # one module per framework layer
├── data/                     # (empty; datasets are generated, seeded)
└── results/                  # figures + tables (regenerated on each run)
```

## Reproducibility

Every random process is seeded (`SEED = 42` in `src/data_loader.py`; per-seed
loops for the annealing benchmark). Two consecutive runs produce identical
tables and figures.
