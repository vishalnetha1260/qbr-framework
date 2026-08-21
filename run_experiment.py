#!/usr/bin/env python3
"""QBR Framework companion experiment — single entry point.

Runs every simulation supporting the article "Quantum Computing and Business
Readiness: A Human-Centered Framework for Risk-Aware Strategic Adoption of
Quantum Technologies" and regenerates ALL figures and tables into results/.

Usage:  python run_experiment.py
"""
import os, sys, time, platform
import numpy as np
import pandas as pd

from src.data_loader import (load_use_case_portfolio, load_asset_universe,
                             load_crypto_inventory, load_initiative_scenarios)
from src.use_case_screening import screen_use_cases
from src.quantum_inspired import run_benchmark
from src.decision_intelligence import expected_strategic_value, scenario_sensitivity
from src.risk_module import mosca_analysis, exposure_curve
from src.explainability import tornado_sensitivity, narrative_explanation
from src.evaluation import write_table
from src import figures

Z_YEARS = 12.0   # assumed years to a cryptographically relevant quantum computer

def main():
    t_start = time.time()
    os.makedirs("results/figures", exist_ok=True)
    os.makedirs("results/tables", exist_ok=True)
    print(f"QBR companion experiment | python {platform.python_version()} | numpy {np.__version__}\n")

    print("[1/6] Layer 2 - use-case screening")
    screened = screen_use_cases(load_use_case_portfolio())
    write_table(screened, "table4_use_case_screening",
                "Decision-first screening of candidate quantum use cases.", "tab:screening")
    figures.fig8_screening(screened, "results/figures/fig8_use_case_screening.png")

    print("[2/6] Layer 3 - quantum-inspired vs classical optimization benchmark")
    _, mu, cov = load_asset_universe(n_assets=18)
    bench = run_benchmark(mu, cov, k=6, n_seeds=10)
    bench_df = pd.DataFrame(bench).round(4)
    write_table(bench_df, "table5_optimization_benchmark",
                "Cardinality-constrained portfolio QUBO: method comparison (10 seeds).",
                "tab:benchmark")
    figures.fig4_benchmark(bench, "results/figures/fig4_optimization_benchmark.png")

    print("[3/6] Layer 5 - quantum-safe (Mosca) risk analysis")
    inv = load_crypto_inventory()
    mosca = mosca_analysis(inv, z_years=Z_YEARS)
    write_table(mosca, "table6_mosca_migration_queue",
                f"Mosca timing analysis and prioritized PQC migration queue (z={Z_YEARS:.0f}y).",
                "tab:mosca")
    exposure = exposure_curve(inv)
    figures.fig6_mosca(exposure, mosca, Z_YEARS, "results/figures/fig6_mosca_analysis.png")

    print("[4/6] Layer 6 - Equation (1) strategic decision intelligence")
    init_df, scenarios = load_initiative_scenarios()
    ev = expected_strategic_value(init_df, scenarios)
    write_table(ev, "table7_equation1_ranking",
                "Scenario-weighted expected strategic value E[V] per initiative (Equation 1).",
                "tab:ev")
    sens = scenario_sensitivity(init_df, scenarios, n_draws=2000)
    write_table(sens, "table8_scenario_sensitivity",
                "Monte Carlo sensitivity of E[V] to scenario-probability uncertainty.",
                "tab:sens")
    figures.fig5_ev_ranking(sens, "results/figures/fig5_ev_ranking.png")

    print("[5/6] Layer 4 / P3 - decision-level explainability")
    top = ev.initiative.iloc[0]
    tornado = tornado_sensitivity(init_df, scenarios, top)
    write_table(tornado, "table9_tornado_sensitivity",
                f"One-at-a-time (+/-25%) sensitivity of E[V] for '{top}'.", "tab:tornado")
    figures.fig7_tornado(tornado, top, "results/figures/fig7_explainability_tornado.png")
    explanation = narrative_explanation(tornado, top)
    with open("results/tables/explanation_top_initiative.txt", "w") as f:
        f.write(explanation + "\n")
    print("  wrote results/tables/explanation_top_initiative.txt")

    print("[6/6] Conceptual figures (article Figures 1-3)")
    figures.fig1_evolution("results/figures/fig1_evolution.png")
    figures.fig2_qbr_framework("results/figures/fig2_qbr_framework.png")
    figures.fig3_decision_loop("results/figures/fig3_decision_loop.png")

    print(f"\nDone in {time.time() - t_start:.1f}s. All outputs in results/figures and results/tables.")
    print("\n" + explanation)

if __name__ == "__main__":
    sys.exit(main())
