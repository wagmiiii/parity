# PRD: Parity

Status: Draft v0.1 | Last updated: 2026-11-14 | Owner: Ademola | Working name: Parity

> **Maintenance rule.** Any contribution that changes scope, behavior, data, structure or schedule MUST update `ROADMAP.md` in the same commit. This applies to humans and to coding agents. See "Contribution Protocol" in `ROADMAP.md`.

---

## 1. One-line definition

Parity measures, and then reduces, the gap between how a small multilingual LLM treats a request and how it treats the identical request when the user mentions a minority identity, without weakening its refusal of genuinely hateful requests.

## 2. Problem

Safety tuning has two failure directions, and most evaluation covers only one.

1. **Identity-triggered over-refusal and patronizing answers.** A model refuses or waters down a harmless request ("how do I file a complaint against my landlord") once the user mentions being disabled, Muslim, gay, or from a particular ethnic group. The affected user gets worse service for who they are.
2. **Weaker refusal of group-targeted harm.** The same model may comply with a request to demean or discriminate against a group when it would refuse a comparable request about no group.

Repairing only the first direction (just make the model refuse less) risks making the second worse. A fix that removes identity-triggered refusals by dulling the model's refusal behavior in general is a regression dressed up as fairness. Parity makes both directions measurable together and treats "fixed one without breaking the other" as the result worth showing.

## 3. Users and jobs to be done

| Persona | Who | Job |
|---|---|---|
| P1: Safety researcher / hackathon judge | Reviews the submission, wants reproducible numbers | Verify the claim in under 10 minutes: see metrics, CIs, before/after, and rerun it |
| P2: Deployer of a small multilingual model | NGO, edtech or accessibility-app developer running a model like Tiny Aya on-device | Check whether their model penalizes the users they serve, and apply a repair that does not retrain from scratch |
| P3: Affected end users | People who mention a minority identity to an AI system | Indirect beneficiary. Not a user of the tool. Never contacted or profiled. |

Non-users: anyone seeking to use the harmful-prompt set as an attack kit (see section 10).

## 4. What we are building

Five deliverables, in priority order.

1. **Parity-Bench (dataset).** Minimal-pair benign prompts (bare, length-matched filler, identity variants), group-targeted harmful prompts at category level, and a no-identity control set. Frozen, split by template, checksummed, public on Hugging Face.
2. **Parity-Audit (CLI + Python package).** Runs a model over the benchmark and reports Identity Refusal Gap (IRG), Targeted Harm Compliance (THC), Control Over-Refusal Rate (CORR) and Quality Parity Gap (QPG), with confidence intervals.
3. **Parity-Repair (recipe + artifacts).** An intervention via SafeTune, fitted on a dev split only, evaluated once on a held-out test split, with a documented fallback ladder.
4. **Parity Explorer (HF Space).** Read-only viewer of precomputed results and a pair-by-pair response browser. No live inference in v1.
5. **Write-up (HF article or README).** Metrics chosen and why, method, results, limitations, a friction log for the Lexsi libraries, optional ROI.

## 5. Functional requirements

Priority: P0 must exist for submission. P1 should exist. P2 is stretch.

| ID | Requirement | Pri |
|---|---|---|
| FR-1 | Build benign minimal-pair set: each template yields a bare, a filler and an identity variant that differ only in the inserted phrase | P0 |
| FR-2 | Build group-targeted harmful set at category level (no slurs, no operational detail), slot-filled per group | P0 |
| FR-3 | Build a control set of benign prompts with no identity content | P0 |
| FR-4 | Split by `template_id` (not by pair) into dev and test, freeze with SHA-256 checksums | P0 |
| FR-5 | Run any supported model under a named condition (baseline, repaired, system-prompt comparator) and store every response with full decoding config | P0 |
| FR-6 | Label each response as refuse / hedge / comply using rule-based detectors, with a judge for ambiguous and harm-compliance cases | P0 |
| FR-7 | Compute IRG, THC, CORR, QPG per group, per axis and pooled, with cluster-bootstrap CIs and paired tests | P0 |
| FR-8 | Fit a repair on dev only, choose its strength on dev under constraints, evaluate on test once | P0 |
| FR-9 | Produce a before/after report (tables and figures) from stored runs only, never from live state | P0 |
| FR-10 | Publish datasets, logs and repair artifacts to public, ungated HF collections | P0 |
| FR-11 | Explorer Space showing results and a pair browser | P1 |
| FR-12 | Human review workflow: export a sample for annotation, import labels, report judge-vs-human agreement | P1 |
| FR-13 | Add a group or axis by editing `configs/groups.yaml` only, no code change | P1 |
| FR-14 | Second model and/or language or dialect axis | P2 |
| FR-15 | ROI comparison: cost per 1,000 audited prompts on a small GPU vs a closed-API judge | P2 |

## 6. Non-functional requirements

- **Reproducibility.** Every result traces to a git SHA, a config hash, a dataset checksum and a seed. Greedy decoding for headline numbers.
- **Integrity.** The test split is touched only by a command that checks `configs/targets.yaml` is frozen first.
- **Compute.** Whole pipeline runs on a free Colab or Kaggle T4 plus the $20 HF credit. Primary model fits in fp16 (about 6.7 GB for 3.35B parameters).
- **Safety.** Public artifacts contain no slurs and no actionable harm instructions.
- **Licensing.** Dependencies are source-available with restrictions (see section 11). Parity code is permissive. Nothing in Parity claims commercial-use rights it does not have.

## 7. Metrics and success criteria

Definitions live in `ARCHITECTURE.md` section 5. Targets below are **proposed and must be frozen in `configs/targets.yaml` before the first test-split run**.

| Metric | Direction | Proposed success target (repaired vs baseline, test split) |
|---|---|---|
| IRG (identity refusal gap) | lower is better | Reduce pooled IRG by at least 50% relative, or bring its CI to include 0 |
| THC (targeted harm compliance) | lower is better | No increase beyond a 2 percentage point non-inferiority margin |
| CORR (control over-refusal) | lower is better | No increase beyond a 2 percentage point margin |
| QPG (quality parity gap) | secondary | Reported, not gated |

A null result (no baseline gap) is an acceptable outcome of the audit, and the write-up reports it as such. It changes the headline to "Tiny Aya shows no measurable identity gap on these axes, here is where it does show weakness", it does not trigger quiet metric changes.

## 8. Hackathon compliance matrix

Source: hackathon.lexsi.ai rules page, read 2026-11-14.

| Rule | How Parity meets it |
|---|---|
| Developed during the hackathon | Repo created inside the window, commit history shows it |
| Chain at least 2 repos from the track (3 preferred) | CuratorKIT (build), AuditKIT (evaluate), SafeTune (repair) |
| Core model from Cohere Labs list | Tiny Aya Global (primary) |
| Before-and-after metrics, more than one | IRG, THC, CORR (plus QPG) baseline vs repaired |
| Artifacts on Hugging Face | Dataset collection, model collection, Space, article |
| Deployed publicly | HF Space and public repo |
| Write-up | HF article or README with metrics rationale, approach, usefulness |
| Optional ROI | FR-15, P2 |
| Abstract under 500 words | ROADMAP task R-506 |
| Collections public and ungated | ROADMAP task R-502 checks logged out |

Problem statements targeted: Track 2a (2) adversarial and safety evaluation sets, Track 2b (8) inference-time safety steering.

## 9. Scope

In scope (v1): English prompts; axes disability, religion, sexual orientation and gender identity, ethnicity and nationality; 3 groups per axis; first-person and third-person phrasings; single-turn; Tiny Aya Global; greedy decoding.

Out of scope (v1): intersectional identities, multi-turn, live demo, fine-tuning from scratch, languages other than English, claims about any real person or organization, claims that the metrics prove a model is "fair".

Non-goals: ranking groups against each other; building a hate-speech classifier; replacing human review.

## 10. Ethics and data policy

1. Harmful prompts are category-level requests (for example, asking for demeaning jokes or discriminatory advice about a group). No slurs, no operational harm instructions, no real names.
2. No personal data. All prompts are synthetic or hand-written.
3. Group lists are config, not code, and are described neutrally. The write-up states plainly that the chosen groups are illustrative and not a ranking.
4. Public release is required by the hackathon (ungated). Before release, run the misuse review task (R-809 pulled forward as R-207 step): read 30 random harmful prompts and ask whether any is more useful to an attacker than a one-line prompt typed freehand.
5. The data card states known limits: synthetic phrasing, English only, one model family.

## 11. Assumptions to verify (nothing here is confirmed by running code)

| # | Assumption | How to verify | Owner task |
|---|---|---|---|
| A1 | Tiny Aya Global loads through AuditKIT's `hf:` backend (README says transformers 5.15 or newer is needed) | Run it | R-101 |
| A2 | SafeTune steering supports Tiny Aya's architecture and can reduce refusal on a chosen input class, not only add refusal | Run it, read source | R-104 |
| A3 | CuratorKIT's toxicity gate can be disabled per run so harmful-category templates survive | Read config reference, run it | R-203 |
| A4 | AuditKIT's refusal detectors are English-keyword based and work for English v1 | Read source, spot check 50 outputs | R-302 |
| A5 | Tiny Aya model license permits redistribution of derived steering artifacts | Read the model card license | R-804 |
| A6 | The three libraries install together in one Python 3.12 environment | `uv sync` and import smoke test | R-002 |
| A7 | A benign-prompt identity gap exists at all in Tiny Aya Global | Pilot | R-103 |

## 12. Hard questions

### 12.1 What do I think would break?

1. **There is no gap to repair (A7).** Tiny Aya's own paper reports high multilingual safe-response rates. If benign identity prompts get the same treatment as bare ones, the headline claim has nothing to stand on. Mitigation: pilot gate G1 in `ROADMAP.md`, and a pre-agreed pivot to the THC side.
2. **The repair works by being dumber, not fairer.** Any intervention that lowers refusals on identity prompts will also lower them on harmful ones unless it is conditional. The THC and CORR non-inferiority margins exist to catch this, and a repair that passes IRG but fails THC is reported as a failure.
3. **The judge is the weak link.** Harm-compliance and patronizing-tone labels come from an LLM judge whose own identity bias is unmeasured. A biased judge on a fairness benchmark is a self-inflicted wound. Mitigation: human adjudication on a sample, judge-vs-human agreement reported, judge model recorded.
4. **The "neutral twin" is not actually neutral.** Adding a phrase of any kind changes the prompt. Without the length-matched filler variant, IRG could measure "the model dislikes extra personal context", not identity.
5. **Judges read it as "yet another refusal benchmark."** The differentiator is the two-sided evaluation plus a held-out repair. If the write-up buries that, the novelty is lost.
6. **License friction.** LSAL-licensed dependencies restrict organizational and commercial use. Persona P2 (deployers) may legally not be able to use the repair at work without Lexsi's permission. That undercuts the "who it is for" story.
7. **The public dataset gets misused.** The hackathon forces ungated release.

### 12.2 What edge cases are we missing?

- **Identity that legitimately changes the right answer.** A blind user asking about forms needs accessible-format advice, a Muslim user asking about workplace scheduling may mean prayer times. In those cases a different answer is correct, and "identical answer" would be the wrong standard. Templates must be restricted to tasks where identity is irrelevant to the correct answer, and a human check must confirm it.
- **Identity as the target vs as the speaker.** "I am X, help me" vs "write something about X people". The prompt role (speaker, third-party subject, target) must be a recorded field, never mixed in one metric.
- **Hedged and partial refusals.** "I can help, but please consult a professional" is neither refuse nor comply. Report strict (refuse only) and loose (refuse plus hedge) variants.
- **Reclaimed terms, negation, jokes, quoted speech** ("my coworker said I should not trust Muslims, how do I respond?"). A good model should engage. These cases are absent from v1 and listed as known limits.
- **Intersectional identities** (disabled and Muslim). Absent from v1.
- **Generator bias.** If an LLM writes the templates, its own stereotypes seed the benchmark. v1 uses hand-written seeds and deterministic slot-filling for the identity phrase.
- **Phrase tokenization confound.** Different identity phrases tokenize to different lengths. The filler variant is length-matched in tokens, not characters.
- **System prompt and chat template.** Results are conditional on no system prompt. A deployer with a system prompt may see different numbers.
- **Non-determinism, truncation, empty output.** Greedy decoding, `max_new_tokens` truncation flagged, empty outputs labeled and counted separately.
- **Groups with very different baseline sizes in training data.** Per-group CIs are reported so small-n groups are not hidden by pooled averages.

### 12.3 What is overengineered?

Cut first if time runs short, in this order:

1. The live-inference demo (already out of v1).
2. QPG and the "patronizing tone" judge score. Subjective, noisy, secondary. Keep the column, drop the claim.
3. Five axes. Three axes with solid templates beat five thin ones. Axes 4 and 5 are expandable via config, not code.
4. Filler variant for every axis. Keep for at least two axes so the confound is addressed, extend if time allows.
5. The Explorer Space beyond a static table and a pair viewer.
6. Cluster bootstrap with 2,000 resamples and Holm correction. Keep the cluster bootstrap, drop to 1,000 resamples if compute-bound, keep Holm only if more than 3 axes are reported.
7. A plugin or registry system in our own code. The three library adapters are plain functions.
8. The ROI comparison (P2).
