"""Figure and plot generation for Parity evaluation reports."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_irg_by_group(
    irg_df: pd.DataFrame,
    output_path: Path | str = "reports/figures/irg_by_group.png",
) -> None:
    """Plot IRG point estimates and confidence intervals across demographic groups."""
    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    if not irg_df.empty and "Scope ID" in irg_df.columns and "Estimate" in irg_df.columns:
        ax.barh(irg_df["Scope ID"], irg_df["Estimate"].astype(float), color="skyblue")
        ax.set_xlabel("Identity Refusal Gap (IRG)")
        ax.set_title("Identity Refusal Gap by Demographic Group")
        ax.axvline(0, color="gray", linestyle="--")

    plt.tight_layout()
    fig.savefig(p, dpi=300)
    plt.close(fig)
