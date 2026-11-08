# Post-freeze supplementary report — Addendum v2.4 (2026-11-08)

Executed under Protocol Addendum v2.4 (filed on OSF before any data touch).
No frozen file was modified; all inputs verified by sha256 against the
freeze sets. Contents: S1 cluster intervals · S2 PMID-only sensitivity ·
S3a/S3b residual-error verification. **One escalation fired (S3b)** — see §4;
remediation requires Amendment v2.5 and a user ruling, and has NOT begun.

## S1 — Cluster-aware intervals (detail: s1_cluster_intervals.md)

Cluster bootstrap (10,000 reps, seed 20261108, unit = transition):
document turnover 0.662 [0.589, 0.714]; pivotal persistence 0.195
[0.139, 0.281]; Phase-1 survival 0.921 [0.894, 0.946] (vs Wilson
[0.889, 0.943] — clustering changes little). Item-level turnover
transition-clustered mean interval [0.591, 0.770] contains the frozen pooled
0.678. L4 FULL concordance 24/24: Wilson [0.862, 1.000]. Flip sensitivity
excl. two flagged coding artefacts: 5/267 = 1.87%.

## S2 — PMID-only sensitivity (detail: s2_pmid_only_sensitivity.md)

Full-mode rerun inside the adapted script reproduces every frozen
per-transition field and pooled sum exactly (verification PASS).
Restricting identity to PMID on both sides:

| Measure | Frozen | PMID-only | Δ | Rule |
|---|---|---|---|---|
| Document turnover | 0.662 | 0.558 | −10.4 pp | **FLAGGED ≥5 pp** |
| Item turnover | 0.678 | 0.592 | −8.6 pp | **FLAGGED ≥5 pp** |
| Pivotal persistence | 0.195 | 0.195 | 0.0 pp | not flagged |

A stricter bracket (designs-record PMIDs only) gives 0.617 / 0.635 — both
restricted variants sit below the frozen headlines: **the frozen turnover
figures are upper bounds; the manuscript must present turnover as a range
(document-level 0.56–0.66)** per the pre-stated §S2 rule. Mechanism: 95.0%
of persistent intersections survive the restriction vs 75.0% of current-set
mass — non-persistent citations are systematically harder to identify.
Pivotal persistence is invariant by construction (PMID-resolved on both
sides by definition) and is now verified as such. T16 tinnitus turnover is
unchanged (0.804 → 0.806); parse-heavy documents (T13/T08/T12) have small
restricted denominators and are not individually quotable.

## S3a — L5 classification table: PASS, no upheld errors

Independent re-classification of 150 sampled rows (seed 20261108): raw
disagreement 11/150 (7.3%) on identity_status, 1/116 (0.9%) on design.
Parent adjudication (s3a_adjudication.csv): **all 11 status disagreements
resolved as FROZEN STANDS** — each frozen PMID passes all three frozen
gates against the verbatim cited title; the verifier had queried with the
normalised title string, which cannot retrieve glued-token citations (a
verification-input artefact, mirroring the project's standing lesson that
an audit's tooling bounds what it can see). The single design disagreement
(weicc 2013): the verifier's F2 override misread the abstract — the record
is a systematic review whose "randomized controlled trials" phrase
describes its included studies; frozen 'other' stands under the frozen
SR/MA signalling convention. **Upheld error rates: identity_status 0/150,
design 0/116. The 5% escalation threshold is not approached.**

## S3b — L3 frozen set: ESCALATION FIRED (detail: s3b_recheck_results.csv)

Independent blind re-verification of 41 sampled items (5%, seed 20261108),
mirroring the 2026-11-06 audit pack's fields. Upheld errors:
citations_n 0/41 · **pivotal identity 3/41 = 7.3%** · **pivotal design
3/41 = 7.3%** · pivotal_n 8/39 checkable = 20.5% · applicability 5/40 =
12.5% · surrogate 2/40 = 5.0%. Item-level: 11/41 = 26.8% with ≥1 upheld
error (pre-remediation audit: 49.4% — remediation halved the rate, and
attachment counts are now clean, but residual errors concentrate in the
headline-bearing pivotal fields). Both pivotal fields exceed the
pre-stated 5% threshold → **STOP per §S3: remediation / re-freeze requires
Amendment v2.5 and a user ruling.**

Named mechanisms: (i) designs-artefact corruption silently removing a true
pivotal from an item's roster (ICAR2021RS-29; the missed pivotal is PMID
30184244, the withdrawn Cochrane review) and an empty-review false pivotal
(ICAR2021RS-80 → none); (ii) abstract-only pivotal_n retrieval missing
totals stated in tables/full text (both directions: 'unavailable' where a
total exists; one completer-count substitution where it does not);
(iii) applicability/surrogate judgement residuals (5 + 2 cases, each with
verbatim basis in the results file). One S3b ruling (ICAR2022OLF-06
pivotal_n) is a recorded rule-interpretation call (full-text total vs the
production abstract-only practice) — a v2.5 design question, not a silent
correction.

Downstream exposure if L3 pivotals change under v2.5: the L4 deep-dive
"0/23 discordant pairs share a pivotal" and the L5 pivotal-persistence
denominator (292 pairs) must be recomputed on the re-frozen L3; both
computations are scripted and small.

## Standing of the frozen headlines after v2.4

- L1/L2, L4: untouched by every check; intervals added for L4 FULL.
- L5 Phase 1: untouched; cluster interval confirms the Wilson interval.
- L5 Phase 2 turnover: **present as ranges** (0.56–0.66 document-level;
  0.59–0.68 item-level) with the frozen figures as upper bounds.
- L5 pivotal persistence 19.5% [0.139, 0.281]: robust to the identity
  restriction and to clustering.
- L3 pivotal composition (376 SR/MA / 238 RCT / 145 primary / 46 none) and
  every pivotal-dependent number: **provisional pending the user's v2.5
  ruling** — measured residual error in pivotal identity/design is 7.3%
  at item level in the verification sample.
