"""One-off helper script to generate pilot pairs (R-102) for Gate G1.

Reads data/pilot/pilot_templates.yaml and configs/groups.yaml,
deterministically generates pilot pairs across disability and religion axes,
and saves the output to data/pilot/pilot_pairs.jsonl.
"""

from pathlib import Path

import yaml

from parity.build.assemble import assemble_pilot_pairs, save_jsonl
from parity.config import load_groups_config


def main() -> None:
    templates_path = Path("data/pilot/pilot_templates.yaml")
    with open(templates_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    templates = data["templates"]

    groups_config = load_groups_config("configs/groups.yaml")

    pairs = assemble_pilot_pairs(
        templates=templates,
        groups_config=groups_config,
        target_axes=("disability", "religion"),
        groups_per_axis=2,
    )

    out_path = Path("data/pilot/pilot_pairs.jsonl")
    save_jsonl(pairs, out_path)
    print(f"Successfully generated {len(pairs)} pilot pairs in {out_path}")


if __name__ == "__main__":
    main()
