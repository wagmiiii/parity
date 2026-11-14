"""Human review sampling and annotation workflow."""

from pathlib import Path

import pandas as pd

from parity.schemas import Label


def export_sample_for_review(
    labels: list[Label], sample_size: int = 50, seed: int = 42
) -> pd.DataFrame:
    """Sample labels for human adjudication spot checks."""
    df = pd.DataFrame([label.model_dump() for label in labels])
    if len(df) <= sample_size:
        return df
    return df.sample(n=sample_size, random_state=seed)


def import_human_annotations(csv_path: Path | str) -> pd.DataFrame:
    """Import human spot check annotations."""
    return pd.read_csv(csv_path)
