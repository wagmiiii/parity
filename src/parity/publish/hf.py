"""Hugging Face Hub publishing utilities for datasets, models, and Spaces."""

from pathlib import Path


def publish_dataset(
    data_dir: Path | str,
    repo_id: str,
    private: bool = False,
) -> None:
    """Upload frozen benchmark or response datasets to Hugging Face Hub."""
    # Stub: will use HfApi().upload_folder(...)
    pass


def publish_space(
    space_dir: Path | str,
    space_repo_id: str,
) -> None:
    """Deploy the Parity Explorer Space."""
    # Stub
    pass
