# AGENTS.md

Instructions for any coding agent (Claude Code, Codex, Cursor, others) working in this repo. Last updated: 2026-11-14.

## 0. The one rule that overrides convenience

**Every contribution updates `ROADMAP.md` in the same commit.** No exceptions for "small" changes, refactors, docs, config or data. If you changed anything, ROADMAP changes too. A pull request or commit without a ROADMAP update is incomplete. See the Contribution Protocol at the top of `ROADMAP.md`.

## 1. What this project is

Parity audits and repairs identity-based treatment gaps in a small multilingual LLM (Tiny Aya Global) for the Lexsi AI Safety and Alignment Hackathon, Track 2. It chains CuratorKIT (build data), AuditKIT (evaluate) and SafeTune (repair).

Deadline: **Nov 15, 2026, 11:59 PM AoE**. Finalist window ends Nov 22. Time is short. Prefer the smallest change that moves a ROADMAP task to Done.

## 2. Read order (context economy)

1. `ARCHITECTURE_ESSENTIALS.md` (always)
2. `ROADMAP.md` "Current focus" and the task you were given
3. `project_structure.md` if you are creating or moving files
4. `ARCHITECTURE.md` only the section relevant to your task
5. `PRD.md` only if the task touches scope or success criteria

Do not load every doc by default.

## 3. Commands

Target interface. Check ROADMAP for which exist yet (R-003 creates the skeleton).

```bash
uv sync                          # install
uv run pytest -q                 # tests
uv run ruff check . && uv run ruff format --check .
uv run parity build|validate|run|label|analyze|repair-fit|publish --help
```

If a command in this list does not exist yet, say so and do not fake its output.

## 4. Rules

### 4.1 Third-party APIs (CuratorKIT, AuditKIT, SafeTune, transformers)

- These libraries are young and their docs and PyPI pages disagree on versions. **Never write a call from memory.**
- Before using a function: install the pinned version, then check it exists and read its signature (`python -c "import x, inspect; print(inspect.signature(x.f))"` or read the installed source).
- If you cannot verify (no GPU, no network, library missing), write `# VERIFY:` next to the call, add a "Blocked" or "Unverified" line to ROADMAP, and tell the user. Do not present unverified code as working.
- All calls into these libraries go through `src/parity/adapters/`. Nowhere else.
- Keep adapters to plain functions with our own types in and out. No registries, no base classes.

### 4.2 Experiment integrity

- Splits are by `template_id`. Never move a template between dev and test.
- Never fit, tune, or choose hyperparameters on test.
- Do not run `--split test` for a non-baseline condition unless `configs/targets.yaml` is committed and frozen.
- Never edit files in `data/frozen/`. Changes mean a new version directory and a ROADMAP entry.
- Never change a metric definition after seeing test results. If a definition is wrong, record it in ROADMAP "Decisions" and rerun everything affected.
- Greedy decoding and fixed seeds for headline numbers. Record seeds, git SHA, library versions.
- Never hide a failed run. Keep it in `artifacts/` and mention it.

### 4.3 Data and safety

- No slurs. No operational harm instructions. Harmful prompts stay at category level.
- Identity variants are made by the deterministic slot-filler, never by an LLM.
- No personal data. No secrets in git. Use `.env`, keep `.env.example` names only.
- Do not weaken refusal behavior in any demo or example code outside the measured repair.
- Public artifacts must be ungated.

### 4.4 Code

- Python 3.12, typed signatures, `ruff` clean.
- Pydantic at file boundaries only.
- Every new function with logic gets a test. Metrics and splitting code needs tests before results are trusted.
- Tests never hit the network or a GPU. Use fixtures. GPU smoke tests are opt-in (`-m gpu`).
- No new dependency without a ROADMAP note saying why.
- Do not build frameworks. Three similar lines beat an abstraction.

### 4.5 Writing style for docs and reports

- Plain, direct prose. No em dashes. No filler, no hype.
- State uncertainty explicitly. Mark facts you did not verify as unverified.

### 4.6 Git

- Small commits, conventional style (`feat:`, `fix:`, `docs:`, `data:`, `exp:`).
- Each commit that changes behavior, data, structure or scope includes its `ROADMAP.md` update.
- Do not rewrite history on shared branches.

## 5. Definition of Done (check all before saying "done")

- [ ] The task works as described, verified by running it, not by reading it
- [ ] Tests added or updated and passing (`uv run pytest -q`)
- [ ] `ruff` clean
- [ ] **`ROADMAP.md` updated**: task status, date, notes, Changelog row, progress count
- [ ] `ARCHITECTURE.md` / `ARCHITECTURE_ESSENTIALS.md` updated if a decision, data model or stack changed
- [ ] `project_structure.md` updated if files or folders were added, moved or removed
- [ ] `PRD.md` updated if scope or success criteria changed
- [ ] No secrets, no test-split leakage, no edits to frozen data

## 6. When blocked or unsure

Stop. Add the blocker to ROADMAP "Blocked", state what you tried and what you need, and ask the user. Do not guess an API, invent a result, or loosen a test to make it pass.

## 7. Hard questions agents must ask before finishing

1. **What would break?** If a library updates, a GPU is missing, or a file is empty, does my change fail loudly or silently?
2. **What edge cases am I missing?** Empty outputs, truncated generations, Unicode, groups with few templates, rerun after a crash.
3. **What is overengineered?** Did I add an abstraction, option or file that no ROADMAP task needs? Remove it.
4. **Did I just make a number look better?** Check THC and CORR whenever IRG moves.

If the answer to any is uncomfortable, put it in ROADMAP under the task's notes.
