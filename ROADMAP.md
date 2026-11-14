# ROADMAP: Parity

Last updated: 2026-11-14 | Progress: **4 / 46 tasks done** | Phase: 1 (Pilot and gate G1)

---

## Contribution Protocol (mandatory)

**This file is updated on every contribution, by humans and by agents, in the same commit as the change.** That includes code, data, configs, docs, refactors and experiments.

On every contribution:

1. Set the status of each task you touched (`Todo`, `Doing`, `Done`, `Blocked`, `Cut`).
2. Fill the "Notes" cell with what was actually verified, not what was intended.
3. Add a row to the **Changelog** at the bottom: date, who, what, task ids.
4. Update the **Progress** count and **Current focus** block at the top.
5. If you found a new task, add it with the next free id. If you cut or changed scope, record it under **Decisions**.
6. If you are blocked, add it under **Blocked** with what you tried.

A change with no ROADMAP update is incomplete.

Status legend: `Todo` not started | `Doing` in progress | `Done` verified by running | `Blocked` waiting on something named | `Cut` dropped on purpose, reason in Decisions.

Owner legend: `H` human, `A` agent, `H+A` either.

---

## Current focus

- Now: Phase 1 pilot. R-102 Done (160 pilot pairs built and verified against pair-diff property). R-101 Colab notebook prepared in notebooks/01_colab_tiny_aya_smoke.ipynb. Next is Colab T4 GPU execution of R-101 and pilot inference (R-103) & SafeTune spike (R-104).
- Next gate: **G1** (end of Phase 1), decides repair method D4.
- Hard deadline: **Nov 15, 2026, 11:59 PM AoE**, which is **Nov 16, 12:59 PM in Lagos (WAT)**. Submission may be repeated, the latest counts.
- Time is the binding constraint. At most about 36 hours of wall clock remain, fewer after sleep. Planned effort through submission (Phases 0 to 6) is about 38 hours, so **the cut ladder applies**.

## Cut ladder (pre-agreed, apply in order when behind)

| Level | Name | Contents | Cut when |
|---|---|---|---|
| L0 | Full v1 | 4 axes, filler variant, steering repair, sysprompt comparator, Space, article | on schedule |
| L1 | Lean | 3 axes, filler on 2 axes, drop QPG, Space is a static table | behind by more than 4h at G1 |
| L2 | Minimum viable submission (MVS) | 2 axes, 15 templates per group, Plan C repair (sysprompt) as the "after", CuratorKIT + AuditKIT only, README instead of Space | steering not working after R-104 timebox, or behind by more than 8h |
| L3 | Emergency | Whatever has numbers: baseline audit only, honest write-up that the repair stage is unfinished | less than 6h to deadline and no repaired run |

Submit at the highest level reached with at least **6 hours of buffer** before the deadline. A rough submission now beats a better one after the deadline.

## Gates

| Gate | When | Rule |
|---|---|---|
| **G1** Pilot go/no-go | End of Phase 1 | If steering loads on Tiny Aya and the pilot shows an identity gap of at least 5 percentage points on any axis (point estimate): Plan A on the benign side. If no gap on benign pairs but THC varies by group: pivot headline to THC parity, still Plan A. If steering fails after the 2h timebox: Plan B if SafeTune harden loads, else Plan C and go to L2. If everything is null: report the null honestly and use the harmful side. Thresholds are proposals, record any change in Decisions. |
| **G2** Benchmark freeze | End of Phase 2 | Human review done, invalid-pair rate at most 5%, checksums written. No benchmark edits after this without a version bump. |
| **G3** Targets freeze | Before first non-baseline test run | `configs/targets.yaml` committed. |
| **G4** Submission readiness | Phase 6 | Every item in R-601 checked from a logged-out browser. |

---

## Phase 0: Bootstrap (about 3h)

| ID | Task | Owner | Est | Depends | Status | Done when / Notes |
|---|---|---|---|---|---|---|
| R-001 | Create public repo `parity`, commit the 7 doc files, LICENSE, `.gitignore`, `.env.example`. Repo must be created inside the hackathon window | H | 0.5h | none | Done | Repo created and public under wagmiiii/parity. Docs, LICENSE, .gitignore, .env.example committed |
| R-002 | `pyproject.toml` on Python 3.12 with uv. Try one environment with `auditkit[transformers,litellm]`, `curatorkit[generation,hygiene]`, `safetune`, `transformers>=5.15`. If unresolvable, split into two envs and record in ARCHITECTURE D5 | A | 1h | R-001 | Done | Single environment resolved with uv: auditkit==1.1.12, curatorkit==0.1.28, safetune==0.1.19, transformers==5.23.0 |
| R-003 | Skeleton: `src/parity/` package, `cli.py` with stub subcommands, `schemas.py`, Makefile, ruff and pytest config, one passing test | A | 1h | R-002 | Done | 7 Typer CLI subcommands scaffolded, full Pydantic v2 schemas in schemas.py, full project structure and test suite passing |
| R-004 | Confirm eligibility: registration email known, HF username matches registration, joined Discord (needed for credits), $20 HF credit redeemed. Ask in `#report-issues` whether a benchmark-plus-repair submission satisfies "before-and-after metrics" | H | 0.5h | none | Todo | Written answer or screenshot saved, credit visible in HF |

## Phase 1: Pilot and gate G1 (about 6h)

| ID | Task | Owner | Est | Depends | Status | Done when / Notes |
|---|---|---|---|---|---|---|
| R-101 | Load Tiny Aya Global on a Colab T4 via AuditKIT `hf:` backend, generate 5 prompts, record tokens per second and peak memory. Read AuditKIT source for the refusal detectors | H+A | 1h | R-002 | Todo | Throughput and memory numbers written into ARCHITECTURE section 10, replacing the guesses |
| R-102 | Hand-write 20 neutral task templates and fill 2 axes (disability, religion) with 2 groups each, bare/filler/identity, about 50 pairs, in `data/pilot/` | H+A | 1.5h | none | Done | Pair-diff property test verified on 160 pilot pairs across disability and religion axes (4 groups, 2 roles, 20 neutral templates in data/pilot/pilot_pairs.jsonl) |
| R-103 | Run pilot baseline, label with rule-based detector, compute IRG with a bootstrap CI | A | 1h | R-101, R-102 | Todo | IRG per axis with CI in `reports/pilot.md`, and 50 outputs eyeballed for detector mislabels |
| R-104 | **Timeboxed 2h spike:** does SafeTune steering load, fit and apply on Tiny Aya Global? Can it reduce refusal on a chosen input class rather than only add refusal? Read installed source first | H+A | 2h | R-101 | Todo | Written verdict: works / works with changes / does not. Library bugs go to `reports/friction_log.md` |
| R-105 | **Gate G1:** apply the G1 rule, record choice D4 and cut level in Decisions | H | 0.5h | R-103, R-104 | Todo | Decision recorded |

## Phase 2: Dataset build and freeze (about 9.5h)

| ID | Task | Owner | Est | Depends | Status | Done when / Notes |
|---|---|---|---|---|---|---|
| R-201 | Write the neutral template bank in `data/seeds/`: 40 tasks across 8 domains where identity is irrelevant to the correct answer. Human-authored | H+A | 2h | R-105 | Todo | 40 templates committed, each tagged with a domain |
| R-202 | Finalize `configs/groups.yaml`: axes, groups (3 per axis), speaker and subject phrasings, filler phrases matched on Tiny Aya **token** length | H+A | 1h | R-101 | Todo | Test asserts token-length match for every group |
| R-203 | CuratorKIT pass to diversify neutral templates, with quality gates and minhash dedupe. Verify the toxicity gate setting and that rejected rows are counted | A | 2h | R-201 | Todo | `build` asserts expected template counts, rejected rows reported, provenance files kept |
| R-204 | Harmful template bank, category-level, no slurs, 4 categories, about 25 templates, with matched no-group variants | H+A | 1.5h | R-105 | Todo | Reviewed against PRD section 10 |
| R-205 | Control set: 100 benign prompts, no identity content | A | 0.5h | R-201 | Todo | 100 prompts, domains balanced |
| R-206 | Deterministic slot-fill and seeded template-level 50/50 dev/test split, harmful and control split the same way | A | 1h | R-202, R-203, R-204, R-205 | Todo | Property tests: pair differs only by the phrase, no template in both splits |
| R-207 | Human review of at least 10% of pairs (minimum 40) for validity, identity irrelevance and absence of harm cues, plus misuse review of 30 harmful prompts. Fix, then **G2 freeze** to `data/frozen/v0.1/` with checksums and push to HF | H | 1.5h | R-206 | Todo | Invalid rate at most 5%, `CHECKSUMS.txt` committed, HF dataset public |

## Phase 3: Baseline audit (about 5h)

| ID | Task | Owner | Est | Depends | Status | Done when / Notes |
|---|---|---|---|---|---|---|
| R-301 | Implement runner: resumable, idempotent per `(run_id, prompt_id, variant)`, logs truncation and empty outputs. Run baseline on dev and test | A | 1.5h | R-207 | Todo | Interrupt and resume test passes, response counts match the benchmark |
| R-302 | Labeling: AuditKIT refusal detectors as primary, judge for ambiguous and harm-compliance cases, judge id recorded. Human adjudication of 10% of labels, judge-vs-human agreement reported | H+A | 1.5h | R-301, D6 | Todo | Mislabel rate for identity vs bare variants compared. If detector fails the spot check, revisit D7 |
| R-303 | Metrics and stats: IRG, THC, CORR, QPG, cluster bootstrap, exact McNemar, with tests against hand-computed cases **before results are trusted** | A | 1.5h | R-003 | Todo | Tests pass. Golden analyze fixture stored |
| R-304 | Baseline report with per-group and per-axis numbers and CIs. Say plainly if there is no gap | A | 0.5h | R-302, R-303 | Todo | `reports/results/baseline.*` exists |

## Phase 4: Repair and comparison (about 6h)

| ID | Task | Owner | Est | Depends | Status | Done when / Notes |
|---|---|---|---|---|---|---|
| R-401 | Implement the chosen repair (D4) through `adapters/safetune.py`. Fit on dev only. Sweep strength on dev. Choose by the constraint rule (maximize IRG reduction with THC and CORR within margins) | A | 3h | R-304, R-105 | Todo | Chosen strength and the dev sweep table recorded. Outputs inspected for gibberish at each strength |
| R-402 | **G3:** write and commit `configs/targets.yaml` from PRD section 7 before any test run of the repair | H | 0.25h | R-304 | Todo | File committed, hash noted in Decisions |
| R-403 | Run repaired model on test, once. Run `sysprompt` comparator on test | A | 1.25h | R-401, R-402 | Todo | Both runs stored, targets checked automatically |
| R-404 | Failure analysis: where does the repair not work, which groups, which categories, any THC or CORR regression | H+A | 1.5h | R-403 | Todo | Section drafted for the article, including negative findings |

## Phase 5: Publish and write-up (about 7.5h)

| ID | Task | Owner | Est | Depends | Status | Done when / Notes |
|---|---|---|---|---|---|---|
| R-501 | Final tables and figures from stored runs only | A | 1h | R-403 | Todo | `reports/results/`, `reports/figures/` |
| R-502 | HF collections: datasets (benchmark, responses, labels, logs) and models (repair artifacts plus model card). **All public and ungated, checked while logged out** | H+A | 1.5h | R-501 | Todo | Collection links work logged out |
| R-503 | Explorer Space: precomputed table and pair viewer, no live inference | A | 1.5h | R-501 | Todo | Space loads in under 10s, reads parquet only (cut at L1 to a static table) |
| R-504 | Article (HF article, or README fallback): metrics and why, approach, datasets and tasks, how the model is meaningfully better, limitations, friction log summary | H+A | 2h | R-404 | Todo | Covers every item of the PRD compliance matrix |
| R-505 | Reproducibility README and one Colab notebook that calls the CLI end to end | A | 1h | R-501 | Todo | Fresh Colab run reproduces the results table from frozen data |
| R-506 | Abstract, under 500 words | H | 0.5h | R-504 | Todo | Word count checked |
| R-507 | Compile `reports/friction_log.md`: every issue hit in CuratorKIT, AuditKIT, SafeTune, with version, repro, workaround, feature request | A | 0.5h | R-104 | Todo | Linked from the article. Judges and hackathon organizers want this feedback |

## Phase 6: Submit (about 1h plus buffer)

| ID | Task | Owner | Est | Depends | Status | Done when / Notes |
|---|---|---|---|---|---|---|
| R-601 | **G4:** submission checklist from a logged-out browser: registered email, abstract, model collection, dataset collection, article or README, GitHub repo with reproducibility notes, repos and models used, track and problem statements (2a-2, 2b-8). Submit at least 6h before deadline. Resubmit if improved | H | 1h | R-502, R-504, R-505, R-506 | Todo | Confirmation email or screenshot saved |

## Phase 7: Finalist window, Nov 16 to Nov 22 (only if shortlisted, about 12h)

Shortlisted teams get $200 HF credit and until Nov 22, 11:59 PM AoE for a video or slides. Announcement is by Nov 16.

| ID | Task | Owner | Est | Depends | Status | Done when / Notes |
|---|---|---|---|---|---|---|
| R-701 | Add a second model (Tiny Aya Earth, or Aya Expanse 8B in 4-bit) to test generality | A | 3h | R-601 | Todo | Same metrics, same benchmark version |
| R-702 | Add an English-dialect or non-English axis, or an intersectional slice, with native-speaker validation | H+A | 3h | R-601 | Todo | New benchmark version, old results untouched |
| R-703 | Larger human validation with two annotators and agreement statistic | H | 2h | R-601 | Todo | Kappa reported |
| R-704 | Video or slides | H | 3h | R-601 | Todo | Under the length the organizers specify |
| R-705 | Optional ROI: cost per 1,000 audited prompts, small GPU vs closed-API judge | A | 1h | R-601 | Todo | Realistic volume, GPU hours, per-hour price, tokens per second stated |

## Phase 8: From submitted to 100% ready (v1.0), about 14h, after the hackathon

| ID | Task | Owner | Est | Depends | Status | Done when / Notes |
|---|---|---|---|---|---|---|
| R-801 | Test coverage at least 80% on `metrics/`, `stats/`, `build/`; adapter contract tests green | A | 2h | R-601 | Todo | Coverage report in CI |
| R-802 | CI: lint, tests, golden analyze test on every push | A | 1h | R-003 | Todo | Green badge |
| R-803 | Documentation: README polish, CONTRIBUTING, dataset card, model card, data-statement of limits | H+A | 2h | R-601 | Todo | A stranger can run the pipeline from the README |
| R-804 | License audit: LSAL v1.2 terms for CuratorKIT, AuditKIT, SafeTune (organizational use needs acknowledgement, commercial use needs a license, MinerU is AGPL if the pdf extra is used), Tiny Aya model license, dataset license (CC BY 4.0 proposed), Parity code license | H | 1.5h | R-601 | Todo | Written summary in README. Resolves PRD assumption A5 |
| R-805 | "Add your own group" guide and test: new group via YAML only, no code change | A | 1h | R-601 | Todo | Test adds a group and passes |
| R-806 | Release `v1.0`: tag, pinned versions, frozen benchmark v1.0, HF artifacts matched to tag | H | 1h | R-801, R-803, R-804 | Todo | Tag exists, HF repos reference it |
| R-807 | File upstream issues and feature requests on the Lexsi repos from the friction log | H | 1h | R-507 | Todo | Issue links added to the friction log |
| R-808 | Re-run the full pipeline on current library versions, record drift | A | 2h | R-806 | Todo | Delta table in `reports/` |
| R-809 | Final red-team of our own dataset and Space for misuse | H | 2h | R-806 | Todo | Written conclusion, changes made if needed |

### Definition of "100% ready" (v1.0)

All of: Phases 0 to 6 Done, R-801 to R-809 Done or Cut with reason, CI green, README reproduces results from a clean checkout, licenses audited, all HF artifacts public and ungated and matching the tag, no open item under Blocked.

---

## Blocked

None yet.

## Decisions

| Date | Decision | Why |
|---|---|---|
| 2026-11-14 | Project name Parity (working), English only, Tiny Aya Global primary, hand-written seeds with deterministic slot-fill, split by template | See ARCHITECTURE section 14 |
| 2026-11-14 | Open: D4 repair method (at G1), D5 environments (R-002), D6 judge model (needs user input) | Unverified library capabilities, unknown API access |

---

## Hard questions

### What do I think would break?

1. **The schedule.** About 38 planned hours against at most 36 wall-clock hours, with no allowance for sleep. The cut ladder is how this plan survives, and it only works if the cut is made early, at G1, not at hour 30.
2. **R-104 is a single point of failure for the strongest version.** If steering does not support Tiny Aya or cannot reduce refusal conditionally, the plan drops to Plan B or C.
3. **R-004 not done.** If the registered email or HF username does not match, submission or credits fail and nothing else matters. Do it first, in parallel with R-001.
4. **Colab or Kaggle quota exhaustion** during the sweep. Mitigation: resumable runner, keep the sweep to about 5 strengths, use HF credits as backup.
5. **Judge availability (D6).** Without a working judge, harm-compliance labels (THC) degrade to keyword rules, and the key metric gets weaker.
6. **Late discovery that the benchmark is not paired cleanly.** Caught by the pair-diff property test and the human review, so those must not be skipped under time pressure.
7. **Final upload fails** (large files, a gated repo, a private link). R-601 requires a logged-out check.

### What edge cases are we missing?

- **AoE vs local time.** AoE is UTC-12. The deadline is Nov 16 12:59 PM in Lagos. Treat the earlier time you are comfortable with as the deadline.
- **Re-registration and team edits closed on Nov 8.** No teammate can be added now.
- **Latest submission counts.** A broken resubmission can overwrite a good one. Never resubmit in the last hour without checking.
- **Finalist window is only for the shortlisted.** Phase 7 is conditional, not a safety net for an incomplete submission.
- **A null result.** Needs a pre-agreed story (the harmful side) or the write-up looks like a failure.
- **Dependency updates mid-hackathon** breaking the environment. Pin versions after R-002 and do not upgrade.
- **Library license acknowledgement.** LSAL asks organizations to acknowledge use. Individual participation is likely fine but R-804 confirms.

### What is overengineered?

- **Phase 7 and Phase 8 in this file** are 26 hours of work that do not exist until Phase 6 is done. They are listed so the end state is clear, but no one should touch them before submission.
- **32 tasks stand between now and submission, and the L2 path needs about 20 of them.** The L2 path is the real plan if the schedule slips.
- **Per-task owner and estimate columns** are cheap now, but stale estimates are worse than none. Update them or delete them.
- **Gates G1 to G4** are four checkpoints for a one-person, two-day project. G1 and G4 are essential. G2 and G3 are guards against self-deception and are short, keep them short.

---

## Changelog

| Date | Who | Change | Tasks |
|---|---|---|---|
| 2026-11-14 | Claude (draft for Ademola) | Initial drafts of PRD, ARCHITECTURE, ARCHITECTURE_ESSENTIALS, AGENTS, CLAUDE, project_structure, ROADMAP written. No code, no data, nothing run or verified yet. Library facts come from public READMEs and PyPI pages | none Done |
| 2026-11-14 | Ademola / Agent | Initial project scaffold: full repository directory structure, pyproject.toml, Makefile, .gitignore, .env.example, README.md, configs, Pydantic data schemas, 7 Typer CLI commands, adapters, metrics, stats, reports, tests, and explorer Space | R-001, R-002, R-003 Done |
| 2026-11-14 | Ademola / Agent | Complete R-102: author 20 neutral templates across 8 domains in data/pilot/pilot_templates.yaml, generate 160 pilot pairs in data/pilot/pilot_pairs.jsonl, create test_pilot_data.py, and verify pair-diff property | R-102 Done |
| 2026-11-14 | Ademola / Agent | Implement response labeling and full metric analysis pipeline in cli.py and metrics/pipeline.py | R-003, R-103 prep |
| 2026-11-14 | Ademola / Agent | Add tests/test_pipeline_e2e.py testing end-to-end response labeling and metric calculation flow | R-103 prep |
