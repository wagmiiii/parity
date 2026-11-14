# Parity

Audit and repair of identity-based treatment gaps in a small multilingual LLM (Tiny Aya Global) for the Lexsi AI Safety and Alignment Hackathon (Track 2: Data & Alignment Track).

Parity chains **CuratorKIT** (dataset generation and curation), **AuditKIT** (evaluation and safety probes), and **SafeTune** (inference-time steering and repair).

## Problem

Safety tuning often fails in two opposite directions:
1. **Identity-triggered over-refusal:** Models refuse or hedge benign everyday requests when a user mentions a minority identity (e.g. disability, religion, sexual orientation, ethnicity).
2. **Weaker refusal of group-targeted harm:** The same models can be more compliant when a request targets or demeans a minority group compared to neutral harm requests.

Parity measures both directions simultaneously and evaluates whether safety steering can close the treatment gap without compromising harm refusal or general helpfulness.

## Headline Metrics

- **IRG (Identity Refusal Gap):** Refusal rate difference between identity-explicit prompts and bare/filler variants on benign tasks. Lower is better.
- **THC (Targeted Harm Compliance):** Compliance rate on group-targeted harmful requests. Lower is better.
- **CORR (Control Over-Refusal Rate):** Refusal rate on neutral non-identity control prompts. Lower is better.
- **QPG (Quality Parity Gap):** Secondary judge quality difference on compliant pairs.

## Quickstart

```bash
# Install dependencies
uv sync

# Run tests and linter
make check

# View CLI options
uv run parity --help
```

## Pipeline Stages

```bash
uv run parity build --help       # Construct minimal-pair, harmful, and control sets
uv run parity validate --help    # Validate pairs and freeze benchmark with checksums
uv run parity run --help         # Execute inference runs across conditions and splits
uv run parity label --help       # Classify refusals and harm compliance (rules + judge)
uv run parity analyze --help     # Compute IRG, THC, CORR, bootstrap CIs, and McNemar tests
uv run parity repair-fit --help  # Fit inference-time steering vectors on dev split
uv run parity publish --help     # Export results to Hugging Face datasets and spaces
```

## Structure

See [project_structure.md](file:///home/ademola/parity/project_structure.md) for detailed layout and component responsibilities.

## License

Code is licensed under the Apache License 2.0 (see [LICENSE](file:///home/ademola/parity/LICENSE)). Third-party libraries (CuratorKIT, AuditKIT, SafeTune) are subject to Lexsi Source Available License (LSAL v1.2).
