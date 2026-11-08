# L4 FREEZE REPORT — cross-guideline concordance layer (2026-11-07)

## Status: L4 FROZEN
Method of record: Protocol v2.1 amendment + addendum (filed on OSF before data touch).
Substrate: 1,084 items (805 corpus current-version items, 31 documents + 279 NICE
recommendations, 7 guidelines). Candidate pairs 6,879 (blocking over shared tokens/stems/
synonym groups, same disease area, cross-document).

## Alignment (final, post-audit)
FULL 27 / PARTIAL 224 / NO_MATCH 6,628. Provenance: dual-channel agreement 5,158;
pilot finals reused 1,294; parent adjudication 427; audit flips 5.
Channel A (rule-based) vs Channel B (frozen Gemma3-27B, Kaggle): agreement 92.4%.
Post-assembly audit (blind independent readers, 119-pair stratified pack): agreement with
finals 84.0%; 19 mismatches adjudicated in writing, 5 flips upheld (all NO_MATCH -> PARTIAL,
four from the class-ruled tail, one parent concession on F3241). The audit's first execution
(a rerun of the production verifier) was void as an independence check and is retained only
as a B-channel reproducibility measurement (97.6% exact reproduction).

## Frozen universe
union_question_universe_v2.csv — 905 questions; 63 multi-document questions covering 242
items; 842 items single-coverage (77.7%). Frozen BEFORE any concordance computation.

## Headline results
- Coverage cascade: 1,084 items -> 242 (22.3%) in multi-document questions -> 842 (77.7%)
  single-coverage.
- Direction concordance (both-stanced pairs; strata never pooled):
  FULL: 24/24 = 100% (n small; boundary soft — see audit).
  PARTIAL: 170/197 = 86.3%, question-cluster bootstrap 95% CI [77.1%, 93.0%].
  Unresolved-involved pairs: 30 (one side 'no recommendation').
- Strength concordance (secondary; unified S/M/W; direction-concordant pairs): 84/171 = 49.1%.
- Discordant deep-dive (27 pairs, 9 questions): discordance tracks evidence-tier gaps
  (median |dU| 1 vs 0, p < 0.001), not guideline age (p = 0.074) or strength gaps (p = 0.51);
  no discordant pair shares its L3 pivotal study (0/23 resolvable).

## Frozen files (analysis/frozen_l4/ + this directory)
full_alignment_final.csv sha256 c51dfb70a5fff9c5cd566fdd07187cb62f7b717744bf0240599fdeafb117cfc6
union_question_universe_v2.csv sha256 ca7b072f96bbbf384c8f5da85b25e084d591cb8243fa665206155f14cf809826
computation/concordance_pairs.csv sha256 aa372892ac0025db667754bc7831e7f83a44090501b9a10a4b6d78e2d9bc9120
computation/deep_dive_pairs.csv sha256 8c9ea62f9f245fe5106b1bb4e7fff378fa40425ee4eb9ba92f773e5f9d0e4477

## Known limitations (for the manuscript)
FULL stratum thin (27 pairs) and its boundary against specification-style PARTIALs is the
method's declared soft spot (11 audit judgement calls stand). Adjudicated-NO_MATCH tail
carries ~10% residual missed-PARTIAL rate (one-directional: overlap understated). Setting
axis near-empty (effectively a two-axis alignment). NICE participates at direction level
only. ICAR2022OLF-39 stored-direction anomaly never enters any pair (its document generated
no candidates); the pre-specified sensitivity is vacuous. Both AAO tinnitus versions sit in
the frozen denominator as current — an L5 ruling is owed. Pivotal publication years are not
carried in the frozen L3 records; evidence age is guideline-level.

## Amendment v2.5 addendum (2026-11-08) — L3 re-freeze downstream

The L3 dataset was re-frozen under Amendment v2.5 (sha256 2785235d…;
see the L3 freeze report's v2.5 section). L4's frozen data files are
unchanged. The deep-dive pivotal-sharing line is recomputed on the
re-frozen L3: **discordant pairs sharing a pivotal remain 0/23** (all 23
pairs PMID-determined under the new L3) — the frozen headline stands.
Secondary concordant line: 4 shares among 168 PMID-determined pairs
(frozen title-based count: 2/171); the two additional shares are
EPOS2020-50 × ICAR2021RS-29 (both now PMID 30199594, a direct v2.5
effect) and AAO2014TIN-10 × AAO2026TIN2-12 (identity-method difference,
not a pivotal change). Detail:
l3_production/remediation_v25/downstream/downstream_report.md.
