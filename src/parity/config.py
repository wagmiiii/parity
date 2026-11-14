"""Configuration loading and hashing utilities for Parity."""

import hashlib
from pathlib import Path
from typing import Any

import yaml

from parity.schemas import GroupsConfig


def compute_sha256(path_or_bytes: Path | str | bytes) -> str:
    """Compute hex SHA-256 digest of file or bytes."""
    if isinstance(path_or_bytes, bytes):
        return hashlib.sha256(path_or_bytes).hexdigest()
    path = Path(path_or_bytes)
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def load_yaml(path: Path | str) -> dict[str, Any]:
    """Load a raw YAML configuration file."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Configuration file not found: {p}")
    with open(p, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def load_groups_config(path: Path | str = "configs/groups.yaml") -> GroupsConfig:
    """Load and validate groups.yaml."""
    raw = load_yaml(path)
    return GroupsConfig.model_validate(raw)
