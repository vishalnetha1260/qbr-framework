"""All publication figures for the QBR companion repository.

Static IEEE-style matplotlib figures: single light theme, one validated
categorical palette used in fixed slot order, recessive grids, selective
direct labels, no dual axes.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

# Validated categorical palette (fixed order) + ink tokens
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e5e4e0", "#fcfcfb"

plt.rcParams.update({
    "font.family": "DejaVu Serif", "font.size": 9.5,
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "axes.titlesize": 10.5,
    "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.dpi": 300,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
})

def _save(fig, path):
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {path}")

# ---------- Conceptual figures (Figures 1-3 of the article) ----------

def fig1_evolution(path):
    stages = ["Data\nanalytics", "Business\nintelligence", "AI-driven\nanalytics",
              "Decision\nintelligence", "Quantum-enhanced\ndecision intelligence"]
    fig, ax = plt.subplots(figsize=(7.0, 2.9))
    ax.set_axis_off(); ax.grid(False)
    for i, s in enumerate(stages):
        x, y = i * 1.9, i * 0.52
        w = 1.8
        box = FancyBboxPatch((x, y), w, 0.85, boxstyle="round,pad=0.06",
                             fc=C[0] if i < 4 else C[1], ec="none", alpha=0.92)
        ax.add_patch(box)
        ax.text(x + w / 2, y + 0.43, s, ha="center", va="center",
                color="white", fontsize=7.6, fontweight="bold")
        if i:
            ax.add_patch(FancyArrowPatch((x - 0.22, y + 0.15), (x + 0.03, y + 0.32),
                                         arrowstyle="-|>", mutation_scale=13, color=INK2))
    ax.text(0.05, 3.15, "Decision quality", rotation=90, fontsize=8.5, color=INK2,
            ha="center", va="top", transform=ax.transData)
    ax.set_xlim(-0.4, 10.0); ax.set_ylim(-0.35, 3.45)
    ax.set_title("Figure 1. Evolution from data analytics to quantum-enhanced strategic decision intelligence")
    _save(fig, path)

def fig2_qbr_framework(path):
    layers = [
        ("L1  Technology and market intelligence", "confidence-graded technology/threat picture"),
        ("L2  Use-case and value analytics", "scored portfolio; explicit no-go rationales"),
        ("L3  Quantum and hybrid computation", "performance evidence; reusable formulations"),
        ("L4  Knowledge, talent, and translation", "explainable, justified recommendations"),
        ("L5  Risk and quantum-safe resilience", "PQC migration program; risk-adjusted view"),
        ("L6  Strategic decision intelligence", "ranked alternatives with trade-offs"),
        ("L7  Human governance and action", "governed action; recorded rationale"),
    ]
    fig, ax = plt.subplots(figsize=(6.6, 6.4))
    ax.set_axis_off(); ax.grid(False)
    n = len(layers)
    for i, (name, out) in enumerate(layers):
        y = (n - 1 - i) * 1.0
        color = C[0] if i < 4 else (C[2] if i == 4 else (C[1] if i == 5 else C[3]))
        ax.add_patch(FancyBboxPatch((0.0, y), 5.6, 0.72, boxstyle="round,pad=0.05",
                                    fc=color, ec="none", alpha=0.92))
        ax.text(0.18, y + 0.47, name, fontsize=9.3, fontweight="bold", color="white")
        ax.text(0.18, y + 0.18, out, fontsize=7.8, color="white")
        if i:
            ax.add_patch(FancyArrowPatch((2.8, y + 1.0 - 0.13), (2.8, y + 0.82),
                                         arrowstyle="-|>", mutation_scale=13, color=INK))
    ax.add_patch(FancyArrowPatch((5.95, 0.35), (5.95, 6.4),
                                 connectionstyle="arc3,rad=-0.28",
                                 arrowstyle="-|>", mutation_scale=14,
                                 color=INK2, linestyle=(0, (4, 2))))
    ax.text(6.9, 3.4, "continuous\nreadiness\nlearning loop", fontsize=8.2,
            color=INK2, ha="center", style="italic")
    ax.set_xlim(-0.2, 7.6); ax.set_ylim(-0.3, 7.35)
    ax.set_title("Figure 2. The QBR Framework: seven layers with continuous feedback")
    _save(fig, path)

def fig3_decision_loop(path):
    nodes = ["Business\ndecision need", "Formulation\n(QUBO / hybrid)",
             "Quantum /\nquantum-inspired\ncomputation", "Explainable\nrecommendation",
             "Human governance\nand commitment", "Outcome and\nlearning"]
    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    ax.set_axis_off(); ax.grid(False)
    R, cx, cy = 2.35, 0, 0
    pts = []
    for i in range(len(nodes)):
        a = np.pi / 2 - 2 * np.pi * i / len(nodes)
        pts.append((cx + R * np.cos(a), cy + R * np.sin(a)))
    for i, (x, y) in enumerate(pts):
        color = C[i % 4]
        ax.add_patch(FancyBboxPatch((x - 0.78, y - 0.4), 1.56, 0.8,
                                    boxstyle="round,pad=0.06", fc=color, ec="none", alpha=0.92))
        ax.text(x, y, nodes[i], ha="center", va="center", color="white",
                fontsize=8.0, fontweight="bold")
    for i in range(len(pts)):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % len(pts)]
        v = np.array([x2 - x1, y2 - y1]); v = v / np.linalg.norm(v)
        ax.add_patch(FancyArrowPatch((x1 + v[0] * 0.95, y1 + v[1] * 0.62),
                                     (x2 - v[0] * 0.95, y2 - v[1] * 0.62),
                                     arrowstyle="-|>", mutation_scale=13,
                                     color=INK2, connectionstyle="arc3,rad=0.12"))
    ax.text(0, 0, "human-quantum-AI\nstrategic decision loop", ha="center",
            va="center", fontsize=9, style="italic", color=INK2)
    ax.set_xlim(-3.6, 3.6); ax.set_ylim(-3.4, 3.5)
    ax.set_title("Figure 3. The human-quantum-AI strategic decision loop")
    _save(fig, path)

# ---------- Simulation figures ----------

def fig4_benchmark(bench_rows, path):
    methods = [r["method"].replace(" (", "\n(") for r in bench_rows]
    gaps = [max(r["optimality_gap_pct"], 0) for r in bench_rows]
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    bars = ax.bar(methods, gaps, width=0.55, color=[C[2], C[3], C[1], C[0]], zorder=3)
    for b, g in zip(bars, gaps):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.06,
                f"{g:.2f}%", ha="center", fontsize=8.6, color=INK)
    ax.set_ylabel("Optimality gap vs exact (%)")
    ax.set_axisbelow(True); ax.grid(axis="x", visible=False)
    ax.tick_params(axis="x", labelsize=8)
    ax.set_title("Portfolio-selection QUBO: quantum-inspired annealing vs classical baselines")
    _save(fig, path)

def fig5_ev_ranking(sens_df, path):
    d = sens_df.iloc[::-1]
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    y = np.arange(len(d))
    ax.hlines(y, d.ev_p05, d.ev_p95, color=C[0], lw=2.2, alpha=0.55, zorder=3)
    ax.plot(d.ev_mean, y, "o", ms=8, color=C[0], zorder=4)
    for yi, (m, lo, hi) in enumerate(zip(d.ev_mean, d.ev_p05, d.ev_p95)):
        ax.text(hi + 0.03, yi, f"{m:.2f}", va="center", fontsize=8.4, color=INK2)
    ax.set_yticks(y, d.initiative, fontsize=8.6)
    ax.axvline(0, color=INK2, lw=0.8)
    ax.set_xlabel("Scenario-weighted expected strategic value  E[V]  ($M)")
    ax.set_axisbelow(True); ax.grid(axis="y", visible=False)
    ax.set_title("Equation (1): initiative ranking with 5-95% scenario-uncertainty bands")
    _save(fig, path)

def fig6_mosca(exposure_df, mosca_df, z_years, path):
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.2))
    ax = axes[0]
    ax.plot(exposure_df.z_years, exposure_df.pct_exposed, lw=2, color=C[0], zorder=3)
    ax.plot(exposure_df.z_years, exposure_df.weighted_pct_exposed, lw=2,
            color=C[1], zorder=3)
    ax.text(4, 72, "% systems exposed", color=C[0], fontsize=8)
    ax.text(4, 62, "sensitivity-weighted", color=C[1], fontsize=8)
    ax.axvline(z_years, color=INK2, lw=0.9, ls=(0, (4, 2)))
    ax.text(z_years + 0.4, 92, f"assumed z = {z_years:.0f}y", fontsize=7.8, color=INK2)
    ax.set_xlabel("Assumed years to CRQC (z)")
    ax.set_ylabel("Exposed share (%)"); ax.set_ylim(0, 105)
    ax.set_axisbelow(True)
    ax.set_title("Harvest-now-decrypt-later exposure", fontsize=9.5)
    ax = axes[1]
    exposed = mosca_df.exposed
    ax.scatter(mosca_df.shelf_life_years[~exposed], mosca_df.migration_years[~exposed],
               s=55, color=C[0], zorder=4, label="Within margin")
    ax.scatter(mosca_df.shelf_life_years[exposed], mosca_df.migration_years[exposed],
               s=55, color=C[1], marker="s", zorder=4, label="Exposed (x+y>z)")
    zz = np.linspace(0, z_years, 10)
    ax.plot(zz, z_years - zz, color=INK2, lw=0.9, ls=(0, (4, 2)), zorder=2)
    ax.set_ylim(0, None); ax.set_xlim(0, None)
    ax.set_xlabel("Data shelf life x (years)"); ax.set_ylabel("Migration time y (years)")
    ax.set_axisbelow(True)
    ax.legend(fontsize=7.6, frameon=False, loc="upper right")
    ax.set_title("Mosca inequality by system", fontsize=9.5)
    fig.suptitle("Layer 5: quantum-safe timing analysis", y=1.02, fontsize=10.5)
    _save(fig, path)

def fig7_tornado(tornado_df, initiative, path):
    base = tornado_df.attrs["base_ev"]
    piv = tornado_df.pivot_table(index="parameter", columns="direction", values="expected_value")
    span = (piv.high - piv.low).abs().sort_values()
    piv = piv.loc[span.index]
    fig, ax = plt.subplots(figsize=(6.0, 3.0))
    y = np.arange(len(piv))
    ax.barh(y, piv.high - base, left=base, height=0.5, color=C[0], zorder=3, label="+25%")
    ax.barh(y, piv.low - base, left=base, height=0.5, color=C[1], zorder=3, label="-25%")
    ax.axvline(base, color=INK, lw=1.0)
    ax.set_yticks(y, [p.replace("_", " ") for p in piv.index], fontsize=8.8)
    ax.set_xlabel("E[V] ($M)")
    ax.set_axisbelow(True); ax.grid(axis="y", visible=False)
    ax.legend(fontsize=7.8, frameon=False, loc="lower right")
    ax.set_title(f"Decision-level explainability: E[V] sensitivity, '{initiative}'")
    _save(fig, path)

def fig8_screening(screened_df, path):
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    colors = {"GO (pilot now)": C[2], "PILOT (quantum-inspired first)": C[0],
              "NO-GO (harden classical pipeline)": C[1]}
    for rec, g in screened_df.groupby("recommendation"):
        ax.scatter(g.near_term_feasibility, g.amenability_score, s=60,
                   color=colors[rec], label=rec, zorder=4,
                   marker={"GO (pilot now)": "o", "PILOT (quantum-inspired first)": "^",
                           "NO-GO (harden classical pipeline)": "s"}[rec])
    top = screened_df.nlargest(3, "amenability_score")
    for _, r in top.iterrows():
        ax.annotate(r.use_case, (r.near_term_feasibility, r.amenability_score),
                    textcoords="offset points", xytext=(-8, -3), fontsize=7.2,
                    color=INK2, ha="right")
    ax.set_xlabel("Near-term feasibility"); ax.set_ylabel("Quantum-amenability score")
    ax.set_xlim(None, screened_df.near_term_feasibility.max() + 0.08)
    ax.set_axisbelow(True)
    ax.legend(fontsize=7.4, frameon=False, loc="lower right")
    ax.set_title("Layer 2: decision-first use-case screening")
    _save(fig, path)
