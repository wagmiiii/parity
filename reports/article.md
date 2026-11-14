# Parity: Auditing and Repairing Treatment Gaps in Tiny Aya Global

*Draft article for Hugging Face submission / publication.*

## Abstract

[Draft abstract - under 500 words]

## 1. Introduction: The Two-Sided Safety Problem

Safety tuning in small multilingual language models faces a fundamental duality:
1. **Identity-triggered over-refusal:** Harmless requests trigger refusal when minority identity markers appear.
2. **Under-refusal of targeted harm:** Models comply with group-targeted demeaning or discriminatory content more readily than generic harm.

## 2. Methodology

### 2.1 Minimal-Pair Benchmark Construction
- Neutral templates across 8 domains
- Deterministic slot-filling for identity phrases and length-matched filler variants
- Split by template ID into dev/test splits

### 2.2 Metrics
- **IRG (Identity Refusal Gap):** Refusal probability difference on benign prompts.
- **THC (Targeted Harm Compliance):** Harm compliance rate on targeted prompts.
- **CORR (Control Over-Refusal Rate):** False refusal rate on neutral control prompts.
- **QPG (Quality Parity Gap):** Secondary tone and quality difference.

## 3. Baseline Audit Results

[To be populated after baseline run]

## 4. Safety Steering and Repair

[To be populated after Phase 4 repair run]

## 5. Limitations and Discussion

[Data constraints, English-only v1 scope, synthetic phrasing limits]
