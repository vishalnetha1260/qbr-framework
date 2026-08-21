"""Table writer: emits every result table as CSV and LaTeX (booktabs)."""
import pandas as pd

def write_table(df: pd.DataFrame, stem: str, caption: str, label: str, tables_dir="results/tables"):
    csv_path = f"{tables_dir}/{stem}.csv"
    tex_path = f"{tables_dir}/{stem}.tex"
    df.to_csv(csv_path, index=False)
    with open(tex_path, "w") as f:
        f.write(df.to_latex(index=False, caption=caption, label=label,
                            float_format="%.3f", escape=True))
    print(f"  wrote {csv_path} and {tex_path}")
