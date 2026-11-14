# ARCHITECTURE_ESSENTIALS: Parity

Read this first. Open `ARCHITECTURE.md` only for the section you need. Last updated: 2026-11-14.

> **Maintenance rule.** Any contribution that changes behavior, data, structure or schedule MUST update `ROADMAP.md` in the same commit. If a decision below changes, update this file and `ARCHITECTURE.md` section 14 too.

## What it is
- Audit and repair of identity-based treatment gaps in a small multilingual LLM (Tiny Aya Global).
- Two-sided: benign identity prompts (over-refusal) and group-targeted harmful prompts (under-refusal) are always measured together.

## Pipeline (one CLI subcommand per stage)
1. `build`: seeds + groups.yaml -> CuratorKIT -> deterministic slot-fill -> pairs, harmful, control
2. `validate`: human spot check, freeze, checksum
3. `run`: model x condition x split -> responses
4. `label`: rules + judge + human sample -> labels
5. `analyze`: metrics, CIs, paired tests
6. `publish`: HF datasets, models, Space, article
- Side flow: `repair-fit` on dev only.

## Non-negotiable invariants
- A pair differs only by the inserted phrase. Built by code, never by an LLM.
- Split by `template_id`, 50/50 dev/test. Fit and tune on dev only.
- Test split runs only after `configs/targets.yaml` is frozen. Once per condition.
- Report IRG, THC, CORR together. A repair that fails THC or CORR margins is a failed repair.
- Third-party library calls live only in `src/parity/adapters/`.
- Never write a Lexsi-library call from memory. Read installed source, run it, then write it.
- Public artifacts: no slurs, no actionable harm detail, public and ungated on HF.
- `ROADMAP.md` is updated in every contribution.

## Metrics
- IRG: `refuse(identity) - refuse(bare)`, paired, also vs filler variant. Lower is better.
- THC: harm-compliance rate on group-targeted harmful prompts. Lower is better.
- CORR: refusal rate on no-identity control prompts. Lower is better.
- QPG: judge quality gap. Secondary.
- CIs: cluster bootstrap by `template_id`. Paired comparisons: exact McNemar.

## Repair (D4 open until gate G1)
- Plan A: SafeTune steering, fitted on dev. Unverified that it can reduce refusal conditionally.
- Plan B: SafeTune LoRA harden on CuratorKIT data.
- Plan C: system-prompt only (2-repo minimum). Always built as a comparator.

## Stack
- Python 3.12, uv, typer, pydantic v2 (file boundaries only), pandas/pyarrow, scipy/statsmodels, matplotlib, gradio.
- `auditkit[transformers,litellm]`, `curatorkit[generation,hygiene]`, `safetune`, `transformers>=5.15`.
- Files not services. JSONL in, Parquet out.

## Data records (details in ARCHITECTURE.md section 4)
- `PromptPair`: pair_id, template_id, axis, group_id, role, task_domain, variants{bare,filler,identity}, split
- `HarmPrompt`: prompt_id, template_id, axis, group_id, harm_category, text, split
- `ControlPrompt`: prompt_id, task_domain, text, split
- `Run`, `Response`, `Label`, `MetricResult`: provenance in every record

## Open decisions
- D4 repair method (gate G1), D5 one vs two environments (R-002), D6 judge model (needs user input)

## Top risks (full list in ARCHITECTURE.md section 15)
- Break: steering unsupported on Tiny Aya; dependency conflict; CuratorKIT toxicity gate silently deletes harmful templates; English-only refusal detector mislabels.
- Edge: empty or gibberish output under steering; token-length mismatch in filler; test leakage through shared templates; identity that legitimately changes the right answer.
- Overbuilt: plugin registries, multi-model runner, rich manifests, SafeTune's circuit tooling, anything in the Space beyond reading parquet.
