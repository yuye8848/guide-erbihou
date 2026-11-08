# Amendment v2.5 remediation — completion report (2026-11-08)

Trigger: the v2.4 §S3b independent re-audit measured residual pivotal
identity and design error rates of 7.3% each (3/41), above the pre-stated
5% threshold. The user ordered full remediation (2026-11-08 09:15).
Amendment v2.5 was filed and uploaded to OSF before any data touch.

## What was done

1. **Mechanism 1 — identity integrity sweep.** All 4,615 title-bearing
   designs-artefact entries checked against the documents' own reference
   lists: 293 true mismatches (the naive pass flagged 756; the remainder
   were rendering artefacts). Re-resolution under the frozen strict gates,
   never relaxed: 169 recovered (146 identities replaced, 23 rendering
   variants confirmed), 124 corrected to 'unverified'. 41 recovered
   entries changed design class.
2. **Pivotal re-derivation.** Candidate rosters rebuilt for all 805 items
   (coverage proven two ways); the 151 operatively affected items were
   re-derived under the frozen rule (class-agnostic span order + F3 screen
   + F2 abstract-substance designs): 129 stand, 22 proposals — 21 accepted
   by parent adjudication, 1 rejected (ICAR2021RS-56, F3). Plus
   AAO2020MEN-KAS13 via the S3b sample clause. All 14 S3b-adjudicated
   field corrections incorporated.
3. **Mechanism 2 — pivotal_n completion.** The 299 items whose frozen
   pivotal_n was 'unavailable'/blank despite a pivotal were re-searched
   under the clarified rule (stated total wherever stated — abstract,
   tables, full text): 66 totals found; a triple identity guard applied
   62, rejected 2 as wrong-record totals, and 2 arrived via reselection.
4. **Re-freeze.** 254 of 805 items carry ≥1 changed cell; statement, tier,
   evidence grade and citations_n are byte-identical to v2.0 throughout.
   Pivotal composition: **SR/MA 375 / RCT 233 / primary 151 / none 46**
   (v2.0: 376 / 238 / 145 / 46). pivotal_n numeric 522 (v2.0 raw: 460).
5. **Zombie/version rulings.** EPOS2020-16's zombie determination is
   WITHDRAWN (EPOS cites the 2011 zinc record, PMID 21328251, never
   withdrawn; the withdrawn 2015 update is not cited; pivotal_n corrected
   to the cited record's stated 1,360). ICAR2021RS-29's Head 2018 review
   (PMID 30199594) is a different review from the withdrawn Sacks record
   and is not a zombie. Standing zombies: 2 (AAO2025SIN2-KAS12,
   EPOS2020-69), re-verified withdrawn 2026-11-08.
6. **Downstream recomputation** (frozen constructions first replicated
   exactly, then re-measured): L4 deep-dive discordant pivotal sharing
   **0/23, unchanged**; L5 pivotal persistence **57/292 = 19.5% →
   60/292 = 20.5%** [cluster 95% CI 0.154–0.285]; all 22 changed pivotals
   re-screened for retraction: 22/22 live. Addenda appended to the L3, L4
   and L5 freeze reports.
7. **Post-remediation verification.** Fresh 41-item sample (seed
   20261109), independent blind re-derivation, verifier barred from the
   remediation artefacts. Raw disagreements were high (identity 42.5%)
   but decomposed, on parent adjudication, into convention differences —
   attachment width, table-row vs presentation order, screening and
   applicability thresholds (the same pattern as the v2.4 §S3a audit,
   where raw 7.3% adjudicated to 0 upheld). **Upheld: pivotal identity
   1/40 = 2.5% (ICAR2021RS-73 → Hudon 2018), pivotal design 0/41** — both
   within the pre-stated 5% limits. Seven adjudicated corrections were
   applied as a documented verification round (the RS-73 pivotal and six
   pivotal_n values).

**Final frozen file: analysis/frozen_dataset_l3.csv, sha256
cebf5e51b110248d1a66376ed0848f40e31b8f5a652fbe9fe0ea6999393f2313**,
mirrored to VPS2 and VPS3 with hashes verified. v2.0 archived in full.

## Disclosed residuals

- **Numeric pivotal_n subset/completer counts.** Three of the six upheld
  pivotal_n corrections were numeric frozen values carrying pooled-subset
  or completer counts (e.g. AAO2020EPI-KAS09's 830). The completion sweep
  covered only 'unavailable'/blank values, so this class was swept only
  where sampled: 3 of ~14 checkable numeric values on identity-agreeing
  items in the verification sample. A dedicated sweep of all 522 numeric
  values is costed and proposed to the user as a separate decision; it
  has NOT been launched.
- ESBS and olfactory database-parsed designs entries without verifiable
  titles stand at production values (disclosed at step 1).
- ICAR2022OLF-43's pivotal key cannot be resolved to a printed citation
  (production keying, per-section lists) — recorded unresolved.
- Judgement residuals: the F3 screen threshold, the applicability
  subset-narrowing threshold, EPOS presentation-order basis, and the
  ICAR2023AR shared-table block are documented conventions; independent
  re-derivation under different thresholds disagrees at the rates shown
  in verify_v25/verify_report.md.

## Addendum outcome (2026-11-08, later the same day)

The user commissioned the disclosed numeric-value sweep (OSF addendum
filed before data touch). All 522 numeric pivotal_n values were checked:
497 confirmed, 19 errors corrected, 6 not verified (values stand). Final
frozen file: sha256 db769136a5bc0ebde77fa8c9f38298a6fecaf2ddd5e9e56c5a251aa240e8a75d.
One sweep correction reverts a verification-round change by the parent
(AAO2019TONS-KAS03 39→26; the earlier quote belonged to a different
trial — see the sweep adjudication). With this, the numeric pivotal_n
residual disclosed above is closed except for the 6 named not-verified
items, which remain disclosed.
