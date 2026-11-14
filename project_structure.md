# project_structure.md

Where everything lives and where new things go. Last updated: 2026-11-14.

> **Maintenance rule.** Any contribution that adds, moves or removes a file or folder updates this file, and every contribution updates `ROADMAP.md` in the same commit.

## Tree (target state)

```
parity/
├── README.md                     # what it is, reproduce in one command, results summary, license notes
├── PRD.md                        # what and for whom
├── ARCHITECTURE.md               # full design, data models, stack, decision log
├── ARCHITECTURE_ESSENTIALS.md    # outline of critical decisions for agents
├── AGENTS.md                     # rules for any coding agent
├── CLAUDE.md                     # Claude Code additions, imports AGENTS.md
├── ROADMAP.md                    # all remaining work, updated on every contribution
├── project_structure.md          # this file
├── LICENSE
├── pyproject.toml                # deps, ruff, pytest config
├── uv.lock
├── Makefile                      # thin aliases: test, lint, pilot, all
├── .env.example                  # variable names only
├── .gitignore
│
├── configs/
│   ├── groups.yaml               # axes, groups, identity and filler phrases
│   ├── curator_templates.yaml    # CuratorKIT pipeline for neutral task diversification
│   ├── run_baseline.yaml
│   ├── run_steered.yaml
│   ├── run_sysprompt.yaml
│   ├── judge.yaml                # judge model id, prompts
│   ├── repair.yaml               # method, layer range, strength grid
│   └── targets.yaml              # success targets and margins, FROZEN before test runs
│
├── data/
│   ├── seeds/                    # hand-written neutral and harmful templates (YAML), human-authored
│   ├── pilot/                    # ~50 pairs for gate G1, never part of the benchmark (pilot_templates.yaml, pilot_pairs.jsonl)
│   ├── build/<ver>/              # generated, not frozen (gitignored if large)
│   ├── review/                   # human spot-check CSVs
│   └── frozen/<ver>/             # immutable benchmark + CHECKSUMS.txt. Never edit.
│
├── src/parity/
│   ├── __init__.py
│   ├── cli.py                    # typer app, one subcommand per stage
│   ├── schemas.py                # pydantic models at file boundaries
│   ├── config.py                 # YAML loading, config hashing
│   ├── build/                    # slot_fill.py, split.py, assemble.py
│   ├── adapters/                 # ONLY place third-party libs are called
│   │   ├── curator.py
│   │   ├── audit.py
│   │   └── safetune.py
│   ├── run/                      # runner.py (resumable, idempotent), conditions.py
│   ├── label/                    # rules.py, judge.py, human.py
│   ├── metrics/                  # irg.py, thc.py, corr.py, qpg.py, pipeline.py
│   ├── stats/                    # bootstrap.py, mcnemar.py
│   ├── report/                   # tables.py, figures.py
│   └── publish/                  # hf.py
│
├── tests/
│   ├── fixtures/                 # tiny datasets, mocked responses
│   ├── test_slot_fill.py         # pair-diff property
│   ├── test_split.py             # no template in both splits
│   ├── test_metrics.py           # hand-computed cases
│   ├── test_stats.py
│   ├── test_adapters_contract.py # 5-prompt fixtures per adapter
│   ├── test_golden_analyze.py
│   ├── test_pilot_data.py        # pilot pair-diff property tests (R-102)
│   └── test_pipeline_e2e.py      # end-to-end labeling & analysis pipeline test
│
├── notebooks/                    # Colab entrypoints that call the CLI, no logic of their own
├── spaces/parity-explorer/       # Gradio app, reads precomputed parquet only
│   ├── app.py
│   └── requirements.txt
├── scripts/                      # one-off helpers, each with a header comment saying why it exists
├── artifacts/                    # gitignored, stage outputs with manifest.json
├── runs/                         # gitignored, raw responses
└── reports/
    ├── results/                  # parquet + csv of final metrics
    ├── figures/
    ├── article.md                # HF article source
    └── friction_log.md           # issues hit with CuratorKIT, AuditKIT, SafeTune
```

## Placement rules

| If you are adding... | Put it in... |
|---|---|
| A call to CuratorKIT, AuditKIT or SafeTune | `src/parity/adapters/` and nowhere else |
| A metric | `src/parity/metrics/`, with a hand-computed test |
| Hand-written prompt templates | `data/seeds/` (human-authored only) |
| A new group or axis | `configs/groups.yaml`, no code change |
| A one-off analysis | `scripts/`, with a header comment, and delete it when done |
| A decision or changed assumption | `ARCHITECTURE.md` section 14, and `ROADMAP.md` Decisions |
| A bug in a Lexsi library | `reports/friction_log.md` (with version, repro, workaround) |

## Naming

- Files and modules: `snake_case`. CLI subcommands: lowercase single words or hyphenated (`repair-fit`).
- Benchmark versions: `v0.1`, `v0.2`. Run ids: `{model}-{condition}-{split}-{YYYYMMDDTHHMM}`.
- IDs: `template_id` like `T-housing-014`, `pair_id` like `T-housing-014-wheelchair_user-speaker`.

## Generated vs source

- Source of truth: `configs/`, `data/seeds/`, `data/frozen/`, `src/`, `tests/`, docs.
- Generated, gitignored, rebuildable: `artifacts/`, `runs/`, `data/build/`.
- Published: HF repos mirror `data/frozen/`, `runs/` responses and labels, and repair artifacts.

## Hard questions

**What would break?** Two sources of truth for the same data (git vs HF). Rule: git holds the frozen benchmark, HF mirrors it, and `publish` verifies checksums match before uploading.

**What edge cases are we missing?** Large files accidentally committed (`runs/`), notebooks accumulating logic that never reaches `src/`, `data/pilot/` leaking into the benchmark. Mitigations: `.gitignore`, notebooks may only call the CLI, `build` refuses inputs under `data/pilot/`.

**What is overengineered?** `report/` and `publish/` as packages for what may be two functions each. Start as single files, split only when they exceed about 200 lines. The same applies to `build/`, `label/` and `run/`.
